from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from authapp.models import User
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user and user.is_active:
#             login(request, user)
#             messages.add_message(request, messages.INFO, mark_safe(f"Something goes worng:<br>"))
#             return HttpResponseRedirect(reverse("mainapp:index"))
#
#     context = {
#
#     }
#
#     return render(request, 'authapp/login.html', context)

class CustomLoginView(LoginView):

    template_name = 'authapp/login.html'

    def form_valid(self, form):
        ret = super().form_valid(form)
        message = gettext_lazy("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )

        return self.render_to_response(self.get_context_data(form=form))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("mainapp:index"))


def register(request):
    # if request.method == "POST":

    return render(request, 'authapp/register.html')


def update(request):
    return render(request, 'authapp/register.html')