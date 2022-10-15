import pickle
from unittest import mock

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from prompt_toolkit.contrib.telnet.protocol import EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from selenium.webdriver.support.wait import WebDriverWait

from mainapp.models import News, Courses
from authapp.models import User
from django.core.paginator import Paginator
from mainapp.tasks import send_feedback_mail
from django.core.mail import outbox

class StaticPageSmokeTest(TestCase):
    def test_open_main_page(self):
        url_index = reverse('mainapp:index')  # берем url
        result = self.client.get(url_index)  # возвращаем результат url (response)
        self.assertEqual(result.status_code, HTTPStatus.OK)  # проверяем равен статус кода клиента с 200 (успешным)


class NewsTestCase(TestCase):
    def setUp(self) -> None:

        for i in range(10):
            News.objects.create(
                title=f'Главная новость {i}',
                preambule=f'Вводная часть {i}',
                body=f'Описание новости {i}'
            )

        User.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'django', 'password': 'geekbrains'}
        )

    def test_open_page_read_news_anonim_user(self): # решить вопрос с пагинацией
        url = reverse('mainapp:news') + '?href=1'
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_open_page_read_detail_news_anonim_user(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_detail', args=[news_obj.pk])
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_not_open_page_create_news_anonim_user(self):
        url = reverse('mainapp:news_create')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND) # запретить доступ в представлениях и заменить на HTTPStatus.FOUND

    def test_open_page_create_news_auth_user(self):
        url = reverse('mainapp:news_create')
        result = self.client_with_auth.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_not_create_news_anonim_user(self):
        count_news = News.objects.all().count()
        url = reverse('mainapp:news_create')
        result = self.client.post(
            url,
            data= {
                'title': "Главная новость 2",
                'preambule': 'Вводная часть 2',
                'body': 'Описание новости 2',
            }
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(count_news, News.objects.all().count())

    def test_create_news_auth_user(self):
        news_count = News.objects.all().count()
        url = reverse('mainapp:news_create')
        result = self.client_with_auth.post(
            url,
            data= {
                'title': "Главная новость 2",
                'preambule': 'Вводная часть 2',
                'body': 'Описание новости 2',
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(news_count+1, News.objects.all().count())

    def test_not_open_page_update_news_anonim_user(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_open_page_update_news_auth_user(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client_with_auth.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_news_auth_user(self):
        title = 'Худшая новость'
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, title)
        url = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client_with_auth.post(
            url,
            data={
                'title': title,
                'preambule': news_obj.preambule,
                'body': news_obj.body,
            }
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, title)

    def test_open_page_delete_news_auth_user(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_delete', args=[news_obj.pk])
        result = self.client_with_auth.post(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_news_auth_user(self):
        news_obj = News.objects.first()
        url = reverse('mainapp:news_delete', args=[news_obj.pk])
        self.client_with_auth.post(url)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestTaskMailSend(TestCase):
    fixtures = ('authapp/fixtures/001_users.json',)

    def test_mail_send(self):
        message_text = "test_message_text_1"
        user_obj = User.objects.first()
        send_feedback_mail(
            {"user_id": user_obj.id, "message": message_text}
        )
        self.assertEqual(outbox[0].body, message_text)


class TestCoursesWithMock(TestCase):
    fixtures = (
        'mainapp/fixtures/003_courses.json',
        'authapp/fixtures/001_users.json',
        'mainapp/fixtures/004_lessons.json',
        'mainapp/fixtures/005_teachers.json'
    )

    def test_page_open_detail(self):
        course_obj = Courses.objects.get(pk=1) # создается обьект курса
        path = reverse('mainapp:courses_detail', args=[course_obj.pk]) # возвращает url-путь к курсу
        with open ('mainapp/fixtures/006_feedback_list_1.bin', 'rb') as inpf, mock.patch(
                'django.core.cache.cache.get') as mocked_cache:# открываем файл на чтение в двоичном режиме
            mocked_cache.return_value = pickle.load(inpf)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)


class TestNewsSelenium(StaticLiveServerTestCase):
    fixtures = (
        "authapp/fixtures/001_users.json",
        "mainapp/fixtures/002_news.json",
    )

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver(
            executable_path=settings.SELENIUM_DRIVER_PATH_FF
        )
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[type="submit"]')
            )
        )
        self.selenium.find_element_by_id("id_username").send_keys("admin")
        self.selenium.find_element_by_id("id_password").send_keys("admin")
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto"))
        )

    def test_create_button_clickable(self):
        path_list = f"{self.live_server_url}{reverse('mainapp:news')}"
        path_add = reverse("mainapp:news_create")
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
        EC.visibility_of_element_located(
        (By.CSS_SELECTOR, f'[href="{path_add}"]')
        )
        )
        print("Trying to click button ...")
        button_create.click() # Test that button clickable
        WebDriverWait(self.selenium, 5).until(
        EC.visibility_of_element_located((By.ID, "id_title"))
        )
        print("Button clickable!")
        # With no element - test will be failed
        # WebDriverWait(self.selenium, 5).until(
        # EC.visibility_of_element_located((By.ID, "id_title111"))
        # )

    def test_pick_color(self):
        path = f"{self.live_server_url}{reverse('mainapp:main_page')}"
        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "navbar"))
        )
        try:
            self.assertEqual(
            navbar_el.value_of_css_property("background-color"),
            "rgb(255, 255, 155)",
            )
        except AssertionError:
            with open("var/screenshots/001_navbar_el_scrnsht.png", "wb") as outf:
                outf.write(navbar_el.screenshot_as_png)
        raise

    def tearDown(self):
        # Close browser
        self.selenium.quit()
        super().tearDown()