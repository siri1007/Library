from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author} ({self.available_copies}/{self.total_copies} available)"

    def save(self, *args, **kwargs):
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

class BookRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('issued', 'Issued'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_requests')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approval_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')

    def __str__(self):
        return f"{self.student.username} requested {self.book.title} ({self.status})"

class IssuedBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request = models.OneToOneField(BookRequest, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.book.title} (issued: {self.issue_date})"
