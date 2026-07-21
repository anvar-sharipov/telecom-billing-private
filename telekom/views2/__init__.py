# from django.shortcuts import render, redirect
# from django.contrib import messages

# def internetBolum(request):
#     if request.user.username[:8] == 'internet' or request.user.username[:-1] == 'admin':
#         context = {}
#         context['internetBilling'] = True
#         return render(request, 'telekom/InternetBilling/internetBolum.html', context)
#     else:
#         messages.error(request, f'Вход в Интернет отдел разрешено только соотрудникам Интернет отдела')
#         return redirect('user-login')
