from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from dictionary.models import article, user_plants
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add_to_plantList(request, slug):
    n_item = get_object_or_404(article.Article, slug=slug)
    w_item = article.Article.objects.get_or_create(item=n_item, slug=n_item.slug, user=request.user)
    return redirect('store:homepage')