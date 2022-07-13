from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


@login_required
def index(request):
    return render(request, "instagram/index.html", {
        
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
    
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 실제 db에 쿼리 던지게 됩니다. -> post_list가 길때, len()을 쓰는 것보다 빠르게 작동
    return render(request, "instagram/user_page.html", {
        "page_user":page_user,
        "post_list":post_list,
        "post_list_count":post_list_count,
    })