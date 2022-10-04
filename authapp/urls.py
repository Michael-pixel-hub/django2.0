from django.urls import path
from authapp.views import logout_user, register, update, login_user

app_name = 'authapp'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('update/', update, name='update')
]