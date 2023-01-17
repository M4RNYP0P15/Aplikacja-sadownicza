from django.shortcuts import render, redirect, HttpResponseRedirect
from dictionary.models import article

def homepage(request):
    matching_series = article.Article.objects.all()
    
    return render(
        request=request,
        template_name='articles.html',
        context={
            "objects": matching_series,
            "type": "series"
            }
        )