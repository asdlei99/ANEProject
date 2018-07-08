# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-5-2

from django.conf.urls import url
from .views import (
    BookDetailView,
    UserBookListView,
    BookPublishView,
    BookListView,
    ShopPublishView,
    FoodCommentPublishView,
    FoodCommentDetailView,
    ShopDetailView,
    GetShopCommentView,
    GetAllShopView,
    UploadImagesView,
    AnimalsMsgPublishView,
    AnimalsMsgDetailView,
    AnimalsMsgListView,
)


urlpatterns = [
    url(r'^books/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    url(r'^books/user/(?P<user_id>\d+)$', UserBookListView.as_view(), name='user_book'),
    url(r'^books/(?P<pk>\d+)/publish/', BookPublishView.as_view(), name='book_publish'),
    url(r'^books/$', BookListView.as_view(), name='get_all_books'),
    url(r'^shops/publish/', ShopPublishView.as_view(), name="shop_publish"),
    url(r'^shops/(?P<pk>\d+)/comment/(?P<shop_id>\d+)/$', FoodCommentPublishView.as_view(), name='shop_comment_pub'),
    url(r'^shops/comments/(?P<pk>\d+)$', FoodCommentDetailView.as_view(), name='foodComment_detail'),
    url(r'^shops/(?P<pk>\d+)$', ShopDetailView.as_view(), name='shop_detail'),
    url(r'^shops/(?P<shop_id>\d+)/comments', GetShopCommentView.as_view(), name='get_shop_comments'),
    url(r'^shops/$', GetAllShopView.as_view(), name='get_all_shop'),
    url(r'^uploadImage/(?P<bid>\d+)/(?P<sid>\d+)/(?P<aid>\d+)$', UploadImagesView.as_view(), name='upload_image'),
    url(r'^animals/(?P<pk>\d+)/publish/', AnimalsMsgPublishView.as_view(), name='animal_publish'),
    url(r'^animals/$', AnimalsMsgListView.as_view(), name='animal_list'),
    url(r'^animals/(?P<pk>\d+)$', AnimalsMsgDetailView.as_view(), name='animal_detail'),

]
