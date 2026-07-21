# Код с transaction
from django.shortcuts import render
import sqlite3
from dbfread import DBF
import datetime
from datetime import date
import datetime
import math
import time
import os
import sys
from telekom.models import *
from django.contrib import messages
from bulk_update.helper import bulk_update
import re
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
def bell():
    sys.stdout.write('\r\a')
    sys.stdout.flush()


mugut = ['8888888','111','119','01','02','071','05', '03','9938001211','04','003229938001211','0032213000','00322071','383217','993322071','383272','384129',
    '383988','00488803','003229938001211', '112']

etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

turkmenistan = ['Sotowyy',
        'Ashgabat','Ahal Baharly','Ahal Gokdepe','Ahal Kaka','Ahal Seraks','Ahal Tejen','Ahal Babadayhan','Ahal Anew','Ahal Abadan','Ahal Ruhabat','Ahal Ashgabat',
        'Balkan Nebitdag','Balkan Hazar','Balkan Gumdag','Balkan Gyzyl Atr','Balkan Turkmenbashy','Balkan Gumdag','Balkan Esenguly','Balkan Serdar','Balkan Bereket','Balkan Magtymguly',
        'Lebap Turkmenabat','Lebap Magdanly','Lebap Garashsyzlyk','Lebap Gazajak','Lebap Koytendag','Lebap Halach','Lebap Hojambaz','Lebap Garabekewul','Lebap Atamyrat','Lebap Birata',
        'Lebap Galkynysh','Lebap Sayat','Lebap Farap', 'Lebap Sakar','Lebap Seydi','Lebap Turkmenbashy','Lebap Serdarabat','Lebap Serdarabat',
        'Mary','Mary Garagum','Mary Wekilbazar','Mary Oguzhan','Mary Yoleten','Mary Serhetabat','Mary Bayramaly','Mary Murgap','Mary Sakarchage','Mary Tagtabazar','Mary Turkm-gala']

international = ['Moldowa','Fransiya','Germaniya','Gresiya','Wengriya','Italiya','Niderlandy','Norwegiya','Polsha','Rumyniya','Shwesiya','Shweysariya','Welikobritaniya','Ispaniya','Albaniya','Andorra','Bosniya Gersogowina','Bolgariya','Horwatiya','Kipr',
        'Estoniya','Finlyandiya','Gibraltar','Grenlandiya','Islandiya','Latwiya','Lihtenshteyn','Litwa','Luksenburg','Makedoniya','Malta','Portugaliya','Slowakiya','Sloweniya','Yugoslawiya','Cheshskaya Respublika',
        'Kazakstan','Rossiya','Kyrgystan','Tajikistan','Uzbekistan','Belorussiya','Armeniya','Azerbayjan','Gruziya','Ukraina','Afganistan','Turkiya','Iran','Awstriya','Belgiya','Daniya',
        'Awstraliya','Nowaya Zenlandiya','Fidji','Fransuskaya Polineziya','Kiribati','Nowaya Kaledoniya','Norfolkskiye ostrowa','Papua Nowaya Gwineya','Tonga','Wanuatu','Hytay','Kuba','Indiya','Indoneziya','Yaponiya','Malaziya','Meksika','Myanma',
        'Pakistan','Filipiny','Singapur','Yujnaya Koreya','Tailand','Wyetnam','Bahreyn','Bangladesh','Bruney Daruesaalam','Kombodja','Kosta-Rika','Wostochnyy Timor','Gwatelama','Gaiti','Gonduras','Gonk-Kong','Irak','Izrail','Iordaniya','Kuweit','Laos','Liwan',
        'Makao (Aomyn)','Mongoliya','Nepal','Niderlandskie Antilly','Nikaragua','Sewernaya Koreya','Sewernyy Yemen','Oman','Panama' 'Katar','Saudowskaya Arawiya','Yujnyy Yemen','Siriya','Taiwan','O.A.E','USA/CANADA','Argentina','Braziliya','Chili',
        'Kolumbiya','Peru','Wenesuella','Boliwiya','Ekwador','Farerskie Ostrowa','Fransuskatya Gwiana','Gayana','Martitnka','Surinam','Urugway','Egipet','UAR','Aljir','Angola','Benin','Botswana','Burkina Faso','Burundi','Kamerun',
        'Kape Werde','SAR','Chad','Kongo','Jibuti','Ekwatorialnaya gwineya','Efiopiya','Gabon','Gambiya','Gana','Gwineya','Gwineya Bissau','Keniya','Liberiya','Liviya','Madagaskar','Malawi','Mali','Mawritaniya','Mawrikiy',
        'Moroko','Mozambik','Namibiya','Niger','Nigeriya','Reonyon','Respublika Ruanda','Senegal','Seyshelskie ostrowa','Syerra Leonne','Somali','Sudan','Tanzaniya','Respublika Togoleze','Tunis','Uganda','Zair','Zambiya','Zimbabwe']



