from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404, HttpResponseForbidden, \
    HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator
from mainapp.models import News, Courses, CourseTeachers, CourseFeedback
from mainapp.forms import FeedbackForm, MailFeedbackForm
from authapp.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
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


class ContactsPageView(TemplateView): # создается классическое представление CBV
    template_name = "mainapp/contacts.html" # прописывается шаблон

    def get_context_data(self, **kwargs): # переопределяем метод родительского класса
        context = super().get_context_data(**kwargs) # вызываем функцию родительского класса
        context['title'] = 'Контакты' # добавляем в контекст новые данные
        if self.request.user.is_authenticated: # проверяем аутентифицирован пользователь или нет
            context["form"] = MailFeedbackForm(user=self.request.user) # если аутентифицирован, то добавляем форму сообщения в контекст
        return context # возвращаем контекст

    def post(self, *args, **kwargs): # если был get запрос
        if self.request.user.is_authenticated: # проверяем аутентифицирован пользователь или нет
            cached = cache.get(f'mail_user_{self.request.user.pk}') # если аутентифицирован, то добавляем в переменную кеш
            if cached: # если кеш есть
                messages.add_message(self.request, messages.WARNING,
                                     "You can send only one message per 5 minutes",
                                     ) # то отправляем сообщение пользователю
            else: # если кеша нет
                cache.set(f'mail_user_{self.request.user.pk}', 'lock', timeout=20) # добавляем кеш на 20 секунд
                messages.add_message(self.request, messages.INFO, 'Message sended!') # отправляем сообщение пользователю
                tasks.send_feedback_mail.delay(
                    {
                        'user_id': self.request.POST.get('user_id'),
                        'message': self.request.POST.get('message')
                    }
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


def news(request):
    paginator = Paginator(News.objects.filter(deleted=0), 2)
    logger.info('Create paginator')
    news_paginator = paginator.page(request.GET['href'])
    user_permission = request.user.get_all_permissions()

    # if "mainapp:add_news" not in user_permission:
    #     return HttpResponseNotFound

    context = {
        "news": news_paginator,
        "title": "Новости",
        'user_permission': user_permission
    }

    return render(request, "mainapp/news.html", context)


def news_detail(request, pk=1):
    context = {
        'news_object': News.objects.filter(pk=pk)[0],
    }
    return render(request, 'mainapp/news_detail.html', context)


class NewsCreateView(PermissionRequiredMixin, CreateView):

    model = News
    fields = "__all__"
    success_url = '/news/?href=1' # сделать норм переход
    permission_required = ("mainapp.add_news",)
    login_url = '/user/login/'
    # raise_exception = True


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = '/news/?href=1' # сделать норм переход
    permission_required = ('mainapp.change_news',)
    login_url = 'authapp:login'


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = '/news/?href=1'
    permission_required = ("mainapp.delete_news",)
    login_url = 'authapp:login'


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
    extra_context = {
        'courses': Courses.objects.all(),
        'title': "Курсы"
    }


def courses_detail(request, pk=None): # создается представление курса
    context = {
        'course_object': Courses.objects.filter(pk=pk)[0], # обьект курса с переданным pk
        'teachers': CourseTeachers.objects.all() # обьект учителей
    } # создаем контекст

    if request.user.is_authenticated: # проверяем, явл. ли пользователь аутентифицированным
        if CourseFeedback.objects.filter(user_id=request.user.pk, course_id=pk).count() == 0: # проверяем есть ли у пользователя отзывы
            context['feedback_form'] = FeedbackForm(
                user=request.user,
                course=context['course_object']
            ) # если нет, то создаем форму отзывов, сразу заносим в нее пользователя и курс, после доб. форму в контекст
    cashed = cache.get(f'feedback_list_{pk}') # пытаемся достать из кеша отзывы курса

    if cashed: # если в кеше отзывы по курсу были, то...
        context['feedback_list'] = cashed # добавляем в контекст отзывы из кеша
    else: # иначе ...
        context['feedback_list'] = CourseFeedback.objects.filter(
            course=context['course_object']).order_by('-created', '-rating')[:5].select_related()
        # добавляем в контекст отзывы по курсу из б.д.
        cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)
        # добавляем в кеш отзывы по курсу из контекста на 5 мин
        import pickle # добавляет модуль по мощной сереализации и десериализации
        with open(f"mainapp/fixtures/006_feedback_list_{pk}.bin", "wb") as outf:
        # открываем файл фикстур на запись байтов
            pickle.dump(context["feedback_list"], outf)
        # записываем данные контекста (отзывы) в файл
    return render(request, 'mainapp/courses_detail.html', context) # возвращаем готовый шаблон в ответ на запрос


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
