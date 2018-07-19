# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-08

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)
from .serializers import (
    PostCommentDetailSerializer,
    PostCommentPublishSerializer,
    PyPostPublishSerializer,
    PyPostDetailSerializer,
    PyPostListSerializer,
    PostLikePublishSerializer,
    PostLikeReturnSerializer,
    UploadPostImageSerializer,
)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from .models import PostLike, PostComment, PostImage, PyPost
from rewrite.permissions import get_authentication
from rewrite.pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rewrite.exception import (
    FoundPostFailed,
    UserLikedPost,
    FoundLikeFailed,
)
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from notice.models import Notice


def msg(request, username):
    return render(request, 'example/dongtai.html', {
        'room_name_json': mark_safe(json.dumps(username))
    })



# 发帖
class PyPostPublishView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PyPostPublishSerializer

    def post(self, request):
        serializer = PyPostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pk = serializer.validated_data['uid']
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            owner = get_authentication(pk=pk, sign=request.META.get("HTTP_SIGN"))
            passage = PyPost.objects.create(owner=owner, title=title, content=content)
            passage.save()
            msg = Response({
                'error': 0,
                'data': PyPostListSerializer(passage, context={'request': request}).data,
                'message': 'Success to publish the post.'
            }, HTTP_201_CREATED)
            return msg


# 获取全部帖子并展示
class PyPostListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = PyPostListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    # filter_fields = ('status', 'place', 'country', 'language', 'types')
    # ordering_fields = ('level', 'place')
    search_fields = ('title',)

    def get_queryset(self):
        queryset = PyPost.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.order_by('-created_at')


# 某个帖子详情
class PyPostDetailView(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = PyPostDetailSerializer
    queryset = PyPost.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundPostFailed
        else:
            return msg

    def delete(self, request, pk):
        try:
            PyPost.objects.get(pk=pk).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Http404:
            raise FoundPostFailed


# 返回某用户发布的所有帖子
class PyPostOfUserListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = PyPostListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        pk = self.request.META.get('HTTP_NAMEPLATE')[3:-2]
        user = get_authentication(sign=self.request.META.get('HTTP_SIGN'), pk=pk)
        queryset = PyPost.objects.filter(owner=user)
        return queryset.order_by('-created_at')


# 上传图片
class PostImageUploadView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadPostImageSerializer

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def post(self, request):
        serializer = UploadPostImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uid = serializer.validated_data['uid']
            pid = serializer.validated_data['pid']
            image = serializer.validated_data['image']
            get_authentication(pk=uid, sign=request.META.get('HTTP_SIGN'))
            passage = self.get_posts(pid=pid)
            images = PostImage.objects.create(passage=passage, image=image)
            images.save()
            msg = Response({
                'error': 0,
                'data': {"pid": pid, 'image': images.get_img_url()},
                'message': 'Success to upload the image'
            }, HTTP_201_CREATED)
            return msg


# 评论
class PostCommentPublishView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PostCommentPublishSerializer

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def post(self, request):
        serializer = PostCommentPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uid = serializer.validated_data['uid']
            owner = get_authentication(pk=uid, sign=request.META.get("HTTP_SIGN"))
            pid = serializer.validated_data['pid']
            psg = self.get_posts(pid)
            content = serializer.validated_data['content']
            passage = PostComment.objects.create(owner=owner, passage=psg, content=content)
            passage.save()
            msg = Response({
                'error': 0,
                'data': PostCommentDetailSerializer(passage, context={'request': request}).data,
                'message': 'Success to comment the post.'
            }, HTTP_201_CREATED)
            return msg


# 某篇帖子的所有评论
class PostCommentsListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = PostCommentDetailSerializer
    pagination_class = Pagination

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def get_queryset(self):
        passage = self.get_posts(pid=self.kwargs['pid'])
        queryset = PostComment.objects.filter(passage=passage)
        return queryset.order_by('-created_at')


# 点赞
class PostLikePublishView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PostLikePublishSerializer

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def post(self, request):
        serializer = PostLikePublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uid = serializer.validated_data['uid']
            owner = get_authentication(pk=uid, sign=request.META.get("HTTP_SIGN"))
            pid = serializer.validated_data['pid']
            psg = self.get_posts(pid)
            try:
                PostLike.objects.get(owner=owner, passage=psg)
                raise UserLikedPost
            except PostLike.DoesNotExist:
                passage = PostLike.objects.create(owner=owner, passage=psg)
                passage.save()
                msg = Response({
                    'error': 0,
                    'data': PostLikeReturnSerializer(passage, context={'request': request}).data,
                    'message': 'Success to like the post.'
                }, HTTP_201_CREATED)
                return msg


# 取消点赞
class PostLikeDeleteView(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request, lid):
        try:
            like = PostLike.objects.get(id=lid)
            like.delete()
            Notice.objects.get(object_id=lid, type=4).delete()
        except PostLike.DoesNotExist:
            raise FoundLikeFailed
        else:
            msg = Response(status=HTTP_204_NO_CONTENT)
            return msg

