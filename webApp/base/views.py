from django.shortcuts import render

# Create your views here.
def homepage(request):
    if not(request.user.is_authenticated):
        return render(request, 'base/login.html')
    return render(request, 'base/index.html')