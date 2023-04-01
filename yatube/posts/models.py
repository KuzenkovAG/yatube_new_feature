from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from core.models import ModelWithDate

User = get_user_model()
SHORT_TEXT_LENGTH = settings.SHORT_TEXT_LENGTH
LAST_COMMENTS = 3


class Group(models.Model):
    """Group of post."""
    title = models.CharField(
        verbose_name='Заголовок группы',
        help_text="Краткое описание группы",
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Адрес группы',
        help_text='Используйте только латинские символы, дефисы и знаки '
                  'подчеркивания',
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text="Подробно опишите группу",
    )

    def __str__(self):
        return self.title


class Post(ModelWithDate):
    """Post which user create."""
    text = models.TextField(
        verbose_name='Текст поста',
        help_text="Текст нового поста"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )
    likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField(User)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.text[:SHORT_TEXT_LENGTH]

    def get_length(self):
        return len(self.text)

    def get_last_comments(self):
        """Get last comments."""
        count = self.comments.count()
        if count <= LAST_COMMENTS:
            return self.comments.all()
        return self.comments.all()[count - LAST_COMMENTS:]


class Comment(ModelWithDate):
    """Comment of post."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text="Текст комментария к посту"
    )

    def __str__(self):
        return self.text[:SHORT_TEXT_LENGTH]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписан',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]
