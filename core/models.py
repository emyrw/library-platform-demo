from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    READER = 'reader'
    LIBRARIAN = 'librarian'
    ROLE_CHOICES = [(READER, 'Reader'), (LIBRARIAN, 'Librarian')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=READER)

    def is_librarian(self):
        return self.role == self.LIBRARIAN

    def is_reader(self):
        return self.role == self.READER


class Book(models.Model):
    BOOK = 'book'
    CD = 'cd'
    DVD = 'dvd'
    MAGAZINE = 'magazine'
    AUDIOBOOK = 'audiobook'
    MEDIA_TYPE_CHOICES = [
        (BOOK, 'Book'),
        (CD, 'CD'),
        (DVD, 'DVD'),
        (MAGAZINE, 'Magazine'),
        (AUDIOBOOK, 'Audiobook'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default=BOOK)
   
    def is_available(self):
        return self.loans.count() == 0;

    def __str__(self):
        return f"{self.title} by {self.author}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book.title} → {self.reader.username}"
