from django import forms
from .models import Loan, User, Book


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class LoanForm(forms.ModelForm):
    reader = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.READER),
        empty_label='— Select a reader —',
    )

    book = forms.ModelChoiceField(
        # Only show books that are not on loan.
        queryset=Book.objects.filter(loans__isnull=True),
        empty_label='— Select an item —',
    )

    class Meta:
        model = Loan
        fields = ['reader', 'book', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ExtendLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
