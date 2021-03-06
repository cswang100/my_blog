from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.shortcuts import redirect

# Create your views here.

def home(request):
	return render(request, 'blog/home.html')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
#    if request.user.is_anonymous:
#        return(redirect('login'))          
    if not request.user.is_authenticated():
        return(redirect('login'))     
    post = get_object_or_404(Post, pk=pk)
    post.visits += 1
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
#    if request.user.is_anonymous:
#        return(redirect('login'))     
    if not request.user.is_authenticated():
        return(redirect('login')) 
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return(redirect('post_list'))
 #           return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})	
 
def post_edit(request, pk):
#    if request.user.is_anonymous:
#       return(redirect('login'))         
    if not request.user.is_authenticated():
        return(redirect('login')) 
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return(redirect('post_list'))
#            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
