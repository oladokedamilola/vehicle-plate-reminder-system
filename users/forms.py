from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }
        labels = {
            'email': 'Email Address',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True  # ✅ Make email required
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")  # ✅ Prevent duplicates
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")




class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write something about yourself',
                'rows': 4,
                'maxlength': '300'  # HTML-level enforcement
            }),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




# forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['notify_by_email', 'notify_by_sms', 'reminder_days_before']
        labels = {
            'notify_by_email': 'Receive Email Notifications',
            'notify_by_sms': 'Receive SMS Notifications',
            'reminder_days_before': 'Remind Me (Days Before Expiry)',
        }
        widgets = {
            'notify_by_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_by_sms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reminder_days_before': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
