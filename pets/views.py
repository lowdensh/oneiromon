from django.http import HttpResponse
from django.shortcuts import render


def pets_index(request):
  return HttpResponse("Hello, world. You're at the pets index.")
