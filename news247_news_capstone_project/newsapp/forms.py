"""Form classes used by the News 24/7 web interface."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Article, CustomUser, Newsletter


class LoginForm(AuthenticationForm):
    """Authenticate a user from the login page."""

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))


class RegisterForm(UserCreationForm):
    """Register a new user with an email address and role selection."""

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")

    def __init__(self, *args, **kwargs):
        """Apply Bootstrap classes to the default user creation fields."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ArticleForm(forms.ModelForm):
    """Create or edit a news article from the web interface."""

    class Meta:
        model = Article
        fields = ["title", "summary", "content", "publisher"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "summary": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "publisher": forms.Select(attrs={"class": "form-select"}),
        }


class NewsletterForm(forms.ModelForm):
    """Create or edit a newsletter and attach selected articles."""

    class Meta:
        model = Newsletter
        fields = ["title", "description", "articles"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "articles": forms.SelectMultiple(attrs={"class": "form-select", "size": 10}),
        }
