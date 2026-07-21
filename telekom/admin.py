from django.contrib import admin
from django.http import HttpResponse

# from .models import AbonentService, AccountName, AlemCount, DontRepeatYourself, ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, ImportInternetPlateji, ImportInternetPlatejiOFF, InterpayPerekidkaBilling, KassaExcelFiles, ManagerNames, MonthBalance, MonthPlatejiFromBilling, MonthPlatejiOFFFromBilling, NachMonthDebetKredet, NachisleniyaOtchet, OldLoginDogowor, PlatejiWhichAddKassirsEveryDay, SagidDecemberDebetKredet, UserTableArhiw, Zakaz, dbfNameList
# from .models import StaffAction, KabelCount, InternetTarif, NachMinus, PerekidkaInfo
# from .models import PayHistory, InterpayBilling, LocalCall, NonLocalCall
# from .models import UserTable, HozOrBudjet
from .models import *


class UserTableAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'number', 'etrap', 'surname', 'name')
    list_display_links = ('id', 'number',)
    list_filter = ('etrap', 'is_enterprises')
    search_fields = ('id', 'number', 'etrap', 'surname', 'name', 'dogowor', 'login')
    list_editable = ('surname', 'name')


class PerekidkaInfoNewAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'user1Number', 'user1Etrap', 'user2Number', 'user2Etrap', 'operator', 'date', 'type_perekidka')
    list_display_links = ('id', 'user1Number')
    list_filter = ('user1Etrap', 'user2Etrap', 'operator', 'date', 'type_perekidka')
    search_fields = ('id', 'user1Number', 'user2Number', 'comment')


class SnyatieInfoAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'number', 'etrap', 'operator_galochka', 'date_galochka', 'operator_snyal', 'date_snyal')
    list_display_links = ('id', 'number', 'etrap')
    list_filter = ('etrap', 'operator_galochka', 'operator_snyal', 'date_galochka', 'date_snyal')
    search_fields = ('id', 'number', 'comment_galochka')


@admin.register(PaysWithComment)
class PaysWithCommentAdmin(admin.ModelAdmin):
    list_display = ('number', 'etrap', 'operator', 'date', 'date_pay', 'pays_pk', 'internet', 'kabel', 'alem', 'prochee', 'changed')
    list_filter = ('etrap', 'changed', 'date', 'date_pay')
    search_fields = ('number', 'operator', 'comment', 'pays_pk')
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'etrap', 'operator', 'comment', 'date_pay', 'pays_pk')
        }),
        ('Платежи', {
            'fields': ('internet', 'kabel', 'alem', 'prochee')
        }),
        ('Изменения', {
            'fields': ('changed', 'when_changed', 'who_changed', 'changed_comment'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date',)  # Автоматически заполняемое поле
    
    def save_model(self, request, obj, form, change):
        if 'changed' in form.changed_data and obj.changed:
            obj.who_changed = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)


@admin.register(NachWithComment)
class NachWithCommentAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'etrap', 'operator', 'internet', 'kabel', 'alem', 'prochee',
        'telefon', 'slr', 'kod', 'zakaz', 'dop_uslugi', 'year', 'month', 'date',
    )
    list_filter = ('etrap', 'operator', 'year', 'month')
    search_fields = ('number', 'etrap', 'operator', 'comment')
    readonly_fields = ('date',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'etrap', 'operator', 'comment')
        }),
        ('Начисления по услугам', {
            'fields': (
                'internet', 'kabel', 'alem', 'prochee',
                'telefon', 'slr', 'kod', 'zakaz', 'dop_uslugi',
            )
        }),
        ('Период', {
            'fields': ('year', 'month', 'date')
        }),
    )


# class AbonentBeneficiaryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'beneficiary', 'percent')
#     list_display_links = ('id', 'beneficiary',)


class HozOrBudjetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'percent')
    list_display_links = ('id', 'name',)


class StaffActionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'user', 'comment', 'action', 'date')
    list_display_links = ('id',)
    list_filter = ('action', 'date')
    search_fields = ('id', 'user', 'comment')


class NachMinusAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'get_number', 'get_etrap', 'get_name', 'get_surname', 'year', 'month', 'dop_uslugi', 'internet', 'kabel', 'alem', 'telefon', 'slr', 'kod', 'zakaz', 'prochee', 'dop_usligi_added_Pk')
    list_display_links = ('id',)
    list_filter = ('year', 'month', 'user__etrap')
    search_fields = ('user__surname', 'user__number', 'user__name')
    list_editable = ('dop_uslugi', 'telefon', 'slr', 'kod', 'zakaz', 'prochee', 'internet', 'alem', 'kabel')
    raw_id_fields = ['user']

    def get_number(self, obj):
        return obj.user.number
    
    def get_etrap(self, obj):
        return obj.user.etrap
    
    def get_name(self, obj):
        return obj.user.name
    
    def get_surname(self, obj):
        return obj.user.surname


class NachislitWruchnuyuHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'etrap', 'number', 'column', 'price', 'user')
    list_display_links = ('id',)
    list_filter = ('column', 'user', 'etrap')
    search_fields = ('id', 'number', 'price')


class UstanowkaSnyatieDopUslugHistoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'number', 'etrap', 'which_action', 'which_type')
    list_display_links = ('id', 'number', 'etrap', 'which_action', 'which_type')
    list_filter = ('etrap', 'which_action', 'which_type')
    search_fields = ('id', 'number')


class CheckPaysWithKassirsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'etrap', 'checked_date', 'operator', 'date')
    list_display_links = ('id', 'etrap')
    list_filter = ('etrap', 'operator', 'date')
    search_fields = ('id', 'comment')


class SaveInfoAboutWhoAddAndNachPaysFromBillingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'file_name', 'etrap_add', 'who_add', 'etrap_nach', 'who_nach', 'is_delete')
    list_display_links = ('id', 'file_name')
    list_filter = ('etrap_add', 'etrap_nach', 'is_delete', 'when_add', 'when_nach', 'who_add', 'who_nach')
    search_fields = ('id', 'file_name', 'comment', 'manager')


class SaldoBalancePoGodamAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'etrap', 'number', 'year')
    list_display_links = ('id', 'etrap')
    list_filter = ('etrap', 'year')
    search_fields = ('id', 'number')


class BazaChangeInfoAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'etrap', 'number', 'operator', 'akt_raport')
    list_display_links = ('id', 'etrap')
    list_filter = ('etrap', 'operator')
    search_fields = ('id', 'comment', 'akt_raport')


class NachPerekidkaHistoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'user1Number', 'user1Etrap', 'user2Number', 'user2Etrap', 'operator')
    list_display_links = ('id', 'user1Number')
    list_filter = ('user1Etrap', 'user2Etrap', 'operator')
    search_fields = ('id', 'user1Number', 'user2Number')
    
class ZakazAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'DATE', 'NUMBER_A', 'NUMBER_B', 'NUMBER_LOCATIONS', 'etrap', 'DUR', 'MT', 'price', 'total_price', 'CALL_TYPE', 'action', 'agent_id')
    list_display_links = ('id', 'DATE', 'NUMBER_A', 'NUMBER_B', 'NUMBER_LOCATIONS', 'etrap', 'DUR', 'MT', 'price', 'total_price', 'CALL_TYPE', 'action', 'agent_id')
    list_filter = ('NUMBER_LOCATIONS', 'CALL_TYPE', 'etrap', 'action', 'DATE')
    search_fields = ('id', 'NUMBER_A', 'NUMBER_B')


class DontRepeatYourselfAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'id', 
        'internetPlatejiXlsxName',
        'internetNachisleniyaXlsxName', 
        'slrNachisleniyaYearMonth', 
        'kodNachisleniyaYearMonth', 
        'platejiNachisleniyaYearMonthEtrapONOFF', 
        'internetNachisleniyaYearMonthEtrapONOFF', 
        'dopUslugiNachisleniyaYearMonthEtrap',
        'KabelNachisleniaYearMonthEtrap',
        'abonplataNachisleniaYearMonthEtrap',
        'zakazNachisleniaYearMonthEtrap',
        'alemNachisleniyaYearMonthEtrapONOFF',
        'platejiSkassyKassirami'
        )
    list_display_links = (
        'id', 
        'internetPlatejiXlsxName',
        'internetNachisleniyaXlsxName', 
        'slrNachisleniyaYearMonth', 
        'kodNachisleniyaYearMonth', 
        'platejiNachisleniyaYearMonthEtrapONOFF', 
        'internetNachisleniyaYearMonthEtrapONOFF', 
        'dopUslugiNachisleniyaYearMonthEtrap',
        'KabelNachisleniaYearMonthEtrap',
        'abonplataNachisleniaYearMonthEtrap',
        'zakazNachisleniaYearMonthEtrap',
        'alemNachisleniyaYearMonthEtrapONOFF',
        'platejiSkassyKassirami'
        )
    search_fields = (
        'id', 
        'internetPlatejiXlsxName',
        'internetNachisleniyaXlsxName', 
        'slrNachisleniyaYearMonth', 
        'kodNachisleniyaYearMonth', 
        'platejiNachisleniyaYearMonthEtrapONOFF', 
        'internetNachisleniyaYearMonthEtrapONOFF', 
        'dopUslugiNachisleniyaYearMonthEtrap',
        'KabelNachisleniaYearMonthEtrap',
        'abonplataNachisleniaYearMonthEtrap',
        'zakazNachisleniaYearMonthEtrap',
        'alemNachisleniyaYearMonthEtrapONOFF',
        'platejiSkassyKassirami'
        )



class InternetTarifAdmin(admin.ModelAdmin):
    list_display = ('id', 'tarif', 'price')
    list_display_links = ('id', 'tarif',)


# class AbonLengthAdmin(admin.ModelAdmin):
#     list_display = ('id', 'metr', 'price')
#     list_display_links = ('id', 'metr',)
#     search_fields = ('metr',)


# class AbonentNumbersCountAdmin(admin.ModelAdmin):
#     list_display = ('id', 'count_of_numbers', 'price')
#     list_display_links = ('id', 'count_of_numbers',)


class AbonentServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'price')
    list_display_links = ('id', 'service',)
    search_fields = ('service', 'price')


class KabelCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'kabel_count', 'price')
    list_display_links = ('id', 'kabel_count',)


class AlemCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'alem_count', 'price')
    list_display_links = ('id', 'alem_count',)


class PayHistoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('get_number', 'get_etrap', 'get_surname', 'get_name', 'total', 'prochee', 'internet', 'kabel', 'alem', 'kassir', 'date', 'edara_ilat', 'type', 'kassir_etrap', 'is_card')
    list_display_links = ('get_number',)
    list_filter = ('is_card', 'kassir', 'date', 'edara_ilat', 'type', 'kassir_etrap')
    search_fields = ('abonent__number',)
    list_editable=('is_card',)
    raw_id_fields = ['abonent']

    def get_number(self, obj):
        return obj.abonent.number
    
    def get_etrap(self, obj):
        return obj.abonent.etrap
    
    def get_name(self, obj):
        return obj.abonent.name
    
    def get_surname(self, obj):
        return obj.abonent.surname
  




class LocalCallAdmin(admin.ModelAdmin):
    list_display = ('id', 'etrap', 'SUB_A', 'SUB_B', 'DATE', 'START', 'FIN', 'DUR', 'MT')
    list_display_links = ('id', 'etrap')
    list_filter = ('etrap', 'DATE', 'MT')
    search_fields = ('SUB_A', 'SUB_B')
    

class NonLocalCallAdmin(admin.ModelAdmin):
    list_display = ( 'SUB_A_etrap', 'file_name','edara','SUB_A','SUB_B_locations', 'SUB_B','START', 'price', 'DATE', 'FIN', 'DUR', 'MT', 'total_price')
    list_display_links = ('SUB_A_etrap',)
    list_filter = ('edara','SUB_B_locations', 'file_name', 'DATE', 'SUB_A_etrap')
    search_fields = ('SUB_A', 'SUB_B', 'SUB_A_etrap')


class dbfNameListAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'name', 'is_nach')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'is_nach')
    list_editable=('is_nach',)


class MonthBalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'etrap', 'year', 'month', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
    list_display_links = ('id', 'etrap', 'year', 'month', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
    list_filter = ('etrap', 'year', 'month')
    search_fields = ('id', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')


# class MonthBalanceRezerwAdmin(admin.ModelAdmin):
#     list_display = ('id', 'etrap', 'year', 'month', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
#     list_display_links = ('id', 'etrap', 'year', 'month', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
#     list_filter = ('etrap', 'year', 'month')
#     search_fields = ('id', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
# admin.site.register(MonthBalanceRezerw, MonthBalanceRezerwAdmin) 


class ImportInternetPlatejiAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'pay_date','dogowor', 'FAO', 'price', 'etrap')
    list_display_links = ('id',)
    list_filter = ('type', 'pay_date', 'etrap')
    search_fields = ('id', 'dogowor', 'FAO', 'price')


class ImportInternetPlatejiOFFAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'pay_date','dogowor', 'FAO', 'price', 'etrap')
    list_display_links = ('id',)
    list_filter = ('type', 'pay_date', 'etrap')
    search_fields = ('id', 'dogowor', 'FAO', 'price')


class ImportInternetNachisleniyaONAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'month','dogowor', 'FAO', 'login', 'price', 'etrap')
    list_display_links = ('id',)
    list_filter = ('year', 'month', 'etrap')
    search_fields = ('id', 'dogowor', 'FAO', 'price', 'login')
    # list_editable=('is_nach', 'dogowor', 'login')

class ImportInternetNachisleniyaOFFAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'month','dogowor', 'FAO', 'login', 'price', 'etrap')
    list_display_links = ('id',)
    list_filter = ('year', 'month', 'etrap')
    search_fields = ('id', 'dogowor', 'FAO', 'price', 'login')

class ImportAlemNachisleniyaONAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'month','dogowor', 'FAO', 'login', 'price', 'etrap')
    list_display_links = ('id',)
    list_filter = ('year', 'month', 'etrap')
    search_fields = ('id', 'dogowor', 'FAO', 'price', 'login')

class ImportAlemNachisleniyaOFFAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'month','dogowor', 'FAO', 'login', 'price', 'etrap')
    list_display_links = ('id',)
    list_filter = ('year', 'month', 'etrap')
    search_fields = ('id', 'dogowor', 'FAO', 'price', 'login')





# class UserTableRezerwAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = ('id', 'number', 'etrap', 'surname', 'name')
#     list_display_links = ('id', 'number',)
#     list_filter = ('etrap',)
#     search_fields = ('id', 'number', 'etrap', 'surname', 'name', 'dogowor', 'login')
#     list_editable = ('surname', 'name')


# class NachMinusRezerwAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = ('id', 'get_number', 'get_etrap', 'get_name', 'get_surname', 'year', 'month', 'internet', 'kabel', 'alem', 'telefon', 'slr', 'kod', 'zakaz', 'prochee', 'dop_uslugi')
#     list_display_links = ('id',)
#     list_filter = ('year', 'month')
#     search_fields = ('id', 'month', 'internet', 'kabel', 'alem', 'telefon', 'slr', 'kod', 'zakaz', 'prochee', 'dop_uslugi')

#     def get_number(self, obj):
#         return obj.user.number
    
#     def get_etrap(self, obj):
#         return obj.user.etrap
    
#     def get_name(self, obj):
#         return obj.user.name
    
#     def get_surname(self, obj):
#         return obj.user.surname
    

# class PayHistoryRezerwAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = ('id', 'get_number', 'get_etrap', 'get_surname', 'get_name', 'is_card', 'kassir', 'total', 'date')
#     list_display_links = ('id', 'get_number')
#     list_filter = ('is_card', 'kassir', 'date')

#     def get_number(self, obj):
#         return obj.abonent.number
    
#     def get_etrap(self, obj):
#         return obj.abonent.etrap
    
#     def get_name(self, obj):
#         return obj.abonent.name
    
#     def get_surname(self, obj):
#         return obj.abonent.surname
    
  
# admin.site.register(PayHistoryRezerw, PayHistoryRezerwAdmin)   
# admin.site.register(UserTableRezerw, UserTableRezerwAdmin)
# admin.site.register(NachMinusRezerw, NachMinusRezerwAdmin)


class UserTableArhiwAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'number', 'etrap', 'surname', 'name')
    list_display_links = ('id', 'number',)
    list_filter = ('etrap',)
    search_fields = ('id', 'number', 'etrap', 'surname', 'name', 'dogowor', 'login')
    list_editable = ('surname', 'name')


# class PayHistoryArhiwAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = ('id', 'get_number', 'get_etrap', 'get_surname', 'get_name', 'is_card', 'kassir', 'total', 'date')
#     list_display_links = ('id', 'get_number')
#     list_filter = ('is_card', 'kassir', 'date')

#     def get_number(self, obj):
#         return obj.abonent.number
    
#     def get_etrap(self, obj):
#         return obj.abonent.etrap
    
#     def get_name(self, obj):
#         return obj.abonent.name
    
#     def get_surname(self, obj):
#         return obj.abonent.surname
    
# admin.site.register(PayHistoryArhiw, PayHistoryArhiwAdmin)


# class NachMinusArhiwAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = ('id', 'get_number', 'get_etrap', 'get_name', 'get_surname', 'year', 'month', 'internet', 'kabel', 'alem', 'telefon', 'slr', 'kod', 'zakaz', 'prochee', 'dop_uslugi')
#     list_display_links = ('id',)
#     list_filter = ('year', 'month')
#     search_fields = ('id', 'month', 'internet', 'kabel', 'alem', 'telefon', 'slr', 'kod', 'zakaz', 'prochee', 'dop_uslugi')

# admin.site.register(NachMinusArhiw, NachMinusAdmin)


# class MonthBalanceArhiwAdmin(admin.ModelAdmin):
#     list_display = ('id', 'etrap', 'year', 'month', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
#     list_display_links = ('id', 'etrap', 'year', 'month', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
#     list_filter = ('etrap', 'year', 'month')
#     search_fields = ('id', 'internetPlus', 'kabelPlus', 'alemPlus', 'telefonPlus', 'slrPlus', 'kodPlus', 'zakazPlus', 'procheePlus', 'dop_uslugiPlus', 'internetMinus', 'kabelMinus', 'alemMinus', 'telefonMinus', 'slrMinus', 'kodMinus', 'zakazMinus', 'procheeMinus', 'dop_uslugiMinus')
# admin.site.register(MonthBalanceArhiw, MonthBalanceArhiwAdmin) 


class NachMonthDebetKredetAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'edaraOrNasel', 'year', 'month', 'etrap', 'number', 'debet', 'kredet') 
    list_display_links = ('id', 'edaraOrNasel', 'year', 'month', 'etrap', 'number', 'debet', 'kredet')
    list_filter = ('etrap','edaraOrNasel','year', 'month', 'debet', 'kredet')
    search_fields = ('id', 'number')
    # list_editable = ('surname', 'name')


class MonthPlatejiFromBillingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'manager', 'pay_date', 'dogowor', 'price', 'kod_oplaty', 'platejiType', 'YurOrFiz')
    list_display_links = ('id', 'manager')
    list_filter = ('manager', 'pay_date', 'platejiType', 'YurOrFiz')
    search_fields = ('dogowor', 'price', 'kod_oplaty')


class MonthPlatejiOFFFromBillingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', 'manager', 'pay_date', 'dogowor', 'price', 'kod_oplaty', 'platejiType', 'YurOrFiz')
    list_display_links = ('id', 'manager')
    list_filter = ('manager', 'pay_date', 'platejiType', 'YurOrFiz')
    search_fields = ('dogowor', 'price', 'kod_oplaty')





class OldLoginDogoworAdmin(admin.ModelAdmin):
    list_display = ('id', 'number','etrap','dogowor', 'login', 'is_enterprises', 'hb', 'operator', 'saved_in_action')
    list_display_links = ('id', 'dogowor','login')
    search_fields = ('id', 'number','dogowor', 'login')
    list_filter = ('etrap', 'is_enterprises', 'hb', 'operator', 'saved_in_action')




