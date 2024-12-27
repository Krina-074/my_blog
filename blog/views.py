from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Post, Comment
from .forms import PostForm
from django.core.cache import cache


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Fetch comments related to the post

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, content=content)
            return redirect('post_detail', post_id=post.id)  # Redirect to the same post detail page

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@cache_page(60 * 15)  # Cache for 15 minutes
def post_list(request):
    posts = Post.objects.prefetch_related('comments').all()  # Use prefetch_related for comments
    return render(request, 'blog/post_list.html', {'posts': posts})

def get_recent_posts():
    recent_posts = cache.get('recent_posts')
    if not recent_posts:
        recent_posts = Post.objects.order_by('-created_at')[:5]
        cache.set('recent_posts', recent_posts, timeout=60 * 15)  # Cache for 15 minutes
    return recent_posts