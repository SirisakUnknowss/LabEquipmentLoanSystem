from django.urls import reverse
from django.shortcuts import render, redirect

# Create your views here.
def homepage(request):
    if not(request.user.is_authenticated):
        return render(request, 'base/login.html')
    return render(request, 'base/index.html')

def registerpage(request):
    return render(request, 'base/signup.html')

def notificationspage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/notifications_page.html')

def informationpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/information_page.html')

def equipmentlistpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/equipment_list_page.html')

def borrowinghistorypage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/borrowing_history_page.html')

def contactpage(request):
    if not(request.user.is_authenticated):
        return redirect(reverse('homepage'))
    return render(request, 'pages/contact_page.html')
