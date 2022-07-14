import re
from django.conf import settings
from django.db import models
from django.urls import reverse


class BaseModel(models.Model): # 공통된 필드가 존재할 경우 추상화
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# user에 대해 해당 유저가 작성한 post에 접근할 때, 
# -> Post.objects.filter(author=user)
# -> user.post_set.all() -> like_user_set과 ORM단에서 충돌 가능성 존재 => related_name 변경 필요
class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="my_post_set", # default는 post_set -> user.my_post_name으로 post접근 가능
                              on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                            related_name="like_post_set",)


    def __str__(self) -> str:
        return self.caption
    
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagram:post_detail", args=[self.pk])

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ['-id']



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name