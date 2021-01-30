from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User, AbstractUser
from datetime import datetime, timedelta


# Create your models here.
'''
class CustomUser(AbstractUser):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    count = models.Value(value=0)

    def __str__(self):
        return self.first_name
'''


class Admin(models.Model):
    user_ID = models.CharField(max_length=5)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Add_Book(models.Model):
    cat = [
        ('education', 'Education'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('adventure', 'Adventure'),
        ('dystopian', 'Dystopian'),
        ('science fiction', 'Science Fiction'),
        ('classics', 'Classics'),
        ]
    statusop = (('Not issued', 'Not issued'), ('Issued', 'Issued'))
    Book_ID = models.CharField(max_length=6)
    Book_Name = models.CharField(max_length=100)
    Author = models.CharField(max_length=100, default='')
    Copy_Num = models.Value(value=3)
    Genre = models.CharField(max_length=100, choices=cat, default='education')
    Book_Publisher = models.CharField(max_length=100)
    status = models.CharField(choices=statusop, default='Not Issued', max_length=150)

    def __str__(self):
        return self.Book_Name


def expiry():
    return datetime.today() + timedelta(days=15)


class Issued(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Add_Book, null=True, on_delete=models.SET_NULL)
    issue_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

    def __str__(self):
        return self.book.Book_Name




