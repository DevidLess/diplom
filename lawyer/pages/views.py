from django.shortcuts import render
from .models import TestDB


def index(request):
    slova = TestDB.objects.get(pk=1)
    return render(request, "pages/index.html", {"slova": slova})