# Функция для прибавления секунд в время (Чтобы узнать END Разговора)
def add_secs_to_time(timeval, secs_to_add):
    secs = timeval.hour * 3600 + timeval.minute * 60 + timeval.second
    secs += secs_to_add
    if secs // 3600 > 23:
        return datetime.time(00, (secs % 3600) // 60, secs % 60)
    else:
        return datetime.time(secs // 3600, (secs % 3600) // 60, secs % 60)


# достаем локацию номера в виде списка:
def getNumberLocations(number):
    # Etraps
    # Dashoguz
    if number[0:8] == '00800322' and len(number) == 13:
        return [number[8:], 'Dashoguz']
    if (number[0:6] == '800322' or number[0:6] == '993322') and len(number) == 11:
        return [number[6:], 'Dashoguz']
    if (number[0:5] == '00322' and len(number) == 10) and number != '0032213000':
        return [number[5:], 'Dashoguz']
    if number[0:3] == '322' and len(number) == 8:
        return [number[3:], 'Dashoguz']
    
    # local
    if (len(number) == 5) and number != '13000':
        return [number, 'five']

    # Akdepe
    if (number[0:8] == '00800344' or number[0:8] == '00800343') and len(number) == 13:
        return [number[8:], 'Akdepe']
    if (number[0:6] == '800344' or number[0:6] == '800343' or number[0:6] == '993344' or number[0:6] == '993343') and len(number) == 11:
        return [number[6:], 'Akdepe']
    if (number[0:5] == '00344' or number[0:5] == '00343') and len(number) == 10:
        return [number[5:], 'Akdepe']
    if (number[0:3] == '344' and len(number) == 8) or (number[0:3] == '343' and len(number) == 8):
        return [number[3:], 'Akdepe']

    # Boldumsaz
    if (number[0:8] == '00800346' or number[0:8] == '00800345') and len(number) == 13:
        return [number[8:], 'Boldumsaz']
    if (number[0:6] == '800346' or number[0:6] == '800345' or number[0:6] == '993346' or number[0:6] == '993345') and len(number) == 11:
        return [number[6:], 'Boldumsaz']
    if (number[0:5] == '00346' or number[0:5] == '00345') and len(number) == 10:
        return [number[5:], 'Boldumsaz']
    if (number[0:3] == '346' and len(number) == 8) or (number[0:3] == '345' and len(number) == 8):
        return [number[3:], 'Boldumsaz']

    # Gorogly
    if number[0:8] == '00800340' and len(number) == 13:
        return [number[8:], 'Gorogly']
    if (number[0:6] == '800340' or number[0:6] == '993340') and len(number) == 11:
        return [number[6:], 'Gorogly']
    if  number[0:5] == '00340' and len(number) == 10:
        return [number[5:], 'Gorogly']
    if number[0:3] == '340' and len(number) == 8:
        return [number[3:], 'Gorogly']

    # Koneurgench
    if number[0:8] == '00800347' and len(number) == 13:
        return [number[8:], 'Koneurgench']
    if (number[0:6] == '800347' or number[0:6] == '993347') and len(number) == 11:
        return [number[6:], 'Koneurgench']
    if number[0:5] == '00347' and len(number) == 10:
        return [number[5:], 'Koneurgench']
    if number[0:3] == '347' and len(number) == 8:
        return [number[3:], 'Koneurgench']


    # Turkmenbashy
    if number[0:8] == '00800349' and len(number) == 13:
        return [number[8:], 'Turkmenbashy']
    if (number[0:6] == '800349' or number[0:6] == '993349') and len(number) == 11:
        return [number[6:], 'Turkmenbashy']
    if number[0:5] == '00349' and len(number) == 10:
        return [number[5:], 'Turkmenbashy']
    if number[0:3] == '349' and len(number) == 8:
        return [number[3:], 'Turkmenbashy']

    # S.A.Nyyazow
    if number[0:8] == '00800348' and len(number) == 13:
        return [number[8:], 'S.A.Nyyazow']
    if (number[0:6] == '800348' or number[0:6] == '993348') and len(number) == 11:
        return [number[6:], 'S.A.Nyyazow']
    if number[0:5] == '00348' and len(number) == 10:
        return [number[5:], 'S.A.Nyyazow']
    if number[0:3] == '348' and len(number) == 8:
        return [number[3:], 'S.A.Nyyazow']

    # Ruhubelent
    if number[0:8] == '00800342' and len(number) == 13:
        return [number[8:], 'Ruhubelent']
    if (number[0:6] == '800342' or number[0:6] == '993342') and len(number) == 11:
        return [number[6:], 'Ruhubelent']
    if number[0:5] == '00342' and len(number) == 10:
        return [number[5:], 'Ruhubelent']
    if number[0:3] == '342' and len(number) == 8:
        return [number[3:], 'Ruhubelent']

    # Altyn Asyr
    if (number[0:5] == '99360' or number[0:5] == '99361' or number[0:5] == '99362' or number[0:5] == '99363' or number[0:5] == '99364' or number[0:5] == '99365' or number[0:5] == '99371' or 
        number[0:5] == '80060' or number[0:5] == '80061' or number[0:5] == '80062' or number[0:5] == '80063' or number[0:5] == '80064' or number[0:5] == '80065' or number[0:5] == '80071' or
        number[0:4] == '0060' or number[0:4] == '0061' or number[0:4] == '0062' or number[0:4] == '0063' or number[0:4] == '0064' or number[0:4] == '0065' or number[0:4] == '0071' or
        (len(number) == 8 and number[0:2] == '60') or 
        (len(number) == 8 and number[0:2] == '61') or 
        (len(number) == 8 and number[0:2] == '62') or 
        (len(number) == 8 and number[0:2] == '63') or 
        (len(number) == 8 and number[0:2] == '64') or 
        (len(number) == 8 and number[0:2] == '65') or
        (len(number) == 8 and number[0:2] == '71') or
        (len(number) == 10 and number[:3] == '936') or
        (len(number) == 10 and number[:3] == '937')
        ):
        return [0.08, 'Sotowyy']

    # Ashgabat wel.
    if number[:5] == '80012' or number[:4] == '0012' or (len(number) == 8 and number[:2] == '12'):
        return [0.08, 'Ashgabat']
    if number[:6] == '800131' or number[:5] == '00131' or (len(number) == 8 and number[:3] == '131'):
        return [0.08, 'Ahal Baharly']
    if number[:6] == '800132' or number[:5] == '00132' or (len(number) == 8 and number[:3] == '132'):
        return [0.08, 'Ahal Gokdepe']
    if number[:6] == '800133' or number[:5] == '00133' or (len(number) == 8 and number[:3] == '133'):
        return [0.08, 'Ahal Kaka']
    if number[:6] == '800134' or number[:5] == '00134' or (len(number) == 8 and number[:3] == '134'):
        return [0.08, 'Ahal Seraks']
    if number[:6] == '800135' or number[:5] == '00135' or (len(number) == 8 and number[:3] == '135'):
        return [0.08, 'Ahal Tejen']
    if number[:6] == '800136' or number[:5] == '00136' or (len(number) == 8 and number[:3] == '136'):
        return [0.08, 'Ahal Babadayhan']
    if number[:6] == '800137' or number[:5] == '00137' or (len(number) == 8 and number[:3] == '137'):
        return [0.08, 'Ahal Anew']
    if number[:6] == '800138' or number[:5] == '00138' or (len(number) == 8 and number[:3] == '138'):
        return [0.08, 'Ahal Abadan']
    if number[:6] == '800139' or number[:5] == '00139' or (len(number) == 8 and number[:3] == '139'):
        return [0.08, 'Ahal Ruhabat']
    if number[:6] == '800181' or number[:5] == '00181' or (len(number) == 8 and number[:3] == '181'):
        return [0.08, 'Ahal Ashgabat']

    # Balkan wel.
    if number[:6] == '800222' or number[:5] == '00222' or (len(number) == 8 and number[:3] == '222'):
        return [0.08, 'Balkan Nebitdag']
    if number[:6] == '800240' or number[:5] == '00240' or (len(number) == 8 and number[:3] == '240'):
        return [0.08, 'Balkan Hazar']
    if number[:6] == '800241' or number[:5] == '00241' or (len(number) == 8 and number[:3] == '241'):
        return [0.08, 'Balkan Gumdag']
    if number[:6] == '800242' or number[:5] == '00242' or (len(number) == 8 and number[:3] == '242'):
        return [0.08, 'Balkan Gyzyl Atr']
    if number[:6] == '800243' or number[:5] == '00243' or (len(number) == 8 and number[:3] == '243'):
        return [0.08, 'Balkan Turkmenbashy']
    if number[:6] == '800244' or number[:5] == '00244' or (len(number) == 8 and number[:3] == '244'):
        return [0.08, 'Balkan Gumdag']
    if number[:6] == '800245' or number[:5] == '00245' or (len(number) == 8 and number[:3] == '245'):
        return [0.08, 'Balkan Esenguly']
    if number[:6] == '800246' or number[:5] == '00246' or (len(number) == 8 and number[:3] == '246'):
        return [0.08, 'Balkan Serdar']
    if number[:6] == '800247' or number[:5] == '00247' or (len(number) == 8 and number[:3] == '247'):
        return [0.08, 'Balkan Bereket']
    if number[:6] == '800248' or number[:5] == '00248' or (len(number) == 8 and number[:3] == '248'):
        return [0.08, 'Balkan Magtymguly']

    # Lebap wel.
    if number[:6] == '800422' or number[:5] == '00422' or (len(number) == 8 and number[:3] == '422'):
        return [0.08, 'Lebap Turkmenabat']
    if number[:6] == '800431' or number[:5] == '00431' or (len(number) == 8 and number[:3] == '431'):
        return [0.08, 'Lebap Magdanly']
    if number[:6] == '800432' or number[:5] == '00432' or (len(number) == 8 and number[:3] == '432'):
        return [0.08, 'Lebap Garashsyzlyk']
    if number[:6] == '800438' or number[:5] == '00438' or (len(number) == 8 and number[:3] == '438'):
        return [0.08, 'Lebap Gazajak']
    if number[:6] == '800440' or number[:5] == '00440' or (len(number) == 8 and number[:3] == '440'):
        return [0.08, 'Lebap Koytendag']
    if number[:6] == '800441' or number[:5] == '00441' or (len(number) == 8 and number[:3] == '441'):
        return [0.08, 'Lebap Halach']
    if number[:6] == '800442' or number[:5] == '00442' or (len(number) == 8 and number[:3] == '442'):
        return [0.08, 'Lebap Hojambaz']
    if number[:6] == '800443' or number[:5] == '00443' or (len(number) == 8 and number[:3] == '443'):
        return [0.08, 'Lebap Garabekewul']
    if number[:6] == '800444' or number[:5] == '00444' or (len(number) == 8 and number[:3] == '444'):
        return [0.08, 'Lebap Atamyrat']
    if number[:6] == '800445' or number[:5] == '00445' or (len(number) == 8 and number[:3] == '445'):
        return [0.08, 'Lebap Birata']
    if number[:6] == '800446' or number[:5] == '00446' or (len(number) == 8 and number[:3] == '446'):
        return [0.08, 'Lebap Galkynysh']
    if number[:6] == '800447' or number[:5] == '00447' or (len(number) == 8 and number[:3] == '447'):
        return [0.08, 'Lebap Sayat']
    if number[:6] == '800448' or number[:5] == '00448' or (len(number) == 8 and number[:3] == '448'):
        return [0.08, 'Lebap Farap']
    if number[:6] == '800449' or number[:5] == '00449' or (len(number) == 8 and number[:3] == '449'):
        return [0.08, 'Lebap Sakar']
    if number[:6] == '800461' or number[:5] == '00461' or (len(number) == 8 and number[:3] == '461'):
        return [0.08, 'Lebap Seydi']
    if number[:6] == '800465' or number[:5] == '00465' or (len(number) == 8 and number[:3] == '465'):
        return [0.08, 'Lebap Turkmenbashy']
    if number[:6] == '800433' or number[:5] == '00433' or (len(number) == 8 and number[:3] == '433'):
        return [0.08, 'Lebap Serdarabat']
    if number[:6] == '800434' or number[:5] == '00434' or (len(number) == 8 and number[:3] == '434'):
        return [0.08, 'Lebap Serdarabat']

    # Mary wel.
    if number[:6] == '800522' or number[:5] == '00522' or (len(number) == 8 and number[:3] == '552'):
        return [0.08, 'Mary']
    if number[:6] == '800557' or number[:5] == '00557' or (len(number) == 8 and number[:3] == '557'):
        return [0.08, 'Mary Garagum']
    if number[:6] == '800558' or number[:5] == '00558' or (len(number) == 8 and number[:3] == '558'):
        return [0.08, 'Mary Wekilbazar']
    if number[:6] == '800559' or number[:5] == '00559' or (len(number) == 8 and number[:3] == '559'):
        return [0.08, 'Mary Oguzhan']
    if number[:6] == '800560' or number[:5] == '00560' or (len(number) == 8 and number[:3] == '560'):
        return [0.08, 'Mary Yoleten']
    if number[:6] == '800561' or number[:5] == '00561' or (len(number) == 8 and number[:3] == '561'):
        return [0.08, 'Mary Serhetabat']
    if number[:6] == '800564' or number[:5] == '00564' or (len(number) == 8 and number[:3] == '564'):
        return [0.08, 'Mary Bayramaly']
    if number[:6] == '800565' or number[:5] == '00565' or (len(number) == 8 and number[:3] == '565'):
        return [0.08, 'Mary Murgap']
    if number[:6] == '800566' or number[:5] == '00566' or (len(number) == 8 and number[:3] == '566'):
        return [0.08, 'Mary Sakarchage']
    if number[:6] == '800568' or number[:5] == '00568' or (len(number) == 8 and number[:3] == '568'):
        return [0.08, 'Mary Tagtabazar']
    if number[:6] == '800569' or number[:5] == '00569' or (len(number) == 8 and number[:3] == '569'):
        return [0.08, 'Mary Turkm-gala']

    # Другие страны
    if number[:5] == '81077' or number[:5] == '81076' or number[:4] == '1076' or number[:4] == '1077' or number[:2] == '77' or number[:2] == '76':
        return [1.44, 'Kazakstan']
    if (number[:4] == '8107' and number[:5] != '81077' and number[:5] != '81076') or (number[:1] == '7' and number[:2] != '76' and number[:2] != '77'):
        return [1.94, 'Rossiya']
    if number[:3] == '107' and number[:4] != '1077' and number[:4] != '1076':
        return [1.94, 'Rossiya']
    if number[:6] == '810996' or number[:5] == '10996' or number[:3] == '996':
        return [1.44, 'Kyrgystan']
    if number[:6] == '810373' or number[:5] == '10373' or number[:3] == '373':
        return [1.8, 'Moldowa']
    if number[:6] == '810992' or number[:5] == '10992' or number[:3] == '992':
        return [1.44, 'Tajikistan']
    if number[:6] == '810998' or number[:5] == '10998' or number[:3] == '998':
        return [1.44, 'Uzbekistan']
    if number[:6] == '810375' or number[:5] == '10375' or number[:3] == '375':
        return [1.8, 'Belorussiya']
    if number[:6] == '810374' or number[:5] == '10374' or number[:3] == '374':
        return [2.16, 'Armeniya']
    if number[:6] == '810994' or number[:5] == '10994' or number[:3] == '994':
        return [2.16, 'Azerbayjan']
    if number[:6] == '810995' or number[:5] == '10995' or number[:3] == '995':
        return [2.16, 'Gruziya']
    if number[:6] == '810380' or number[:5] == '10380' or number[:3] == '380':
        return [2.16, 'Ukraina']
    if number[:5] == '81093' or number[:4] == '1093' or number[:2] == '93':
        return [2.31, 'Afganistan']
    if number[:5] == '81090' or number[:4] == '1090' or number[:2] == '90':
        return [3.06, 'Turkiya']
    if number[:5] == '81098' or number[:4] == '1098' or number[:2] == '98':
        return [3.3, 'Iran']
    if number[:5] == '81043' or number[:4] == '1043' or number[:2] == '43':
        return [3.96, 'Awstriya']
    if number[:5] == '81032' or number[:4] == '1032' or (number[:2] == '32' and len(number) > 8):
        return [3.96, 'Belgiya']
    if number[:5] == '81045' or number[:4] == '1045' or number[:2] == '45':
        return [3.96, 'Daniya']


    # 3.96 manat
    if number[:5] == '81033' or number[:4] == '1033' or number[:2] == '33':
        return [3.96, 'Fransiya']
    if number[:5] == '81049' or number[:4] == '1049' or number[:2] == '49' and len(number) > 8:
        return [3.96, 'Germaniya']
    if number[:5] == '81030' or number[:4] == '1030' or number[:2] == '30':
        return [3.96, 'Gresiya']
    if number[:5] == '81036' or number[:4] == '1036' or number[:2] == '36':
        return [3.96, 'Wengriya']
    if number[:5] == '81039' or number[:4] == '1039' or number[:2] == '39':
        return [3.96, 'Italiya']
    if number[:5] == '81031' or number[:4] == '1031' or number[:2] == '31':
        return [3.96, 'Niderlandy']
    if number[:5] == '81047' or number[:4] == '1047' or number[:2] == '47' and len(number) > 8:
        return [3.96, 'Norwegiya']
    if number[:5] == '81048' or number[:4] == '1048' or (len(number) > 8 and number[:2] == '48'):
        return [3.96, 'Polsha']
    if number[:5] == '81040' or number[:4] == '1040' or number[:2] == '40' and len(number) > 8:
        return [3.96, 'Rumyniya']
    if number[:5] == '81046' or number[:4] == '1046' or number[:2] == '46' and len(number) > 8:
        return [3.96, 'Shwesiya']
    if number[:5] == '81041' or number[:4] == '1041' or number[:2] == '41':
        return [3.96, 'Shweysariya']
    if number[:5] == '81044' or number[:4] == '1044' or number[:2] == '44':
        return [3.96, 'Welikobritaniya']
    if number[:5] == '81034' or number[:4] == '1034' or (number[:2] == '34' and len(number) > 8):
        return [3.96, 'Ispaniya']
    if number[:6] == '810355' or number[:5] == '10355' or number[:3] == '355':
        return [3.96, 'Albaniya']
    if number[:6] == '810376' or number[:5] == '10376' or number[:3] == '376':
        return [3.96, 'Andorra']
    if number[:6] == '810387' or number[:5] == '10387' or number[:3] == '387':
        return [3.96, 'Bosniya Gersogowina']
    if number[:6] == '810359' or number[:5] == '10359' or number[:3] == '359':
        return [3.96, 'Bolgariya']
    if number[:6] == '810385' or number[:5] == '10385' or number[:3] == '385':
        return [3.96, 'Horwatiya']
    if number[:6] == '810357' or number[:5] == '10357' or number[:3] == '357':
        return [3.96, 'Kipr']
    if number[:6] == '810372' or number[:5] == '10372' or number[:3] == '372':
        return [3.96, 'Estoniya']
    if number[:6] == '810358' or number[:5] == '10358' or number[:3] == '358':
        return [3.96, 'Finlyandiya']
    if number[:6] == '810350' or number[:5] == '10350' or number[:3] == '350':
        return [3.96, 'Gibraltar']
    if number[:6] == '810299' or number[:5] == '10299' or number[:3] == '299':
        return [3.96, 'Grenlandiya']
    if number[:6] == '810354' or number[:5] == '10354' or number[:3] == '354':
        return [3.96, 'Islandiya']
    if number[:6] == '810371' or number[:5] == '10371' or number[:3] == '371':
        return [3.96, 'Latwiya']
    if number[:6] == '810423' or number[:5] == '10423' or number[:3] == '423':
        return [3.96, 'Lihtenshteyn']
    if number[:6] == '810370' or number[:5] == '10370' or number[:3] == '370':
        return [3.96, 'Litwa']
    if number[:6] == '810352' or number[:5] == '10352' or number[:3] == '352':
        return [3.96, 'Luksenburg']
    if number[:6] == '810389' or number[:5] == '10389' or number[:3] == '389':
        return [3.96, 'Makedoniya']
    if number[:6] == '810356' or number[:5] == '10356' or number[:3] == '356':
        return [3.96, 'Malta']
    if number[:6] == '810351' or number[:5] == '10351' or number[:3] == '351':
        return [3.96, 'Portugaliya']
    if number[:6] == '810421' or number[:5] == '10421' or number[:3] == '421':
        return [3.96, 'Slowakiya']
    if number[:6] == '810386' or number[:5] == '10386' or number[:3] == '386':
        return [3.96, 'Sloweniya']
    if number[:6] == '810381' or number[:5] == '10381' or number[:3] == '381':
        return [3.96, 'Yugoslawiya']
    if number[:6] == '810420' or number[:5] == '10420' or number[:3] == '420':
        return [3.96, 'Cheshskaya Respublika']
    

    # 6.07 manat
    if number[:5] == '81061' or number[:4] == '1061' or number[:2] == '61':
        return [6.07, 'Awstraliya']
    if number[:5] == '81064' or number[:4] == '1064' or number[:2] == '64':
            return [6.07, 'Nowaya Zenlandiya']
    if number[:6] == '810679' or number[:5] == '10679' or number[:3] == '679':
        return [6.07, 'Fidji']
    if number[:6] == '810689' or number[:5] == '10689' or number[:3] == '689':
            return [6.07, 'Fransuskaya Polineziya']
    if number[:6] == '810686' or number[:5] == '10686' or number[:3] == '686':
        return [6.07, 'Kiribati']
    if number[:6] == '810687' or number[:5] == '10687' or number[:3] == '687':
            return [6.07, 'Nowaya Kaledoniya']
    if number[:6] == '810672' or number[:5] == '10672' or number[:3] == '672':
            return [6.07, 'Norfolkskiye ostrowa']
    if number[:6] == '810675' or number[:5] == '10675' or number[:3] == '675':
            return [6.07, 'Papua Nowaya Gwineya']
    if number[:6] == '810676' or number[:5] == '10676' or number[:3] == '676':
            return [6.07, 'Tonga']
    if number[:6] == '810678' or number[:5] == '10678' or number[:3] == '678':
            return [6.07, 'Wanuatu']


    # 6.56 manat
    if number[:5] == '81086' or number[:4] == '1086' or number[:2] == '86':
        return [6.56, 'Hytay']
    if number[:5] == '81053' or number[:4] == '1053' or number[:2] == '53':
        return [6.56, 'Kuba']
    if number[:5] == '81091' or number[:4] == '1091' or number[:2] == '91':
        return [6.56, 'Indiya']
    if number[:5] == '81062' or number[:4] == '1062' or number[:2] == '62':
        return [6.56, 'Indoneziya']
    if number[:5] == '81081' or number[:4] == '1081':
        return [6.56, 'Yaponiya']
    if number[:5] == '81060' or number[:4] == '1060' or number[:2] == '60':
        return [6.56, 'Malaziya']
    if number[:5] == '81052' or number[:4] == '1052' or number[:2] == '52':
        return [6.56, 'Meksika']
    if number[:5] == '81095' or number[:4] == '1095' or number[:2] == '95':
        return [6.56, 'Myanma']
    if number[:5] == '81092' or number[:4] == '1092' or number[:2] == '92':
        return [6.56, 'Pakistan']
    if number[:5] == '81063' or number[:4] == '1063' or number[:2] == '63':
        return [6.56, 'Filipiny']
    if number[:5] == '81065' or number[:4] == '1065' or number[:2] == '65':
        return [6.56, 'Singapur']
    if number[:5] == '81082' or number[:4] == '1082' or number[:2] == '82':
        return [6.56, 'Yujnaya Koreya']
    if number[:5] == '81066' or number[:4] == '1066' or number[:2] == '66':
        return [6.56, 'Tailand']
    if number[:5] == '81084' or number[:4] == '1084' or number[:2] == '84':
        return [6.56, 'Wyetnam']        
    if number[:6] == '810973' or number[:5] == '10973' or number[:3] == '973':
        return [6.56, 'Bahreyn']
    if number[:6] == '810880' or number[:5] == '10880' or number[:3] == '880':
        return [6.56, 'Bangladesh']
    if number[:6] == '810673' or number[:5] == '10673' or number[:3] == '673':
        return [6.56, 'Bruney Daruesaalam']
    if number[:6] == '810855' or number[:5] == '10855' or number[:3] == '855':
        return [6.56, 'Kombodja']
    if number[:6] == '810506' or number[:5] == '10506' or number[:3] == '506':
        return [6.56, 'Kosta-Rika']
    if number[:6] == '810670' or number[:5] == '10670' or number[:3] == '670':
        return [6.56, 'Wostochnyy Timor']
    if number[:6] == '810502' or number[:5] == '10502' or number[:3] == '502':
        return [6.56, 'Gwatelama']
    if number[:6] == '810509' or number[:5] == '10509' or number[:3] == '509':
        return [6.56, 'Gaiti']
    if number[:6] == '810504' or number[:5] == '10504' or number[:3] == '504':
        return [6.56, 'Gonduras']
    if number[:6] == '810852' or number[:5] == '10852' or number[:3] == '852':
        return [6.56, 'Gonk-Kong']
    if number[:6] == '810964' or number[:5] == '10964' or number[:3] == '964':
        return [6.56, 'Irak']
    if number[:6] == '810972' or number[:5] == '10972' or number[:3] == '972':
        return [6.56, 'Izrail']
    if number[:6] == '810962' or number[:5] == '10962' or number[:3] == '962':
        return [6.56, 'Iordaniya']
    if number[:6] == '810965' or number[:5] == '10965' or number[:3] == '965':
        return [6.56, 'Kuweit']
    if number[:6] == '810856' or number[:5] == '10856' or number[:3] == '856':
        return [6.56, 'Laos']
    if number[:6] == '810961' or number[:5] == '10961' or number[:3] == '961':
        return [6.56, 'Liwan']
    if number[:6] == '810853' or number[:5] == '10853' or number[:3] == '853':
        return [6.56, 'Makao (Aomyn)']
    if number[:6] == '810976' or number[:5] == '10976' or number[:3] == '976':
        return [6.56, 'Mongoliya']
    if number[:6] == '810977' or number[:5] == '10977' or number[:3] == '977':
        return [6.56, 'Nepal']
    if number[:6] == '810599' or number[:5] == '10599' or number[:3] == '599':
        return [6.56, 'Niderlandskie Antilly']
    if number[:6] == '810505' or number[:5] == '10505' or number[:3] == '505':
        return [6.56, 'Nikaragua']
    if number[:6] == '810850' or number[:5] == '10850' or number[:3] == '850':
        return [6.56, 'Sewernaya Koreya']
    if number[:6] == '810967' or number[:5] == '10967' or number[:3] == '967':
        return [6.56, 'Sewernyy Yemen']
    if number[:6] == '810968' or number[:5] == '10968' or number[:3] == '968':
        return [6.56, 'Oman']
    if number[:6] == '810507' or number[:5] == '10507' or number[:3] == '507':
        return [6.56, 'Panama'] 
    if number[:6] == '810974' or number[:5] == '10974' or number[:3] == '974':
        return [6.56, 'Katar']
    if number[:6] == '810966' or number[:5] == '10966'or number[:3] == '966':
        return [6.56, 'Saudowskaya Arawiya']   
    if number[:6] == '810967' or number[:5] == '10967' or number[:3] == '967':
        return [6.56, 'Yujnyy Yemen']
    if number[:6] == '810963' or number[:5] == '10963' or number[:3] == '963':
        return [6.56, 'Siriya']
    if number[:6] == '810886' or number[:5] == '10886' or number[:3] == '886':
        return [6.56, 'Taiwan']
    if number[:6] == '810971' or number[:5] == '10971' or number[:3] == '971':
        return [6.56, 'O.A.E']
    if number[:4] == '8101' or number[:3] == '101' or (len(number) > 8 and number[:1] == '1' and number[1:2] != '0'):
        return [6.56, 'USA/CANADA']
    

    # 6.78 manat
    if number[:5] == '81054' or number[:4] == '1054' or number[:2] == '54':
        return [6.78, 'Argentina']
    if number[:5] == '81055' or number[:4] == '1055' or number[:2] == '55':
        return [6.78, 'Braziliya']
    if number[:5] == '81056' or number[:4] == '1056' or number[:2] == '56':
        return [6.78, 'Chili']
    if number[:5] == '81057' or number[:4] == '1057' or number[:2] == '57':
        return [6.78, 'Kolumbiya']
    if number[:5] == '81051' or number[:4] == '1051' or number[:2] == '51':
        return [6.78, 'Peru']
    if number[:5] == '81058' or number[:4] == '1058' or number[:2] == '58':
        return [6.78, 'Wenesuella']
    if number[:6] == '810591' or number[:5] == '10591' or number[:3] == '591':
        return [6.78, 'Boliwiya']
    if number[:6] == '810593' or number[:5] == '10593' or number[:3] == '593':
        return [6.78, 'Ekwador']
    if number[:6] == '810298' or number[:5] == '10298' or number[:3] == '298':
        return [6.78, 'Farerskie Ostrowa']
    if number[:6] == '810594' or number[:5] == '10594' or number[:3] == '594':
        return [6.78, 'Fransuskatya Gwiana']
    if number[:6] == '810592' or number[:5] == '10592' or number[:3] == '592':
        return [6.78, 'Gayana']
    if number[:6] == '810596' or number[:5] == '10596' or number[:3] == '596':
        return [6.78, 'Martitnka']
    if number[:6] == '810597' or number[:5] == '10597' or number[:3] == '597':
        return [6.78, 'Surinam']
    if number[:6] == '810598' or number[:5] == '10598' or number[:3] == '598':
        return [6.78, 'Urugway']

    # 7.27 manat
    if number[:5] == '81020' or number[:4] == '1020' or number[:2] == '20':
        return [7.27, 'Egipet']
    if number[:5] == '81027' or number[:4] == '1027' or number[:2] == '27':
        return [7.27, 'UAR']
    if number[:6] == '810213' or number[:5] == '10213' or number[:3] == '213':
        return [7.27, 'Aljir']
    if number[:6] == '810244' or number[:5] == '10244' or number[:3] == '244':
        return [7.27, 'Angola']
    if number[:6] == '810229' or number[:5] == '10229' or number[:3] == '229':
        return [7.27, 'Benin']
    if number[:6] == '810267' or number[:5] == '10267' or number[:3] == '267':
        return [7.27, 'Botswana']
    if number[:6] == '810226' or number[:5] == '10226' or number[:3] == '226':
        return [7.27, 'Burkina Faso']
    if number[:6] == '810257' or number[:5] == '10257' or number[:3] == '257':
        return [7.27, 'Burundi']
    if number[:6] == '810237' or number[:5] == '10237' or number[:3] == '237':
        return [7.27, 'Kamerun']
    if number[:6] == '810238' or number[:5] == '10238' or number[:3] == '238':
        return [7.27, 'Kape Werde']
    if number[:6] == '810236' or number[:5] == '10236' or number[:3] == '236':
        return [7.27, 'SAR']
    if number[:6] == '810235' or number[:5] == '10235' or number[:3] == '235':
        return [7.27, 'Chad']
    if number[:6] == '810242' or number[:5] == '10242' or number[:3] == '242':
        return [7.27, 'Kongo']
    if number[:6] == '810253' or number[:5] == '10253' or number[:3] == '253':
        return [7.27, 'Jibuti']
    if number[:6] == '810240' or number[:5] == '10240' or number[:3] == '240':
        return [7.27, 'Ekwatorialnaya gwineya']
    if number[:6] == '810251' or number[:5] == '10251' or number[:3] == '251':
        return [7.27, 'Efiopiya']
    if number[:6] == '810241' or number[:5] == '10241' or number[:3] == '241':
        return [7.27, 'Gabon']
    if number[:6] == '810220' or number[:5] == '10220' or number[:3] == '220':
        return [7.27, 'Gambiya']
    if number[:6] == '810233' or number[:5] == '10233' or number[:3] == '233':
        return [7.27, 'Gana']
    if number[:6] == '810224' or number[:5] == '10224' or number[:3] == '224':
        return [7.27, 'Gwineya']
    if number[:6] == '810245' or number[:5] == '10245' or number[:3] == '245':
        return [7.27, 'Gwineya Bissau']
    if number[:6] == '810254' or number[:5] == '10254' or number[:3] == '254':
        return [7.27, 'Keniya']
    if number[:6] == '810231' or number[:5] == '10231' or number[:3] == '231':
        return [7.27, 'Liberiya']
    if number[:6] == '810218' or number[:5] == '10218' or number[:3] == '218':
        return [7.27, 'Liviya']
    if number[:6] == '810261' or number[:5] == '10261' or number[:3] == '261':
        return [7.27, 'Madagaskar']
    if number[:6] == '810265' or number[:5] == '10265' or number[:3] == '265':
        return [7.27, 'Malawi']
    if number[:6] == '810223' or number[:5] == '10223' or number[:3] == '223':
        return [7.27, 'Mali']
    if number[:6] == '810222' or number[:5] == '10222' or number[:3] == '222':
        return [7.27, 'Mawritaniya']
    if number[:6] == '810230' or number[:5] == '10230' or number[:3] == '230':
        return [7.27, 'Mawrikiy']
    if number[:6] == '810212' or number[:5] == '10212' or number[:3] == '212':
        return [7.27, 'Moroko']
    if number[:6] == '810258' or number[:5] == '10258' or number[:3] == '258':
        return [7.27, 'Mozambik']
    if number[:6] == '810264' or number[:5] == '10264' or number[:3] == '264':
        return [7.27, 'Namibiya']
    if number[:6] == '810227' or number[:5] == '10227' or number[:3] == '227':
        return [7.27, 'Niger']
    if number[:6] == '810234' or number[:5] == '10234' or number[:3] == '234':
        return [7.27, 'Nigeriya']
    if number[:6] == '810262' or number[:5] == '10262' or number[:3] == '262':
        return [7.27, 'Reonyon']
    if number[:6] == '810250' or number[:5] == '10250' or number[:3] == '250':
        return [7.27, 'Respublika Ruanda']
    if number[:6] == '810221' or number[:5] == '10221' or number[:3] == '221':
        return [7.27, 'Senegal']
    if number[:6] == '810248' or number[:5] == '10248' or number[:3] == '248':
        return [7.27, 'Seyshelskie ostrowa']
    if number[:6] == '810232' or number[:5] == '10232' or number[:3] == '232':
        return [7.27, 'Syerra Leonne']
    if number[:6] == '810252' or number[:5] == '10252' or number[:3] == '252':
        return [7.27, 'Somali']
    if number[:6] == '810249' or number[:5] == '10249' or number[:3] == '249':
        return [7.27, 'Sudan']
    if number[:6] == '810255' or number[:5] == '10255' or number[:3] == '255':
        return [7.27, 'Tanzaniya']
    if number[:6] == '810228' or number[:5] == '10228' or number[:3] == '228':
        return [7.27, 'Respublika Togoleze']
    if number[:6] == '810216' or number[:5] == '10216' or number[:3] == '216':
        return [7.27, 'Tunis']
    if number[:6] == '810256' or number[:5] == '10256' or number[:3] == '256':
        return [7.27, 'Uganda']
    if number[:6] == '810243' or number[:5] == '10243' or number[:3] == '243':
        return [7.27, 'Zair']
    if number[:6] == '810260' or number[:5] == '10260' or number[:3] == '260':
        return [7.27, 'Zambiya']
    if number[:6] == '810263' or number[:5] == '10263' or number[:3] == '263':
        return [7.27, 'Zimbabwe']
    
    # show errors
    # if number == '8888888':
    # 	return [number, '8888888']
    
    # if number == '111':
    # 	return [number, '111']
    
    # if number == '112':
    # 	return [number, '112']
    
    # if number == '119':
    # 	return [number, '119']
    
    # if number == '01':
    # 	return [number, '01']
    
    # if number == '02':
    # 	return [number, '02']

    # if number == '03':
    # 	return [number, '03']
    
    # if number == '071':
    # 	return [number, '071']
    
    # if number == '05':
    # 	return [number, '05']
    
    # if number == '9938001211':
    # 	return [number, '9938001211']
    
    # if number == '04':
    # 	return [number, '04']
    
    # if number == '003229938001211':
    # 	return [number, '003229938001211']
    
    # if number == '0032213000':
    # 	return [number, '0032213000']
    
    # if number == '13000':
    # 	return [number, '13000']

    
    # if number == '00322071':
    # 	return [number, '00322071']
    
    # if number == '383217':
    # 	return [number, '383217']
    
    # if number == '993322071':
    # 	return [number, '993322071']
    
    # if number == '383272':
    # 	return [number, '383272']
    
    # if number == '384129':
    # 	return [number, '384129']
    
    # if number == '383988':
    # 	return [number, '383988']
    
    # if number == '00488803':
    # 	return [number, '00488803']
    
    # if len(number) == 6:
    # 	return [number, '6']
    
    # if number == '003229938001211':
    # 	return [number, '003229938001211']
    
    
    
    
    
    
    return [number, False]



def zte_nach(request):
    context = {}
    if request.user.username == 'Gayyp':
          pass
    else: 
        if not request.user.is_superuser and request.user.username != 'admin1':
            messages.error(request, f"У вас не достаточео прав")
            return render(request, 'telekom/HomePage/HomePage.html', context)
    context['matbIndex'] = True
    context['zte_nach'] = True


    if request.method == 'POST':
        nachislit = request.POST.get('nachislit')
   
    # Свернуть
        # Dashoguz
        hozUsersQuery = UserTable.objects.filter(etrap='Dashoguz', hb__name='H').values('number', 'etrap')
        hozUsers = [f"{user['number']}{user['etrap']}" for user in hozUsersQuery]
        budUsersQuery = UserTable.objects.filter(etrap='Dashoguz', hb__name='B').values('number', 'etrap')
        budUsers = [f"{user['number']}{user['etrap']}" for user in budUsersQuery]
        unknownEdaraQuery = UserTable.objects.filter(etrap='Dashoguz', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsers = [f"{user['number']}{user['etrap']}" for user in unknownEdaraQuery]
        emptyIlatQuery = UserTable.objects.filter(etrap='Dashoguz', name='', surname='').values('number', 'etrap')
        emptyNumberUsers = [f"{user['number']}{user['etrap']}" for user in emptyIlatQuery]

        # Boldumsaz
        hozUsersListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', hb__name='H').values('number', 'etrap')
        hozUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in hozUsersListBoldumsaz]
        budUsersListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', hb__name='B').values('number', 'etrap')
        budUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in budUsersListBoldumsaz]
        UnknownEdaraListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListBoldumsaz]
        emptyIlatListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', name='', surname='').values('number', 'etrap')
        emptyNumberUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in emptyIlatListBoldumsaz]

        # Turkmenbashy
        hozUsersListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', hb__name='H').values('number', 'etrap')
        hozUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in hozUsersListTurkmenbashy]
        budUsersListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', hb__name='B').values('number', 'etrap')
        budUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in budUsersListTurkmenbashy]
        UnknownEdaraListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListTurkmenbashy]
        emptyIlatListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', name='', surname='').values('number', 'etrap')
        emptyNumberUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in emptyIlatListTurkmenbashy]
        
        # Gorogly
        hozUsersListGorogly = UserTable.objects.filter(etrap='Gorogly', hb__name='H').values('number', 'etrap')
        hozUsersGorogly = [f"{user['number']}{user['etrap']}" for user in hozUsersListGorogly]
        budUsersListGorogly = UserTable.objects.filter(etrap='Gorogly', hb__name='B').values('number', 'etrap')
        budUsersGorogly = [f"{user['number']}{user['etrap']}" for user in budUsersListGorogly]
        UnknownEdaraListGorogly = UserTable.objects.filter(etrap='Gorogly', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersGorogly = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListGorogly]
        emptyIlatListGorogly = UserTable.objects.filter(etrap='Gorogly', name='', surname='').values('number', 'etrap')
        emptyNumberUsersGorogly = [f"{user['number']}{user['etrap']}" for user in emptyIlatListGorogly]


        # Koneurgench
        hozUsersListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', hb__name='H').values('number', 'etrap')
        hozUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in hozUsersListKoneurgench]
        budUsersListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', hb__name='B').values('number', 'etrap')
        budUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in budUsersListKoneurgench]
        UnknownEdaraListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListKoneurgench]
        emptyIlatListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', name='', surname='').values('number', 'etrap')
        emptyNumberUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in emptyIlatListKoneurgench]

        # Ruhubelent
        hozUsersListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', hb__name='H').values('number', 'etrap')
        hozUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in hozUsersListRuhubelent]
        budUsersListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', hb__name='B').values('number', 'etrap')
        budUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in budUsersListRuhubelent]
        UnknownEdaraListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListRuhubelent]
        emptyIlatListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', name='', surname='').values('number', 'etrap')
        emptyNumberUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in emptyIlatListRuhubelent]

        # Akdepe
        hozUsersListAkdepe = UserTable.objects.filter(etrap='Akdepe', hb__name='H').values('number', 'etrap')
        hozUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in hozUsersListAkdepe]
        budUsersListAkdepe = UserTable.objects.filter(etrap='Akdepe', hb__name='B').values('number', 'etrap')
        budUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in budUsersListAkdepe]
        UnknownEdaraListAkdepe = UserTable.objects.filter(etrap='Akdepe', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListAkdepe]
        emptyIlatListAkdepe = UserTable.objects.filter(etrap='Akdepe', name='', surname='').values('number', 'etrap')
        emptyNumberUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in emptyIlatListAkdepe]


        # Nyyazow
        hozUsersListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', hb__name='H').values('number', 'etrap')
        hozUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in hozUsersListNyyazow]
        budUsersListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', hb__name='B').values('number', 'etrap')
        budUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in budUsersListNyyazow]
        UnknownEdaraListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', is_enterprises=True, hb=None).values('number', 'etrap')
        UnknowEdaraUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListNyyazow]
        emptyIlatListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', name='', surname='').values('number', 'etrap')
        emptyNumberUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in emptyIlatListNyyazow]
    # Свернуть
    
    
        # Путь к dbf файлам 
        directory = "C:\\Users\\PyView\\Desktop\\zte_files"
     

    

        files_names = os.listdir(directory)
        for index in range(len(files_names)):
            files_names[index] = f"{files_names[index][:-4]}"

        file_name_error = []

        transaction_error = []
        transaction_success = []
        error_file_names = []
        # Сначало проверим dbfNameList начислены ли уже такие файлы или нет
        error_name_list = []
        for myFile in files_names: 
            name_in_DB = dbfNameList.objects.filter(name=myFile).first()

            if re.search("[a-zA-Z]", myFile):
                # print("Есть хотя бы одна буква.")
                file_name_error.append(myFile)
            else:
                pass
                # print("Букв нет.")

            if name_in_DB:
                error_name_list.append(myFile)

        if file_name_error:
            messages.error(request, f'ошибка в имени файла {file_name_error}')
            return render(request, 'telekom/dbfs_nachs/zte_nach.html', context)

        if error_name_list:
            messages.error(request, f'файлы {error_name_list} уже начислены')
            return render(request, 'telekom/dbfs_nachs/zte_nach.html', context)
        else:
            if not nachislit:
                messages.success(request, f"файлы {files_names} прошли проверку успешно")
       
        
        
        test_zte_count = 0
        have_success_messages = False
        count = 0
        for myFile in files_names:
            bulk_create_nonLocal = []
            bulk_create_Local = []
            name = myFile
            file_path = f"{directory}/{myFile}.txt"

            count += 1
            logger.info(f" ==== {count} из {len(files_names)} == {myFile}")
        
            txt = [i.strip('\n').split(';') for i in open(file_path)]

            data = [[a, *b] for a, *b in txt] 

            
            for call in data:
                test_zte_count += 1

                SUB_A = getNumberLocations(call[0])
                SUB_B = getNumberLocations(call[1])

                date_object = call[2]
                DATE = datetime.datetime.strptime(date_object, '%d.%m.%Y').date()
                START = call[3]
                FIN = call[4]
                
                time_format = "%H:%M:%S"
                time1 = datetime.datetime.strptime(START, time_format)
                time2 = datetime.datetime.strptime(FIN, time_format)
                DUR = time2 - time1
                DUR_total_seconds = DUR.total_seconds()
                if DUR_total_seconds / 60 <= 1:
                    MT = 1
                else:
                    MT = int(math.ceil(DUR_total_seconds / 60))



                # Проверка диапазонов
                if SUB_A[1] == 'Boldumsaz' and SUB_A[0][0] == '3':

                    if f"{SUB_A[0]}Boldumsaz" in budUsersBoldumsaz and f"{SUB_A[0]}Boldumsaz" not in emptyNumberUsersBoldumsaz:
                        edaraChar = 'B'
                    elif f"{SUB_A[0]}Boldumsaz" in hozUsersBoldumsaz and f"{SUB_A[0]}Boldumsaz" not in emptyNumberUsersBoldumsaz:
                        edaraChar = 'H'
                    elif f"{SUB_A[0]}Boldumsaz" in emptyNumberUsersBoldumsaz:
                        edaraChar = 'E'
                    else:
                        edaraChar = 'I'



                    # local (без парога)
                    if SUB_B[1] == 'five' or SUB_B[1] == 'Boldumsaz':
                        # для Бюджетных локальные звонки не начисляются
                        if edaraChar == 'B':
                            continue
                        obj = LocalCall(
                            etrap='Boldumsaz',
                            SUB_A=SUB_A[0],
                            SUB_B=SUB_B[0],
                            DATE=DATE,
                            START=str(START),
                            FIN=str(FIN),
                            DUR=str(DUR),
                            MT=MT,
                            file_name=name,
                            edara=edaraChar
                        )
                        bulk_create_Local.append(obj)
                        continue
                    
                    # Порог
                    if DUR_total_seconds <= 4:
                        continue

                    # Turkmenistan
                    if (SUB_B[1] in turkmenistan or SUB_B[1] in etraps) and SUB_B[1] != 'Boldumsaz' and SUB_B[1] != 'five':
                        if edaraChar in ['H', 'B']:
                            price_for_1_min = 0.14
                        else:
                            price_for_1_min = 0.08
                        obj = NonLocalCall(
                            SUB_A_etrap='Boldumsaz',
                            SUB_A=SUB_A[0],
                            SUB_B_locations=SUB_B[1],
                            SUB_B=call[1],
                            type='intercity',
                            price=price_for_1_min,
                            DATE=DATE,
                            START=str(START),
                            FIN=str(FIN),
                            DUR=str(DUR),
                            MT=MT,
                            total_price=int(MT) * price_for_1_min,
                            file_name=name,
                            edara=edaraChar
                        )
                        bulk_create_nonLocal.append(obj)
                        continue

                    # Международные разговоры
                    if SUB_B[1] in international:
                        obj = NonLocalCall(
                            SUB_A_etrap='Boldumsaz',
                            SUB_A=SUB_A[0],
                            SUB_B_locations=SUB_B[1],
                            SUB_B=call[1],
                            type='international',
                            price=SUB_B[0],
                            DATE=DATE,
                            START=str(START),
                            FIN=str(FIN),
                            DUR=str(DUR),
                            MT=MT,
                            total_price=int(MT) * SUB_B[0],
                            file_name=name,
                            edara=edaraChar
                        )
                        bulk_create_nonLocal.append(obj)
                        continue
            if nachislit:
                try:
                    with transaction.atomic():
                        if bulk_create_Local:
                            LocalCall.objects.bulk_create(bulk_create_Local)
                        if bulk_create_nonLocal:
                            NonLocalCall.objects.bulk_create(bulk_create_nonLocal)
                        if bulk_create_Local or bulk_create_nonLocal:
                            have_success_messages = True
                            dbfNameList.objects.create(name=name)
                    
                        # Удаление дубликатов deepai
                        calls_obj = NonLocalCall.objects.filter(file_name=name)
                        unique_records = {}
                        duplicates = []
                        for record in calls_obj:
                            # Создаем уникальный идентификатор для дублирующей записи
                            identifier = (record.SUB_A_etrap, record.SUB_A, record.SUB_B_locations, record.SUB_B, record.DATE, record.START, record.FIN)

                            if identifier in unique_records:
                                # Если идентификатор уже встречался, добавляем ID записи в дубликаты
                                duplicates.append(record.id)
                            else:
                                # Сохраняем уникальную запись
                                unique_records[identifier] = record.id  # Или просто можете сохранить сам объект, если это нужно
                        # Удаляем дубликаты
                        if duplicates:
                            NonLocalCall.objects.filter(id__in=duplicates).delete()
                            logger.info(f"Удалено дубликатов: {len(duplicates)} {name}")
                        else:
                            logger.info(f"Дубликатов не найдено. {name}")
                        transaction_success.append(name)
                except Exception as e:
                    logger.warning(f"Не удалось начислить файл {name} по причине {str(e)}")
                    transaction_error.append(name)

        if have_success_messages:
            if transaction_success and not transaction_error:
                messages.success(request, f"Все файлы zte успешно начислены")
            elif not transaction_success and transaction_error:
                messages.error(request, f"Все файлы zte не начислены по причине transaction")
            else:
                messages.error(request, f"Файлы zte частично начислены по причине transaction: начисленные{transaction_success}, не начисленные {transaction_error}")



        # print('test_zte_count', test_zte_count)



     

    return render(request, 'telekom/dbfs_nachs/zte_nach.html', context)







