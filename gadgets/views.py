from django.shortcuts import render

def index(request):
    return render(
        request,
        'gadgets/grenier.html'
        )

def ecritoire(request):
    return render(
        request,
        'gadgets/word_counter.html'
    )
