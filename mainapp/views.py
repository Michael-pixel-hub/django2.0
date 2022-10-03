from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from mainapp.models import News, Courses, CourseTeachers


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"
    extra_context = {
        'title': 'Главная'
    }


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"
    extra_context = {
        'title': "Контакты"
    }


def news(request, page=1):
    paginator = Paginator(News.objects.all(), 2)
    news_paginator = paginator.page(page)
    context = {
        "news": news_paginator,
        "title": "Новости"
    }

    return render(request, "mainapp/news.html", context)


def news_detail(request, page=None, pk=1):
    context = {
        'news_object': News.objects.filter(pk=pk)[0],
    }
    return render(request, 'mainapp/news_detail.html', context)


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
    extra_context = {
        'courses': Courses.objects.all(),
        'title': "Курсы"
    }


def courses_detail(request, pk=None):
    context = {
        'course_object': Courses.objects.filter(pk=pk)[0],
        'teachers': CourseTeachers.objects.all()
    }

    return render(request, 'mainapp/courses_detail.html', context)
