from django.http import JsonResponse
from django.shortcuts import render

from .ressources import YaoiGenerator

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

def yaoi_generator(request):
    prompt = YaoiGenerator.return_random_prompt()
    response = JsonResponse({"result": prompt})
    return response
