from .models import MyUser
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('fullname', 'email', 'date_of_birth', 'mobile', 'pan', 'address', 'city', 'state', 'password')
        fields_required = ('fullname', 'email', 'password',)
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('fullname', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }


YEAR_CHOICES = [
    (0, '0 year'),
    (1, '1 year'),
    (2, '2 years'),
    (3, '3 years'),
    (4, '4 years'),
    (5, '5 years'),
    (6, '6 years'),
    (7, '7 years'),
    (8, '8 years'),
    (9, '9 years'),
    (10, '10 years'),
    (11, '11 years'),
    (12, '12 years'),
    (13, '13 years'),
    (14, '14 years'),
    (15, '15 years'),
    (16, '16 years'),
]

MONTH_CHOICES = [
    (0, '0 month'),
    (1, '1 month'),
    (2, '2 months'),
    (3, '3 months'),
    (4, '4 months'),
    (5, '5 months'),
    (6, '6 months'),
    (7, '7 months'),
    (8, '8 months'),
    (9, '9 months'),
    (10, '10 months'),
    (11, '11 months'),
    (12, '12 months'),
]

INTEREST_CHOICES = [
    (8, '8% pa'),
    (9, '9% pa'),
    (10, '10% pa'),
    (11, '11% pa'),
    (12, '12% pa'),
    (13, '13% pa'),
    (14, '14% pa'),
    (15, '15% pa'),
    (16, '16% pa'),
    (17, '17% pa'),
    (18, '18% pa'),
]


class LoanForm(forms.Form):
    email = forms.EmailField(max_length=100)
    loan_amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'max limit 1,00,000'}))
    rate_of_interest = forms.ChoiceField(
        choices=INTEREST_CHOICES,
    )
    tenure_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
    )
    tenure_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
    )