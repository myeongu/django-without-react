from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CommentForm, PostForm
from .models import Post


@login_required
def index(request):
    timesince = timezone.now() - timedelta(days=3) # 현재 시간 - 시간 간격
    # 전체 post에서 filtering
    post_list = Post.objects.all()\
        .filter( # Q를 통해서 'OR' 구현
            Q(author=request.user) | 
            Q(author__in=request.user.following_set.all())
        )\
        .filter(
            created_at__gte=timesince # greater than equal 
        )

    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all())[:3] # 현재 유저의 전체 following set

    return render(request, "instagram/index.html", {
        "post_list":post_list,
        "suggested_user_list":suggested_user_list,
    })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # model폼이므로 디폴트 commit은 True. DB에 저장하기 전에 무언가 하고자 할 때.
            post.author = request.user
            post.save() # many-to-many에는 pk가 필요하므로 먼저 저장을 해야 함
            post.tag_set.add(*post.extract_tag_list()) # many-to-many field이므로 add 사용
            messages.success(request, "포스팅을 저장했습니다.")
            return redirect(post)
    else: # get요청
        form = PostForm()
    
    return render(request, "instagram/post_form.html",{
        "form": form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post , pk=pk)
    return render(request, "instagram/post_detail.html", {
        "post":post,
    })

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post , pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"포스팅#{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
         
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "instagram/comment_form.html", {
        "form":form,
    })



@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post , pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"포스팅#{post.pk}를 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

    
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 db에 쿼리 던지게 됩니다. -> post_list가 길때, len()을 쓰는 것보다 빠르게 작동

    if request.user.is_authenticated: # request.user -> 로그인 되어있으면 User 객체, 안되어 있으면 AnonymousUser
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False
    
    return render(request, "instagram/user_page.html", {
        "page_user":page_user,
        "post_list":post_list,
        "post_list_count":post_list_count,
        "is_follow":is_follow,
    })