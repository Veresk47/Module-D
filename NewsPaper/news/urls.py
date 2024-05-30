from django.urls import path
from .views import (
    AuthorList, PostDetail, PostList,PostSearch, NewsCreate,PostUpdate,PostDelete,
ArticlesCreate, CategoryListView, subscribe, IndexView)

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(),name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(),name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('hello', IndexView.as_view()),

]