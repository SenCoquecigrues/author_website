from django.shortcuts import render

def error_404(request, exception):
    return render(request, 'errors/error_404.html')

def error_500(request):
    return render(request, 'errors/error_500.html')

def pine_portfolio(request):
    return render(
        request,
        'pinytree/pine_portfolio.html'
    )