from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from telekom.forms import MyUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, Group


def registerPage(request):
	context = {}
	etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
	context['etraps'] = etraps
	form = MyUserCreationForm()
	context['form'] = form
	
	dzGroup = Group.objects.get(name='Dashoguz_Kassa')
	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
				
			login(request, user)

			
			

			return redirect('HomePage')
		else:
			messages.error(request, 'Ошибка при регистрации')
			
        

	
	return render(request, 'telekom/Login/register.html', context)