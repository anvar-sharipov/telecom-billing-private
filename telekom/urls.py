from django.urls import path














# login, register
from .views2.Login.UserLogin import UserLogin, userLogout
from .views2.HomePage.HomePage import HomePage
from .views2.Login.register import registerPage

# MATB
from .views2.MATB.index import matbIndex
from telekom.views2.MATB.staffActionList import staffActionList
# DBF
from telekom.views2.MATB.DBF.slrNachisleniyaIndex import slrNachisleniyaIndex
from telekom.views2.MATB.DBF.kodNachisleniyaIndex import kodNachisleniyaIndex
# DBFSearch
from telekom.views2.MATB.DBF.DBFSearch.localCalls import localCalls
from telekom.views2.MATB.DBF.DBFSearch.nonLocalCalls import nonLocalCalls
# DBF txt
from telekom.views2.MATB.DBF.DBFtxt.localSuccess import localSuccess
from telekom.views2.MATB.DBF.DBFtxt.localError import localError
from telekom.views2.MATB.DBF.DBFtxt.globalSuccess import globalSuccess
from telekom.views2.MATB.DBF.DBFtxt.globalError import globalError
from telekom.views2.MATB.DBF.DBFtxt.kodSuccesTxt import kodSuccesTxt
from telekom.views2.MATB.DBF.DBFtxt.kodErrorTxt import kodErrorTxt
from telekom.views2.MATB.DBF.DBFtxt.slrSuccesTxt import slrSuccessTxt
from telekom.views2.MATB.DBF.DBFtxt.slrErrorTxt import slrErrorTxt
# DBF начисления
from telekom.views2.MATB.DBF.DBFNachisleniyaBtn.slrNachisleniyaBtn import slrNachisleniyaBtn
from telekom.views2.MATB.DBF.DBFNachisleniyaBtn.kodNachisleniyaBtn import kodNachisleniyaBtn
from telekom.views2.MATB.DBF.kodSlrFileNachisleniya import kodSlrFileNachisleniya
from telekom.views2.MATB.import_calls_files import import_calls_files

# xlsxl начисления
from telekom.views2.MATB.xlsx.XlsxNachisleniya.nachisleniyaInternetPlateji import nachisleniyaInternetPlateji
from telekom.views2.MATB.xlsx.XlsxNachisleniya.internetNachisleniyaBtn import internetNachisleniyaBtn
from telekom.views2.MATB.alemNachisleniya import alemNachisleniya
from telekom.views2.MATB.pays_from_billing.add_month_pays_from_billing_to_my_programm import add_month_pays_from_billing_to_my_programm
from telekom.views2.MATB.pays_from_billing.nach_pays_from_billing import nach_pays_from_billing
# xlsx search
from telekom.views2.MATB.xlsx.xlsxSearch.internetPlatejiSearch import internetPlatejiSearch
from telekom.views2.MATB.xlsx.xlsxSearch.internetNachisleniyaSearch import internetNachisleniyaSearch
from telekom.views2.MATB.xlsx.xlsxSearch.alemNachisleniyaSearch import alemNachisleniyaSearch
from telekom.views2.MATB.showZakaz import showZakaz
# xlsx Добавить в БД
from telekom.views2.MATB.xlsx.importXlsx.importXlsx import importXlsx
# xlsx txt plateji
from telekom.views2.MATB.xlsx.xlsxTxt.internetPlatejiSuccessTxt import internetPlatejiSuccessTxt
from telekom.views2.MATB.xlsx.xlsxTxt.internetPlatejiErrorTxt import internetPlatejiErrorTxt
from telekom.views2.MATB.xlsx.xlsxTxt.internetPlatejiTotalTxt import internetPlatejiTotalTxt
# xlsx txt nachisleniya internet
from telekom.views2.MATB.xlsx.xlsxTxt.internetNachisleniyaSuccessTxt import internetNachisleniyaSuccessTxt
from telekom.views2.MATB.xlsx.xlsxTxt.internetNachisleniyaErrorTxt import internetNachisleniyaErrorTxt
from telekom.views2.MATB.xlsx.xlsxTxt.internetNachisleniyaTotalTxt import internetNachisleniyaTotalTxt
# xlsx txt nachisleniya alem
from telekom.views2.MATB.xlsx.xlsxTxt.alemNachisleniyaSuccessTxt import alemNachisleniyaSuccessTxt
from telekom.views2.MATB.xlsx.xlsxTxt.alemNachisleniyaErrorTxt import alemNachisleniyaErrorTxt

