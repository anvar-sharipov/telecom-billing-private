
from telekom.models import NachMinus

from calendar import monthrange
from datetime import datetime
from datetime import date
from django.contrib.auth.models import Group

current_date = date.today()
current_date = str(current_date)
current_year = current_date[0:4]
current_month = current_date[5:7]
current_day = current_date[8:]
days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]



# возвращает Dashoguz если matbdashoguz1 или kassadashoguz1 или interpaydashoguz1 или servicedashoguz1
# или например возвращает S.A.Nyyazow если matbS.A.Nyyazow1 или kassaS.A.Nyyazow1 или interpayS.A.Nyyazow1 # old
def getLoggedUserEtrap(log):

    if log[:4] == 'matb':
        return log[4:-1].title()
    if log[:5] == 'kassa':
        return log[5:-1].title()
    if log[:8] == 'interpay':
        return log[8:-1].title()
    if log[:7] == 'service':
        return log[7:-1].title()
    if log[:11] == '071operator':
        
        return log[11:-1].title()
    return False

# old удалить потом
def loggedUserEtrapAndGroup(user):
    try:
        if user in Group.objects.get(name="Dashoguz_MTB").user_set.all():
            return ['Dashoguz', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Akdepe_MTB").user_set.all():
            return ['Akdepe', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Garashsyzlyk_MTB").user_set.all():
            return ['Garashsyzlyk', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gorogly_MTB").user_set.all():
            return ['Gorogly', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Ruhubelent_MTB").user_set.all():
            return ['Ruhubelent', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="S.A.Nyyazow_MTB").user_set.all():
            return ['S.A.Nyyazow', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Turkmenbashy_MTB").user_set.all():
            return ['Turkmenbashy', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Boldumsaz_MTB").user_set.all():
            return ['Boldumsaz', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gubadag_MTB").user_set.all():
            return ['Gubadag', 'MTB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Koneurgench_MTB").user_set.all():
            return ['Koneurgench', 'MTB']
    except:
        pass
    ###########################################################################
    try:
        if user in Group.objects.get(name="Dashoguz_Kassa").user_set.all():
            return ['Dashoguz', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Akdepe_Kassa").user_set.all():
            return ['Akdepe', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Garashsyzlyk_Kassa").user_set.all():
            return ['Garashsyzlyk', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gorogly_Kassa").user_set.all():
            return ['Gorogly', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Ruhubelent_Kassa").user_set.all():
            return ['Ruhubelent', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="S.A.Nyyazow_Kassa").user_set.all():
            return ['S.A.Nyyazow', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Turkmenbashy_Kassa").user_set.all():
            return ['Turkmenbashy', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Boldumsaz_Kassa").user_set.all():
            return ['Boldumsaz', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gubadag_Kassa").user_set.all():
            return ['Gubadag', 'Kassa']
    except:
        pass
    try:
        if user in Group.objects.get(name="Koneurgench_Kassa").user_set.all():
            return ['Koneurgench', 'Kassa']
    except:
        pass 
    ############################################################################
    try:
        if user in Group.objects.get(name="Dashoguz_MB").user_set.all():
            return ['Dashoguz', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Akdepe_MB").user_set.all():
            return ['Akdepe', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Garashsyzlyk_MB").user_set.all():
            return ['Garashsyzlyk', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gorogly_MB").user_set.all():
            return ['Gorogly', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Ruhubelent_MB").user_set.all():
            return ['Ruhubelent', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="S.A.Nyyazow_MB").user_set.all():
            return ['S.A.Nyyazow', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Turkmenbashy_MB").user_set.all():
            return ['Turkmenbashy', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Boldumsaz_MB").user_set.all():
            return ['Boldumsaz', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gubadag_MB").user_set.all():
            return ['Gubadag', 'MB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Koneurgench_MB").user_set.all():
            return ['Koneurgench', 'MB']
    except:
        pass 
    ############################################################################
    try:
        if user in Group.objects.get(name="Dashoguz_071").user_set.all():
            return ['Dashoguz', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Akdepe_071").user_set.all():
            return ['Akdepe', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Garashsyzlyk_071").user_set.all():
            return ['Garashsyzlyk', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gorogly_071").user_set.all():
            return ['Gorogly', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Ruhubelent_071").user_set.all():
            return ['Ruhubelent', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="S.A.Nyyazow_071").user_set.all():
            return ['S.A.Nyyazow', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Turkmenbashy_071").user_set.all():
            return ['Turkmenbashy', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Boldumsaz_071").user_set.all():
            return ['Boldumsaz', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gubadag_071").user_set.all():
            return ['Gubadag', '071']
    except:
        pass
    try:
        if user in Group.objects.get(name="Koneurgench_071").user_set.all():
            return ['Koneurgench', '071']
    except:
        pass
    ############################################################################
    try:
        if user in Group.objects.get(name="Dashoguz_Internet").user_set.all():
            return ['Dashoguz', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Akdepe_Internet").user_set.all():
            return ['Akdepe', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Garashsyzlyk_Internet").user_set.all():
            return ['Garashsyzlyk', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gorogly_Internet").user_set.all():
            return ['Gorogly', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Ruhubelent_Internet").user_set.all():
            return ['Ruhubelent', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="S.A.Nyyazow_Internet").user_set.all():
            return ['S.A.Nyyazow', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Turkmenbashy_Internet").user_set.all():
            return ['Turkmenbashy', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Boldumsaz_Internet").user_set.all():
            return ['Boldumsaz', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gubadag_Internet").user_set.all():
            return ['Gubadag', 'Internet']
    except:
        pass
    try:
        if user in Group.objects.get(name="Koneurgench_Internet").user_set.all():
            return ['Koneurgench', 'Internet']
    except:
        pass
    ############################################################################
    try:
        if user in Group.objects.get(name="Dashoguz_SHB").user_set.all():
            return ['Dashoguz', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Akdepe_SHB").user_set.all():
            return ['Akdepe', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Garashsyzlyk_SHB").user_set.all():
            return ['Garashsyzlyk', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gorogly_SHB").user_set.all():
            return ['Gorogly', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Ruhubelent_SHB").user_set.all():
            return ['Ruhubelent', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="S.A.Nyyazow_SHB").user_set.all():
            return ['S.A.Nyyazow', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Turkmenbashy_SHB").user_set.all():
            return ['Turkmenbashy', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Boldumsaz_SHB").user_set.all():
            return ['Boldumsaz', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Gubadag_SHB").user_set.all():
            return ['Gubadag', 'SHB']
    except:
        pass
    try:
        if user in Group.objects.get(name="Koneurgench_SHB").user_set.all():
            return ['Koneurgench', 'SHB']
    except:
        pass 
    return ['', '']

def get_etrap_and_types(user):
    groups = []
    etrap_types = {'etraps':[], 'types':[]} # {etrap:['Dashoguz', 'Akdepe'], types:['Kassa', 'MTB']}
    for obj in user.groups.all():
        groups.append(obj.name)
    for group in groups:
        l = group.split('_')
        etrap = l[0]
        type_ = l[1]
        if etrap not in etrap_types['etraps']:
            etrap_types['etraps'].append(etrap)
        if type_ not in etrap_types['types']:
            etrap_types['types'].append(type_)
    return etrap_types
        


def monthСonvert(month):
	if month == '01' or month == 1:
		return 'Январь'
	if month == '02' or month == 2:
		return 'Февраль'
	if month == '03' or month == 3:
		return 'Март'
	if month == '04' or month == 4:
		return 'Апрель'
	if month == '05' or month == 5:
		return 'Май'
	if month == '06' or month == 6:
		return 'Июнь'
	if month == '07' or month == 7:
		return 'Июль'
	if month == '08' or month == 8:
		return 'Август'
	if month == '09' or month == 9:
		return 'Сентябрь'
	if month == '10' or month == 10:
		return 'Октябрь'
	if month == '11' or month == 11:
		return 'Ноябрь'
	if month == '12' or month == 12:
		return 'Декабрь'

	if month == 'Январь':
		return '01'
	if month == 'Февраль':
		return '02'
	if month == 'Март':
		return '03'
	if month == 'Апрель':
		return '04'
	if month == 'Май':
		return '05'
	if month == 'Июнь':
		return '06'
	if month == 'Июль':
		return '07'
	if month == 'Август':
		return '08'
	if month == 'Сентябрь':
		return '09'
	if month == 'Октябрь':
		return '10'
	if month == 'Ноябрь':
		return '11'
	if month == 'Декабрь':
		return '12'
	return False
    
def getEtrapCode(etrap):
    if etrap == 'Dashoguz':
        return '322'
    if etrap == 'Akdepe':
        return '344'
    if etrap == 'Boldumsaz':
        return '346'
    if etrap == 'Gorogly':
        return '340'
    if etrap == 'Koneurgench':
        return '347'
    if etrap == 'Turkmenbashy':
        return '349'
    if etrap == 'S.A.Nyyazow':
        return '348'
    if etrap == 'Ruhubelent':
        return '342'
    if etrap == 'Garashsyzlyk':
        return '343'
    if etrap == 'Gubadag':
        return '345'
    

def getCodeEtrap(code):
    if code == '322':
        return 'Dashoguz'
    if code == '344':
        return 'Akdepe'
    if code == '346':
        return 'Boldumsaz'
    if code == '340':
        return 'Gorogly'
    if code == '347':
        return 'Koneurgench'
    if code == '349':
        return 'Turkmenbashy'
    if code == '348':
        return 'S.A.Nyyazow'
    if code == '342':
        return 'Ruhubelent'
    



def getPreviousMonth(month):
    
    if month == "Январь":
        return 'Декабрь'
    
    if month == "Февраль":
        return 'Январь'
    
    if month == "Март":
        return 'Февраль'
    
    if month == "Апрель":
        return 'Март'
    
    if month == "Май":
        return 'Апрель'
    
    if month == "Июнь":
        return 'Май'
    
    if month == "Июль":
        return 'Июнь'
    
    if month == "Август":
        return 'Июль'
    
    if month == "Сентябрь":
        return 'Август'
    
    if month == "Октябрь":
        return 'Сентябрь'
    
    if month == "Ноябрь":
        return 'Октябрь'
    
    if month == "Декабрь":
        return 'Ноябрь'
    return False










# setService
def getAbonNachOrNone(pk):
    try:
        return NachMinus.objects.get(user=pk, year=current_year, month=current_month)
    except:
        return False
    

def dictHaveServiceType(dict_, service_type):
    print('service_type', service_type)
    for item, value in dict_.items():
        print(item)
        if item == service_type:
            return True    
    return False
    

def  appendHistoryDict(dict_, abonent, serv_type, reason, pay):
    if serv_type == 'abon_length':
        dict_[serv_type].append({
            'service': abonent.abon_length.metr,
            'total_price': abonent.abon_length.price,
            'connect_date': str(abonent.abon_length_connect_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            })
        return (dict_)
    
    if serv_type == 'count_of_numbers':
        dict_[serv_type].append({
            'service': abonent.count_of_numbers.count_of_numbers,
            'total_price': abonent.count_of_numbers.price,
            'connect_date': str(abonent.count_of_numbers_connect_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            })
        return (dict_)
    
    if serv_type == 'kabel_count':
        dict_[serv_type].append({
            'service': abonent.kabel_count.kabel_count,
            'total_price': abonent.kabel_count.price,
            'connect_date': str(abonent.kabel_activated_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            })
        return (dict_)


def createServiceType(dict_, abonent, serv_type, reason, pay):
    if serv_type == 'abon_length':
        dict_[serv_type] = [{
            'service': abonent.abon_length.metr,
            'total_price': abonent.abon_length.price,
            'connect_date': str(abonent.abon_length_connect_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            }]
        return (dict_)
    
    if serv_type == 'count_of_numbers':
        dict_[serv_type] = [{
            'service': abonent.count_of_numbers.count_of_numbers,
            'total_price': abonent.count_of_numbers.price,
            'connect_date': str(abonent.count_of_numbers_connect_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            }]
        return (dict_)
    
    if serv_type == 'kabel_count':
        dict_[serv_type] = [{
            'service': abonent.kabel_count.kabel_count,
            'total_price': abonent.kabel_count.price,
            'connect_date': str(abonent.kabel_activated_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            }]
        return (dict_)


def createServiceDict(abonent, serv_type, reason, pay):
    dict_ = {}
    if serv_type == 'abon_length': 
        dict_[serv_type] = [{
            'service': abonent.abon_length.metr,
            'total_price': abonent.abon_length.price,
            'connect_date': str(abonent.abon_length_connect_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            }]
        return (dict_)
    
    if serv_type == 'count_of_numbers': 
        dict_[serv_type] = [{
            'service': abonent.count_of_numbers.count_of_numbers,
            'total_price': abonent.count_of_numbers.price,
            'connect_date': str(abonent.count_of_numbers_connect_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            }]
        return (dict_)
    
    if serv_type == 'kabel_count':
        dict_[serv_type] = [{
            'service': abonent.kabel_count.kabel_count,
            'total_price': abonent.kabel_count.price,
            'connect_date': str(abonent.kabel_activated_date),
            'disconnect_date': str(datetime.now()),
            'pay': pay,
            'reasons_disconnect': reason,
            }]
        return (dict_)
    


######
###
#####
#######
########

# MATB/index.py 
# Возвращаем dict_ NachMinus.deleted если есть (или False)
def getDelDict(nachMinus):
    if nachMinus:
        if nachMinus.deleted:
            return eval(nachMinus.deleted)        
    return False

# MATB/index.py 
# Возвращаем dict_ NachMinus.added если есть (или False)
def getAddDict(nachMinus):
    if nachMinus:
        if nachMinus.added:
            return eval(nachMinus.added)
    return False

# MATB/index.py 
# Возвращаем авто начисления если есть (если нет возвращаем 0)
def getPay(abonent, add_dict):
    if abonent.count_of_numbers:
        if add_dict:
            print('tut')
            for serv_type, value in add_dict.items():
                if serv_type == 'count_of_numbers':
                    if value[0][:7] == current_date[:7]:
                        if abonent.beneficiary:
                            return ((int(current_date[8:10]) -  int(value[0][8:10])) * (abonent.count_of_numbers.price / days_in_month)) * float('0.' + str(100 - abonent.beneficiary.percent))
                        else:
                            return (int(current_date[8:10]) -  int(value[0][8:10])) * (abonent.count_of_numbers.price / days_in_month)
        else:
            return int(current_date[8:10]) * (abonent.count_of_numbers.price / days_in_month)
    return 0

# MATB/index.py 
# Сохраненем инфу о удаленнй услуге в NachMinus.deleted
def saveDelServOnDelDict(abonent, del_dict, pay):
    if del_dict:
        for serv_type, value in del_dict.items():
            if serv_type == 'count_of_numbers':
                value = [current_date, str(abonent.pk), pay]
            else:
                del_dict['count_of_numbers'] = [current_date, str(abonent.pk), pay]
    else:
        del_dict = {'count_of_numbers': [current_date, str(abonent.pk), pay]}
    return del_dict



def getEtrapNameFromCode(code):
    if code == '322' or code == 322:
        return 'Dashoguz'
    if code == '344' or code == 344:
        return 'Akdepe'
    if code == '346' or code == 346:
        return 'Boldumsaz'
    if code == '340' or code == 340:
        return 'Gorogly'
    if code == '347' or code == 347:
        return 'Koneurgench'
    if code == '349' or code == 349:
        return 'Turkmenbashy'
    if code == '348' or code == 348:
        return 'S.A.Nyyazow'
    if code == '342' or code == 342:
        return 'Ruhubelent'
    if code == '343' or code == 343:
        return 'Garashsyzlyk'
    if code == '345' or code == 345:
        return 'Gubadag'
    return False


###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################
# diapazon Akdepe Garashsyzlyk, Boldumsaz and Gubadag START

garashsyzlyk_ranges = [
    (20000, 29999),
    (37000, 38000),
    (50000, 59999),
    (74161, 78999),
    (79125, 79999),
    (90000, 99999),
]

akdepe_ranges = [
    (30000, 39999),
    (40000, 49999),
    (70000, 74160),
    (79000, 79124),
]

boldumsaz_ranges = [
    (30000, 49999),
    (50000, 54287),
    (90000, 91023),
    (70000, 72432),
    (79700, 79955),
]

gubadag_ranges = [
    (20000, 29999),   
    (60000, 69999),      
    (72433, 73392),   
    (73521, 79536),   
    (95000, 95315),
    (54294, 59999),
      
]

dzk_ranges = [
  (37000, 38000),  
]

def is_Akdepe(num):
    num = int(num)
    for start, end in akdepe_ranges:
        if start <= num <= end:
            return True
    return False

def is_Garashsyzlyk(num):
    num = int(num)
    for start, end in garashsyzlyk_ranges:
        if start <= num <= end:
            return True
    return False

def is_Boldumsaz(num):
    num = int(num)
    for start, end in boldumsaz_ranges:
        if start <= num <= end:
            return True
    return False

def is_Gubadag(num):
    num = int(num)
    for start, end in gubadag_ranges:
        if start <= num <= end:
            return True
    return False

def is_Dzk(num):
    num = int(num)
    for start, end in dzk_ranges:
        if start <= num <= end:
            return True
    return False

# diapazon Akdepe Garashsyzlyk, Boldumsaz and Gubadag END
###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################



def get_sahypa(lenCalls):
    if lenCalls == 0:
        return False
    if lenCalls <= 60 and lenCalls != 0:
        return 1
    elif lenCalls > 60 and lenCalls <= 120:
        return 2
    elif lenCalls > 120 and lenCalls <= 180:
        return 3
    elif lenCalls > 180 and lenCalls <= 240:
        return 4
    elif lenCalls > 240 and lenCalls <= 300:
        return 5
    elif lenCalls > 300 and lenCalls <= 360:
        return 6
    elif lenCalls > 360 and lenCalls <= 420:
        return 7
    elif lenCalls > 420 and lenCalls <= 480:
        return 8
    elif lenCalls > 480 and lenCalls <= 540:
        return 9
    elif lenCalls > 540 and lenCalls <= 600:
        return 10
    elif lenCalls > 600 and lenCalls <= 660:
        return 11
    elif lenCalls > 660 and lenCalls <= 720:
        return 12
    elif lenCalls > 720 and lenCalls <= 780:
        return 13
    elif lenCalls > 780 and lenCalls <= 840:
        return 14
    elif lenCalls > 840 and lenCalls <= 900:
        return 15
    elif lenCalls > 900 and lenCalls <= 960:
        return 16
    elif lenCalls > 960 and lenCalls <= 1020:
        return 17
    elif lenCalls > 1020 and lenCalls <= 1080:
        return 18
    elif lenCalls > 1080 and lenCalls <= 1140:
        return 19
    elif lenCalls > 1140 and lenCalls <= 1200:
        return 20
    elif lenCalls > 1200 and lenCalls <= 1260:
        return 21
    elif lenCalls > 1260 and lenCalls <= 1320:
        return 22
    elif lenCalls > 1320 and lenCalls <= 1380:
        return 23
    elif lenCalls > 1380 and lenCalls <= 1440:
        return 24
    elif lenCalls > 1440 and lenCalls <= 1500:
        return 25
    elif lenCalls > 1500 and lenCalls <= 1560:
        return 26
    elif lenCalls > 1560 and lenCalls <= 1620:
        return 27
    elif lenCalls > 1620 and lenCalls <= 1680:
        return 28
    elif lenCalls > 1680 and lenCalls <= 1740:
        return 29
    elif lenCalls > 1740 and lenCalls <= 1800:
        return 30
    elif lenCalls > 1800 and lenCalls <= 1860:
        return 31
    elif lenCalls > 1860 and lenCalls <= 1920:
        return 32
    elif lenCalls > 1920 and lenCalls <= 1980:
        return 33
    elif lenCalls > 1980 and lenCalls <= 2040:
        return 34
    elif lenCalls > 2040 and lenCalls <= 2100:
        return 35
    elif lenCalls > 2100 and lenCalls <= 2160:
        return 36
    elif lenCalls > 2160 and lenCalls <= 2220:
        return 37
    elif lenCalls > 2220 and lenCalls <= 2280:
        return 38
    elif lenCalls > 2280 and lenCalls <= 2340:
        return 39
    elif lenCalls > 2340 and lenCalls <= 2400:
        return 40
    elif lenCalls > 2400 and lenCalls <= 2460:
        return 41
    elif lenCalls > 2460 and lenCalls <= 2520:
        return 42
    elif lenCalls > 2520 and lenCalls <= 2580:
        return 43
    elif lenCalls > 2580 and lenCalls <= 2640:
        return 44
    elif lenCalls > 2640 and lenCalls <= 2700:
        return 45
    elif lenCalls > 2700 and lenCalls <= 2760:
        return 46
    elif lenCalls > 2760 and lenCalls <= 2820:
        return 47
    elif lenCalls > 2820 and lenCalls <= 2880:
        return 48
    elif lenCalls > 2880 and lenCalls <= 2940:
        return 49
    elif lenCalls > 2940 and lenCalls <= 3000:
        return 50
    elif lenCalls > 3000 and lenCalls <= 3060:
        return 51
    elif lenCalls > 3060 and lenCalls <= 3120:
        return 52
    elif lenCalls > 3120 and lenCalls <= 3180:
        return 53
    elif lenCalls > 3180 and lenCalls <= 3240:
        return 54
    elif lenCalls > 3240 and lenCalls <= 3300:
        return 55
    elif lenCalls > 3300 and lenCalls <= 3360:
        return 56
    elif lenCalls > 3360 and lenCalls <= 3420:
        return 57
    elif lenCalls > 3420 and lenCalls <= 3480:
        return 58
    elif lenCalls > 3480 and lenCalls <= 3540:
        return 59
    elif lenCalls > 3540 and lenCalls <= 3600:
        return 60
    elif lenCalls > 3600 and lenCalls <= 3660:
        return 61
    elif lenCalls > 3660 and lenCalls <= 3720:
        return 62
    elif lenCalls > 3720 and lenCalls <= 3780:
        return 63
    elif lenCalls > 3780 and lenCalls <= 3840:
        return 64
    elif lenCalls > 3840 and lenCalls <= 3900:
        return 65
    elif lenCalls > 3900 and lenCalls <= 3960:
        return 66
    elif lenCalls > 3960 and lenCalls <= 4020:
        return 67
    elif lenCalls > 4020 and lenCalls <= 4080:
        return 68
    elif lenCalls > 4080 and lenCalls <= 4140:
        return 69
    elif lenCalls > 4140 and lenCalls <= 4200:
        return 70
    elif lenCalls > 4200 and lenCalls <= 4260:
        return 71
    elif lenCalls > 4260 and lenCalls <= 4320:
        return 72
    elif lenCalls > 4320 and lenCalls <= 4380:
        return 73
    elif lenCalls > 4380 and lenCalls <= 4440:
        return 74
    elif lenCalls > 4440 and lenCalls <= 4500:
        return 75
    elif lenCalls > 4500 and lenCalls <= 4560:
        return 76
    elif lenCalls > 4560 and lenCalls <= 4620:
        return 77
    elif lenCalls > 4620 and lenCalls <= 4680:
        return 78
    elif lenCalls > 4680 and lenCalls <= 4740:
        return 79
    elif lenCalls > 4740 and lenCalls <= 4800:
        return 80
    elif lenCalls > 4800 and lenCalls <= 4860:
        return 81
    elif lenCalls > 4860 and lenCalls <= 4920:
        return 82
    elif lenCalls > 4920 and lenCalls <= 4980:
        return 83
    elif lenCalls > 4980 and lenCalls <= 5040:
        return 84
    elif lenCalls > 5040 and lenCalls <= 5100:
        return 85
    elif lenCalls > 5100 and lenCalls <= 5160:
        return 86
    elif lenCalls > 5160 and lenCalls <= 5220:
        return 87
    elif lenCalls > 5220 and lenCalls <= 5280:
        return 88
    elif lenCalls > 5280 and lenCalls <= 5340:
        return 89
    elif lenCalls > 5340 and lenCalls <= 5400:
        return 90
    elif lenCalls > 5400 and lenCalls <= 5460:
        return 91
    elif lenCalls > 5460 and lenCalls <= 5520:
        return 92
    elif lenCalls > 5520 and lenCalls <= 5580:
        return 93
    elif lenCalls > 5580 and lenCalls <= 5640:
        return 94
    elif lenCalls > 5640 and lenCalls <= 5700:
        return 95
    elif lenCalls > 5700 and lenCalls <= 5760:
        return 96
    elif lenCalls > 5760 and lenCalls <= 5820:
        return 97
    elif lenCalls > 5820 and lenCalls <= 5880:
        return 98
    elif lenCalls > 5880 and lenCalls <= 5940:
        return 99
    elif lenCalls > 5940 and lenCalls <= 6000:
        return 100
    elif lenCalls > 6000 and lenCalls <= 6060:
        return 101
    elif lenCalls > 6060 and lenCalls <= 6120:
        return 102
    elif lenCalls > 6120 and lenCalls <= 6180:
        return 103
    elif lenCalls > 6180 and lenCalls <= 6240:
        return 104
    elif lenCalls > 6240 and lenCalls <= 6300:
        return 105
    elif lenCalls > 6300 and lenCalls <= 6360:
        return 106
    elif lenCalls > 6360 and lenCalls <= 6420:
        return 107
    elif lenCalls > 6420 and lenCalls <= 6480:
        return 108
    elif lenCalls > 6480 and lenCalls <= 6540:
        return 109
    elif lenCalls > 6540 and lenCalls <= 6600:
        return 110
    elif lenCalls > 6600 and lenCalls <= 6660:
        return 111
    elif lenCalls > 6660 and lenCalls <= 6720:
        return 112
    elif lenCalls > 6720 and lenCalls <= 6780:
        return 113
    elif lenCalls > 6780 and lenCalls <= 6840:
        return 114
    elif lenCalls > 6840 and lenCalls <= 6900:
        return 115
    elif lenCalls > 6900 and lenCalls <= 6960:
        return 116
    elif lenCalls > 6960 and lenCalls <= 7020:
        return 117
    elif lenCalls > 7020 and lenCalls <= 7080:
        return 118
    elif lenCalls > 7080 and lenCalls <= 7140:
        return 119
    elif lenCalls > 7140 and lenCalls <= 7200:
        return 120
    elif lenCalls > 7200 and lenCalls <= 7260:
        return 121
    elif lenCalls > 7260 and lenCalls <= 7320:
        return 122
    elif lenCalls > 7320 and lenCalls <= 7380:
        return 123
    elif lenCalls > 7380 and lenCalls <= 7440:
        return 124
    elif lenCalls > 7440 and lenCalls <= 7500:
        return 125
    elif lenCalls > 7500 and lenCalls <= 7560:
        return 126
    elif lenCalls > 7560 and lenCalls <= 7620:
        return 127
    elif lenCalls > 7620 and lenCalls <= 7680:
        return 128
    elif lenCalls > 7680 and lenCalls <= 7740:
        return 129
    elif lenCalls > 7740 and lenCalls <= 7800:
        return 130
    elif lenCalls > 7800 and lenCalls <= 7860:
        return 131
    elif lenCalls > 7860 and lenCalls <= 7920:
        return 132
    elif lenCalls > 7920 and lenCalls <= 7980:
        return 133
    elif lenCalls > 7980 and lenCalls <= 8040:
        return 134
    elif lenCalls > 8040 and lenCalls <= 8100:
        return 135
    elif lenCalls > 8100 and lenCalls <= 8160:
        return 136
    elif lenCalls > 8160 and lenCalls <= 8220:
        return 137
    elif lenCalls > 8220 and lenCalls <= 8280:
        return 138
    elif lenCalls > 8280 and lenCalls <= 8340:
        return 139
    elif lenCalls > 8340 and lenCalls <= 8400:
        return 140
    elif lenCalls > 8400 and lenCalls <= 8460:
        return 141
    elif lenCalls > 8460 and lenCalls <= 8520:
        return 142
    elif lenCalls > 8520 and lenCalls <= 8580:
        return 143
    elif lenCalls > 8580 and lenCalls <= 8640:
        return 144
    elif lenCalls > 8640 and lenCalls <= 8700:
        return 145
    elif lenCalls > 8700 and lenCalls <= 8760:
        return 146
    elif lenCalls > 8760 and lenCalls <= 8820:
        return 147
    elif lenCalls > 8820 and lenCalls <= 8880:
        return 148
    elif lenCalls > 8880 and lenCalls <= 8940:
        return 149
    elif lenCalls > 8940 and lenCalls <= 9000:
        return 150
    elif lenCalls > 9000 and lenCalls <= 9060:
        return 151
    elif lenCalls > 9060 and lenCalls <= 9120:
        return 152
    elif lenCalls > 9120 and lenCalls <= 9180:
        return 153
    elif lenCalls > 9180 and lenCalls <= 9240:
        return 154
    elif lenCalls > 9240 and lenCalls <= 9300:
        return 155
    elif lenCalls > 9300 and lenCalls <= 9360:
        return 156
    elif lenCalls > 9360 and lenCalls <= 9420:
        return 157
    elif lenCalls > 9420 and lenCalls <= 9480:
        return 158
    elif lenCalls > 9480 and lenCalls <= 9540:
        return 159
    elif lenCalls > 9540 and lenCalls <= 9600:
        return 160
    elif lenCalls > 9600 and lenCalls <= 9660:
        return 161
    elif lenCalls > 9660 and lenCalls <= 9720:
        return 162
    elif lenCalls > 9720 and lenCalls <= 9780:
        return 163
    elif lenCalls > 9780 and lenCalls <= 9840:
        return 164
    elif lenCalls > 9840 and lenCalls <= 9900:
        return 165
    elif lenCalls > 9900 and lenCalls <= 9960:
        return 166
    elif lenCalls > 9960 and lenCalls <= 10020:
        return 167
    elif lenCalls > 10020 and lenCalls <= 10080:
        return 168
    elif lenCalls > 10080 and lenCalls <= 10140:
        return 169
    elif lenCalls > 10140 and lenCalls <= 10200:
        return 170
    elif lenCalls > 10200 and lenCalls <= 10260:
        return 171
    elif lenCalls > 10260 and lenCalls <= 10320:
        return 172
    elif lenCalls > 10320 and lenCalls <= 10380:
        return 173
    elif lenCalls > 10380 and lenCalls <= 10440:
        return 174
    elif lenCalls > 10440 and lenCalls <= 10500:
        return 175
    elif lenCalls > 10500 and lenCalls <= 10560:
        return 176
    elif lenCalls > 10560 and lenCalls <= 10620:
        return 177
    elif lenCalls > 10620 and lenCalls <= 10680:
        return 178
    elif lenCalls > 10680 and lenCalls <= 10740:
        return 179
    elif lenCalls > 10740 and lenCalls <= 10800:
        return 180
    elif lenCalls > 10800 and lenCalls <= 10860:
        return 181
    elif lenCalls > 10860 and lenCalls <= 10920:
        return 182
    elif lenCalls > 10920 and lenCalls <= 10980:
        return 183
    elif lenCalls > 10980 and lenCalls <= 11040:
        return 184
    elif lenCalls > 11040 and lenCalls <= 11100:
        return 185
    elif lenCalls > 11100 and lenCalls <= 11160:
        return 186
    elif lenCalls > 11160 and lenCalls <= 11220:
        return 187
    elif lenCalls > 11220 and lenCalls <= 11280:
        return 188
    elif lenCalls > 11280 and lenCalls <= 11340:
        return 189
    elif lenCalls > 11340 and lenCalls <= 11400:
        return 190
    elif lenCalls > 11400 and lenCalls <= 11460:
        return 191
    elif lenCalls > 11460 and lenCalls <= 11520:
        return 192
    elif lenCalls > 11520 and lenCalls <= 11580:
        return 193
    elif lenCalls > 11580 and lenCalls <= 11640:
        return 194
    elif lenCalls > 11640 and lenCalls <= 11700:
        return 195
    elif lenCalls > 11700 and lenCalls <= 11760:
        return 196
    elif lenCalls > 11760 and lenCalls <= 11820:
        return 197
    elif lenCalls > 11820 and lenCalls <= 11880:
        return 198
    elif lenCalls > 11880 and lenCalls <= 11940:
        return 199
    elif lenCalls > 11940 and lenCalls <= 12000:
        return 200
    elif lenCalls > 12000 and lenCalls <= 12060:
        return 201
    elif lenCalls > 12060 and lenCalls <= 12120:
        return 202
    elif lenCalls > 12120 and lenCalls <= 12180:
        return 203
    elif lenCalls > 12180 and lenCalls <= 12240:
        return 204
    elif lenCalls > 12240 and lenCalls <= 12300:
        return 205
    elif lenCalls > 12300 and lenCalls <= 12360:
        return 206
    elif lenCalls > 12360 and lenCalls <= 12420:
        return 207
    elif lenCalls > 12420 and lenCalls <= 12480:
        return 208
    elif lenCalls > 12480 and lenCalls <= 12540:
        return 209
    elif lenCalls > 12540 and lenCalls <= 12600:
        return 210
    elif lenCalls > 12600 and lenCalls <= 12660:
        return 211
    elif lenCalls > 12660 and lenCalls <= 12720:
        return 212
    elif lenCalls > 12720 and lenCalls <= 12780:
        return 213
    elif lenCalls > 12780 and lenCalls <= 12840:
        return 214
    elif lenCalls > 12840 and lenCalls <= 12900:
        return 215
    elif lenCalls > 12900 and lenCalls <= 12960:
        return 216
    elif lenCalls > 12960 and lenCalls <= 13020:
        return 217
    elif lenCalls > 13020 and lenCalls <= 13080:
        return 218
    elif lenCalls > 13080 and lenCalls <= 13140:
        return 219
    elif lenCalls > 13140 and lenCalls <= 13200:
        return 220
    elif lenCalls > 13200 and lenCalls <= 13260:
        return 221
    elif lenCalls > 13260 and lenCalls <= 13320:
        return 222
    elif lenCalls > 13320 and lenCalls <= 13380:
        return 223
    elif lenCalls > 13380 and lenCalls <= 13440:
        return 224
    elif lenCalls > 13440 and lenCalls <= 13500:
        return 225
    elif lenCalls > 13500 and lenCalls <= 13560:
        return 226
    elif lenCalls > 13560 and lenCalls <= 13620:
        return 227
    elif lenCalls > 13620 and lenCalls <= 13680:
        return 228
    elif lenCalls > 13680 and lenCalls <= 13740:
        return 229
    elif lenCalls > 13740 and lenCalls <= 13800:
        return 230
    elif lenCalls > 13800 and lenCalls <= 13860:
        return 231
    elif lenCalls > 13860 and lenCalls <= 13920:
        return 232
    elif lenCalls > 13920 and lenCalls <= 13980:
        return 233
    elif lenCalls > 13980 and lenCalls <= 14040:
        return 234
    elif lenCalls > 14040 and lenCalls <= 14100:
        return 235
    elif lenCalls > 14100 and lenCalls <= 14160:
        return 236
    elif lenCalls > 14160 and lenCalls <= 14220:
        return 237
    elif lenCalls > 14220 and lenCalls <= 14280:
        return 238
    elif lenCalls > 14280 and lenCalls <= 14340:
        return 239
    elif lenCalls > 14340 and lenCalls <= 14400:
        return 240
    elif lenCalls > 14400 and lenCalls <= 14460:
        return 241
    elif lenCalls > 14460 and lenCalls <= 14520:
        return 242
    elif lenCalls > 14520 and lenCalls <= 14580:
        return 243
    elif lenCalls > 14580 and lenCalls <= 14640:
        return 244
    elif lenCalls > 14640 and lenCalls <= 14700:
        return 245
    elif lenCalls > 14700 and lenCalls <= 14760:
        return 246
    elif lenCalls > 14760 and lenCalls <= 14820:
        return 247
    elif lenCalls > 14820 and lenCalls <= 14880:
        return 248
    elif lenCalls > 14880 and lenCalls <= 14940:
        return 249
    elif lenCalls > 14940 and lenCalls <= 15000:
        return 250
    elif lenCalls > 15000 and lenCalls <= 15060:
        return 251
    elif lenCalls > 15060 and lenCalls <= 15120:
        return 252
    elif lenCalls > 15120 and lenCalls <= 15180:
        return 253
    elif lenCalls > 15180 and lenCalls <= 15240:
        return 254
    elif lenCalls > 15240 and lenCalls <= 15300:
        return 255
    elif lenCalls > 15300 and lenCalls <= 15360:
        return 256
    elif lenCalls > 15360 and lenCalls <= 15420:
        return 257
    elif lenCalls > 15420 and lenCalls <= 15480:
        return 258
    elif lenCalls > 15480 and lenCalls <= 15540:
        return 259
    elif lenCalls > 15540 and lenCalls <= 15600:
        return 260
    elif lenCalls > 15600 and lenCalls <= 15660:
        return 261
    elif lenCalls > 15660 and lenCalls <= 15720:
        return 262
    elif lenCalls > 15720 and lenCalls <= 15780:
        return 263
    elif lenCalls > 15780 and lenCalls <= 15840:
        return 264
    elif lenCalls > 15840 and lenCalls <= 15900:
        return 265
    elif lenCalls > 15900 and lenCalls <= 15960:
        return 266
    elif lenCalls > 15960 and lenCalls <= 16020:
        return 267
    elif lenCalls > 16020 and lenCalls <= 16080:
        return 268
    elif lenCalls > 16080 and lenCalls <= 16140:
        return 269
    elif lenCalls > 16140 and lenCalls <= 16200:
        return 270
    elif lenCalls > 16200 and lenCalls <= 16260:
        return 271
    elif lenCalls > 16260 and lenCalls <= 16320:
        return 272
    elif lenCalls > 16320 and lenCalls <= 16380:
        return 273
    elif lenCalls > 16380 and lenCalls <= 16440:
        return 274
    elif lenCalls > 16440 and lenCalls <= 16500:
        return 275
    elif lenCalls > 16500 and lenCalls <= 16560:
        return 276
    elif lenCalls > 16560 and lenCalls <= 16620:
        return 277
    elif lenCalls > 16620 and lenCalls <= 16680:
        return 278
    elif lenCalls > 16680 and lenCalls <= 16740:
        return 279
    elif lenCalls > 16740 and lenCalls <= 16800:
        return 280
    elif lenCalls > 16800 and lenCalls <= 16860:
        return 281
    elif lenCalls > 16860 and lenCalls <= 16920:
        return 282
    elif lenCalls > 16920 and lenCalls <= 16980:
        return 283
    elif lenCalls > 16980 and lenCalls <= 17040:
        return 284
    elif lenCalls > 17040 and lenCalls <= 17100:
        return 285
    elif lenCalls > 17100 and lenCalls <= 17160:
        return 286
    elif lenCalls > 17160 and lenCalls <= 17220:
        return 287
    elif lenCalls > 17220 and lenCalls <= 17280:
        return 288
    elif lenCalls > 17280 and lenCalls <= 17340:
        return 289
    elif lenCalls > 17340 and lenCalls <= 17400:
        return 290
    elif lenCalls > 17400 and lenCalls <= 17460:
        return 291
    elif lenCalls > 17460 and lenCalls <= 17520:
        return 292
    elif lenCalls > 17520 and lenCalls <= 17580:
        return 293
    elif lenCalls > 17580 and lenCalls <= 17640:
        return 294
    elif lenCalls > 17640 and lenCalls <= 17700:
        return 295
    elif lenCalls > 17700 and lenCalls <= 17760:
        return 296
    elif lenCalls > 17760 and lenCalls <= 17820:
        return 297
    elif lenCalls > 17820 and lenCalls <= 17880:
        return 298
    elif lenCalls > 17880 and lenCalls <= 17940:
        return 299
    elif lenCalls > 17940 and lenCalls <= 18000:
        return 300
    elif lenCalls > 18000 and lenCalls <= 18060:
        return 301
    elif lenCalls > 18060 and lenCalls <= 18120:
        return 302
    elif lenCalls > 18120 and lenCalls <= 18180:
        return 303
    elif lenCalls > 18180 and lenCalls <= 18240:
        return 304
    elif lenCalls > 18240 and lenCalls <= 18300:
        return 305
    elif lenCalls > 18300 and lenCalls <= 18360:
        return 306
    elif lenCalls > 18360 and lenCalls <= 18420:
        return 307
    elif lenCalls > 18420 and lenCalls <= 18480:
        return 308
    elif lenCalls > 18480 and lenCalls <= 18540:
        return 309
    elif lenCalls > 18540 and lenCalls <= 18600:
        return 310
    elif lenCalls > 18600 and lenCalls <= 18660:
        return 311
    elif lenCalls > 18660 and lenCalls <= 18720:
        return 312
    elif lenCalls > 18720 and lenCalls <= 18780:
        return 313
    elif lenCalls > 18780 and lenCalls <= 18840:
        return 314
    elif lenCalls > 18840 and lenCalls <= 18900:
        return 315
    elif lenCalls > 18900 and lenCalls <= 18960:
        return 316
    elif lenCalls > 18960 and lenCalls <= 19020:
        return 317
    elif lenCalls > 19020 and lenCalls <= 19080:
        return 318
    elif lenCalls > 19080 and lenCalls <= 19140:
        return 319
    elif lenCalls > 19140 and lenCalls <= 19200:
        return 320
    elif lenCalls > 19200 and lenCalls <= 19260:
        return 321
    elif lenCalls > 19260 and lenCalls <= 19320:
        return 322
    elif lenCalls > 19320 and lenCalls <= 19380:
        return 323
    elif lenCalls > 19380 and lenCalls <= 19440:
        return 324
    elif lenCalls > 19440 and lenCalls <= 19500:
        return 325
    elif lenCalls > 19500 and lenCalls <= 19560:
        return 326
    elif lenCalls > 19560 and lenCalls <= 19620:
        return 327
    elif lenCalls > 19620 and lenCalls <= 19680:
        return 328
    elif lenCalls > 19680 and lenCalls <= 19740:
        return 329
    elif lenCalls > 19740 and lenCalls <= 19800:
        return 330
    elif lenCalls > 19800 and lenCalls <= 19860:
        return 331
    elif lenCalls > 19860 and lenCalls <= 19920:
        return 332
    elif lenCalls > 19920 and lenCalls <= 19980:
        return 333
    elif lenCalls > 19980 and lenCalls <= 20040:
        return 334
    elif lenCalls > 20040 and lenCalls <= 20100:
        return 335
    elif lenCalls > 20100 and lenCalls <= 20160:
        return 336
    elif lenCalls > 20160 and lenCalls <= 20220:
        return 337
    elif lenCalls > 20220 and lenCalls <= 20280:
        return 338
    elif lenCalls > 20280 and lenCalls <= 20340:
        return 339
    elif lenCalls > 20340 and lenCalls <= 20400:
        return 340
    elif lenCalls > 20400 and lenCalls <= 20460:
        return 341
    elif lenCalls > 20460 and lenCalls <= 20520:
        return 342
    elif lenCalls > 20520 and lenCalls <= 20580:
        return 343
    elif lenCalls > 20580 and lenCalls <= 20640:
        return 344
    elif lenCalls > 20640 and lenCalls <= 20700:
        return 345
    elif lenCalls > 20700 and lenCalls <= 20760:
        return 346
    elif lenCalls > 20760 and lenCalls <= 20820:
        return 347
    elif lenCalls > 20820 and lenCalls <= 20880:
        return 348
    elif lenCalls > 20880 and lenCalls <= 20940:
        return 349
    elif lenCalls > 20940 and lenCalls <= 21000:
        return 350
    elif lenCalls > 21000 and lenCalls <= 21060:
        return 351
    elif lenCalls > 21060 and lenCalls <= 21120:
        return 352
    elif lenCalls > 21120 and lenCalls <= 21180:
        return 353
    elif lenCalls > 21180 and lenCalls <= 21240:
        return 354
    elif lenCalls > 21240 and lenCalls <= 21300:
        return 355
    elif lenCalls > 21300 and lenCalls <= 21360:
        return 356
    elif lenCalls > 21360 and lenCalls <= 21420:
        return 357
    elif lenCalls > 21420 and lenCalls <= 21480:
        return 358
    elif lenCalls > 21480 and lenCalls <= 21540:
        return 359
    elif lenCalls > 21540 and lenCalls <= 21600:
        return 360
    elif lenCalls > 21600 and lenCalls <= 21660:
        return 361
    elif lenCalls > 21660 and lenCalls <= 21720:
        return 362
    elif lenCalls > 21720 and lenCalls <= 21780:
        return 363
    elif lenCalls > 21780 and lenCalls <= 21840:
        return 364
    elif lenCalls > 21840 and lenCalls <= 21900:
        return 365
    elif lenCalls > 21900 and lenCalls <= 21960:
        return 366
    elif lenCalls > 21960 and lenCalls <= 22020:
        return 367
    elif lenCalls > 22020 and lenCalls <= 22080:
        return 368
    elif lenCalls > 22080 and lenCalls <= 22140:
        return 369
    elif lenCalls > 22140 and lenCalls <= 22200:
        return 370
    elif lenCalls > 22200 and lenCalls <= 22260:
        return 371
    elif lenCalls > 22260 and lenCalls <= 22320:
        return 372
    elif lenCalls > 22320 and lenCalls <= 22380:
        return 373
    elif lenCalls > 22380 and lenCalls <= 22440:
        return 374
    elif lenCalls > 22440 and lenCalls <= 22500:
        return 375
    elif lenCalls > 22500 and lenCalls <= 22560:
        return 376
    elif lenCalls > 22560 and lenCalls <= 22620:
        return 377
    elif lenCalls > 22620 and lenCalls <= 22680:
        return 378
    elif lenCalls > 22680 and lenCalls <= 22740:
        return 379
    elif lenCalls > 22740 and lenCalls <= 22800:
        return 380
    elif lenCalls > 22800 and lenCalls <= 22860:
        return 381
    elif lenCalls > 22860 and lenCalls <= 22920:
        return 382
    elif lenCalls > 22920 and lenCalls <= 22980:
        return 383
    elif lenCalls > 22980 and lenCalls <= 23040:
        return 384
    elif lenCalls > 23040 and lenCalls <= 23100:
        return 385
    elif lenCalls > 23100 and lenCalls <= 23160:
        return 386
    elif lenCalls > 23160 and lenCalls <= 23220:
        return 387
    elif lenCalls > 23220 and lenCalls <= 23280:
        return 388
    elif lenCalls > 23280 and lenCalls <= 23340:
        return 389
    elif lenCalls > 23340 and lenCalls <= 23400:
        return 390
    elif lenCalls > 23400 and lenCalls <= 23460:
        return 391
    elif lenCalls > 23460 and lenCalls <= 23520:
        return 392
    elif lenCalls > 23520 and lenCalls <= 23580:
        return 393
    elif lenCalls > 23580 and lenCalls <= 23640:
        return 394
    elif lenCalls > 23640 and lenCalls <= 23700:
        return 395
    elif lenCalls > 23700 and lenCalls <= 23760:
        return 396
    elif lenCalls > 23760 and lenCalls <= 23820:
        return 397
    elif lenCalls > 23820 and lenCalls <= 23880:
        return 398
    elif lenCalls > 23880 and lenCalls <= 23940:
        return 399
    elif lenCalls > 23940 and lenCalls <= 24000:
        return 400
    elif lenCalls > 24000 and lenCalls <= 24060:
        return 401
    elif lenCalls > 24060 and lenCalls <= 24120:
        return 402
    elif lenCalls > 24120 and lenCalls <= 24180:
        return 403
    elif lenCalls > 24180 and lenCalls <= 24240:
        return 404
    elif lenCalls > 24240 and lenCalls <= 24300:
        return 405
    elif lenCalls > 24300 and lenCalls <= 24360:
        return 406
    elif lenCalls > 24360 and lenCalls <= 24420:
        return 407
    elif lenCalls > 24420 and lenCalls <= 24480:
        return 408
    elif lenCalls > 24480 and lenCalls <= 24540:
        return 409
    elif lenCalls > 24540 and lenCalls <= 24600:
        return 410
    elif lenCalls > 24600 and lenCalls <= 24660:
        return 411
    elif lenCalls > 24660 and lenCalls <= 24720:
        return 412
    elif lenCalls > 24720 and lenCalls <= 24780:
        return 413
    elif lenCalls > 24780 and lenCalls <= 24840:
        return 414
    elif lenCalls > 24840 and lenCalls <= 24900:
        return 415
    elif lenCalls > 24900 and lenCalls <= 24960:
        return 416
    elif lenCalls > 24960 and lenCalls <= 25020:
        return 417
    elif lenCalls > 25020 and lenCalls <= 25080:
        return 418
    elif lenCalls > 25080 and lenCalls <= 25140:
        return 419
    elif lenCalls > 25140 and lenCalls <= 25200:
        return 420
    elif lenCalls > 25200 and lenCalls <= 25260:
        return 421
    elif lenCalls > 25260 and lenCalls <= 25320:
        return 422
    elif lenCalls > 25320 and lenCalls <= 25380:
        return 423
    elif lenCalls > 25380 and lenCalls <= 25440:
        return 424
    elif lenCalls > 25440 and lenCalls <= 25500:
        return 425
    elif lenCalls > 25500 and lenCalls <= 25560:
        return 426
    elif lenCalls > 25560 and lenCalls <= 25620:
        return 427
    elif lenCalls > 25620 and lenCalls <= 25680:
        return 428
    elif lenCalls > 25680 and lenCalls <= 25740:
        return 429
    elif lenCalls > 25740 and lenCalls <= 25800:
        return 430
    elif lenCalls > 25800 and lenCalls <= 25860:
        return 431
    elif lenCalls > 25860 and lenCalls <= 25920:
        return 432
    elif lenCalls > 25920 and lenCalls <= 25980:
        return 433
    elif lenCalls > 25980 and lenCalls <= 26040:
        return 434
    elif lenCalls > 26040 and lenCalls <= 26100:
        return 435
    elif lenCalls > 26100 and lenCalls <= 26160:
        return 436
    elif lenCalls > 26160 and lenCalls <= 26220:
        return 437
    elif lenCalls > 26220 and lenCalls <= 26280:
        return 438
    elif lenCalls > 26280 and lenCalls <= 26340:
        return 439
    elif lenCalls > 26340 and lenCalls <= 26400:
        return 440
    elif lenCalls > 26400 and lenCalls <= 26460:
        return 441
    elif lenCalls > 26460 and lenCalls <= 26520:
        return 442
    elif lenCalls > 26520 and lenCalls <= 26580:
        return 443
    elif lenCalls > 26580 and lenCalls <= 26640:
        return 444
    elif lenCalls > 26640 and lenCalls <= 26700:
        return 445
    elif lenCalls > 26700 and lenCalls <= 26760:
        return 446
    elif lenCalls > 26760 and lenCalls <= 26820:
        return 447
    elif lenCalls > 26820 and lenCalls <= 26880:
        return 448
    elif lenCalls > 26880 and lenCalls <= 26940:
        return 449
    elif lenCalls > 26940 and lenCalls <= 27000:
        return 450
    elif lenCalls > 27000 and lenCalls <= 27060:
        return 451
    elif lenCalls > 27060 and lenCalls <= 27120:
        return 452
    elif lenCalls > 27120 and lenCalls <= 27180:
        return 453
    elif lenCalls > 27180 and lenCalls <= 27240:
        return 454
    elif lenCalls > 27240 and lenCalls <= 27300:
        return 455
    elif lenCalls > 27300 and lenCalls <= 27360:
        return 456
    elif lenCalls > 27360 and lenCalls <= 27420:
        return 457
    elif lenCalls > 27420 and lenCalls <= 27480:
        return 458
    elif lenCalls > 27480 and lenCalls <= 27540:
        return 459
    elif lenCalls > 27540 and lenCalls <= 27600:
        return 460
    elif lenCalls > 27600 and lenCalls <= 27660:
        return 461
    elif lenCalls > 27660 and lenCalls <= 27720:
        return 462
    elif lenCalls > 27720 and lenCalls <= 27780:
        return 463
    elif lenCalls > 27780 and lenCalls <= 27840:
        return 464
    elif lenCalls > 27840 and lenCalls <= 27900:
        return 465
    elif lenCalls > 27900 and lenCalls <= 27960:
        return 466
    elif lenCalls > 27960 and lenCalls <= 28020:
        return 467
    elif lenCalls > 28020 and lenCalls <= 28080:
        return 468
    elif lenCalls > 28080 and lenCalls <= 28140:
        return 469
    elif lenCalls > 28140 and lenCalls <= 28200:
        return 470
    elif lenCalls > 28200 and lenCalls <= 28260:
        return 471
    elif lenCalls > 28260 and lenCalls <= 28320:
        return 472
    elif lenCalls > 28320 and lenCalls <= 28380:
        return 473
    elif lenCalls > 28380 and lenCalls <= 28440:
        return 474
    elif lenCalls > 28440 and lenCalls <= 28500:
        return 475
    elif lenCalls > 28500 and lenCalls <= 28560:
        return 476
    elif lenCalls > 28560 and lenCalls <= 28620:
        return 477
    elif lenCalls > 28620 and lenCalls <= 28680:
        return 478
    elif lenCalls > 28680 and lenCalls <= 28740:
        return 479
    elif lenCalls > 28740 and lenCalls <= 28800:
        return 480
    elif lenCalls > 28800 and lenCalls <= 28860:
        return 481
    elif lenCalls > 28860 and lenCalls <= 28920:
        return 482
    elif lenCalls > 28920 and lenCalls <= 28980:
        return 483
    elif lenCalls > 28980 and lenCalls <= 29040:
        return 484
    elif lenCalls > 29040 and lenCalls <= 29100:
        return 485
    elif lenCalls > 29100 and lenCalls <= 29160:
        return 486
    elif lenCalls > 29160 and lenCalls <= 29220:
        return 487
    elif lenCalls > 29220 and lenCalls <= 29280:
        return 488
    elif lenCalls > 29280 and lenCalls <= 29340:
        return 489
    elif lenCalls > 29340 and lenCalls <= 29400:
        return 490
    elif lenCalls > 29400 and lenCalls <= 29460:
        return 491
    elif lenCalls > 29460 and lenCalls <= 29520:
        return 492
    elif lenCalls > 29520 and lenCalls <= 29580:
        return 493
    elif lenCalls > 29580 and lenCalls <= 29640:
        return 494
    elif lenCalls > 29640 and lenCalls <= 29700:
        return 495
    elif lenCalls > 29700 and lenCalls <= 29760:
        return 496
    elif lenCalls > 29760 and lenCalls <= 29820:
        return 497
    elif lenCalls > 29820 and lenCalls <= 29880:
        return 498
    elif lenCalls > 29880 and lenCalls <= 29940:
        return 499
    elif lenCalls > 29940 and lenCalls <= 30000:
        return 500
    elif lenCalls > 30000 and lenCalls <= 30060:
        return 501
    elif lenCalls > 30060 and lenCalls <= 30120:
        return 502
    elif lenCalls > 30120 and lenCalls <= 30180:
        return 503
    elif lenCalls > 30180 and lenCalls <= 30240:
        return 504
    elif lenCalls > 30240 and lenCalls <= 30300:
        return 505
    elif lenCalls > 30300 and lenCalls <= 30360:
        return 506
    elif lenCalls > 30360 and lenCalls <= 30420:
        return 507
    elif lenCalls > 30420 and lenCalls <= 30480:
        return 508
    elif lenCalls > 30480 and lenCalls <= 30540:
        return 509
    elif lenCalls > 30540 and lenCalls <= 30600:
        return 510
    elif lenCalls > 30600 and lenCalls <= 30660:
        return 511
    elif lenCalls > 30660 and lenCalls <= 30720:
        return 512
    elif lenCalls > 30720 and lenCalls <= 30780:
        return 513
    elif lenCalls > 30780 and lenCalls <= 30840:
        return 514
    elif lenCalls > 30840 and lenCalls <= 30900:
        return 515
    elif lenCalls > 30900 and lenCalls <= 30960:
        return 516
    elif lenCalls > 30960 and lenCalls <= 31020:
        return 517
    elif lenCalls > 31020 and lenCalls <= 31080:
        return 518
    elif lenCalls > 31080 and lenCalls <= 31140:
        return 519
    elif lenCalls > 31140 and lenCalls <= 31200:
        return 520
    elif lenCalls > 31200 and lenCalls <= 31260:
        return 521
    elif lenCalls > 31260 and lenCalls <= 31320:
        return 522
    elif lenCalls > 31320 and lenCalls <= 31380:
        return 523
    elif lenCalls > 31380 and lenCalls <= 31440:
        return 524
    elif lenCalls > 31440 and lenCalls <= 31500:
        return 525
    elif lenCalls > 31500 and lenCalls <= 31560:
        return 526
    elif lenCalls > 31560 and lenCalls <= 31620:
        return 527
    elif lenCalls > 31620 and lenCalls <= 31680:
        return 528
    elif lenCalls > 31680 and lenCalls <= 31740:
        return 529
    elif lenCalls > 31740 and lenCalls <= 31800:
        return 530
    elif lenCalls > 31800 and lenCalls <= 31860:
        return 531
    elif lenCalls > 31860 and lenCalls <= 31920:
        return 532
    elif lenCalls > 31920 and lenCalls <= 31980:
        return 533
    elif lenCalls > 31980 and lenCalls <= 32040:
        return 534
    elif lenCalls > 32040 and lenCalls <= 32100:
        return 535
    elif lenCalls > 32100 and lenCalls <= 32160:
        return 536
    elif lenCalls > 32160 and lenCalls <= 32220:
        return 537
    elif lenCalls > 32220 and lenCalls <= 32280:
        return 538
    elif lenCalls > 32280 and lenCalls <= 32340:
        return 539
    elif lenCalls > 32340 and lenCalls <= 32400:
        return 540
    elif lenCalls > 32400 and lenCalls <= 32460:
        return 541
    elif lenCalls > 32460 and lenCalls <= 32520:
        return 542
    elif lenCalls > 32520 and lenCalls <= 32580:
        return 543
    elif lenCalls > 32580 and lenCalls <= 32640:
        return 544
    elif lenCalls > 32640 and lenCalls <= 32700:
        return 545
    elif lenCalls > 32700 and lenCalls <= 32760:
        return 546
    elif lenCalls > 32760 and lenCalls <= 32820:
        return 547
    elif lenCalls > 32820 and lenCalls <= 32880:
        return 548
    elif lenCalls > 32880 and lenCalls <= 32940:
        return 549
    elif lenCalls > 32940 and lenCalls <= 33000:
        return 550
    elif lenCalls > 33000 and lenCalls <= 33060:
        return 551
    elif lenCalls > 33060 and lenCalls <= 33120:
        return 552
    elif lenCalls > 33120 and lenCalls <= 33180:
        return 553
    elif lenCalls > 33180 and lenCalls <= 33240:
        return 554
    elif lenCalls > 33240 and lenCalls <= 33300:
        return 555
    elif lenCalls > 33300 and lenCalls <= 33360:
        return 556
    elif lenCalls > 33360 and lenCalls <= 33420:
        return 557
    elif lenCalls > 33420 and lenCalls <= 33480:
        return 558
    elif lenCalls > 33480 and lenCalls <= 33540:
        return 559
    elif lenCalls > 33540 and lenCalls <= 33600:
        return 560
    elif lenCalls > 33600 and lenCalls <= 33660:
        return 561
    elif lenCalls > 33660 and lenCalls <= 33720:
        return 562
    elif lenCalls > 33720 and lenCalls <= 33780:
        return 563
    elif lenCalls > 33780 and lenCalls <= 33840:
        return 564
    elif lenCalls > 33840 and lenCalls <= 33900:
        return 565
    elif lenCalls > 33900 and lenCalls <= 33960:
        return 566
    elif lenCalls > 33960 and lenCalls <= 34020:
        return 567
    elif lenCalls > 34020 and lenCalls <= 34080:
        return 568
    elif lenCalls > 34080 and lenCalls <= 34140:
        return 569
    elif lenCalls > 34140 and lenCalls <= 34200:
        return 570
    elif lenCalls > 34200 and lenCalls <= 34260:
        return 571
    elif lenCalls > 34260 and lenCalls <= 34320:
        return 572
    elif lenCalls > 34320 and lenCalls <= 34380:
        return 573
    elif lenCalls > 34380 and lenCalls <= 34440:
        return 574
    elif lenCalls > 34440 and lenCalls <= 34500:
        return 575
    elif lenCalls > 34500 and lenCalls <= 34560:
        return 576
    elif lenCalls > 34560 and lenCalls <= 34620:
        return 577
    elif lenCalls > 34620 and lenCalls <= 34680:
        return 578
    elif lenCalls > 34680 and lenCalls <= 34740:
        return 579
    elif lenCalls > 34740 and lenCalls <= 34800:
        return 580
    elif lenCalls > 34800 and lenCalls <= 34860:
        return 581
    elif lenCalls > 34860 and lenCalls <= 34920:
        return 582
    elif lenCalls > 34920 and lenCalls <= 34980:
        return 583
    elif lenCalls > 34980 and lenCalls <= 35040:
        return 584
    elif lenCalls > 35040 and lenCalls <= 35100:
        return 585
    elif lenCalls > 35100 and lenCalls <= 35160:
        return 586
    elif lenCalls > 35160 and lenCalls <= 35220:
        return 587
    elif lenCalls > 35220 and lenCalls <= 35280:
        return 588
    elif lenCalls > 35280 and lenCalls <= 35340:
        return 589
    elif lenCalls > 35340 and lenCalls <= 35400:
        return 590
    elif lenCalls > 35400 and lenCalls <= 35460:
        return 591
    elif lenCalls > 35460 and lenCalls <= 35520:
        return 592
    elif lenCalls > 35520 and lenCalls <= 35580:
        return 593
    elif lenCalls > 35580 and lenCalls <= 35640:
        return 594
    elif lenCalls > 35640 and lenCalls <= 35700:
        return 595
    elif lenCalls > 35700 and lenCalls <= 35760:
        return 596
    elif lenCalls > 35760 and lenCalls <= 35820:
        return 597
    elif lenCalls > 35820 and lenCalls <= 35880:
        return 598
    elif lenCalls > 35880 and lenCalls <= 35940:
        return 599
    elif lenCalls > 35940 and lenCalls <= 36000:
        return 600
    elif lenCalls > 36000 and lenCalls <= 36060:
        return 601
    elif lenCalls > 36060 and lenCalls <= 36120:
        return 602
    elif lenCalls > 36120 and lenCalls <= 36180:
        return 603
    elif lenCalls > 36180 and lenCalls <= 36240:
        return 604
    elif lenCalls > 36240 and lenCalls <= 36300:
        return 605
    elif lenCalls > 36300 and lenCalls <= 36360:
        return 606
    elif lenCalls > 36360 and lenCalls <= 36420:
        return 607
    elif lenCalls > 36420 and lenCalls <= 36480:
        return 608
    elif lenCalls > 36480 and lenCalls <= 36540:
        return 609
    elif lenCalls > 36540 and lenCalls <= 36600:
        return 610
    elif lenCalls > 36600 and lenCalls <= 36660:
        return 611
    elif lenCalls > 36660 and lenCalls <= 36720:
        return 612
    elif lenCalls > 36720 and lenCalls <= 36780:
        return 613
    elif lenCalls > 36780 and lenCalls <= 36840:
        return 614
    elif lenCalls > 36840 and lenCalls <= 36900:
        return 615
    elif lenCalls > 36900 and lenCalls <= 36960:
        return 616
    elif lenCalls > 36960 and lenCalls <= 37020:
        return 617
    elif lenCalls > 37020 and lenCalls <= 37080:
        return 618
    elif lenCalls > 37080 and lenCalls <= 37140:
        return 619
    elif lenCalls > 37140 and lenCalls <= 37200:
        return 620
    elif lenCalls > 37200 and lenCalls <= 37260:
        return 621
    elif lenCalls > 37260 and lenCalls <= 37320:
        return 622
    elif lenCalls > 37320 and lenCalls <= 37380:
        return 623
    elif lenCalls > 37380 and lenCalls <= 37440:
        return 624
    elif lenCalls > 37440 and lenCalls <= 37500:
        return 625
    elif lenCalls > 37500 and lenCalls <= 37560:
        return 626
    elif lenCalls > 37560 and lenCalls <= 37620:
        return 627
    elif lenCalls > 37620 and lenCalls <= 37680:
        return 628
    elif lenCalls > 37680 and lenCalls <= 37740:
        return 629
    elif lenCalls > 37740 and lenCalls <= 37800:
        return 630
    elif lenCalls > 37800 and lenCalls <= 37860:
        return 631
    elif lenCalls > 37860 and lenCalls <= 37920:
        return 632
    elif lenCalls > 37920 and lenCalls <= 37980:
        return 633
    elif lenCalls > 37980 and lenCalls <= 38040:
        return 634
    elif lenCalls > 38040 and lenCalls <= 38100:
        return 635
    elif lenCalls > 38100 and lenCalls <= 38160:
        return 636
    elif lenCalls > 38160 and lenCalls <= 38220:
        return 637
    elif lenCalls > 38220 and lenCalls <= 38280:
        return 638
    elif lenCalls > 38280 and lenCalls <= 38340:
        return 639
    elif lenCalls > 38340 and lenCalls <= 38400:
        return 640
    elif lenCalls > 38400 and lenCalls <= 38460:
        return 641
    elif lenCalls > 38460 and lenCalls <= 38520:
        return 642
    elif lenCalls > 38520 and lenCalls <= 38580:
        return 643
    elif lenCalls > 38580 and lenCalls <= 38640:
        return 644
    elif lenCalls > 38640 and lenCalls <= 38700:
        return 645
    elif lenCalls > 38700 and lenCalls <= 38760:
        return 646
    elif lenCalls > 38760 and lenCalls <= 38820:
        return 647
    elif lenCalls > 38820 and lenCalls <= 38880:
        return 648
    elif lenCalls > 38880 and lenCalls <= 38940:
        return 649
    elif lenCalls > 38940 and lenCalls <= 39000:
        return 650
    elif lenCalls > 39000 and lenCalls <= 39060:
        return 651
    elif lenCalls > 39060 and lenCalls <= 39120:
        return 652
    elif lenCalls > 39120 and lenCalls <= 39180:
        return 653
    elif lenCalls > 39180 and lenCalls <= 39240:
        return 654
    elif lenCalls > 39240 and lenCalls <= 39300:
        return 655
    elif lenCalls > 39300 and lenCalls <= 39360:
        return 656
    elif lenCalls > 39360 and lenCalls <= 39420:
        return 657
    elif lenCalls > 39420 and lenCalls <= 39480:
        return 658
    elif lenCalls > 39480 and lenCalls <= 39540:
        return 659
    elif lenCalls > 39540 and lenCalls <= 39600:
        return 660
    elif lenCalls > 39600 and lenCalls <= 39660:
        return 661
    elif lenCalls > 39660 and lenCalls <= 39720:
        return 662
    elif lenCalls > 39720 and lenCalls <= 39780:
        return 663
    elif lenCalls > 39780 and lenCalls <= 39840:
        return 664
    elif lenCalls > 39840 and lenCalls <= 39900:
        return 665
    elif lenCalls > 39900 and lenCalls <= 39960:
        return 666
    elif lenCalls > 39960 and lenCalls <= 40020:
        return 667
    elif lenCalls > 40020 and lenCalls <= 40080:
        return 668
    elif lenCalls > 40080 and lenCalls <= 40140:
        return 669
    elif lenCalls > 40140 and lenCalls <= 40200:
        return 670
    elif lenCalls > 40200 and lenCalls <= 40260:
        return 671
    elif lenCalls > 40260 and lenCalls <= 40320:
        return 672
    elif lenCalls > 40320 and lenCalls <= 40380:
        return 673
    elif lenCalls > 40380 and lenCalls <= 40440:
        return 674
    elif lenCalls > 40440 and lenCalls <= 40500:
        return 675
    elif lenCalls > 40500 and lenCalls <= 40560:
        return 676
    elif lenCalls > 40560 and lenCalls <= 40620:
        return 677
    elif lenCalls > 40620 and lenCalls <= 40680:
        return 678
    elif lenCalls > 40680 and lenCalls <= 40740:
        return 679
    elif lenCalls > 40740 and lenCalls <= 40800:
        return 680
    elif lenCalls > 40800 and lenCalls <= 40860:
        return 681
    elif lenCalls > 40860 and lenCalls <= 40920:
        return 682
    elif lenCalls > 40920 and lenCalls <= 40980:
        return 683
    elif lenCalls > 40980 and lenCalls <= 41040:
        return 684
    elif lenCalls > 41040 and lenCalls <= 41100:
        return 685
    elif lenCalls > 41100 and lenCalls <= 41160:
        return 686
    elif lenCalls > 41160 and lenCalls <= 41220:
        return 687
    elif lenCalls > 41220 and lenCalls <= 41280:
        return 688
    elif lenCalls > 41280 and lenCalls <= 41340:
        return 689
    elif lenCalls > 41340 and lenCalls <= 41400:
        return 690
    elif lenCalls > 41400 and lenCalls <= 41460:
        return 691
    elif lenCalls > 41460 and lenCalls <= 41520:
        return 692
    elif lenCalls > 41520 and lenCalls <= 41580:
        return 693
    elif lenCalls > 41580 and lenCalls <= 41640:
        return 694
    elif lenCalls > 41640 and lenCalls <= 41700:
        return 695
    elif lenCalls > 41700 and lenCalls <= 41760:
        return 696
    elif lenCalls > 41760 and lenCalls <= 41820:
        return 697
    elif lenCalls > 41820 and lenCalls <= 41880:
        return 698
    elif lenCalls > 41880 and lenCalls <= 41940:
        return 699
    elif lenCalls > 41940 and lenCalls <= 42000:
        return 700
    elif lenCalls > 42000 and lenCalls <= 42060:
        return 701
    elif lenCalls > 42060 and lenCalls <= 42120:
        return 702
    elif lenCalls > 42120 and lenCalls <= 42180:
        return 703
    elif lenCalls > 42180 and lenCalls <= 42240:
        return 704
    elif lenCalls > 42240 and lenCalls <= 42300:
        return 705
    elif lenCalls > 42300 and lenCalls <= 42360:
        return 706
    elif lenCalls > 42360 and lenCalls <= 42420:
        return 707
    elif lenCalls > 42420 and lenCalls <= 42480:
        return 708
    elif lenCalls > 42480 and lenCalls <= 42540:
        return 709
    elif lenCalls > 42540 and lenCalls <= 42600:
        return 710
    elif lenCalls > 42600 and lenCalls <= 42660:
        return 711
    elif lenCalls > 42660 and lenCalls <= 42720:
        return 712
    elif lenCalls > 42720 and lenCalls <= 42780:
        return 713
    elif lenCalls > 42780 and lenCalls <= 42840:
        return 714
    elif lenCalls > 42840 and lenCalls <= 42900:
        return 715
    elif lenCalls > 42900 and lenCalls <= 42960:
        return 716
    elif lenCalls > 42960 and lenCalls <= 43020:
        return 717
    elif lenCalls > 43020 and lenCalls <= 43080:
        return 718
    elif lenCalls > 43080 and lenCalls <= 43140:
        return 719
    elif lenCalls > 43140 and lenCalls <= 43200:
        return 720
    elif lenCalls > 43200 and lenCalls <= 43260:
        return 721
    elif lenCalls > 43260 and lenCalls <= 43320:
        return 722
    elif lenCalls > 43320 and lenCalls <= 43380:
        return 723
    elif lenCalls > 43380 and lenCalls <= 43440:
        return 724
    elif lenCalls > 43440 and lenCalls <= 43500:
        return 725
    elif lenCalls > 43500 and lenCalls <= 43560:
        return 726
    elif lenCalls > 43560 and lenCalls <= 43620:
        return 727
    elif lenCalls > 43620 and lenCalls <= 43680:
        return 728
    elif lenCalls > 43680 and lenCalls <= 43740:
        return 729
    elif lenCalls > 43740 and lenCalls <= 43800:
        return 730
    elif lenCalls > 43800 and lenCalls <= 43860:
        return 731
    elif lenCalls > 43860 and lenCalls <= 43920:
        return 732
    elif lenCalls > 43920 and lenCalls <= 43980:
        return 733
    elif lenCalls > 43980 and lenCalls <= 44040:
        return 734
    elif lenCalls > 44040 and lenCalls <= 44100:
        return 735
    elif lenCalls > 44100 and lenCalls <= 44160:
        return 736
    elif lenCalls > 44160 and lenCalls <= 44220:
        return 737
    elif lenCalls > 44220 and lenCalls <= 44280:
        return 738
    elif lenCalls > 44280 and lenCalls <= 44340:
        return 739
    elif lenCalls > 44340 and lenCalls <= 44400:
        return 740
    elif lenCalls > 44400 and lenCalls <= 44460:
        return 741
    elif lenCalls > 44460 and lenCalls <= 44520:
        return 742
    elif lenCalls > 44520 and lenCalls <= 44580:
        return 743
    elif lenCalls > 44580 and lenCalls <= 44640:
        return 744
    elif lenCalls > 44640 and lenCalls <= 44700:
        return 745
    elif lenCalls > 44700 and lenCalls <= 44760:
        return 746
    elif lenCalls > 44760 and lenCalls <= 44820:
        return 747
    elif lenCalls > 44820 and lenCalls <= 44880:
        return 748
    elif lenCalls > 44880 and lenCalls <= 44940:
        return 749
    elif lenCalls > 44940 and lenCalls <= 45000:
        return 750
    elif lenCalls > 45000 and lenCalls <= 45060:
        return 751
    elif lenCalls > 45060 and lenCalls <= 45120:
        return 752
    elif lenCalls > 45120 and lenCalls <= 45180:
        return 753
    elif lenCalls > 45180 and lenCalls <= 45240:
        return 754
    elif lenCalls > 45240 and lenCalls <= 45300:
        return 755
    elif lenCalls > 45300 and lenCalls <= 45360:
        return 756
    elif lenCalls > 45360 and lenCalls <= 45420:
        return 757
    elif lenCalls > 45420 and lenCalls <= 45480:
        return 758
    elif lenCalls > 45480 and lenCalls <= 45540:
        return 759
    elif lenCalls > 45540 and lenCalls <= 45600:
        return 760
    elif lenCalls > 45600 and lenCalls <= 45660:
        return 761
    elif lenCalls > 45660 and lenCalls <= 45720:
        return 762
    elif lenCalls > 45720 and lenCalls <= 45780:
        return 763
    elif lenCalls > 45780 and lenCalls <= 45840:
        return 764
    elif lenCalls > 45840 and lenCalls <= 45900:
        return 765
    elif lenCalls > 45900 and lenCalls <= 45960:
        return 766
    elif lenCalls > 45960 and lenCalls <= 46020:
        return 767
    elif lenCalls > 46020 and lenCalls <= 46080:
        return 768
    elif lenCalls > 46080 and lenCalls <= 46140:
        return 769
    elif lenCalls > 46140 and lenCalls <= 46200:
        return 770
    elif lenCalls > 46200 and lenCalls <= 46260:
        return 771
    elif lenCalls > 46260 and lenCalls <= 46320:
        return 772
    elif lenCalls > 46320 and lenCalls <= 46380:
        return 773
    elif lenCalls > 46380 and lenCalls <= 46440:
        return 774
    elif lenCalls > 46440 and lenCalls <= 46500:
        return 775
    elif lenCalls > 46500 and lenCalls <= 46560:
        return 776
    elif lenCalls > 46560 and lenCalls <= 46620:
        return 777
    elif lenCalls > 46620 and lenCalls <= 46680:
        return 778
    elif lenCalls > 46680 and lenCalls <= 46740:
        return 779
    elif lenCalls > 46740 and lenCalls <= 46800:
        return 780
    elif lenCalls > 46800 and lenCalls <= 46860:
        return 781
    elif lenCalls > 46860 and lenCalls <= 46920:
        return 782
    elif lenCalls > 46920 and lenCalls <= 46980:
        return 783
    elif lenCalls > 46980 and lenCalls <= 47040:
        return 784
    elif lenCalls > 47040 and lenCalls <= 47100:
        return 785
    elif lenCalls > 47100 and lenCalls <= 47160:
        return 786
    elif lenCalls > 47160 and lenCalls <= 47220:
        return 787
    elif lenCalls > 47220 and lenCalls <= 47280:
        return 788
    elif lenCalls > 47280 and lenCalls <= 47340:
        return 789
    elif lenCalls > 47340 and lenCalls <= 47400:
        return 790
    elif lenCalls > 47400 and lenCalls <= 47460:
        return 791
    elif lenCalls > 47460 and lenCalls <= 47520:
        return 792
    elif lenCalls > 47520 and lenCalls <= 47580:
        return 793
    elif lenCalls > 47580 and lenCalls <= 47640:
        return 794
    elif lenCalls > 47640 and lenCalls <= 47700:
        return 795
    elif lenCalls > 47700 and lenCalls <= 47760:
        return 796
    elif lenCalls > 47760 and lenCalls <= 47820:
        return 797
    elif lenCalls > 47820 and lenCalls <= 47880:
        return 798
    elif lenCalls > 47880 and lenCalls <= 47940:
        return 799
    elif lenCalls > 47940 and lenCalls <= 48000:
        return 800
    elif lenCalls > 48000 and lenCalls <= 48060:
        return 801
    elif lenCalls > 48060 and lenCalls <= 48120:
        return 802
    elif lenCalls > 48120 and lenCalls <= 48180:
        return 803
    elif lenCalls > 48180 and lenCalls <= 48240:
        return 804
    elif lenCalls > 48240 and lenCalls <= 48300:
        return 805
    elif lenCalls > 48300 and lenCalls <= 48360:
        return 806
    elif lenCalls > 48360 and lenCalls <= 48420:
        return 807
    elif lenCalls > 48420 and lenCalls <= 48480:
        return 808
    elif lenCalls > 48480 and lenCalls <= 48540:
        return 809
    elif lenCalls > 48540 and lenCalls <= 48600:
        return 810
    elif lenCalls > 48600 and lenCalls <= 48660:
        return 811
    elif lenCalls > 48660 and lenCalls <= 48720:
        return 812
    elif lenCalls > 48720 and lenCalls <= 48780:
        return 813
    elif lenCalls > 48780 and lenCalls <= 48840:
        return 814
    elif lenCalls > 48840 and lenCalls <= 48900:
        return 815
    elif lenCalls > 48900 and lenCalls <= 48960:
        return 816
    elif lenCalls > 48960 and lenCalls <= 49020:
        return 817
    elif lenCalls > 49020 and lenCalls <= 49080:
        return 818
    elif lenCalls > 49080 and lenCalls <= 49140:
        return 819
    elif lenCalls > 49140 and lenCalls <= 49200:
        return 820
    elif lenCalls > 49200 and lenCalls <= 49260:
        return 821
    elif lenCalls > 49260 and lenCalls <= 49320:
        return 822
    elif lenCalls > 49320 and lenCalls <= 49380:
        return 823
    elif lenCalls > 49380 and lenCalls <= 49440:
        return 824
    elif lenCalls > 49440 and lenCalls <= 49500:
        return 825
    elif lenCalls > 49500 and lenCalls <= 49560:
        return 826
    elif lenCalls > 49560 and lenCalls <= 49620:
        return 827
    elif lenCalls > 49620 and lenCalls <= 49680:
        return 828
    elif lenCalls > 49680 and lenCalls <= 49740:
        return 829
    elif lenCalls > 49740 and lenCalls <= 49800:
        return 830
    elif lenCalls > 49800 and lenCalls <= 49860:
        return 831
    elif lenCalls > 49860 and lenCalls <= 49920:
        return 832
    elif lenCalls > 49920 and lenCalls <= 49980:
        return 833
    elif lenCalls > 49980 and lenCalls <= 50040:
        return 834
    elif lenCalls > 50040 and lenCalls <= 50100:
        return 835
    elif lenCalls > 50100 and lenCalls <= 50160:
        return 836
    elif lenCalls > 50160 and lenCalls <= 50220:
        return 837
    elif lenCalls > 50220 and lenCalls <= 50280:
        return 838
    elif lenCalls > 50280 and lenCalls <= 50340:
        return 839
    elif lenCalls > 50340 and lenCalls <= 50400:
        return 840
    elif lenCalls > 50400 and lenCalls <= 50460:
        return 841
    elif lenCalls > 50460 and lenCalls <= 50520:
        return 842
    elif lenCalls > 50520 and lenCalls <= 50580:
        return 843
    elif lenCalls > 50580 and lenCalls <= 50640:
        return 844
    elif lenCalls > 50640 and lenCalls <= 50700:
        return 845
    elif lenCalls > 50700 and lenCalls <= 50760:
        return 846
    elif lenCalls > 50760 and lenCalls <= 50820:
        return 847
    elif lenCalls > 50820 and lenCalls <= 50880:
        return 848
    elif lenCalls > 50880 and lenCalls <= 50940:
        return 849
    elif lenCalls > 50940 and lenCalls <= 51000:
        return 850
    elif lenCalls > 51000 and lenCalls <= 51060:
        return 851
    elif lenCalls > 51060 and lenCalls <= 51120:
        return 852
    elif lenCalls > 51120 and lenCalls <= 51180:
        return 853
    elif lenCalls > 51180 and lenCalls <= 51240:
        return 854
    elif lenCalls > 51240 and lenCalls <= 51300:
        return 855
    elif lenCalls > 51300 and lenCalls <= 51360:
        return 856
    elif lenCalls > 51360 and lenCalls <= 51420:
        return 857
    elif lenCalls > 51420 and lenCalls <= 51480:
        return 858
    elif lenCalls > 51480 and lenCalls <= 51540:
        return 859
    elif lenCalls > 51540 and lenCalls <= 51600:
        return 860
    elif lenCalls > 51600 and lenCalls <= 51660:
        return 861
    elif lenCalls > 51660 and lenCalls <= 51720:
        return 862
    elif lenCalls > 51720 and lenCalls <= 51780:
        return 863
    elif lenCalls > 51780 and lenCalls <= 51840:
        return 864
    elif lenCalls > 51840 and lenCalls <= 51900:
        return 865
    elif lenCalls > 51900 and lenCalls <= 51960:
        return 866
    elif lenCalls > 51960 and lenCalls <= 52020:
        return 867
    elif lenCalls > 52020 and lenCalls <= 52080:
        return 868
    elif lenCalls > 52080 and lenCalls <= 52140:
        return 869
    elif lenCalls > 52140 and lenCalls <= 52200:
        return 870
    elif lenCalls > 52200 and lenCalls <= 52260:
        return 871
    elif lenCalls > 52260 and lenCalls <= 52320:
        return 872
    elif lenCalls > 52320 and lenCalls <= 52380:
        return 873
    elif lenCalls > 52380 and lenCalls <= 52440:
        return 874
    elif lenCalls > 52440 and lenCalls <= 52500:
        return 875
    elif lenCalls > 52500 and lenCalls <= 52560:
        return 876
    elif lenCalls > 52560 and lenCalls <= 52620:
        return 877
    elif lenCalls > 52620 and lenCalls <= 52680:
        return 878
    elif lenCalls > 52680 and lenCalls <= 52740:
        return 879
    elif lenCalls > 52740 and lenCalls <= 52800:
        return 880
    elif lenCalls > 52800 and lenCalls <= 52860:
        return 881
    elif lenCalls > 52860 and lenCalls <= 52920:
        return 882
    elif lenCalls > 52920 and lenCalls <= 52980:
        return 883
    elif lenCalls > 52980 and lenCalls <= 53040:
        return 884
    elif lenCalls > 53040 and lenCalls <= 53100:
        return 885
    elif lenCalls > 53100 and lenCalls <= 53160:
        return 886
    elif lenCalls > 53160 and lenCalls <= 53220:
        return 887
    elif lenCalls > 53220 and lenCalls <= 53280:
        return 888
    elif lenCalls > 53280 and lenCalls <= 53340:
        return 889
    elif lenCalls > 53340 and lenCalls <= 53400:
        return 890
    elif lenCalls > 53400 and lenCalls <= 53460:
        return 891
    elif lenCalls > 53460 and lenCalls <= 53520:
        return 892
    elif lenCalls > 53520 and lenCalls <= 53580:
        return 893
    elif lenCalls > 53580 and lenCalls <= 53640:
        return 894
    elif lenCalls > 53640 and lenCalls <= 53700:
        return 895
    elif lenCalls > 53700 and lenCalls <= 53760:
        return 896
    elif lenCalls > 53760 and lenCalls <= 53820:
        return 897
    elif lenCalls > 53820 and lenCalls <= 53880:
        return 898
    elif lenCalls > 53880 and lenCalls <= 53940:
        return 899
    elif lenCalls > 53940 and lenCalls <= 54000:
        return 900
    elif lenCalls > 54000 and lenCalls <= 54060:
        return 901
    elif lenCalls > 54060 and lenCalls <= 54120:
        return 902
    elif lenCalls > 54120 and lenCalls <= 54180:
        return 903
    elif lenCalls > 54180 and lenCalls <= 54240:
        return 904
    elif lenCalls > 54240 and lenCalls <= 54300:
        return 905
    elif lenCalls > 54300 and lenCalls <= 54360:
        return 906
    elif lenCalls > 54360 and lenCalls <= 54420:
        return 907
    elif lenCalls > 54420 and lenCalls <= 54480:
        return 908
    elif lenCalls > 54480 and lenCalls <= 54540:
        return 909
    elif lenCalls > 54540 and lenCalls <= 54600:
        return 910
    elif lenCalls > 54600 and lenCalls <= 54660:
        return 911
    elif lenCalls > 54660 and lenCalls <= 54720:
        return 912
    elif lenCalls > 54720 and lenCalls <= 54780:
        return 913
    elif lenCalls > 54780 and lenCalls <= 54840:
        return 914
    elif lenCalls > 54840 and lenCalls <= 54900:
        return 915
    elif lenCalls > 54900 and lenCalls <= 54960:
        return 916
    elif lenCalls > 54960 and lenCalls <= 55020:
        return 917
    elif lenCalls > 55020 and lenCalls <= 55080:
        return 918
    elif lenCalls > 55080 and lenCalls <= 55140:
        return 919
    elif lenCalls > 55140 and lenCalls <= 55200:
        return 920
    elif lenCalls > 55200 and lenCalls <= 55260:
        return 921
    elif lenCalls > 55260 and lenCalls <= 55320:
        return 922
    elif lenCalls > 55320 and lenCalls <= 55380:
        return 923
    elif lenCalls > 55380 and lenCalls <= 55440:
        return 924
    elif lenCalls > 55440 and lenCalls <= 55500:
        return 925
    elif lenCalls > 55500 and lenCalls <= 55560:
        return 926
    elif lenCalls > 55560 and lenCalls <= 55620:
        return 927
    elif lenCalls > 55620 and lenCalls <= 55680:
        return 928
    elif lenCalls > 55680 and lenCalls <= 55740:
        return 929
    elif lenCalls > 55740 and lenCalls <= 55800:
        return 930
    elif lenCalls > 55800 and lenCalls <= 55860:
        return 931
    elif lenCalls > 55860 and lenCalls <= 55920:
        return 932
    elif lenCalls > 55920 and lenCalls <= 55980:
        return 933
    elif lenCalls > 55980 and lenCalls <= 56040:
        return 934
    elif lenCalls > 56040 and lenCalls <= 56100:
        return 935
    elif lenCalls > 56100 and lenCalls <= 56160:
        return 936
    elif lenCalls > 56160 and lenCalls <= 56220:
        return 937
    elif lenCalls > 56220 and lenCalls <= 56280:
        return 938
    elif lenCalls > 56280 and lenCalls <= 56340:
        return 939
    elif lenCalls > 56340 and lenCalls <= 56400:
        return 940
    elif lenCalls > 56400 and lenCalls <= 56460:
        return 941
    elif lenCalls > 56460 and lenCalls <= 56520:
        return 942
    elif lenCalls > 56520 and lenCalls <= 56580:
        return 943
    elif lenCalls > 56580 and lenCalls <= 56640:
        return 944
    elif lenCalls > 56640 and lenCalls <= 56700:
        return 945
    elif lenCalls > 56700 and lenCalls <= 56760:
        return 946
    elif lenCalls > 56760 and lenCalls <= 56820:
        return 947
    elif lenCalls > 56820 and lenCalls <= 56880:
        return 948
    elif lenCalls > 56880 and lenCalls <= 56940:
        return 949
    elif lenCalls > 56940 and lenCalls <= 57000:
        return 950
    elif lenCalls > 57000 and lenCalls <= 57060:
        return 951
    elif lenCalls > 57060 and lenCalls <= 57120:
        return 952
    elif lenCalls > 57120 and lenCalls <= 57180:
        return 953
    elif lenCalls > 57180 and lenCalls <= 57240:
        return 954
    elif lenCalls > 57240 and lenCalls <= 57300:
        return 955
    elif lenCalls > 57300 and lenCalls <= 57360:
        return 956
    elif lenCalls > 57360 and lenCalls <= 57420:
        return 957
    elif lenCalls > 57420 and lenCalls <= 57480:
        return 958
    elif lenCalls > 57480 and lenCalls <= 57540:
        return 959
    elif lenCalls > 57540 and lenCalls <= 57600:
        return 960
    elif lenCalls > 57600 and lenCalls <= 57660:
        return 961
    elif lenCalls > 57660 and lenCalls <= 57720:
        return 962
    elif lenCalls > 57720 and lenCalls <= 57780:
        return 963
    elif lenCalls > 57780 and lenCalls <= 57840:
        return 964
    elif lenCalls > 57840 and lenCalls <= 57900:
        return 965
    elif lenCalls > 57900 and lenCalls <= 57960:
        return 966
    elif lenCalls > 57960 and lenCalls <= 58020:
        return 967
    elif lenCalls > 58020 and lenCalls <= 58080:
        return 968
    elif lenCalls > 58080 and lenCalls <= 58140:
        return 969
    elif lenCalls > 58140 and lenCalls <= 58200:
        return 970
    elif lenCalls > 58200 and lenCalls <= 58260:
        return 971
    elif lenCalls > 58260 and lenCalls <= 58320:
        return 972
    elif lenCalls > 58320 and lenCalls <= 58380:
        return 973
    elif lenCalls > 58380 and lenCalls <= 58440:
        return 974
    elif lenCalls > 58440 and lenCalls <= 58500:
        return 975
    elif lenCalls > 58500 and lenCalls <= 58560:
        return 976
    elif lenCalls > 58560 and lenCalls <= 58620:
        return 977
    elif lenCalls > 58620 and lenCalls <= 58680:
        return 978
    elif lenCalls > 58680 and lenCalls <= 58740:
        return 979
    elif lenCalls > 58740 and lenCalls <= 58800:
        return 980
    elif lenCalls > 58800 and lenCalls <= 58860:
        return 981
    elif lenCalls > 58860 and lenCalls <= 58920:
        return 982
    elif lenCalls > 58920 and lenCalls <= 58980:
        return 983
    elif lenCalls > 58980 and lenCalls <= 59040:
        return 984
    elif lenCalls > 59040 and lenCalls <= 59100:
        return 985
    elif lenCalls > 59100 and lenCalls <= 59160:
        return 986
    elif lenCalls > 59160 and lenCalls <= 59220:
        return 987
    elif lenCalls > 59220 and lenCalls <= 59280:
        return 988
    elif lenCalls > 59280 and lenCalls <= 59340:
        return 989
    elif lenCalls > 59340 and lenCalls <= 59400:
        return 990
    elif lenCalls > 59400 and lenCalls <= 59460:
        return 991
    elif lenCalls > 59460 and lenCalls <= 59520:
        return 992
    elif lenCalls > 59520 and lenCalls <= 59580:
        return 993
    elif lenCalls > 59580 and lenCalls <= 59640:
        return 994
    elif lenCalls > 59640 and lenCalls <= 59700:
        return 995
    elif lenCalls > 59700 and lenCalls <= 59760:
        return 996
    elif lenCalls > 59760 and lenCalls <= 59820:
        return 997
    elif lenCalls > 59820 and lenCalls <= 59880:
        return 998
    elif lenCalls > 59880 and lenCalls <= 59940:
        return 999


    