from django.shortcuts import render


# Home view for the application
def home(request):
    return render(request, "index.html")


def testing_guide(request):
    """
    View to render the testing guide page.
    """
    return render(request, "testing_guide.html")
