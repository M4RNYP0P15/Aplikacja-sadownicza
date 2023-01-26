from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from dictionary.models import article, user_plants
from store.models import category
from django.views import generic

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

class PostList(generic.ListView):
    queryset = article.Article.objects.all().order_by('-publish_date')
    # print(queryset)
    template_name = 'articles/index.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu = category.Category.objects.all()
        context["cat_menu"] = cat_menu
        return context

def post_detail(request, slug):
    template_name = 'articles/post_detail.html'
    post = get_object_or_404(article.Article, slug=slug)
    # connected_comments = post.comments.filter(CommentPost=self.get_object())
    # connected_comments = post.comments.filter(active=True)
    # number_of_comments = connected_comments.count()
    cat_menu = category.Category.objects.all()
    if request.user.is_authenticated:
        plant_list = user_plants.UserPlant.objects.filter(item=post, user=request.user)
    # new_comment = None
    # Comment posted
    # if request.method == 'POST':
    #     # print(request.POST)
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         # print(comment_form)
    #         content = comment_form.cleaned_data['body']
    #         try:
    #             parent = comment_form.cleaned_data['parent']
    #         except:
    #             parent=None
    #         print('-------------Reached here')
            
    #         # Create Comment object but don't save to database yet
    #         # new_comment = comment_form.save(commit=False)
    #         # Assign the current post to the comment
    #         # new_comment.post = post

    #         new_comment = Comment(body=content , author = request.user , post=post , parent=parent)
    #         # Save the comment to the database
    #         # print(new_comment.author)
    #         new_comment.save()
    # else:
    #     comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'cat_menu': cat_menu,
                                           'plant_list':plant_list})
    # return render(request, template_name, {'post': post,
    #                                        'comments': connected_comments,
    #                                        'no_of_comments': number_of_comments,
    #                                        'new_comment': new_comment,
    #                                        'comment_form': comment_form,
    #                                        'cat_menu': cat_menu})