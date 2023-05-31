from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author_rewiew'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
