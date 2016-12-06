#log/forms.py
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate
from sdp.models import User 
from django import forms
import re

# If you don't do this you cannot use Bootstrap CSS
class Login_form(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=8)
    password = forms.CharField(label="Password ", max_length=30, widget=forms.PasswordInput)
    identity = forms.ChoiceField(label = "Identity", choices=[("Participant", "Participant"), ("Instructor", "Instructor"), ("HR", "HR"), ("Administrator", "Administrator")], widget=forms.Select)

    def clean(self):
    	username = self.cleaned_data.get('username')
    	password = self.cleaned_data.get('password')
    	user = authenticate(username=username, password=password)
    	if not user or not user.is_active:
    		print ("Sorry, the username and password entered don't match.")
    		raise forms.ValidationError("Sorry, the username and password entered don't match.")
    	else:
    		this_user = User.objects.filter(username=username)
    		identity_list = this_user[0].get_identity_list()
    		if self.cleaned_data.get('identity') not in identity_list:
    			print ("Sorry, the user doesn't have the identity selected.")
    			raise forms.ValidationError("Sorry, the user doesn't have the identity selected.")
    	return self.cleaned_data

    def login(self, request):
    	username = self.cleaned_data.get('username')
    	password = self.cleaned_data.get('password')
    	user = authenticate(username=username, password=password)
    	return user


class Register_form(forms.ModelForm):
	username = forms.CharField(label="Username", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
	#email = forms.EmailField(required = True)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','password1')

	def clean(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		username = self.cleaned_data.get("username")
		#email = self.cleaned_data.get("email")
		if User.objects.filter(username=username):
			raise forms.ValidationError("The user name already exists!")
		elif len(username) != 8:
			raise forms.ValidationError("Please enter your 8-digit username.")
		elif password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		elif re.search("[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]", username):
			raise forms.ValidationError("Sorry!Username can't contain special characters.")
		return self.cleaned_data

	def save(self, commit=True):
		user = super(Register_form, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.username=self.cleaned_data["username"]
		#user.email=self.cleaned_data["email"]
		if commit:
			user.save()
		return user
