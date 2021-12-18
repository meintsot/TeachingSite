from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default='Blank')
    content = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('date_published', null=True)

    def __str__(self):
        return self.author.username + ':' + self.title

class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Lesson(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    content = models.FileField(upload_to='files')

    def __str__(self):
        return self.category.name + ":" + self.name

class HomeWork(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    content = models.FileField(upload_to='files')

    def __str__(self):
        return self.category.name + ":" + self.name

class Token(models.Model):
    value = models.CharField(max_length=256)

    def __str__(self):
        return 'Token:' + self.value