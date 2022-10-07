from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator
from mainapp.models import News, Courses, CourseTeachers, CourseFeedback
from mainapp.forms import FeedbackForm, MailFeedbackForm
from authapp.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
import logging
from django.urls import reverse_lazy
from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from mainapp import tasks

logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"
    extra_context = {
        'title': 'Главная'
    }


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        if self.request.user.is_authenticated:
            context["form"] = MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cached = cache.get(f'mail_user_{self.request.user.pk}')
            if cached:
                messages.add_message(self.request, messages.WARNING,
                                     "You can send only one message per 5 minutes",
                                     )
            else:
                cache.set(f'mail_user_{self.request.user.pk}', 'lock', timeout=1)
                messages.add_message(self.request, messages.INFO, 'Message sended!')
                tasks.send_feedback_mail.delay(
                    {
                        'user_id': self.request.POST.get('user_id'),
                        'message': self.request.POST.get('message')
                    }
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


def news(request, page=1):
    paginator = Paginator(News.objects.filter(deleted=0), 2)
    logger.info('Create paginator')
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
    cashed = cache.get(f'feedback_list_{pk}')

    if cashed:
        context['feedback_list'] = cashed
    else:
        context['feedback_list'] = CourseFeedback.objects.filter(
            course=context['course_object']).order_by('-created', '-rating')[:5].select_related()

    return render(request, 'mainapp/courses_detail.html', context)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    return reverse_lazy('mainapp:course')


class LogView(TemplateView):
    template_name = 'mainapp/log_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log_list = []
        with open(settings.LOG_FILE, 'r') as log_file:
            for i in log_file:
                log_list.insert(0, i)
                if len(log_list) > 1000:
                    break
            context['log'] = "".join(log_list)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
