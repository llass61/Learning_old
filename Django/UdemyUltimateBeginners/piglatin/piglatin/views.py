from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hello")
    return render(request, 'home.html')


def translate(request):
    orig = request.GET['origText']
    translated = "Translated: " + orig
    return render(request, 'translate.html',
                  {'orig': orig, 'translated': translated})


def reverseTranslate(request):   
    plText = request.GET['plText']
    translated = "Translated: " + plText
    return render(request, 'reverseTranslate.html',
                  {'plText': plText, 'translated': translated})


def about(request):   
    return render(request, 'about.html')