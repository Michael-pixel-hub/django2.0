from django.urls import path
from mainapp.views import MainPageView, CoursesPageView, ContactsPageView, DocSitePageView, LoginPageView, news, newspage

app_name = 'mainapp'

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('courses/', CoursesPageView.as_view(), name='course'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('docsite/', DocSitePageView.as_view(), name='docsite'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('news/', news, name='news'),
    path('news/<int:page>', newspage, name='newspage')
]