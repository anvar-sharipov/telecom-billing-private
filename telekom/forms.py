from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import AbonentService, UserTable, HozOrBudjet
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(
		label = 'Имя пользователя',
		widget = forms.TextInput(attrs={'class': 'form-control', 'autocomplate': 'off'}))
		
	password = forms.CharField(
		label = 'Пароль',
		widget = forms.PasswordInput(attrs={'class': 'form-control', 'autocomplate': 'off'}))
	
class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
	

class UserTableForm(ModelForm):
	# эта функция для замены ----- на Хоз/Бюджет?
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['hb'].empty_label = '---'

	class Meta:
		model = UserTable
		fields =  ['number','etrap','surname', 'name', 'street', 'home', 'flat', 'login', 'dogowor', 'account', 'is_enterprises',  'hb' ]

		widgets = {
			'number': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'etrap': forms.Select(attrs={'class': 'form-control item'}),
			'surname': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'name': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'street': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'home': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'flat': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'is_enterprises': forms.CheckboxInput(attrs={'class': 'form-check-input account'}),
			'account': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'login': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
			'dogowor': forms.TextInput(attrs={'class': 'form-control item', 'autocomplete':'off'}),
		}


# class InternetTarifForm(ModelForm):
# 	class Meta:
# 		model = UserTable
# 		fields =  ['internet_tarif','dogowor', 'abon_length', 'count_of_numbers', 'beneficiary', 'alem'] # 'kabel_connected', 'kabel_count',
# 		widgets = {
# 			# 'kabel_connected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
# 			'alem': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
# 		}



