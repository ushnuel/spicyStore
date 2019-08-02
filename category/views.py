from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models

# Create your views here.
class CreateCategory(LoginRequiredMixin, generic.CreateView):
    model = models.Category

class CategoryList(generic.ListView):
    model = models.Category

class CategoryDetail(generic.DetailView):
    model = models.Category
    