class PlatejiWhichAddKassirsEveryDayAdmin(admin.ModelAdmin):
    list_display = ('number','user_etrap', 'kassir_etrap', 'type_pay', 'dogowor', 'price', 'manager', 'date', 'pay_category', 'kodOplaty', 'name', 'is_enterprises', 'file_name')
    list_display_links = ('number',)
    list_filter = ('user_etrap', 'kassir_etrap', 'type_pay', 'manager', 'date', 'pay_category', 'file_name', 'file_is_nach', 'when_added_file')
    search_fields = ('number', 'name', 'dogowor')


class ManagerNamesAdmin(admin.ModelAdmin):
    list_display = ('etrap','name', 'name2')
    list_display_links = ('etrap','name', 'name2')
    list_filter = ('etrap', 'name', 'name2')
    search_fields = ('name', 'name2')


class KassaExcelFilesAdmin(admin.ModelAdmin):
    list_display = ('get_username','document', 'add_date')
    list_display_links = ('get_username',)
    list_filter = ('operator', 'add_date')
    search_fields = ('document',)

    def get_username(self, obj):
        return obj.operator.username
    


# class PayHistoryAdmin(admin.ModelAdmin):
#     save_on_top = True
#     list_display = ('id', 'get_number', 'get_etrap', 'get_surname', 'get_name', 'is_card', 'kassir', 'total', 'date', 'edara_ilat', 'type', 'kassir_etrap')
#     list_display_links = ('id', 'get_number')
#     list_filter = ('is_card', 'kassir', 'date', 'edara_ilat', 'type', 'kassir_etrap')
#     search_fields = ('abonent__number',)

#     def get_number(self, obj):
#         return obj.abonent.number
    
#     def get_etrap(self, obj):
#         return obj.abonent.etrap
    
#     def get_name(self, obj):
#         return obj.abonent.name
    
#     def get_surname(self, obj):
#         return obj.abonent.surname



# exam models   


class ExamQuestionsAdmin(admin.ModelAdmin):
    list_display = ('question',)
    list_display_links = ('question',)
    # list_filter = ('group',)
    search_fields = ('question',)
    # def get_group(self, obj):
    #     return obj.group.name



class ScoresAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'etrap', 'sotowyy', 'questions_count', 'scores', 'date_of_passing')
    list_display_links = ('surname', 'name')
    list_filter = ('etrap',)



class ExamHistoryAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'Scores_id', 'is_currect_answer', 'currect_answer', 'choised_answer')
    list_display_links = ('surname', 'name',)
    list_filter = ('is_currect_answer', 'Scores_id')




class KabelTvNewAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'surname', 'street', 'home', 'flat', 'sotowyy', 'is_enterprises', 'is_active', 'balance', 'count', 'user_add_date')
    list_display_links = ('number', 'name', 'surname',)
    list_filter = ('is_enterprises', 'is_active', 'count', 'user_add_date')
    search_fields = ('number', 'name', 'surname')
    # list_editable = ('street', 'home', 'flat', 'sotowyy', 'is_enterprises', 'is_active', 'balance', 'count')
 

class KabelCommentAdmin(admin.ModelAdmin):
    list_display = ('get_number', 'get_surname', 'get_name', 'get_street', 'get_home', 'get_flat', 'worker', 'action', 'comment', 'comment_add_date')
    list_display_links = ('get_number',)
    search_fields = ('user__number', 'user__name', 'user__surname', 'comment')
    list_filter = ('comment_add_date', 'worker', 'action')
    

    def get_number(self, obj):
        return obj.user.number
    
    def get_name(self, obj):
        return obj.user.name
    
    def get_surname(self, obj):
        return obj.user.surname

    def get_street(self, obj):
        return obj.user.street

    def get_home(self, obj):
        return obj.user.home

    def get_flat(self, obj):
        return obj.user.flat


class KabelTvPayHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_number', 'get_surname', 'get_name', 'get_street', 'get_home', 'get_flat', 'pay', 'pay_date', 'pay_kassir', 'card')
    list_display_links = ('get_number',)
    search_fields = ('user__number', 'user__name', 'user__surname')
    list_filter = ('pay_date', 'pay_kassir', 'card',)
    list_editable = ('pay', 'card')
    
    

    def get_number(self, obj):
        return obj.user.number
    
    def get_name(self, obj):
        return obj.user.name
    
    def get_surname(self, obj):
        return obj.user.surname

    def get_street(self, obj):
        return obj.user.street

    def get_home(self, obj):
        return obj.user.home

    def get_flat(self, obj):
        return obj.user.flat


