from django.urls import path, include

from .views import *

urlpatterns = [
	path('', FeedList.as_view()),
	path('feed/', FeedList.as_view(), name='feed_list_url'),                  # лента новостей
	path('profiles/', AllProfiles.as_view(), name='all_profiles_url'),                  # лента новостей
	path('<str:username>/subscribe/', Subscribe.as_view(), name='subscribe'), # подписка
	path('<str:username>/', ProfileWallList.as_view(), name='user_page_url'), # юзеры
]
