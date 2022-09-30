from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime
from django.core.paginator import Paginator
from mainapp.models import News


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


# class NewsPageView(TemplateView):
#     template_name = "mainapp/news.html"
#     extra_context = {
#         'products': [{"name": 'Новость 1', "description": 'Описание 1'},
#                      {"name": 'Новость 2', "description": 'Описание 2'},
#                      {"name": 'Новость 3', "description": 'Описание 3'},
#                      {"name": 'Новость 4', "description": 'Описание 4'},
#                      {"name": 'Новость 5', "description": 'Описание 5'},
#                      ],
#
#         "date": datetime.now(),
#     }


# def news(request):
#     context = {
#         "news": News.objects.all()[:2],
#     }
#     return render(request, "mainapp/news.html", context)


def news_page(request, page=1):
    paginator = Paginator(News.objects.all(), 2)
    news_paginator = paginator.page(page)
    context = {
        "news": news_paginator,
    }

    return render(request, "mainapp/news.html", context)


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
