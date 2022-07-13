from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import resolve_url
from django.template.loader import render_to_string

class User(AbstractUser):
    class GenderChoices(models.TextChoices): # django3에서부터 지원해주는 기능
        MALE = "M", "남성" # (db 저장되는 값, 실제 보여지는 값)
        FEMALE = "F", "여성"
        

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True,
                                    validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d", # 이미지 경로 저장, 년월일을 기준으로 폴더 업로드
                                help_text="48px * 48px 크기의 png/jpg 파일을 업로드해주세요") # 커스텀 validator을 구현해서 해당 로직 확인 가능
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)


    # 회원가입 되었을 때 메일 보내기위한 함수
    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt", {
            "user": self, 
        })
        content = render_to_string("accounts/welcome_email_content.txt", {
            "user": self, 
        })
        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)