# Код работает идеально но без transaction
    # from django.shortcuts import render
    # import sqlite3
    # from dbfread import DBF
    # import datetime
    # from datetime import date
    # import datetime
    # import math
    # import time
    # import os
    # import sys
    # from telekom.models import *
    # from django.contrib import messages
    # from bulk_update.helper import bulk_update
    # import re



    # def bell():
    #     sys.stdout.write('\r\a')
    #     sys.stdout.flush()


    # mugut = ['8888888','111','119','01','02','071','05', '03','9938001211','04','003229938001211','0032213000','00322071','383217','993322071','383272','384129',
    #     '383988','00488803','003229938001211', '112']

    # etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    # turkmenistan = ['Sotowyy',
    #         'Ashgabat','Ahal Baharly','Ahal Gokdepe','Ahal Kaka','Ahal Seraks','Ahal Tejen','Ahal Babadayhan','Ahal Anew','Ahal Abadan','Ahal Ruhabat','Ahal Ashgabat',
    #         'Balkan Nebitdag','Balkan Hazar','Balkan Gumdag','Balkan Gyzyl Atr','Balkan Turkmenbashy','Balkan Gumdag','Balkan Esenguly','Balkan Serdar','Balkan Bereket','Balkan Magtymguly',
    #         'Lebap Turkmenabat','Lebap Magdanly','Lebap Garashsyzlyk','Lebap Gazajak','Lebap Koytendag','Lebap Halach','Lebap Hojambaz','Lebap Garabekewul','Lebap Atamyrat','Lebap Birata',
    #         'Lebap Galkynysh','Lebap Sayat','Lebap Farap', 'Lebap Sakar','Lebap Seydi','Lebap Turkmenbashy','Lebap Serdarabat','Lebap Serdarabat',
    #         'Mary','Mary Garagum','Mary Wekilbazar','Mary Oguzhan','Mary Yoleten','Mary Serhetabat','Mary Bayramaly','Mary Murgap','Mary Sakarchage','Mary Tagtabazar','Mary Turkm-gala']

    # international = ['Moldowa','Fransiya','Germaniya','Gresiya','Wengriya','Italiya','Niderlandy','Norwegiya','Polsha','Rumyniya','Shwesiya','Shweysariya','Welikobritaniya','Ispaniya','Albaniya','Andorra','Bosniya Gersogowina','Bolgariya','Horwatiya','Kipr',
    #         'Estoniya','Finlyandiya','Gibraltar','Grenlandiya','Islandiya','Latwiya','Lihtenshteyn','Litwa','Luksenburg','Makedoniya','Malta','Portugaliya','Slowakiya','Sloweniya','Yugoslawiya','Cheshskaya Respublika',
    #         'Kazakstan','Rossiya','Kyrgystan','Tajikistan','Uzbekistan','Belorussiya','Armeniya','Azerbayjan','Gruziya','Ukraina','Afganistan','Turkiya','Iran','Awstriya','Belgiya','Daniya',
    #         'Awstraliya','Nowaya Zenlandiya','Fidji','Fransuskaya Polineziya','Kiribati','Nowaya Kaledoniya','Norfolkskiye ostrowa','Papua Nowaya Gwineya','Tonga','Wanuatu','Hytay','Kuba','Indiya','Indoneziya','Yaponiya','Malaziya','Meksika','Myanma',
    #         'Pakistan','Filipiny','Singapur','Yujnaya Koreya','Tailand','Wyetnam','Bahreyn','Bangladesh','Bruney Daruesaalam','Kombodja','Kosta-Rika','Wostochnyy Timor','Gwatelama','Gaiti','Gonduras','Gonk-Kong','Irak','Izrail','Iordaniya','Kuweit','Laos','Liwan',
    #         'Makao (Aomyn)','Mongoliya','Nepal','Niderlandskie Antilly','Nikaragua','Sewernaya Koreya','Sewernyy Yemen','Oman','Panama' 'Katar','Saudowskaya Arawiya','Yujnyy Yemen','Siriya','Taiwan','O.A.E','USA/CANADA','Argentina','Braziliya','Chili',
    #         'Kolumbiya','Peru','Wenesuella','Boliwiya','Ekwador','Farerskie Ostrowa','Fransuskatya Gwiana','Gayana','Martitnka','Surinam','Urugway','Egipet','UAR','Aljir','Angola','Benin','Botswana','Burkina Faso','Burundi','Kamerun',
    #         'Kape Werde','SAR','Chad','Kongo','Jibuti','Ekwatorialnaya gwineya','Efiopiya','Gabon','Gambiya','Gana','Gwineya','Gwineya Bissau','Keniya','Liberiya','Liviya','Madagaskar','Malawi','Mali','Mawritaniya','Mawrikiy',
    #         'Moroko','Mozambik','Namibiya','Niger','Nigeriya','Reonyon','Respublika Ruanda','Senegal','Seyshelskie ostrowa','Syerra Leonne','Somali','Sudan','Tanzaniya','Respublika Togoleze','Tunis','Uganda','Zair','Zambiya','Zimbabwe']



    # # Функция для прибавления секунд в время (Чтобы узнать END Разговора)
    # def add_secs_to_time(timeval, secs_to_add):
    #     secs = timeval.hour * 3600 + timeval.minute * 60 + timeval.second
    #     secs += secs_to_add
    #     if secs // 3600 > 23:
    #         return datetime.time(00, (secs % 3600) // 60, secs % 60)
    #     else:
    #         return datetime.time(secs // 3600, (secs % 3600) // 60, secs % 60)


    # # достаем локацию номера в виде списка:
    # def getNumberLocations(number):
    #     # Etraps
    #     # Dashoguz
    #     if number[0:8] == '00800322' and len(number) == 13:
    #         return [number[8:], 'Dashoguz']
    #     if (number[0:6] == '800322' or number[0:6] == '993322') and len(number) == 11:
    #         return [number[6:], 'Dashoguz']
    #     if (number[0:5] == '00322' and len(number) == 10) and number != '0032213000':
    #         return [number[5:], 'Dashoguz']
    #     if number[0:3] == '322' and len(number) == 8:
    #         return [number[3:], 'Dashoguz']
        
    #     # local
    #     if (len(number) == 5) and number != '13000':
    #         return [number, 'five']

    #     # Akdepe
    #     if (number[0:8] == '00800344' or number[0:8] == '00800343') and len(number) == 13:
    #         return [number[8:], 'Akdepe']
    #     if (number[0:6] == '800344' or number[0:6] == '800343' or number[0:6] == '993344' or number[0:6] == '993343') and len(number) == 11:
    #         return [number[6:], 'Akdepe']
    #     if (number[0:5] == '00344' or number[0:5] == '00343') and len(number) == 10:
    #         return [number[5:], 'Akdepe']
    #     if (number[0:3] == '344' and len(number) == 8) or (number[0:3] == '343' and len(number) == 8):
    #         return [number[3:], 'Akdepe']

    #     # Boldumsaz
    #     if (number[0:8] == '00800346' or number[0:8] == '00800345') and len(number) == 13:
    #         return [number[8:], 'Boldumsaz']
    #     if (number[0:6] == '800346' or number[0:6] == '800345' or number[0:6] == '993346' or number[0:6] == '993345') and len(number) == 11:
    #         return [number[6:], 'Boldumsaz']
    #     if (number[0:5] == '00346' or number[0:5] == '00345') and len(number) == 10:
    #         return [number[5:], 'Boldumsaz']
    #     if (number[0:3] == '346' and len(number) == 8) or (number[0:3] == '345' and len(number) == 8):
    #         return [number[3:], 'Boldumsaz']

    #     # Gorogly
    #     if number[0:8] == '00800340' and len(number) == 13:
    #         return [number[8:], 'Gorogly']
    #     if (number[0:6] == '800340' or number[0:6] == '993340') and len(number) == 11:
    #         return [number[6:], 'Gorogly']
    #     if  number[0:5] == '00340' and len(number) == 10:
    #         return [number[5:], 'Gorogly']
    #     if number[0:3] == '340' and len(number) == 8:
    #         return [number[3:], 'Gorogly']

    #     # Koneurgench
    #     if number[0:8] == '00800347' and len(number) == 13:
    #         return [number[8:], 'Koneurgench']
    #     if (number[0:6] == '800347' or number[0:6] == '993347') and len(number) == 11:
    #         return [number[6:], 'Koneurgench']
    #     if number[0:5] == '00347' and len(number) == 10:
    #         return [number[5:], 'Koneurgench']
    #     if number[0:3] == '347' and len(number) == 8:
    #         return [number[3:], 'Koneurgench']


    #     # Turkmenbashy
    #     if number[0:8] == '00800349' and len(number) == 13:
    #         return [number[8:], 'Turkmenbashy']
    #     if (number[0:6] == '800349' or number[0:6] == '993349') and len(number) == 11:
    #         return [number[6:], 'Turkmenbashy']
    #     if number[0:5] == '00349' and len(number) == 10:
    #         return [number[5:], 'Turkmenbashy']
    #     if number[0:3] == '349' and len(number) == 8:
    #         return [number[3:], 'Turkmenbashy']

    #     # S.A.Nyyazow
    #     if number[0:8] == '00800348' and len(number) == 13:
    #         return [number[8:], 'S.A.Nyyazow']
    #     if (number[0:6] == '800348' or number[0:6] == '993348') and len(number) == 11:
    #         return [number[6:], 'S.A.Nyyazow']
    #     if number[0:5] == '00348' and len(number) == 10:
    #         return [number[5:], 'S.A.Nyyazow']
    #     if number[0:3] == '348' and len(number) == 8:
    #         return [number[3:], 'S.A.Nyyazow']

    #     # Ruhubelent
    #     if number[0:8] == '00800342' and len(number) == 13:
    #         return [number[8:], 'Ruhubelent']
    #     if (number[0:6] == '800342' or number[0:6] == '993342') and len(number) == 11:
    #         return [number[6:], 'Ruhubelent']
    #     if number[0:5] == '00342' and len(number) == 10:
    #         return [number[5:], 'Ruhubelent']
    #     if number[0:3] == '342' and len(number) == 8:
    #         return [number[3:], 'Ruhubelent']

    #     # Altyn Asyr
    #     if (number[0:5] == '99360' or number[0:5] == '99361' or number[0:5] == '99362' or number[0:5] == '99363' or number[0:5] == '99364' or number[0:5] == '99365' or number[0:5] == '99371' or 
    #         number[0:5] == '80060' or number[0:5] == '80061' or number[0:5] == '80062' or number[0:5] == '80063' or number[0:5] == '80064' or number[0:5] == '80065' or number[0:5] == '80071' or
    #         number[0:4] == '0060' or number[0:4] == '0061' or number[0:4] == '0062' or number[0:4] == '0063' or number[0:4] == '0064' or number[0:4] == '0065' or number[0:4] == '0071' or
    #         (len(number) == 8 and number[0:2] == '60') or 
    #         (len(number) == 8 and number[0:2] == '61') or 
    #         (len(number) == 8 and number[0:2] == '62') or 
    #         (len(number) == 8 and number[0:2] == '63') or 
    #         (len(number) == 8 and number[0:2] == '64') or 
    #         (len(number) == 8 and number[0:2] == '65') or
    #         (len(number) == 8 and number[0:2] == '71') or
    #         (len(number) == 10 and number[:3] == '936') or
    #         (len(number) == 10 and number[:3] == '937')
    #         ):
    #         return [0.08, 'Sotowyy']

    #     # Ashgabat wel.
    #     if number[:5] == '80012' or number[:4] == '0012' or (len(number) == 8 and number[:2] == '12'):
    #         return [0.08, 'Ashgabat']
    #     if number[:6] == '800131' or number[:5] == '00131' or (len(number) == 8 and number[:3] == '131'):
    #         return [0.08, 'Ahal Baharly']
    #     if number[:6] == '800132' or number[:5] == '00132' or (len(number) == 8 and number[:3] == '132'):
    #         return [0.08, 'Ahal Gokdepe']
    #     if number[:6] == '800133' or number[:5] == '00133' or (len(number) == 8 and number[:3] == '133'):
    #         return [0.08, 'Ahal Kaka']
    #     if number[:6] == '800134' or number[:5] == '00134' or (len(number) == 8 and number[:3] == '134'):
    #         return [0.08, 'Ahal Seraks']
    #     if number[:6] == '800135' or number[:5] == '00135' or (len(number) == 8 and number[:3] == '135'):
    #         return [0.08, 'Ahal Tejen']
    #     if number[:6] == '800136' or number[:5] == '00136' or (len(number) == 8 and number[:3] == '136'):
    #         return [0.08, 'Ahal Babadayhan']
    #     if number[:6] == '800137' or number[:5] == '00137' or (len(number) == 8 and number[:3] == '137'):
    #         return [0.08, 'Ahal Anew']
    #     if number[:6] == '800138' or number[:5] == '00138' or (len(number) == 8 and number[:3] == '138'):
    #         return [0.08, 'Ahal Abadan']
    #     if number[:6] == '800139' or number[:5] == '00139' or (len(number) == 8 and number[:3] == '139'):
    #         return [0.08, 'Ahal Ruhabat']
    #     if number[:6] == '800181' or number[:5] == '00181' or (len(number) == 8 and number[:3] == '181'):
    #         return [0.08, 'Ahal Ashgabat']

    #     # Balkan wel.
    #     if number[:6] == '800222' or number[:5] == '00222' or (len(number) == 8 and number[:3] == '222'):
    #         return [0.08, 'Balkan Nebitdag']
    #     if number[:6] == '800240' or number[:5] == '00240' or (len(number) == 8 and number[:3] == '240'):
    #         return [0.08, 'Balkan Hazar']
    #     if number[:6] == '800241' or number[:5] == '00241' or (len(number) == 8 and number[:3] == '241'):
    #         return [0.08, 'Balkan Gumdag']
    #     if number[:6] == '800242' or number[:5] == '00242' or (len(number) == 8 and number[:3] == '242'):
    #         return [0.08, 'Balkan Gyzyl Atr']
    #     if number[:6] == '800243' or number[:5] == '00243' or (len(number) == 8 and number[:3] == '243'):
    #         return [0.08, 'Balkan Turkmenbashy']
    #     if number[:6] == '800244' or number[:5] == '00244' or (len(number) == 8 and number[:3] == '244'):
    #         return [0.08, 'Balkan Gumdag']
    #     if number[:6] == '800245' or number[:5] == '00245' or (len(number) == 8 and number[:3] == '245'):
    #         return [0.08, 'Balkan Esenguly']
    #     if number[:6] == '800246' or number[:5] == '00246' or (len(number) == 8 and number[:3] == '246'):
    #         return [0.08, 'Balkan Serdar']
    #     if number[:6] == '800247' or number[:5] == '00247' or (len(number) == 8 and number[:3] == '247'):
    #         return [0.08, 'Balkan Bereket']
    #     if number[:6] == '800248' or number[:5] == '00248' or (len(number) == 8 and number[:3] == '248'):
    #         return [0.08, 'Balkan Magtymguly']

    #     # Lebap wel.
    #     if number[:6] == '800422' or number[:5] == '00422' or (len(number) == 8 and number[:3] == '422'):
    #         return [0.08, 'Lebap Turkmenabat']
    #     if number[:6] == '800431' or number[:5] == '00431' or (len(number) == 8 and number[:3] == '431'):
    #         return [0.08, 'Lebap Magdanly']
    #     if number[:6] == '800432' or number[:5] == '00432' or (len(number) == 8 and number[:3] == '432'):
    #         return [0.08, 'Lebap Garashsyzlyk']
    #     if number[:6] == '800438' or number[:5] == '00438' or (len(number) == 8 and number[:3] == '438'):
    #         return [0.08, 'Lebap Gazajak']
    #     if number[:6] == '800440' or number[:5] == '00440' or (len(number) == 8 and number[:3] == '440'):
    #         return [0.08, 'Lebap Koytendag']
    #     if number[:6] == '800441' or number[:5] == '00441' or (len(number) == 8 and number[:3] == '441'):
    #         return [0.08, 'Lebap Halach']
    #     if number[:6] == '800442' or number[:5] == '00442' or (len(number) == 8 and number[:3] == '442'):
    #         return [0.08, 'Lebap Hojambaz']
    #     if number[:6] == '800443' or number[:5] == '00443' or (len(number) == 8 and number[:3] == '443'):
    #         return [0.08, 'Lebap Garabekewul']
    #     if number[:6] == '800444' or number[:5] == '00444' or (len(number) == 8 and number[:3] == '444'):
    #         return [0.08, 'Lebap Atamyrat']
    #     if number[:6] == '800445' or number[:5] == '00445' or (len(number) == 8 and number[:3] == '445'):
    #         return [0.08, 'Lebap Birata']
    #     if number[:6] == '800446' or number[:5] == '00446' or (len(number) == 8 and number[:3] == '446'):
    #         return [0.08, 'Lebap Galkynysh']
    #     if number[:6] == '800447' or number[:5] == '00447' or (len(number) == 8 and number[:3] == '447'):
    #         return [0.08, 'Lebap Sayat']
    #     if number[:6] == '800448' or number[:5] == '00448' or (len(number) == 8 and number[:3] == '448'):
    #         return [0.08, 'Lebap Farap']
    #     if number[:6] == '800449' or number[:5] == '00449' or (len(number) == 8 and number[:3] == '449'):
    #         return [0.08, 'Lebap Sakar']
    #     if number[:6] == '800461' or number[:5] == '00461' or (len(number) == 8 and number[:3] == '461'):
    #         return [0.08, 'Lebap Seydi']
    #     if number[:6] == '800465' or number[:5] == '00465' or (len(number) == 8 and number[:3] == '465'):
    #         return [0.08, 'Lebap Turkmenbashy']
    #     if number[:6] == '800433' or number[:5] == '00433' or (len(number) == 8 and number[:3] == '433'):
    #         return [0.08, 'Lebap Serdarabat']
    #     if number[:6] == '800434' or number[:5] == '00434' or (len(number) == 8 and number[:3] == '434'):
    #         return [0.08, 'Lebap Serdarabat']

    #     # Mary wel.
    #     if number[:6] == '800522' or number[:5] == '00522' or (len(number) == 8 and number[:3] == '552'):
    #         return [0.08, 'Mary']
    #     if number[:6] == '800557' or number[:5] == '00557' or (len(number) == 8 and number[:3] == '557'):
    #         return [0.08, 'Mary Garagum']
    #     if number[:6] == '800558' or number[:5] == '00558' or (len(number) == 8 and number[:3] == '558'):
    #         return [0.08, 'Mary Wekilbazar']
    #     if number[:6] == '800559' or number[:5] == '00559' or (len(number) == 8 and number[:3] == '559'):
    #         return [0.08, 'Mary Oguzhan']
    #     if number[:6] == '800560' or number[:5] == '00560' or (len(number) == 8 and number[:3] == '560'):
    #         return [0.08, 'Mary Yoleten']
    #     if number[:6] == '800561' or number[:5] == '00561' or (len(number) == 8 and number[:3] == '561'):
    #         return [0.08, 'Mary Serhetabat']
    #     if number[:6] == '800564' or number[:5] == '00564' or (len(number) == 8 and number[:3] == '564'):
    #         return [0.08, 'Mary Bayramaly']
    #     if number[:6] == '800565' or number[:5] == '00565' or (len(number) == 8 and number[:3] == '565'):
    #         return [0.08, 'Mary Murgap']
    #     if number[:6] == '800566' or number[:5] == '00566' or (len(number) == 8 and number[:3] == '566'):
    #         return [0.08, 'Mary Sakarchage']
    #     if number[:6] == '800568' or number[:5] == '00568' or (len(number) == 8 and number[:3] == '568'):
    #         return [0.08, 'Mary Tagtabazar']
    #     if number[:6] == '800569' or number[:5] == '00569' or (len(number) == 8 and number[:3] == '569'):
    #         return [0.08, 'Mary Turkm-gala']

    #     # Другие страны
    #     if number[:5] == '81077' or number[:5] == '81076' or number[:4] == '1076' or number[:4] == '1077' or number[:2] == '77' or number[:2] == '76':
    #         return [1.44, 'Kazakstan']
    #     if (number[:4] == '8107' and number[:5] != '81077' and number[:5] != '81076') or (number[:1] == '7' and number[:2] != '76' and number[:2] != '77'):
    #         return [1.94, 'Rossiya']
    #     if number[:3] == '107' and number[:4] != '1077' and number[:4] != '1076':
    #         return [1.94, 'Rossiya']
    #     if number[:6] == '810996' or number[:5] == '10996' or number[:3] == '996':
    #         return [1.44, 'Kyrgystan']
    #     if number[:6] == '810373' or number[:5] == '10373' or number[:3] == '373':
    #         return [1.8, 'Moldowa']
    #     if number[:6] == '810992' or number[:5] == '10992' or number[:3] == '992':
    #         return [1.44, 'Tajikistan']
    #     if number[:6] == '810998' or number[:5] == '10998' or number[:3] == '998':
    #         return [1.44, 'Uzbekistan']
    #     if number[:6] == '810375' or number[:5] == '10375' or number[:3] == '375':
    #         return [1.8, 'Belorussiya']
    #     if number[:6] == '810374' or number[:5] == '10374' or number[:3] == '374':
    #         return [2.16, 'Armeniya']
    #     if number[:6] == '810994' or number[:5] == '10994' or number[:3] == '994':
    #         return [2.16, 'Azerbayjan']
    #     if number[:6] == '810995' or number[:5] == '10995' or number[:3] == '995':
    #         return [2.16, 'Gruziya']
    #     if number[:6] == '810380' or number[:5] == '10380' or number[:3] == '380':
    #         return [2.16, 'Ukraina']
    #     if number[:5] == '81093' or number[:4] == '1093' or number[:2] == '93':
    #         return [2.31, 'Afganistan']
    #     if number[:5] == '81090' or number[:4] == '1090' or number[:2] == '90':
    #         return [3.06, 'Turkiya']
    #     if number[:5] == '81098' or number[:4] == '1098' or number[:2] == '98':
    #         return [3.3, 'Iran']
    #     if number[:5] == '81043' or number[:4] == '1043' or number[:2] == '43':
    #         return [3.96, 'Awstriya']
    #     if number[:5] == '81032' or number[:4] == '1032' or (number[:2] == '32' and len(number) > 8):
    #         return [3.96, 'Belgiya']
    #     if number[:5] == '81045' or number[:4] == '1045' or number[:2] == '45':
    #         return [3.96, 'Daniya']


    #     # 3.96 manat
    #     if number[:5] == '81033' or number[:4] == '1033' or number[:2] == '33':
    #         return [3.96, 'Fransiya']
    #     if number[:5] == '81049' or number[:4] == '1049' or number[:2] == '49' and len(number) > 8:
    #         return [3.96, 'Germaniya']
    #     if number[:5] == '81030' or number[:4] == '1030' or number[:2] == '30':
    #         return [3.96, 'Gresiya']
    #     if number[:5] == '81036' or number[:4] == '1036' or number[:2] == '36':
    #         return [3.96, 'Wengriya']
    #     if number[:5] == '81039' or number[:4] == '1039' or number[:2] == '39':
    #         return [3.96, 'Italiya']
    #     if number[:5] == '81031' or number[:4] == '1031' or number[:2] == '31':
    #         return [3.96, 'Niderlandy']
    #     if number[:5] == '81047' or number[:4] == '1047' or number[:2] == '47' and len(number) > 8:
    #         return [3.96, 'Norwegiya']
    #     if number[:5] == '81048' or number[:4] == '1048' or (len(number) > 8 and number[:2] == '48'):
    #         return [3.96, 'Polsha']
    #     if number[:5] == '81040' or number[:4] == '1040' or number[:2] == '40' and len(number) > 8:
    #         return [3.96, 'Rumyniya']
    #     if number[:5] == '81046' or number[:4] == '1046' or number[:2] == '46' and len(number) > 8:
    #         return [3.96, 'Shwesiya']
    #     if number[:5] == '81041' or number[:4] == '1041' or number[:2] == '41':
    #         return [3.96, 'Shweysariya']
    #     if number[:5] == '81044' or number[:4] == '1044' or number[:2] == '44':
    #         return [3.96, 'Welikobritaniya']
    #     if number[:5] == '81034' or number[:4] == '1034' or (number[:2] == '34' and len(number) > 8):
    #         return [3.96, 'Ispaniya']
    #     if number[:6] == '810355' or number[:5] == '10355' or number[:3] == '355':
    #         return [3.96, 'Albaniya']
    #     if number[:6] == '810376' or number[:5] == '10376' or number[:3] == '376':
    #         return [3.96, 'Andorra']
    #     if number[:6] == '810387' or number[:5] == '10387' or number[:3] == '387':
    #         return [3.96, 'Bosniya Gersogowina']
    #     if number[:6] == '810359' or number[:5] == '10359' or number[:3] == '359':
    #         return [3.96, 'Bolgariya']
    #     if number[:6] == '810385' or number[:5] == '10385' or number[:3] == '385':
    #         return [3.96, 'Horwatiya']
    #     if number[:6] == '810357' or number[:5] == '10357' or number[:3] == '357':
    #         return [3.96, 'Kipr']
    #     if number[:6] == '810372' or number[:5] == '10372' or number[:3] == '372':
    #         return [3.96, 'Estoniya']
    #     if number[:6] == '810358' or number[:5] == '10358' or number[:3] == '358':
    #         return [3.96, 'Finlyandiya']
    #     if number[:6] == '810350' or number[:5] == '10350' or number[:3] == '350':
    #         return [3.96, 'Gibraltar']
    #     if number[:6] == '810299' or number[:5] == '10299' or number[:3] == '299':
    #         return [3.96, 'Grenlandiya']
    #     if number[:6] == '810354' or number[:5] == '10354' or number[:3] == '354':
    #         return [3.96, 'Islandiya']
    #     if number[:6] == '810371' or number[:5] == '10371' or number[:3] == '371':
    #         return [3.96, 'Latwiya']
    #     if number[:6] == '810423' or number[:5] == '10423' or number[:3] == '423':
    #         return [3.96, 'Lihtenshteyn']
    #     if number[:6] == '810370' or number[:5] == '10370' or number[:3] == '370':
    #         return [3.96, 'Litwa']
    #     if number[:6] == '810352' or number[:5] == '10352' or number[:3] == '352':
    #         return [3.96, 'Luksenburg']
    #     if number[:6] == '810389' or number[:5] == '10389' or number[:3] == '389':
    #         return [3.96, 'Makedoniya']
    #     if number[:6] == '810356' or number[:5] == '10356' or number[:3] == '356':
    #         return [3.96, 'Malta']
    #     if number[:6] == '810351' or number[:5] == '10351' or number[:3] == '351':
    #         return [3.96, 'Portugaliya']
    #     if number[:6] == '810421' or number[:5] == '10421' or number[:3] == '421':
    #         return [3.96, 'Slowakiya']
    #     if number[:6] == '810386' or number[:5] == '10386' or number[:3] == '386':
    #         return [3.96, 'Sloweniya']
    #     if number[:6] == '810381' or number[:5] == '10381' or number[:3] == '381':
    #         return [3.96, 'Yugoslawiya']
    #     if number[:6] == '810420' or number[:5] == '10420' or number[:3] == '420':
    #         return [3.96, 'Cheshskaya Respublika']
        

    #     # 6.07 manat
    #     if number[:5] == '81061' or number[:4] == '1061' or number[:2] == '61':
    #         return [6.07, 'Awstraliya']
    #     if number[:5] == '81064' or number[:4] == '1064' or number[:2] == '64':
    #             return [6.07, 'Nowaya Zenlandiya']
    #     if number[:6] == '810679' or number[:5] == '10679' or number[:3] == '679':
    #         return [6.07, 'Fidji']
    #     if number[:6] == '810689' or number[:5] == '10689' or number[:3] == '689':
    #             return [6.07, 'Fransuskaya Polineziya']
    #     if number[:6] == '810686' or number[:5] == '10686' or number[:3] == '686':
    #         return [6.07, 'Kiribati']
    #     if number[:6] == '810687' or number[:5] == '10687' or number[:3] == '687':
    #             return [6.07, 'Nowaya Kaledoniya']
    #     if number[:6] == '810672' or number[:5] == '10672' or number[:3] == '672':
    #             return [6.07, 'Norfolkskiye ostrowa']
    #     if number[:6] == '810675' or number[:5] == '10675' or number[:3] == '675':
    #             return [6.07, 'Papua Nowaya Gwineya']
    #     if number[:6] == '810676' or number[:5] == '10676' or number[:3] == '676':
    #             return [6.07, 'Tonga']
    #     if number[:6] == '810678' or number[:5] == '10678' or number[:3] == '678':
    #             return [6.07, 'Wanuatu']


    #     # 6.56 manat
    #     if number[:5] == '81086' or number[:4] == '1086' or number[:2] == '86':
    #         return [6.56, 'Hytay']
    #     if number[:5] == '81053' or number[:4] == '1053' or number[:2] == '53':
    #         return [6.56, 'Kuba']
    #     if number[:5] == '81091' or number[:4] == '1091' or number[:2] == '91':
    #         return [6.56, 'Indiya']
    #     if number[:5] == '81062' or number[:4] == '1062' or number[:2] == '62':
    #         return [6.56, 'Indoneziya']
    #     if number[:5] == '81081' or number[:4] == '1081':
    #         return [6.56, 'Yaponiya']
    #     if number[:5] == '81060' or number[:4] == '1060' or number[:2] == '60':
    #         return [6.56, 'Malaziya']
    #     if number[:5] == '81052' or number[:4] == '1052' or number[:2] == '52':
    #         return [6.56, 'Meksika']
    #     if number[:5] == '81095' or number[:4] == '1095' or number[:2] == '95':
    #         return [6.56, 'Myanma']
    #     if number[:5] == '81092' or number[:4] == '1092' or number[:2] == '92':
    #         return [6.56, 'Pakistan']
    #     if number[:5] == '81063' or number[:4] == '1063' or number[:2] == '63':
    #         return [6.56, 'Filipiny']
    #     if number[:5] == '81065' or number[:4] == '1065' or number[:2] == '65':
    #         return [6.56, 'Singapur']
    #     if number[:5] == '81082' or number[:4] == '1082' or number[:2] == '82':
    #         return [6.56, 'Yujnaya Koreya']
    #     if number[:5] == '81066' or number[:4] == '1066' or number[:2] == '66':
    #         return [6.56, 'Tailand']
    #     if number[:5] == '81084' or number[:4] == '1084' or number[:2] == '84':
    #         return [6.56, 'Wyetnam']        
    #     if number[:6] == '810973' or number[:5] == '10973' or number[:3] == '973':
    #         return [6.56, 'Bahreyn']
    #     if number[:6] == '810880' or number[:5] == '10880' or number[:3] == '880':
    #         return [6.56, 'Bangladesh']
    #     if number[:6] == '810673' or number[:5] == '10673' or number[:3] == '673':
    #         return [6.56, 'Bruney Daruesaalam']
    #     if number[:6] == '810855' or number[:5] == '10855' or number[:3] == '855':
    #         return [6.56, 'Kombodja']
    #     if number[:6] == '810506' or number[:5] == '10506' or number[:3] == '506':
    #         return [6.56, 'Kosta-Rika']
    #     if number[:6] == '810670' or number[:5] == '10670' or number[:3] == '670':
    #         return [6.56, 'Wostochnyy Timor']
    #     if number[:6] == '810502' or number[:5] == '10502' or number[:3] == '502':
    #         return [6.56, 'Gwatelama']
    #     if number[:6] == '810509' or number[:5] == '10509' or number[:3] == '509':
    #         return [6.56, 'Gaiti']
    #     if number[:6] == '810504' or number[:5] == '10504' or number[:3] == '504':
    #         return [6.56, 'Gonduras']
    #     if number[:6] == '810852' or number[:5] == '10852' or number[:3] == '852':
    #         return [6.56, 'Gonk-Kong']
    #     if number[:6] == '810964' or number[:5] == '10964' or number[:3] == '964':
    #         return [6.56, 'Irak']
    #     if number[:6] == '810972' or number[:5] == '10972' or number[:3] == '972':
    #         return [6.56, 'Izrail']
    #     if number[:6] == '810962' or number[:5] == '10962' or number[:3] == '962':
    #         return [6.56, 'Iordaniya']
    #     if number[:6] == '810965' or number[:5] == '10965' or number[:3] == '965':
    #         return [6.56, 'Kuweit']
    #     if number[:6] == '810856' or number[:5] == '10856' or number[:3] == '856':
    #         return [6.56, 'Laos']
    #     if number[:6] == '810961' or number[:5] == '10961' or number[:3] == '961':
    #         return [6.56, 'Liwan']
    #     if number[:6] == '810853' or number[:5] == '10853' or number[:3] == '853':
    #         return [6.56, 'Makao (Aomyn)']
    #     if number[:6] == '810976' or number[:5] == '10976' or number[:3] == '976':
    #         return [6.56, 'Mongoliya']
    #     if number[:6] == '810977' or number[:5] == '10977' or number[:3] == '977':
    #         return [6.56, 'Nepal']
    #     if number[:6] == '810599' or number[:5] == '10599' or number[:3] == '599':
    #         return [6.56, 'Niderlandskie Antilly']
    #     if number[:6] == '810505' or number[:5] == '10505' or number[:3] == '505':
    #         return [6.56, 'Nikaragua']
    #     if number[:6] == '810850' or number[:5] == '10850' or number[:3] == '850':
    #         return [6.56, 'Sewernaya Koreya']
    #     if number[:6] == '810967' or number[:5] == '10967' or number[:3] == '967':
    #         return [6.56, 'Sewernyy Yemen']
    #     if number[:6] == '810968' or number[:5] == '10968' or number[:3] == '968':
    #         return [6.56, 'Oman']
    #     if number[:6] == '810507' or number[:5] == '10507' or number[:3] == '507':
    #         return [6.56, 'Panama'] 
    #     if number[:6] == '810974' or number[:5] == '10974' or number[:3] == '974':
    #         return [6.56, 'Katar']
    #     if number[:6] == '810966' or number[:5] == '10966'or number[:3] == '966':
    #         return [6.56, 'Saudowskaya Arawiya']   
    #     if number[:6] == '810967' or number[:5] == '10967' or number[:3] == '967':
    #         return [6.56, 'Yujnyy Yemen']
    #     if number[:6] == '810963' or number[:5] == '10963' or number[:3] == '963':
    #         return [6.56, 'Siriya']
    #     if number[:6] == '810886' or number[:5] == '10886' or number[:3] == '886':
    #         return [6.56, 'Taiwan']
    #     if number[:6] == '810971' or number[:5] == '10971' or number[:3] == '971':
    #         return [6.56, 'O.A.E']
    #     if number[:4] == '8101' or number[:3] == '101' or (len(number) > 8 and number[:1] == '1' and number[1:2] != '0'):
    #         return [6.56, 'USA/CANADA']
        

    #     # 6.78 manat
    #     if number[:5] == '81054' or number[:4] == '1054' or number[:2] == '54':
    #         return [6.78, 'Argentina']
    #     if number[:5] == '81055' or number[:4] == '1055' or number[:2] == '55':
    #         return [6.78, 'Braziliya']
    #     if number[:5] == '81056' or number[:4] == '1056' or number[:2] == '56':
    #         return [6.78, 'Chili']
    #     if number[:5] == '81057' or number[:4] == '1057' or number[:2] == '57':
    #         return [6.78, 'Kolumbiya']
    #     if number[:5] == '81051' or number[:4] == '1051' or number[:2] == '51':
    #         return [6.78, 'Peru']
    #     if number[:5] == '81058' or number[:4] == '1058' or number[:2] == '58':
    #         return [6.78, 'Wenesuella']
    #     if number[:6] == '810591' or number[:5] == '10591' or number[:3] == '591':
    #         return [6.78, 'Boliwiya']
    #     if number[:6] == '810593' or number[:5] == '10593' or number[:3] == '593':
    #         return [6.78, 'Ekwador']
    #     if number[:6] == '810298' or number[:5] == '10298' or number[:3] == '298':
    #         return [6.78, 'Farerskie Ostrowa']
    #     if number[:6] == '810594' or number[:5] == '10594' or number[:3] == '594':
    #         return [6.78, 'Fransuskatya Gwiana']
    #     if number[:6] == '810592' or number[:5] == '10592' or number[:3] == '592':
    #         return [6.78, 'Gayana']
    #     if number[:6] == '810596' or number[:5] == '10596' or number[:3] == '596':
    #         return [6.78, 'Martitnka']
    #     if number[:6] == '810597' or number[:5] == '10597' or number[:3] == '597':
    #         return [6.78, 'Surinam']
    #     if number[:6] == '810598' or number[:5] == '10598' or number[:3] == '598':
    #         return [6.78, 'Urugway']

    #     # 7.27 manat
    #     if number[:5] == '81020' or number[:4] == '1020' or number[:2] == '20':
    #         return [7.27, 'Egipet']
    #     if number[:5] == '81027' or number[:4] == '1027' or number[:2] == '27':
    #         return [7.27, 'UAR']
    #     if number[:6] == '810213' or number[:5] == '10213' or number[:3] == '213':
    #         return [7.27, 'Aljir']
    #     if number[:6] == '810244' or number[:5] == '10244' or number[:3] == '244':
    #         return [7.27, 'Angola']
    #     if number[:6] == '810229' or number[:5] == '10229' or number[:3] == '229':
    #         return [7.27, 'Benin']
    #     if number[:6] == '810267' or number[:5] == '10267' or number[:3] == '267':
    #         return [7.27, 'Botswana']
    #     if number[:6] == '810226' or number[:5] == '10226' or number[:3] == '226':
    #         return [7.27, 'Burkina Faso']
    #     if number[:6] == '810257' or number[:5] == '10257' or number[:3] == '257':
    #         return [7.27, 'Burundi']
    #     if number[:6] == '810237' or number[:5] == '10237' or number[:3] == '237':
    #         return [7.27, 'Kamerun']
    #     if number[:6] == '810238' or number[:5] == '10238' or number[:3] == '238':
    #         return [7.27, 'Kape Werde']
    #     if number[:6] == '810236' or number[:5] == '10236' or number[:3] == '236':
    #         return [7.27, 'SAR']
    #     if number[:6] == '810235' or number[:5] == '10235' or number[:3] == '235':
    #         return [7.27, 'Chad']
    #     if number[:6] == '810242' or number[:5] == '10242' or number[:3] == '242':
    #         return [7.27, 'Kongo']
    #     if number[:6] == '810253' or number[:5] == '10253' or number[:3] == '253':
    #         return [7.27, 'Jibuti']
    #     if number[:6] == '810240' or number[:5] == '10240' or number[:3] == '240':
    #         return [7.27, 'Ekwatorialnaya gwineya']
    #     if number[:6] == '810251' or number[:5] == '10251' or number[:3] == '251':
    #         return [7.27, 'Efiopiya']
    #     if number[:6] == '810241' or number[:5] == '10241' or number[:3] == '241':
    #         return [7.27, 'Gabon']
    #     if number[:6] == '810220' or number[:5] == '10220' or number[:3] == '220':
    #         return [7.27, 'Gambiya']
    #     if number[:6] == '810233' or number[:5] == '10233' or number[:3] == '233':
    #         return [7.27, 'Gana']
    #     if number[:6] == '810224' or number[:5] == '10224' or number[:3] == '224':
    #         return [7.27, 'Gwineya']
    #     if number[:6] == '810245' or number[:5] == '10245' or number[:3] == '245':
    #         return [7.27, 'Gwineya Bissau']
    #     if number[:6] == '810254' or number[:5] == '10254' or number[:3] == '254':
    #         return [7.27, 'Keniya']
    #     if number[:6] == '810231' or number[:5] == '10231' or number[:3] == '231':
    #         return [7.27, 'Liberiya']
    #     if number[:6] == '810218' or number[:5] == '10218' or number[:3] == '218':
    #         return [7.27, 'Liviya']
    #     if number[:6] == '810261' or number[:5] == '10261' or number[:3] == '261':
    #         return [7.27, 'Madagaskar']
    #     if number[:6] == '810265' or number[:5] == '10265' or number[:3] == '265':
    #         return [7.27, 'Malawi']
    #     if number[:6] == '810223' or number[:5] == '10223' or number[:3] == '223':
    #         return [7.27, 'Mali']
    #     if number[:6] == '810222' or number[:5] == '10222' or number[:3] == '222':
    #         return [7.27, 'Mawritaniya']
    #     if number[:6] == '810230' or number[:5] == '10230' or number[:3] == '230':
    #         return [7.27, 'Mawrikiy']
    #     if number[:6] == '810212' or number[:5] == '10212' or number[:3] == '212':
    #         return [7.27, 'Moroko']
    #     if number[:6] == '810258' or number[:5] == '10258' or number[:3] == '258':
    #         return [7.27, 'Mozambik']
    #     if number[:6] == '810264' or number[:5] == '10264' or number[:3] == '264':
    #         return [7.27, 'Namibiya']
    #     if number[:6] == '810227' or number[:5] == '10227' or number[:3] == '227':
    #         return [7.27, 'Niger']
    #     if number[:6] == '810234' or number[:5] == '10234' or number[:3] == '234':
    #         return [7.27, 'Nigeriya']
    #     if number[:6] == '810262' or number[:5] == '10262' or number[:3] == '262':
    #         return [7.27, 'Reonyon']
    #     if number[:6] == '810250' or number[:5] == '10250' or number[:3] == '250':
    #         return [7.27, 'Respublika Ruanda']
    #     if number[:6] == '810221' or number[:5] == '10221' or number[:3] == '221':
    #         return [7.27, 'Senegal']
    #     if number[:6] == '810248' or number[:5] == '10248' or number[:3] == '248':
    #         return [7.27, 'Seyshelskie ostrowa']
    #     if number[:6] == '810232' or number[:5] == '10232' or number[:3] == '232':
    #         return [7.27, 'Syerra Leonne']
    #     if number[:6] == '810252' or number[:5] == '10252' or number[:3] == '252':
    #         return [7.27, 'Somali']
    #     if number[:6] == '810249' or number[:5] == '10249' or number[:3] == '249':
    #         return [7.27, 'Sudan']
    #     if number[:6] == '810255' or number[:5] == '10255' or number[:3] == '255':
    #         return [7.27, 'Tanzaniya']
    #     if number[:6] == '810228' or number[:5] == '10228' or number[:3] == '228':
    #         return [7.27, 'Respublika Togoleze']
    #     if number[:6] == '810216' or number[:5] == '10216' or number[:3] == '216':
    #         return [7.27, 'Tunis']
    #     if number[:6] == '810256' or number[:5] == '10256' or number[:3] == '256':
    #         return [7.27, 'Uganda']
    #     if number[:6] == '810243' or number[:5] == '10243' or number[:3] == '243':
    #         return [7.27, 'Zair']
    #     if number[:6] == '810260' or number[:5] == '10260' or number[:3] == '260':
    #         return [7.27, 'Zambiya']
    #     if number[:6] == '810263' or number[:5] == '10263' or number[:3] == '263':
    #         return [7.27, 'Zimbabwe']
        
    #     # show errors
    #     # if number == '8888888':
    #     # 	return [number, '8888888']
        
    #     # if number == '111':
    #     # 	return [number, '111']
        
    #     # if number == '112':
    #     # 	return [number, '112']
        
    #     # if number == '119':
    #     # 	return [number, '119']
        
    #     # if number == '01':
    #     # 	return [number, '01']
        
    #     # if number == '02':
    #     # 	return [number, '02']

    #     # if number == '03':
    #     # 	return [number, '03']
        
    #     # if number == '071':
    #     # 	return [number, '071']
        
    #     # if number == '05':
    #     # 	return [number, '05']
        
    #     # if number == '9938001211':
    #     # 	return [number, '9938001211']
        
    #     # if number == '04':
    #     # 	return [number, '04']
        
    #     # if number == '003229938001211':
    #     # 	return [number, '003229938001211']
        
    #     # if number == '0032213000':
    #     # 	return [number, '0032213000']
        
    #     # if number == '13000':
    #     # 	return [number, '13000']

        
    #     # if number == '00322071':
    #     # 	return [number, '00322071']
        
    #     # if number == '383217':
    #     # 	return [number, '383217']
        
    #     # if number == '993322071':
    #     # 	return [number, '993322071']
        
    #     # if number == '383272':
    #     # 	return [number, '383272']
        
    #     # if number == '384129':
    #     # 	return [number, '384129']
        
    #     # if number == '383988':
    #     # 	return [number, '383988']
        
    #     # if number == '00488803':
    #     # 	return [number, '00488803']
        
    #     # if len(number) == 6:
    #     # 	return [number, '6']
        
    #     # if number == '003229938001211':
    #     # 	return [number, '003229938001211']
        
        
        
        
        
        
    #     return [number, False]



    # def zte_nach(request):
    #     context = {}
    #     context['matbIndex'] = True
    #     context['zte_nach'] = True


    #     if request.method == 'POST':
    #         nachislit = request.POST.get('nachislit')
    
    #     # Свернуть
    #         # Dashoguz
    #         hozUsersQuery = UserTable.objects.filter(etrap='Dashoguz', hb__name='H').values('number', 'etrap')
    #         hozUsers = [f"{user['number']}{user['etrap']}" for user in hozUsersQuery]
    #         budUsersQuery = UserTable.objects.filter(etrap='Dashoguz', hb__name='B').values('number', 'etrap')
    #         budUsers = [f"{user['number']}{user['etrap']}" for user in budUsersQuery]
    #         unknownEdaraQuery = UserTable.objects.filter(etrap='Dashoguz', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsers = [f"{user['number']}{user['etrap']}" for user in unknownEdaraQuery]
    #         emptyIlatQuery = UserTable.objects.filter(etrap='Dashoguz', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsers = [f"{user['number']}{user['etrap']}" for user in emptyIlatQuery]

    #         # Boldumsaz
    #         hozUsersListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', hb__name='H').values('number', 'etrap')
    #         hozUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in hozUsersListBoldumsaz]
    #         budUsersListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', hb__name='B').values('number', 'etrap')
    #         budUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in budUsersListBoldumsaz]
    #         UnknownEdaraListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListBoldumsaz]
    #         emptyIlatListBoldumsaz = UserTable.objects.filter(etrap='Boldumsaz', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersBoldumsaz = [f"{user['number']}{user['etrap']}" for user in emptyIlatListBoldumsaz]

    #         # Turkmenbashy
    #         hozUsersListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', hb__name='H').values('number', 'etrap')
    #         hozUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in hozUsersListTurkmenbashy]
    #         budUsersListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', hb__name='B').values('number', 'etrap')
    #         budUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in budUsersListTurkmenbashy]
    #         UnknownEdaraListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListTurkmenbashy]
    #         emptyIlatListTurkmenbashy = UserTable.objects.filter(etrap='Turkmenbashy', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersTurkmenbashy = [f"{user['number']}{user['etrap']}" for user in emptyIlatListTurkmenbashy]
            
    #         # Gorogly
    #         hozUsersListGorogly = UserTable.objects.filter(etrap='Gorogly', hb__name='H').values('number', 'etrap')
    #         hozUsersGorogly = [f"{user['number']}{user['etrap']}" for user in hozUsersListGorogly]
    #         budUsersListGorogly = UserTable.objects.filter(etrap='Gorogly', hb__name='B').values('number', 'etrap')
    #         budUsersGorogly = [f"{user['number']}{user['etrap']}" for user in budUsersListGorogly]
    #         UnknownEdaraListGorogly = UserTable.objects.filter(etrap='Gorogly', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersGorogly = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListGorogly]
    #         emptyIlatListGorogly = UserTable.objects.filter(etrap='Gorogly', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersGorogly = [f"{user['number']}{user['etrap']}" for user in emptyIlatListGorogly]


    #         # Koneurgench
    #         hozUsersListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', hb__name='H').values('number', 'etrap')
    #         hozUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in hozUsersListKoneurgench]
    #         budUsersListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', hb__name='B').values('number', 'etrap')
    #         budUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in budUsersListKoneurgench]
    #         UnknownEdaraListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListKoneurgench]
    #         emptyIlatListKoneurgench = UserTable.objects.filter(etrap='Koneurgench', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersKoneurgench = [f"{user['number']}{user['etrap']}" for user in emptyIlatListKoneurgench]

    #         # Ruhubelent
    #         hozUsersListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', hb__name='H').values('number', 'etrap')
    #         hozUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in hozUsersListRuhubelent]
    #         budUsersListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', hb__name='B').values('number', 'etrap')
    #         budUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in budUsersListRuhubelent]
    #         UnknownEdaraListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListRuhubelent]
    #         emptyIlatListRuhubelent = UserTable.objects.filter(etrap='Ruhubelent', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersRuhubelent = [f"{user['number']}{user['etrap']}" for user in emptyIlatListRuhubelent]

    #         # Akdepe
    #         hozUsersListAkdepe = UserTable.objects.filter(etrap='Akdepe', hb__name='H').values('number', 'etrap')
    #         hozUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in hozUsersListAkdepe]
    #         budUsersListAkdepe = UserTable.objects.filter(etrap='Akdepe', hb__name='B').values('number', 'etrap')
    #         budUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in budUsersListAkdepe]
    #         UnknownEdaraListAkdepe = UserTable.objects.filter(etrap='Akdepe', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListAkdepe]
    #         emptyIlatListAkdepe = UserTable.objects.filter(etrap='Akdepe', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersAkdepe = [f"{user['number']}{user['etrap']}" for user in emptyIlatListAkdepe]


    #         # Nyyazow
    #         hozUsersListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', hb__name='H').values('number', 'etrap')
    #         hozUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in hozUsersListNyyazow]
    #         budUsersListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', hb__name='B').values('number', 'etrap')
    #         budUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in budUsersListNyyazow]
    #         UnknownEdaraListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', is_enterprises=True, hb=None).values('number', 'etrap')
    #         UnknowEdaraUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in UnknownEdaraListNyyazow]
    #         emptyIlatListNyyazow = UserTable.objects.filter(etrap='S.A.Nyyazow', name='', surname='').values('number', 'etrap')
    #         emptyNumberUsersNyyazow = [f"{user['number']}{user['etrap']}" for user in emptyIlatListNyyazow]
    #     # Свернуть
        
        
    #         # Путь к dbf файлам 
    #         directory = "C:\\Users\\Home\\Desktop\\zte_files"
        



    #         files_names = os.listdir(directory)
    #         for index in range(len(files_names)):
    #             files_names[index] = f"{files_names[index][:-4]}"

    #         file_name_error = []


    #         # Сначало проверим dbfNameList начислены ли уже такие файлы или нет
    #         error_name_list = []
    #         for myFile in files_names: 
    #             name_in_DB = dbfNameList.objects.filter(name=myFile).first()

    #             if re.search("[a-zA-Z]", myFile):
    #                 # print("Есть хотя бы одна буква.")
    #                 file_name_error.append(myFile)
    #             else:
    #                 pass
    #                 # print("Букв нет.")

    #             if name_in_DB:
    #                 error_name_list.append(myFile)

    #         if file_name_error:
    #             messages.error(request, f'ошибка в имени файла {file_name_error}')
    #             return render(request, 'telekom/dbfs_nachs/zte_nach.html', context)

    #         if error_name_list:
    #             messages.error(request, f'файлы {error_name_list} уже начислены')
    #             return render(request, 'telekom/dbfs_nachs/zte_nach.html', context)
    #         else:
    #             if not nachislit:
    #                 messages.success(request, f"файлы {files_names} прошли проверку успешно")
        
            
            
    #         test_zte_count = 0
    #         have_success_messages = False
    #         count = 0
    #         for myFile in files_names:
    #             bulk_create_nonLocal = []
    #             bulk_create_Local = []
    #             name = myFile
    #             file_path = f"{directory}/{myFile}.txt"

    #             count += 1
    #             print(f"{count} из {len(files_names)} == {len(myFile)}")
            
    #             txt = [i.strip('\n').split(';') for i in open(file_path)]

    #             data = [[a, *b] for a, *b in txt] 

                
    #             for call in data:
    #                 test_zte_count += 1

    #                 SUB_A = getNumberLocations(call[0])
    #                 SUB_B = getNumberLocations(call[1])

    #                 date_object = call[2]
    #                 DATE = datetime.datetime.strptime(date_object, '%d.%m.%Y').date()
    #                 START = call[3]
    #                 FIN = call[4]
                    
    #                 time_format = "%H:%M:%S"
    #                 time1 = datetime.datetime.strptime(START, time_format)
    #                 time2 = datetime.datetime.strptime(FIN, time_format)
    #                 DUR = time2 - time1
    #                 DUR_total_seconds = DUR.total_seconds()
    #                 if DUR_total_seconds / 60 <= 1:
    #                     MT = 1
    #                 else:
    #                     MT = int(math.ceil(DUR_total_seconds / 60))



    #                 # Проверка диапазонов
    #                 if SUB_A[1] == 'Boldumsaz' and SUB_A[0][0] == '3':

    #                     if f"{SUB_A[0]}Boldumsaz" in budUsersBoldumsaz and f"{SUB_A[0]}Boldumsaz" not in emptyNumberUsersBoldumsaz:
    #                         edaraChar = 'B'
    #                     elif f"{SUB_A[0]}Boldumsaz" in hozUsersBoldumsaz and f"{SUB_A[0]}Boldumsaz" not in emptyNumberUsersBoldumsaz:
    #                         edaraChar = 'H'
    #                     elif f"{SUB_A[0]}Boldumsaz" in emptyNumberUsersBoldumsaz:
    #                         edaraChar = 'E'
    #                     else:
    #                         edaraChar = 'I'



    #                     # local (без парога)
    #                     if SUB_B[1] == 'five' or SUB_B[1] == 'Boldumsaz':
    #                         # для Бюджетных локальные звонки не начисляются
    #                         if edaraChar == 'B':
    #                             continue
    #                         obj = LocalCall(
    #                             etrap='Boldumsaz',
    #                             SUB_A=SUB_A[0],
    #                             SUB_B=SUB_B[0],
    #                             DATE=DATE,
    #                             START=str(START),
    #                             FIN=str(FIN),
    #                             DUR=str(DUR),
    #                             MT=MT,
    #                             file_name=name,
    #                             edara=edaraChar
    #                         )
    #                         bulk_create_Local.append(obj)
    #                         continue
                        
    #                     # Порог
    #                     if DUR_total_seconds <= 4:
    #                         continue

    #                     # Turkmenistan
    #                     if (SUB_B[1] in turkmenistan or SUB_B[1] in etraps) and SUB_B[1] != 'Boldumsaz' and SUB_B[1] != 'five':
    #                         if edaraChar in ['H', 'B']:
    #                             price_for_1_min = 0.14
    #                         else:
    #                             price_for_1_min = 0.08
    #                         obj = NonLocalCall(
    #                             SUB_A_etrap='Boldumsaz',
    #                             SUB_A=SUB_A[0],
    #                             SUB_B_locations=SUB_B[1],
    #                             SUB_B=call[1],
    #                             type='intercity',
    #                             price=price_for_1_min,
    #                             DATE=DATE,
    #                             START=str(START),
    #                             FIN=str(FIN),
    #                             DUR=str(DUR),
    #                             MT=MT,
    #                             total_price=int(MT) * price_for_1_min,
    #                             file_name=name,
    #                             edara=edaraChar
    #                         )
    #                         bulk_create_nonLocal.append(obj)
    #                         continue

    #                     # Международные разговоры
    #                     if SUB_B[1] in international:
    #                         obj = NonLocalCall(
    #                             SUB_A_etrap='Boldumsaz',
    #                             SUB_A=SUB_A[0],
    #                             SUB_B_locations=SUB_B[1],
    #                             SUB_B=call[1],
    #                             type='international',
    #                             price=SUB_B[0],
    #                             DATE=DATE,
    #                             START=str(START),
    #                             FIN=str(FIN),
    #                             DUR=str(DUR),
    #                             MT=MT,
    #                             total_price=int(MT) * SUB_B[0],
    #                             file_name=name,
    #                             edara=edaraChar
    #                         )
    #                         bulk_create_nonLocal.append(obj)
    #                         continue
    #             if nachislit:
    #                 if bulk_create_Local:
    #                     LocalCall.objects.bulk_create(bulk_create_Local)
    #                 if bulk_create_nonLocal:
    #                     NonLocalCall.objects.bulk_create(bulk_create_nonLocal)
    #                 if bulk_create_Local or bulk_create_nonLocal:
    #                     have_success_messages = True
    #                     dbfNameList.objects.create(name=name)
                
    #                 # Удаление дубликатов deepai
    #                 calls_obj = NonLocalCall.objects.filter(file_name=name)
    #                 unique_records = {}
    #                 duplicates = []
    #                 for record in calls_obj:
    #                     # Создаем уникальный идентификатор для дублирующей записи
    #                     identifier = (record.SUB_A_etrap, record.SUB_A, record.SUB_B_locations, record.SUB_B, record.DATE, record.START, record.FIN)

    #                     if identifier in unique_records:
    #                         # Если идентификатор уже встречался, добавляем ID записи в дубликаты
    #                         duplicates.append(record.id)
    #                     else:
    #                         # Сохраняем уникальную запись
    #                         unique_records[identifier] = record.id  # Или просто можете сохранить сам объект, если это нужно
    #                 # Удаляем дубликаты
    #                 if duplicates:
    #                     NonLocalCall.objects.filter(id__in=duplicates).delete()
    #                     print(f"Удалено дубликатов: {len(duplicates)}", name)
    #                 else:
    #                     print("Дубликатов не найдено.", name)
    #         if have_success_messages:
    #             messages.success(request, f"файлы {files_names} успешно начислены")

    #         print('test_zte_count', test_zte_count)



        

    #     return render(request, 'telekom/dbfs_nachs/zte_nach.html', context)
# Код работает идеально но без transaction