class KabelNachAdmin(admin.ModelAdmin):
    list_display = ('get_number', 'get_surname', 'get_name', 'get_street', 'get_home', 'get_flat', 'year', 'month', 'nach', 'nach_date')
    list_display_links = ('get_number',)
    search_fields = ('user__number', 'user__name', 'user__surname')
    list_filter = ('year', 'month',)
    list_editable = ('nach',)
    

    def get_number(self, obj):
        return obj.user.number
    
    def get_name(self, obj):
        return obj.user.name
    
    def get_surname(self, obj):
        return obj.user.surname

    def get_street(self, obj):
        return obj.user.street

    def get_home(self, obj):
        return obj.user.home

    def get_flat(self, obj):
        return obj.user.flat


class KabelTvNewDebitKreditAdmin(admin.ModelAdmin):
    list_display = ('number', 'year', 'month', 'last_DT', 'last_KT', 'nach', 'perekidka_nach', 'is_enterprises', 'current_DT', 'current_KT')
    list_display_links = ('number',)
    search_fields = ('number',)
    list_filter = ('year', 'month', 'is_enterprises')
    list_editable = ('last_DT', 'last_KT', 'nach', 'current_DT', 'current_KT')


class PayAndPayTypeForDebitKreditAdmin(admin.ModelAdmin):
    list_display = ('get_number', 'get_year', 'get_month', 'pay', 'pay_type')
    list_display_links = ('get_number',)
    search_fields = ('KabelTvNewDebitKredit_pk__number',)
    list_filter = ('KabelTvNewDebitKredit_pk__year', 'KabelTvNewDebitKredit_pk__month',)
    list_editable = ('pay',)

    def get_number(self, obj):
        return obj.KabelTvNewDebitKredit_pk.number

    def get_year(self, obj):
        return obj.KabelTvNewDebitKredit_pk.year

    def get_month(self, obj):
        return obj.KabelTvNewDebitKredit_pk.month


class AccountBalanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'balance')
    list_display_links = ('name', 'account', 'balance')
    search_fields = ('name','account')





