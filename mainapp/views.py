from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator
from mainapp.models import News, Courses, CourseTeachers, CourseFeedback
from mainapp.forms import FeedbackForm
from authapp.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin


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
    paginator = Paginator(News.objects.filter(deleted=0), 2)
    news_paginator = paginator.page(page)
    user_permission = request.user.get_all_permissions()

    context = {
        "news": news_paginator,
        "title": "Новости",
        'user_permission': user_permission
    }

    return render(request, "mainapp/news.html", context)


def news_detail(request, page=None, pk=1):
    context = {
        'news_object': News.objects.filter(pk=pk)[0],
    }
    return render(request, 'mainapp/news_detail.html', context)


class NewsCreateView(CreateView, PermissionRequiredMixin):
    model = News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.add_news",)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.delete_news",)


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
    if request.user.is_authenticated:
        if CourseFeedback.objects.filter(user_id=request.user.pk, course_id=pk).count() == 0:
            context['feedback_form'] = FeedbackForm(
                user=request.user,
                course=context['course_object']
            )
    context['feedback_list'] = CourseFeedback.objects.filter(
        course=context['course_object']).order_by('-created', '-rating')[:5]

    return render(request, 'mainapp/courses_detail.html', context)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()