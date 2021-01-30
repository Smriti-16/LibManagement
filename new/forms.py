from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from django.contrib.auth import authenticate
from .models import Add_Book, Issued


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AdminLoginForm(forms.Form):
    user_ID = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        global admin
        user_ID = self.cleaned_data.get('user_ID')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if user_ID and username and password:
            admin = authenticate(user_ID=user_ID, username=username, password=password)
        if not admin:
            raise forms.ValidationError('This admin does not exist')
        if not admin.check_password(password):
            raise forms.ValidationError('The password is incorrect')
        if not admin.is_active:
            raise forms.ValidationError('This user is not active')
        return super(AdminLoginForm, self).clean()


class Add_BookForm(ModelForm):
    require_css_class = 'required'

    class Meta:
        model = Add_Book
        fields = '__all__'

        def clean(self):
            cleaned_data = super().clean()
            Book_ID = cleaned_data.get("Book_ID")
            Book_Name = cleaned_data.get("Book Name")
            if not (Book_ID or Book_Name):
                raise forms.ValidationError("You must enter Book_ID and Name")


class IssuedForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=Add_Book.objects.filter(status='Not Issued'),
                                  empty_label="Select Book",
                                  to_field_name="Book_Name", label='Book Name')
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=0),
                                  empty_label="Select User",
                                  to_field_name='username',
                                  label='User Name')

    class Meta:
        model = Issued
        fields = ('user', 'book')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