admin.site.register(PayHistory, PayHistoryAdmin)
# admin.site.register(InterpayBilling)
# admin.site.register(InterpayPerekidkaBilling)
# admin.site.register(AccountName)
admin.site.register(UserTable, UserTableAdmin)
admin.site.register(PerekidkaInfoNew, PerekidkaInfoNewAdmin)
admin.site.register(SnyatieInfo, SnyatieInfoAdmin)
# admin.site.register(PerekidkaInfo)
# admin.site.register(HozOrBudjet, HozOrBudjetAdmin)
admin.site.register(StaffAction, StaffActionAdmin)
admin.site.register(NachMinus, NachMinusAdmin)
admin.site.register(NachislitWruchnuyuHistory, NachislitWruchnuyuHistoryAdmin)
admin.site.register(UstanowkaSnyatieDopUslugHistory, UstanowkaSnyatieDopUslugHistoryAdmin)
admin.site.register(CheckPaysWithKassirs, CheckPaysWithKassirsAdmin)
admin.site.register(SaveInfoAboutWhoAddAndNachPaysFromBilling, SaveInfoAboutWhoAddAndNachPaysFromBillingAdmin)
admin.site.register(SaldoBalancePoGodam, SaldoBalancePoGodamAdmin)
admin.site.register(BazaChangeInfo, BazaChangeInfoAdmin)
admin.site.register(NachPerekidkaHistory, NachPerekidkaHistoryAdmin)
admin.site.register(Zakaz, ZakazAdmin)
admin.site.register(DontRepeatYourself) 
# admin.site.register(AbonentBeneficiary, AbonentBeneficiaryAdmin)
admin.site.register(InternetTarif, InternetTarifAdmin)
# admin.site.register(AbonLength, AbonLengthAdmin)
# admin.site.register(AbonentNumbersCount, AbonentNumbersCountAdmin)
admin.site.register(AbonentService, AbonentServiceAdmin)
# admin.site.register(KabelCount, KabelCountAdmin)
# admin.site.register(AlemCount, AlemCountAdmin)
admin.site.register(LocalCall, LocalCallAdmin) 
admin.site.register(NonLocalCall, NonLocalCallAdmin) 
admin.site.register(dbfNameList, dbfNameListAdmin) 
# admin.site.register(NachisleniyaOtchet) 
# admin.site.register(MonthBalance, MonthBalanceAdmin) 
# admin.site.register(ImportInternetPlateji, ImportInternetPlatejiAdmin)
# admin.site.register(ImportInternetPlatejiOFF, ImportInternetPlatejiOFFAdmin)
admin.site.register(ImportInternetNachisleniyaON, ImportInternetNachisleniyaONAdmin)
admin.site.register(ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaOFFAdmin)
# admin.site.register(ImportAlemNachisleniyaON, ImportAlemNachisleniyaONAdmin)
# admin.site.register(ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaOFFAdmin)
# admin.site.register(ShowNachService)
# after clear number
# admin.site.register(UserTableAfterClearNumber)
# admin.site.register(NachMinusAfterClearNumber)
# admin.site.register(ShowNachServiceAfterClearNumber)
admin.site.register(UserTableArhiw, UserTableArhiwAdmin)
admin.site.register(NachMonthDebetKredet, NachMonthDebetKredetAdmin)
# admin.site.register(MonthPlatejiFromBilling, MonthPlatejiFromBillingAdmin)
# admin.site.register(MonthPlatejiOFFFromBilling, MonthPlatejiOFFFromBillingAdmin)
admin.site.register(OldLoginDogowor, OldLoginDogoworAdmin)
# admin.site.register(SagidDecemberDebetKredet)
admin.site.register(PlatejiWhichAddKassirsEveryDay, PlatejiWhichAddKassirsEveryDayAdmin)
admin.site.register(ManagerNames, ManagerNamesAdmin)
admin.site.register(KassaExcelFiles, KassaExcelFilesAdmin)
# admin.site.register(ExamGroup)
# admin.site.register(ExamQuestions, ExamQuestionsAdmin)
# admin.site.register(Scores, ScoresAdmin)
# admin.site.register(ExamHistory, ExamHistoryAdmin)

admin.site.register(KabelTvNew, KabelTvNewAdmin)
admin.site.register(KabelComment, KabelCommentAdmin)
admin.site.register(KabelTvPayHistory, KabelTvPayHistoryAdmin)
admin.site.register(KabelNach, KabelNachAdmin)
admin.site.register(KabelTvNewDebitKredit, KabelTvNewDebitKreditAdmin)
admin.site.register(PayAndPayTypeForDebitKredit, PayAndPayTypeForDebitKreditAdmin)
admin.site.register(AccountBalance, AccountBalanceAdmin)



@admin.register(AlemNachFileNames)
class AlemNachFileNamesAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'year', 'month', 'add_date', 'who_add', 'nach_date', 'who_nach')
    search_fields = ('file_name', 'who_add', 'who_nach', 'year', 'month')
    list_filter = ('year', 'month', 'who_add', 'who_nach', 'add_date', 'nach_date')
    ordering = ('-add_date',)
    date_hierarchy = 'add_date'


@admin.action(description="Экспортировать выбранные записи в CSV")
def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)

    return response


@admin.register(AlemNachData)
class AlemNachDataAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'name', 'etrap', 'dogowor', 'account_name',
        'tariff', 'service', 'tariff_charge', 'service_charge',
        'quantity', 'total', 'currency', 'on_off', 'year', 'month', 'file_name'
    )
    list_filter = ('year', 'month', 'etrap', 'currency', 'on_off', 'is_nach')
    search_fields = ('number', 'name', 'dogowor', 'account_name', 'tariff', 'service', 'file_name')
    ordering = ('-year', '-month', 'etrap')
    actions = [export_to_csv]







admin.site.site_title = 'Панель Администратора'
admin.site.site_header = 'Панель Администратора'



















