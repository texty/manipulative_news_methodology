from django.db import models
from django.contrib.auth.models import User

class FakeType(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField(null=True)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('id', )

class Article(models.Model):
    html_id = models.IntegerField(primary_key=True)
    real_url = models.TextField(null=True)
    ra_summary = models.TextField(null=True)
    ra_title = models.TextField(null=True)
    loaded_unix = models.PositiveIntegerField()
    bee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '#{id}: {title}'.format(id=self.html_id, title=self.ra_title)

class Classified(models.Model):
    types = models.ManyToManyField(FakeType)
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    classified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.article.html_id} by {self.article.bee}: {self.article.ra_title}'
    class Meta:
        verbose_name_plural = 'Classified'


class Feedback(models.Model):
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    written_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()

    def __str__(self):
        return f'{self.article.bee} for "{self.article.ra_title}" at {self.written_at}'