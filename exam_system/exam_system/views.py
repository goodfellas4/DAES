from django.shortcuts import render

# Landing page view
def landing_page(request):
    return render(request, 'landing_page.html')
