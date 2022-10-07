from django.urls import path
from mainapp.views import *
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('news/', news, name='news'),
    path('news/<int:page>/', news, name='news_page'),
    path('news/<int:page>/<int:pk>/', news_detail, name="news_detail"),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path("news/<int:pk>/update/", NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),
    path('courses/', cache_page(60*5)(CoursesPageView.as_view()), name='course'),
    path('courses/<int:pk>/', courses_detail, name='courses_detail'),
    path('feedback_course/', feedback, name='feedback_course'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('docsite/', DocSitePageView.as_view(), name='docsite'),
    path('logview/', LogView.as_view(), name='log_view'),
    path('logdownload/', LogDownloadView.as_view(), name='log_download')

]