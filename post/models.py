from django.contrib.auth import get_user_model
from django.db import models

from utils.models import TimestampModel

User = get_user_model()

class Post(TimestampModel):  # utils/models.py 에서 상속 받은 모델
    content = models.TextField('본문')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 외례키 설정, 유저 삭제시 같이 삭제

    def __str__(self):
        return f'[{self.user}] post'

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트 목록'

class PostImage(TimestampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')  # related_name='postimage_set'이 기본값
    image = models.ImageField('이미지', upload_to='post/%Y/%m/%d')  # 이미지 경로가 post/년/월/일

    def __str__(self):
        return f'{self.post} image'

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '이미지 목록'

class Tag(TimestampModel):
    tag = models.CharField('태그', max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.tag

class Comment(TimestampModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField('내용', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} | {self.user}'



# Post
    # 이미지
    # 글
    # 작성자
    # 작성일자
    # 수정일자
# 태그 N:N
# 댓글