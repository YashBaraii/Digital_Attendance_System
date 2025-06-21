from django.shortcuts import render


# Home view for the application
def home(request):
    return render(request, "index.html")