# Kabel TV начисления
from telekom.views2.MATB.kabelTvNachisleniya import kabelTvNachisleniya
# Kabel TV начисления txt
from telekom.views2.MATB.txt.kabelTvNachisleniyaTxt import kabelTvNachisleniyaTxt
# Кабель TV info
from telekom.views2.MATB.kabelTvInfo import kabelTvInfo
# Кабель TV add new user
from telekom.views2.MATB.kabelTvAddUser import kabelTvAddUser
# dop_uslugi начисления
from telekom.views2.MATB.dop_uslugiNachisleniya import dop_uslugiNachisleniya
# Заказ начисления
from telekom.views2.MATB.zakazNachisleniya import zakazNachisleniya
# Заказ Error txt
from telekom.views2.MATB.txt.zakazNachisleniyaErrorTxt import zakazNachisleniyaErrorTxt
from telekom.views2.MATB.oldLoginDogowors import oldLoginDogowors
# dop_uslugi txt
from telekom.views2.MATB.txt.dop_uslugiNachisleniyaTxt import dop_uslugiNachisleniyaTxt
# Абонплата начисления
from telekom.views2.MATB.abonplataNachisleniya import abonplataNachisleniya
# Абонплата начисления txt
from telekom.views2.MATB.txt.abonplataNachisleniyaTxt import abonplataNachisleniyaTxt
# reestr
from telekom.views2.MATB.reestr.reestr import reestr
from telekom.views2.MATB.reestr.P_txt import P_txt
from telekom.views2.MATB.reestr.R_txt import R_txt
from telekom.views2.MATB.reestr.N_txt import N_txt
# Отчет за месяц
from telekom.views2.MATB.monthOtchot import monthOtchot
from telekom.views2.MATB.monthOtchotNew import monthOtchotNew
from telekom.views2.MATB.monthOtchotForAshyr import monthOtchotForAshyr
# Перекидка
from telekom.views2.MATB.perekidka import perekidka
# Arhiw
from telekom.views2.MATB.Arhiw.showArhiw import showArhiw
from telekom.views2.MATB.totalSnyatie import totalSnyatie

from telekom.views2.MATB.otchyot.trafik import trafik
from telekom.views2.MATB.otchyot.trafik_po_DOP import trafik_po_DOP
from telekom.views2.MATB.otchyot.prochie_otchoty import prochie_otchoty
from telekom.views2.MATB.otchyot.balances import balances
# KabelNew
from telekom.views2.MATB.KabelNew.kabelUserList import kabelUserList
from telekom.views2.MATB.KabelNew.kabelNach import kabelNach






# Service
from .views2.Service.setService import setService
from telekom.views2.Service.internetConnect import internetConnect
from telekom.views2.Service.serviceConnect import serviceConnect
from telekom.views2.Service.alemConnect import alemConnect

# Kassa
from .views2.Kassa.KassaIndex import kassaIndex
from .views2.Kassa.receipts import receipts
from telekom.views2.Kassa.kassaReestr import kassaReestr
from telekom.views2.Kassa.kassaAccount import kassaAccount
from telekom.views2.Kassa.addPlatejiForKassirs import addPlatejiForKassirs
from telekom.views2.Kassa.addPlatejiForKassirs2 import addPlatejiForKassirs2
from telekom.views2.Kassa.kassirs_billing_names import kassirs_billing_names
#  # Kassa Rezerw
# from telekom.views2.kassaRezerw.KassaIndex import kassaIndexRezerw
# from telekom.views2.kassaRezerw.kassaReestr import kassaReestrRezerw
# from telekom.views2.kassaRezerw.receipts import receiptsRezerw

# Internet Billing
from telekom.views2.InternetBilling.internetBolum import internetBolum
from telekom.views2.InternetBilling.interpayPerekidka import interpayPerekidka

# SHB bolum
from telekom.views2.SHB.SHBIndex import SHBBolum

