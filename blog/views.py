from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from .forms import NewCommentForm, PostSearchForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse


# Create your views here.

def home(request):
    all_posts = Post.newmanager.all()

    return render(request, 'blog/index.html', {'posts': all_posts})


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    allcomments = post.post2comment.filter(status=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == "POST":
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.comment2post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'allcomments': allcomments,
    }
    return render(request, 'blog/single.html', context)


class CatListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(post2category__name=self.kwargs['category']).filter(status='published'),
        }
        return content


def category_list(request):
    category_list = Category.objects.all()
    context = {
        "category_list": category_list,
    }
    return context


def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Post.objects.filter(
                title__contains=search_string)[:5]

            data = serializers.serialize('json', list(
                search_string), fields=('id', 'title', 'slug'))

            return JsonResponse({'search_string': data})

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)

    return render(request, 'blog/search.html',
                  {'form': form,
                   'q': q,
                   'results': results})
