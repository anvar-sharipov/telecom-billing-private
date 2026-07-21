from django.shortcuts import render, redirect
from telekom.models import *
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import tablib

from datetime import date
from calendar import monthrange
from tablib import Dataset
from icecream import ic
from telekom.views2.myFunc.myFunc import monthСonvert

from datetime import datetime
import calendar
import re

from django.db import transaction
import logging
logger = logging.getLogger(__name__)


def internet_nachisleniya_new(request):

    if not ((request.user.is_superuser and request.user.username == 'admin1') or request.user.username == 'Gayyp'):
        messages.error(request, f'У вас нет доступа')
        return redirect('user-login')
   
    context={}
    context['internet_nachisleniya_new'] = True



    return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/internet_nachisleniya_new.html', context)
    