from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from .models import ChatMessage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def home(request):
    return render(request, 'accounts/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('chat_interface')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):  # 更新名稱
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat_interface')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def chat_interface(request):
    return render(request, 'accounts/chat.html')

@csrf_exempt
@login_required
def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if user_message:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=3000
            )
            response_text = response.choices[0].message.content

            # 保存聊天記錄
            chat_message = ChatMessage(
                user=request.user,
                message=user_message,
                response=response_text
            )
            chat_message.save()

            return JsonResponse({'message': user_message, 'response': response_text}, status=200)
        return JsonResponse({'error': 'No message provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('login')
