from django.urls import path
from mainapp.views import MainPageView, CoursesPageView, ContactsPageView, DocSitePageView, LoginPageView, NewsPageView

urlpatterns = [
    path('', MainPageView.as_view()),
    path('courses/', CoursesPageView.as_view()),
    path('contacts/', ContactsPageView.as_view()),
    path('docsite/', DocSitePageView.as_view()),
    path('login/', LoginPageView.as_view()),
    path('news/', NewsPageView.as_view())
]