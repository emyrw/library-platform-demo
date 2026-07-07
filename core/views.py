from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import User, Book, Loan
from .forms import LoginForm, LoanForm, ExtendLoanForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.is_librarian():
        return redirect('search_readers')
    return redirect('reader_dashboard')


# ── Reader views ──────────────────────────────────────────────────────────────

@login_required
def reader_dashboard(request):
    if request.user.is_librarian():
        return redirect('search_readers')
    active_loans = request.user.loans.select_related('book')
    return render(request, 'core/reader_dashboard.html', {'loans': active_loans})


@login_required
def catalogue(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains=query) | Q(media_type__icontains=query)
        )
    return render(request, 'core/catalogue.html', {'books': books, 'query': query})


# ── Librarian views ───────────────────────────────────────────────────────────

def librarian_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_librarian():
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@librarian_required
def register_loan(request):
    form = LoanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        book = form.cleaned_data['book']
        loan = form.save(commit=False)
        loan.save()
        messages.success(request, f'Loan registered for "{book.title}".')
        return redirect('search_readers')
    return render(request, 'core/register_loan.html', {'form': form})


@librarian_required
def register_return(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    if request.method == 'POST':
        loan.delete()  # Remove the loan record after returning
        messages.success(request, f'"{loan.book.title}"  returned.')
        return redirect('reader_loans', reader_id=loan.reader.pk)
    return render(request, 'core/confirm_return.html', {'loan': loan})


@librarian_required
def reader_loans(request, reader_id):
    reader = get_object_or_404(User, pk=reader_id, role=User.READER)
    loans = reader.loans.select_related('book').order_by('-due_date')
    return render(request, 'core/reader_loans.html', {'reader': reader, 'loans': loans})


@librarian_required
def search_readers(request):
    query = request.GET.get('q', '').strip()
    readers = User.objects.filter(role=User.READER)
    if query:
        readers = readers.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    return render(request, 'core/search_readers.html', {'readers': readers, 'query': query})


@librarian_required
def extend_loan(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    form = ExtendLoanForm(request.POST or None, instance=loan)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Due date updated to {loan.due_date}.')
        return redirect('reader_loans', reader_id=loan.reader.pk)
    return render(request, 'core/extend_loan.html', {'form': form, 'loan': loan})
