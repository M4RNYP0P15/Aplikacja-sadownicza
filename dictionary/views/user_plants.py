from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from dictionary.models import article, user_plants
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add_to_plantList(request, slug):
    n_item = get_object_or_404(article.Article, slug=slug)
    s_item = user_plants.UserPlant.objects.filter(item=n_item, user=request.user)
    if s_item:
        messages.info(request, "Roślina znajduje się już na liście roślin")
    else:
        user_plants.UserPlant.objects.create(item=n_item, user=request.user)
        messages.success(request, "Dodano do listy roślin")
    return redirect('encyklopedia:post_detail', slug=slug)

@login_required
def remove_from_plantList(request, slug):
    n_item = get_object_or_404(article.Article, slug=slug)
    s_item = user_plants.UserPlant.objects.get(item=n_item, user=request.user)
    if s_item:
        s_item.delete()
        messages.success(request, "Usunięto z listy roślin")
    else:
        messages.info(request, "Nie posiadasz tej rośliny na liście roślin")
    return redirect('encyklopedia:post_detail', slug=slug)