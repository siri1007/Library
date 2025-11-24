from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db import transaction
from .models import Book, BookRequest, IssuedBook, User

def is_librarian(user):
    return user.role == 'librarian'

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        total_copies = int(request.POST['total_copies'])
        Book.objects.create(title=title, author=author, total_copies=total_copies, available_copies=total_copies)
        messages.success(request, 'Book added successfully!')
        return redirect('book_list')
    return render(request, 'library/add_book.html')

@login_required
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.total_copies = int(request.POST['total_copies'])
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('book_list')
    return render(request, 'library/update_book.html', {'book': book})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('book_list')

@login_required
def request_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_copies > 0:
        # Check if student already has a pending request for this book
        existing_request = BookRequest.objects.filter(
            student=request.user,
            book=book,
            status__in=['pending', 'approved']
        ).exists()
        if existing_request:
            messages.warning(request, 'You already have a pending or approved request for this book.')
        else:
            BookRequest.objects.create(student=request.user, book=book)
            messages.success(request, 'Book request submitted successfully!')
    else:
        messages.error(request, 'Book not available!')
    return redirect('book_list')

@login_required
def view_my_requests(request):
    requests = BookRequest.objects.filter(student=request.user).order_by('-request_date')
    return render(request, 'library/my_requests.html', {'requests': requests})

@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    # Statistics
    total_books = Book.objects.count()
    issued_books_count = IssuedBook.objects.filter(return_date__isnull=True).count()
    pending_requests_count = BookRequest.objects.filter(status='pending').count()
    total_students = User.objects.filter(role='student').count()

    # Recent data for dashboard
    pending_requests = BookRequest.objects.filter(status='pending').order_by('request_date')[:5]
    approved_requests = BookRequest.objects.filter(status='approved').order_by('request_date')[:5]

    return render(request, 'library/librarian_dashboard.html', {
        'total_books': total_books,
        'issued_books_count': issued_books_count,
        'pending_requests_count': pending_requests_count,
        'total_students': total_students,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests
    })

@login_required
@user_passes_test(is_librarian)
def approve_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk, status='pending')
    book_request.status = 'approved'
    book_request.approval_date = timezone.now()
    book_request.approved_by = request.user
    book_request.save()
    messages.success(request, 'Request approved successfully!')
    return redirect('librarian_dashboard')

@login_required
@user_passes_test(is_librarian)
def reject_request(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk, status='pending')
    book_request.status = 'rejected'
    book_request.approval_date = timezone.now()
    book_request.approved_by = request.user
    book_request.save()
    messages.success(request, 'Request rejected!')
    return redirect('librarian_dashboard')

@login_required
@user_passes_test(is_librarian)
def issue_book(request, pk):
    book_request = get_object_or_404(BookRequest, pk=pk, status='approved')
    with transaction.atomic():
        if book_request.book.available_copies > 0:
            from datetime import timedelta
            due_date = timezone.now() + timedelta(days=14)  # 14 days due date
            IssuedBook.objects.create(
                student=book_request.student,
                book=book_request.book,
                request=book_request,
                due_date=due_date
            )
            book_request.book.available_copies -= 1
            book_request.book.save()
            book_request.status = 'issued'
            book_request.save()
            messages.success(request, 'Book issued successfully!')
        else:
            messages.error(request, 'Book not available!')
    return redirect('librarian_dashboard')

@login_required
@user_passes_test(is_librarian)
def return_book(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk, return_date__isnull=True)
    with transaction.atomic():
        issued_book.return_date = timezone.now()
        issued_book.save()
        issued_book.book.available_copies += 1
        issued_book.book.save()
        messages.success(request, 'Book returned successfully!')
    return redirect('librarian_dashboard')

@login_required
@user_passes_test(is_librarian)
def librarian_requests(request):
    all_requests = BookRequest.objects.all().order_by('-request_date')
    return render(request, 'library/librarian_requests.html', {'requests': all_requests})

@login_required
@user_passes_test(is_librarian)
def librarian_issued(request):
    issued_books = IssuedBook.objects.all().order_by('-issue_date')
    return render(request, 'library/librarian_issued.html', {'issued_books': issued_books})

@login_required
def dashboard(request):
    if request.user.role == 'librarian':
        return redirect('librarian_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    # Statistics
    issued_books_count = IssuedBook.objects.filter(student=request.user, return_date__isnull=True).count()
    pending_requests_count = BookRequest.objects.filter(student=request.user, status='pending').count()
    returned_books_count = IssuedBook.objects.filter(student=request.user, return_date__isnull=False).count()

    # Recent data for dashboard
    issued_books = IssuedBook.objects.filter(student=request.user, return_date__isnull=True).order_by('-issue_date')[:5]
    book_requests = BookRequest.objects.filter(student=request.user).order_by('-request_date')[:5]

    return render(request, 'library/student_dashboard.html', {
        'issued_books_count': issued_books_count,
        'pending_requests_count': pending_requests_count,
        'returned_books_count': returned_books_count,
        'issued_books': issued_books,
        'book_requests': book_requests
    })

@login_required
def student_books(request):
    """View for student's issued books only - accessible to students only"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied. This page is for students only.')
        return redirect('dashboard')

    issued_books = IssuedBook.objects.filter(student=request.user).order_by('-issue_date')
    return render(request, 'library/student_books.html', {
        'issued_books': issued_books
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists
        if not User.objects.filter(username=username).exists():
            return render(request, 'registration/login.html', {
                'error_message': 'No user found. Please create an account.',
                'show_signup_link': True
            })

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard
            if user.role == 'librarian':
                return redirect('librarian_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error_message': 'Incorrect password.',
                'username': username  # Keep username in form
            })

    return render(request, 'registration/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validation
        if not username or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'registration/signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'registration/signup.html')

        # Create user
        user = User.objects.create_user(username=username, password=password, role='student')
        messages.success(request, 'User created successfully. You can login now.')
        return redirect('login')

    return render(request, 'registration/signup.html')
