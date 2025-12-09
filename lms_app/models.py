from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator


class reader(models.Model):
    reader_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_email = models.CharField(max_length=200)
    reader_contact = models.CharField(max_length=200)
    reader_dept = models.CharField(max_length=200)
    reader_batch = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.reader_id} - {self.reader_name}"


class book(models.Model):
    bookid = models.CharField(max_length=20)
    bookname = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.bookid} - {self.bookname}"


class issuedboook(models.Model):
    reader_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_email = models.CharField(max_length=200)
    bookid = models.CharField(max_length=20)
    bookname = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    issueddate = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now() + timedelta(days=7))
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reader_id} - {self.bookid}"
