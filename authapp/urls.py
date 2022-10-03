from django.urls import path
from authapp.views import logout_user, register, update, CustomLoginView

app_name = 'authapp'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('update/', update, name='update')
]