# 071
from telekom.views2.operator071.zakazCalls import zakazCalls
from telekom.views2.operator071.txt.zakazTxt import zakazTxt


# Export DB
from telekom.views2.ExportDB.exportDB import exportDB
from telekom.views2.ExportDB.exportAbonplata import exportAbonplata
from telekom.views2.ExportDB.exportSlr import exportSlr
from telekom.views2.ExportDB.exportKod import exportKod
from telekom.views2.ExportDB.exportZakaz import exportZakaz
from telekom.views2.ExportDB.exportProchee import exportProchee
from telekom.views2.ExportDB.exportDop_uslugi import exportDop_uslugi
from telekom.views2.ExportDB.exportInternet import exportInternet
from telekom.views2.ExportDB.exportKabel import exportKabel
from telekom.views2.ExportDB.exportAlem import exportAlem

# exam
from telekom.views2.exam.exam_index import exam_index
from telekom.views2.exam.start_exam import start_exam
from telekom.views2.exam.exam_history import exam_history
from telekom.views2.exam.exam_history_all import exam_history_all


# dbfs_nachs
from telekom.views2.dbfs_nachs.dbf_a_nach import dbf_a_nach
from telekom.views2.dbfs_nachs.zte_nach import zte_nach

# NachislitWruchnuyu и все новое для MTB
from telekom.views2.MATB.NachislitWruchnuyu.nachislit_wruchnuyu import nachislit_wruchnuyu
from telekom.views2.MATB.NachislitWruchnuyu.nachislit_wruchnuyu_history import nachislit_wruchnuyu_history
from telekom.views2.MATB.NachislitWruchnuyu.perekidka_new import perekidka_new
from telekom.views2.MATB.NachislitWruchnuyu.perekidka_new_history import perekidka_new_history
from telekom.views2.MATB.NachislitWruchnuyu.snyatie_new import snyatie_new
from telekom.views2.MATB.NachislitWruchnuyu.snyatie_new_history import snyatie_new_history
from telekom.views2.MATB.NachislitWruchnuyu.check_pays import check_pays
from telekom.views2.MATB.NachislitWruchnuyu.baza_history import baza_history
from telekom.views2.MATB.NachislitWruchnuyu.perekidkaNachisleniya import perekidkaNachisleniya
from telekom.views2.MATB.NachislitWruchnuyu.pays_with_comment import pays_with_comment
from telekom.views2.MATB.NachislitWruchnuyu.pays_with_comment_history import pays_with_comment_history
from telekom.views2.MATB.NachislitWruchnuyu.change_nachislenie import change_nachislenie
from telekom.views2.MATB.NachislitWruchnuyu.internet_nachisleniya_new.import_internet_nach_new import import_internet_nach_new
from telekom.views2.MATB.NachislitWruchnuyu.internet_nachisleniya_new.internet_nachisleniya_new import internet_nachisleniya_new
from telekom.views2.MATB.NachislitWruchnuyu.check_dogowors import check_dogowors 
from telekom.views2.MATB.NachislitWruchnuyu.AlemNachisleniyaNew.alem_add import alem_add
from telekom.views2.MATB.NachislitWruchnuyu.AlemNachisleniyaNew.alem_nach import alem_nach
from telekom.views2.MATB.NachislitWruchnuyu.dbf_nach_history import dbf_nach_history
from telekom.views2.MATB.NachislitWruchnuyu.changeBalance import changeBalance
from telekom.views2.MATB.NachislitWruchnuyu.changeBalanceHistory import changeBalanceHistory

from telekom.views2.MATB.NachislitWruchnuyu.dbf_nach_history import dbf_nach_history
# Новые начисления
from telekom.views2.MATB.newNachisleniya.abonplata import newAbonplataNachisleniya

# my page
from telekom.views2.admin_pages.saldo_po_godam_save import saldo_po_godam_save
from telekom.views2.admin_pages.saldo_po_godam_save2 import saldo_po_godam_save2
from telekom.views2.admin_pages.add_nachisleniya_from_excel import add_nachisleniya_from_excel





