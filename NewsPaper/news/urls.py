from django.urls import path

from django.views.decorators.cache import cache_page
from .views import (NewsList, NewsDetail, PostCreateNW, PostSearchView,
                    PostEditNW, PostDeleteNW, UserEdit, LoginUser, CategoryList,
                    add_subscribe)


urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='post_list'),
    path('<int:pk>/', cache_page(300)(NewsDetail.as_view()), name='post_detail'),
    path('search/', PostSearchView.as_view()),
    path('create/', PostCreateNW.as_view(), name='post_createNW'),

    path('<int:pk>/edit/', PostEditNW.as_view(), name='post_editNW'),

    path('<int:pk>/delete/', PostDeleteNW.as_view(), name='post_deleteNW'),

    path('login/', LoginUser.as_view(), name='login'),
    path('<username>/edit/', UserEdit.as_view(), name='user_edit'),
    path('category/', CategoryList.as_view(), name='category'),

    path('add_subscribe/<int:pk>/', add_subscribe, name='add_subscribe'),
    # path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),


]