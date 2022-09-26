from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"