urlpatterns = [
    # MATB
    path('', HomePage, name='HomePage'),
    path('user-login', UserLogin, name='user-login'),
    path('user-register', registerPage, name='user-register'),
    path('matb-index', matbIndex, name='matb-index'),
    path('user-logout', userLogout, name='user-logout'),
    path('staff-history-list', staffActionList, name='staff-history-list'),
    # DBFSearch
    path('local-calls', localCalls, name='local-calls'),
    path('none-local-calls', nonLocalCalls, name='none-local-calls'),
    # DBF Index
    path('slr-nachisleniya', slrNachisleniyaIndex, name='slr-nachisleniya'),
    path('kod-nachisleniya', kodNachisleniyaIndex, name='kod-nachisleniya'),
    # DBF txt
    path('local-success/<str:year>/<str:month>/', localSuccess, name='local-success'),
    path('local-error/<str:year>/<str:month>/', localError, name='local-error'),
    path('global-success/<str:year>/<str:month>/', globalSuccess, name='global-success'),
    path('global-error/<str:year>/<str:month>/', globalError, name='global-error'),
    path('kod-succes-txt', kodSuccesTxt, name='kod-succes-txt'),
    path('kod-error-txt', kodErrorTxt, name='kod-error-txt'),
    path('slr-succes-txt', slrSuccessTxt, name='slr-succes-txt'),
    path('slr-error-txt', slrErrorTxt, name='slr-error-txt'),
    # DBF начисления
    path('slr-nachisleniya-btn', slrNachisleniyaBtn, name='slr-nachisleniya-btn'),
    path('kod-nachisleniya-btn', kodNachisleniyaBtn, name='kod-nachisleniya-btn'),
    path('kod-slr-file-nachisleniya', kodSlrFileNachisleniya, name='kod-slr-file-nachisleniya'),
    path('import_calls_files', import_calls_files, name='import_calls_files'),
    
    # xlsxl начисления
    path('nachisleniya-internet-plateji', nachisleniyaInternetPlateji, name='nachisleniya-internet-plateji'),
    path('internet-nachisleniya-btn', internetNachisleniyaBtn, name='internet-nachisleniya-btn'),
    path('alem-nachisleniya', alemNachisleniya, name='alem-nachisleniya'),
    path('add_month_pays_from_billing_to_my_programm', add_month_pays_from_billing_to_my_programm, name='add_month_pays_from_billing_to_my_programm'),
    path('nach_pays_from_billing', nach_pays_from_billing, name='nach_pays_from_billing'),
    # xlsxl search
    path('internet-plateji-search', internetPlatejiSearch, name='internet-plateji-search'),
    path('internet-nachisleniya-search', internetNachisleniyaSearch, name='internet-nachisleniya-search'),
    path('alem-nachisleniya-search', alemNachisleniyaSearch, name='alem-nachisleniya-search'),
    path('zakaz-show', showZakaz, name='zakaz-show'),
    # xlsx Добавить в БД
    path('import-xlsx', importXlsx, name='import-xlsx'),
    # xlsx txt plateji
    path('internet-plateji-success-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', internetPlatejiSuccessTxt, name='internet-plateji-success-txt'),
    path('internet-plateji-error-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', internetPlatejiErrorTxt, name='internet-plateji-error-txt'),
    path('internet-plateji-total-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', internetPlatejiTotalTxt, name='internet-plateji-total-txt'),
    # xlsx txt nachisleniya internet
    path('internet-nachisleniya-success-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', internetNachisleniyaSuccessTxt, name='internet-nachisleniya-success-txt'),
    path('internet-nachisleniya-error-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', internetNachisleniyaErrorTxt, name='internet-nachisleniya-error-txt'),
    path('internet-cnachisleniya-total-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', internetNachisleniyaTotalTxt, name='internet-nachisleniya-total-txt'),
    # xlsx txt nachisleniya alem
    path('alem-nachisleniya-success-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', alemNachisleniyaSuccessTxt, name='alem-nachisleniya-success-txt'),
    path('alem-nachisleniya-error-txt/<str:year>/<str:month>/<str:etrap>/<str:off>/', alemNachisleniyaErrorTxt, name='alem-nachisleniya-error-txt'),

    # Kabel TV начисления
    path('kabel-tv-nachisleniya', kabelTvNachisleniya, name='kabel-tv-nachisleniya'),
    # Kabel TV начисления txt
    path('kabel-tv-txt-nachisleniya/<str:year>/<str:month>/<str:etrap>/', kabelTvNachisleniyaTxt, name='kabel-tv-txt-nachisleniya'),
    # Кабель TV info
    path('kabel-tv-info', kabelTvInfo, name='kabel-tv-info'),
    # Кабель TV add new user
    path('kabel-tv-add-user', kabelTvAddUser, name='kabel-tv-add-user'),
    # Заказ начисления
    path('zakaz-nachisleniya', zakazNachisleniya, name='zakaz-nachisleniya'),
    # Заказ Error txt
    path('zakaz-error-txt-nachisleniya/<str:year>/<str:month>/<str:etrap>/', zakazNachisleniyaErrorTxt, name='zakaz-error-txt-nachisleniya'),
    path('oldLoginDogowors', oldLoginDogowors, name='oldLoginDogowors'),
    

    
    # dop_uslugi начисления
    path('dop-uslugi-nachisleniya', dop_uslugiNachisleniya, name='dop-uslugi-nachisleniya'),
    # txt dop_uslugiNachisleniyaTxt
    path('dop-uslugi-txt-nachisleniya/<str:year>/<str:month>/<str:etrap>/', dop_uslugiNachisleniyaTxt, name='dop-uslugi-txt-nachisleniya'),
    # Абонплата начисления
    path('abonplata-nachisleniya', abonplataNachisleniya, name='abonplata-nachisleniya'),
    # Абонплата начисления txt
    path('abonplata-txt-nachisleniya/<str:etrap>/', abonplataNachisleniyaTxt, name='abonplata-txt-nachisleniya'),
    # reestr
    path('reestr-main', reestr, name='reestr-main'),
    path('p-txt-reestr/<str:year>/<str:month>/<str:etrap>/', P_txt, name='p-txt-reestr'),
    path('r-txt-reestr/<str:year>/<str:month>/<str:etrap>/', R_txt, name='r-txt-reestr'),
    path('n-txt-reestr/<str:year>/<str:month>/<str:etrap>/', N_txt, name='n-txt-reestr'),
    # Отчет за месяц
    path('month-otchot', monthOtchot, name='month-otchot'),
    path('month-new-otchot', monthOtchotNew, name='month-new-otchot'),
    path('month-ashyr-otchot', monthOtchotForAshyr, name='month-ashyr-otchot'),
    # Перекидка
    path('perekidka', perekidka, name='perekidka'),
    # Arhiw
    path('abonent-arhiw', showArhiw, name='abonent-arhiw'),
    path('total-snyatie', totalSnyatie, name='total-snyatie'),
    path('trafik', trafik, name='trafik'),
    path('trafik-dop', trafik_po_DOP, name='trafik-dop'),
    path('prochie-otchoty', prochie_otchoty, name='prochie-otchoty'),
    path('balances', balances, name='balances'),





    # Service
    path('set-service', setService, name='set-service'),
    path('internet-connect', internetConnect, name='internet-connect'),
    path('service-connect', serviceConnect, name='service-connect'),
    path('alem-connect', alemConnect, name='alem-connect'),

    # Kassa
    path('kassa-index', kassaIndex, name='kassa-index'),
    path('receipts', receipts, name='receipts'),
    path('kassa-reestr', kassaReestr, name='kassa-reestr'),
    path('account-page', kassaAccount, name='account-page'),
    path('addPlatejiForKassirs', addPlatejiForKassirs, name='addPlatejiForKassirs'),
    path('addPlatejiForKassirs2', addPlatejiForKassirs2, name='addPlatejiForKassirs2'),
    path('kassirs_billing_names', kassirs_billing_names, name='kassirs_billing_names'),

    # Kassa Rezerw
    # path('kassa-rezerw-index', kassaIndexRezerw, name='kassa-rezerw-index'),
    # path('receipts-rezerw', receiptsRezerw, name='receipts-rezerw'),
    # path('kassa-rezerw-reestr', kassaReestrRezerw, name='kassa-rezerw-reestr'),

    # Internet
    path('internet-bolum', internetBolum, name='internet-bolum'),
    path('interpay-perekidka', interpayPerekidka, name='interpay-perekidka'),

    # SHB
    path('shb-bolum', SHBBolum, name='shb-bolum'),

    # 071
    path('zakaz-calls', zakazCalls, name='zakaz-calls'),
    path('zakaz-txt-calls/<str:etrap>/<str:start>/<str:end>', zakazTxt, name='zakaz-txt-calls'),


    # Export DB
    path('export-db', exportDB, name='export-db'),
    path('export-abonplata/<str:etrap>', exportAbonplata, name='export-abonplata'),
    path('export-slr/<str:etrap>', exportSlr, name='export-slr'),
    path('export-kod/<str:etrap>', exportKod, name='export-kod'),
    path('export-zakaz/<str:etrap>', exportZakaz, name='export-zakaz'),
    path('export-prochee/<str:etrap>', exportProchee, name='export-prochee'),
    path('export-dop_uslugi/<str:etrap>', exportDop_uslugi, name='export-dop_uslugi'),
    path('export-internet/<str:etrap>', exportInternet, name='export-internet'),
    path('export-kabel/<str:etrap>', exportKabel, name='export-kabel'),
    path('export-alem/<str:etrap>', exportAlem, name='export-alem'),

    # exam
    path('exam', exam_index, name='exam-index'),
    path('start-exam', start_exam, name='start-exam'),
    path('exam-history', exam_history, name='exam-history'),
    path('exam-history-all', exam_history_all, name='exam-history-all'),

    # KabelNew
    path('kabel-new-user-list', kabelUserList, name='kabelUserList'),
    path('kabel-nach-new', kabelNach, name='kabelNach'),



    # dbfs_nachs
    path('dbf_a_nach', dbf_a_nach, name='dbf_a_nach'),
    path('zte_nach', zte_nach, name='zte_nach'),


    # NachislitWruchnuyu, и все новое для MTB
    path('nachislit_wruchnuyu', nachislit_wruchnuyu, name='nachislit_wruchnuyu'),
    path('nachislit_wruchnuyu_history', nachislit_wruchnuyu_history, name='nachislit_wruchnuyu_history'),
    path('perekidka_new', perekidka_new, name='perekidka_new'),
    path('perekidka_new_history', perekidka_new_history, name='perekidka_new_history'),
    path('snyatie_new', snyatie_new, name='snyatie_new'),
    path('snyatie_new_history', snyatie_new_history, name='snyatie_new_history'),
    path('check_pays', check_pays, name='check_pays'),
    path('baza_history', baza_history, name='baza_history'),
    path('perekidkaNachisleniya', perekidkaNachisleniya, name='perekidkaNachisleniya'),
    path('import_internet_nach_new', import_internet_nach_new, name='import_internet_nach_new'),
    path('internet_nachisleniya_new', internet_nachisleniya_new, name='internet_nachisleniya_new'),
    path('pays_with_comment', pays_with_comment, name='pays_with_comment'),
    path('pays_with_comment_history', pays_with_comment_history, name='pays_with_comment_history'),
    path('change_nachislenie', change_nachislenie, name='change_nachislenie'),
    path('check_dogowors', check_dogowors, name='check_dogowors'),
    path('alem_add', alem_add, name='alem_add'),
    path('alem_nach', alem_nach, name='alem_nach'),
    path('dbf_nach_history', dbf_nach_history, name='dbf_nach_history'),
    path('changeBalance', changeBalance, name='changeBalance'),
    path('changeBalanceHistory', changeBalanceHistory, name='changeBalanceHistory'),



    path('dbf_nach_history', dbf_nach_history, name='dbf_nach_history'),
    # Новые начисления
    path('newAbonplataNachisleniya', newAbonplataNachisleniya, name='newAbonplataNachisleniya'),


    # my page
    path('saldo_po_godam_save', saldo_po_godam_save, name='saldo_po_godam_save'),
    path('saldo_po_godam_save2', saldo_po_godam_save2, name='saldo_po_godam_save2'),
    path('add_nachisleniya_from_excel', add_nachisleniya_from_excel, name='add_nachisleniya_from_excel'),
  









 



    

    
]
