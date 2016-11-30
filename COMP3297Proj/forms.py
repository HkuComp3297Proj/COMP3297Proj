#log/forms.py
from django.contrib.auth.forms import AuthenticationForm 
from sdp.models import User 
from django import forms

# If you don't do this you cannot use Bootstrap CSS
class Login_form(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)
    identity = forms.ChoiceField(label = "Identity", choices=[("Participant","Participant") ,("Instructor","Instructor"),("HR","HR")], widget=forms.Select)

class Register_form(forms.ModelForm):
	username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
	email = forms.EmailField(required = True)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(Register_form, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.username=self.cleaned_data["username"]
		user.email=self.cleaned_data["email"]
		if commit:
			user.save()
		return user
