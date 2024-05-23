from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # 更改這行
    path('chat-interface/', views.chat_interface, name='chat_interface'),
    path('chat/', views.chat, name='chat'),
    path('logout/', views.logout_view, name='logout'),
]
