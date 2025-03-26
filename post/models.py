import re

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import TimestampModel

User = get_user_model()

# 글
class Post(TimestampModel):  # utils/models.py 에서 상속 받은 모델
    content = models.TextField('본문')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 외례키 설정, 유저 삭제시 같이 삭제

    def __str__(self):
        return f'[{self.user}] post'

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = '포스트 목록'

# 이미지
class PostImage(TimestampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')  # related_name='postimage_set'이 기본값
    image = models.ImageField('이미지', upload_to='post/%Y/%m/%d')  # 이미지 경로가 post/년/월/일

    def __str__(self):
        return f'{self.post} image'

    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = '이미지 목록'

# 태그
class Tag(TimestampModel):
    tag = models.CharField('태그', max_length=100)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.tag

# 댓글
class Comment(TimestampModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField('내용', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[comment] {self.post} | {self.user}'

# 좋아요
class Like(TimestampModel):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'[comment] {self.post} | {self.user}'

# pre_save  세이브 전
# post_save  세이브 후
@receiver(post_save, sender=Post)
def post_post_save(sender, instance, created, **kwargs):
    # 글 내용에서 태그를 찾음.
    # r'#\w{1,100}(?=\s)'   #으로 시작하고, 텍스트가 1~100글자, 공백으로 구분되는 태그
    hashtags = re.findall(r'#(\w{1,100})(?=\s|$)', instance.content)

    instance.tags.clear()  # 글에 연결된 태그 초기화

    if hashtags:
        tags = [
            # 태그가 있으면 가져오고 없으면 만듬.
            Tag.objects.get_or_create(tag=hashtag) for hashtag in hashtags
        ]
        # 이런식으로 나옴
        # tags = [
        #     [Tag, False],
        #     [Tag, True],
        # ]

        tags = [ tag for tag, _ in tags]  # 태그만 빼서 다시 리스트를 만듬

        instance.tags.add(*tags)  # 글에 태그 연결





# Post
    # 이미지
    # 글
    # 작성자
    # 작성일자
    # 수정일자
# 태그 N:N  : 태그가 있으면 검색에 유리, 도서 목록을 검색하는 시스템과 유사
# 댓글