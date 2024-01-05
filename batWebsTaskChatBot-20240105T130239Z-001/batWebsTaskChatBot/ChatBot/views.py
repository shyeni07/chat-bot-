from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from django.contrib import auth
from django.http import JsonResponse
import google.generativeai as genai
import textwrap
def home(request):
    return render(request,'home.html',{})

GOOGLE_API_KEY="AIzaSyD6TjnfEt8UXcL0yssFyWw2i-6tpDmoypA"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def ask_gemini(message):
    response = model.generate_content(message),
    
    answer = response[0].text
    return answer

def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})