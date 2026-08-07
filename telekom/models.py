from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


etraps = (
        (None, 'Этрап'),
        ('Dashoguz', 'Dashoguz'),
        ('Akdepe', 'Akdepe'),
        ('Gorogly', 'Gorogly'),
        ('Ruhubelent', 'Ruhubelent'),
        ('S.A.Nyyazow', 'S.A.Nyyazow'),
        ('Turkmenbashy', 'Turkmenbashy'),
        ('Boldumsaz', 'Boldumsaz'),
        ('Koneurgench', 'Koneurgench'),
        ('Garashsyzlyk', 'Garashsyzlyk'),
        ('Gubadag', 'Gubadag'),
)


"""###################
   Основные таблицы ##
"""###################



class UserTable(models.Model):
	# 37 полей
	number = models.CharField(max_length=500, verbose_name='Номер телефона')
	etrap = models.CharField(max_length=500, choices= etraps)
	surname = models.CharField(max_length=500, verbose_name='Фамилия/организация', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя/Отдел', blank=True)
	street = models.CharField(max_length=500, verbose_name='Улица', blank=True)
	home = models.CharField(max_length=500, verbose_name='Дом', blank=True)
	flat = models.CharField(max_length=500, verbose_name='Квартира', blank=True)

	sotowyy = models.CharField(max_length=500, verbose_name='Сотовый номер', blank=True)
	
	is_enterprises = models.BooleanField(default=False, verbose_name='Предприятия', blank=True)

	alem = models.BooleanField(default=False, verbose_name='Alem TV Активен', blank=True)
	alemCount = models.ForeignKey('AlemCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Alem TV точек')
	alem_connect_date = models.DateTimeField(verbose_name='Дата подсоединения Alem TV', null=True, blank=True)
	alem_on_date = models.DateTimeField(verbose_name='Дата включения Alem TV', null=True, blank=True)
	alem_off_date = models.DateTimeField(verbose_name='Дата отключения Alem TV', null=True, blank=True)
	alem_disconnect_date = models.DateTimeField(verbose_name='Дата отсоединения Alem TV', null=True, blank=True)

	account = models.IntegerField(verbose_name='Счёт', blank=True, null=True)
	accountName = models.CharField(max_length=1000, verbose_name='Имя Счет номера (edara name)', blank=True)
	accountAdress = models.CharField(max_length=1000, verbose_name='Адрес Счет номера (edara adress)', blank=True)

	hb = models.ForeignKey('HozOrBudjet', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Хоз/Бюджет?')

	internet_tarif = models.ForeignKey('InternetTarif', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Интернет тариф')
	internet_connect_date = models.DateTimeField(verbose_name='Дата подсоединения Интернет', null=True, blank=True)
	internet_disconnect_date = models.DateTimeField(verbose_name='Дата отсоединения Интернет', null=True, blank=True)

	# abon_length = models.ForeignKey('AbonLength', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга Метры')
	# abon_length_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения Метров', null=True, blank=True) # -

	# count_of_numbers = models.ForeignKey('AbonentNumbersCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кол-во номеров')
	# count_of_numbers_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения Количество номеров', null=True, blank=True) # -

	abonplata = models.CharField(max_length=500,verbose_name='Абонплата', null=True, blank=True)

	# beneficiary = models.ForeignKey('AbonentBeneficiary', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Льгота')
	beneficiary = models.BooleanField(default=False, verbose_name='Льготник', blank=True)

	# кабель
	is_on = models.BooleanField(default=False, verbose_name='Кабель Включен?', blank=True)
	is_on_date = models.DateTimeField(verbose_name="Дата и время включения кабеля", null=True, blank=True)
	kabel_count = models.ForeignKey('KabelCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кол-во точек кабеля')
	connect_date = models.DateTimeField(verbose_name="Дата и время Подключения кабеля", null=True, blank=True)
	kabel_comments = models.TextField(verbose_name='Комментарии для кабеля', null=True, blank=True)
	# Для кабель TV
	ids = models.CharField(max_length=50, verbose_name='Кабель ID', blank=True)

	# surname name street home flat sotowyy	is_enterprises alem alemCount alem_connect_date alem_on_date alem_off_date alem_disconnect_date
	# account hb internet_tarif internet_connect_date internet_disconnect_date abon_length abon_length_connect_date
	# count_of_numbers count_of_numbers_connect_date beneficiary is_on is_on_date kabel_count connect_date kabel_comments
	# ids service login dogowor b_internet b_kabel b_alem b_telefon b_slr b_kod b_zakaz b_prochee b_dop_uslugi addDate wost_date

	# M2M fields
	service = models.ManyToManyField('AbonentService', verbose_name='Доп.Услуги (добавлять через ctrl)', blank=True)
	# service_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения услуг', null=True, blank=True)

	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='Договор', blank=True)
	dogowor_alem = models.CharField(max_length=100, verbose_name='Договор Алем ТВ', blank=True)
	dogowor_telefoniya = models.CharField(max_length=100, verbose_name='Договор Телефония', blank=True)
	dogowor_belet = models.CharField(max_length=100, verbose_name='Договор Белет', blank=True)

	b_internet = models.FloatField(verbose_name=' Баланс Интернет', default=0)
	b_kabel = models.FloatField(verbose_name=' Баланс Кабель', default=0)
	b_alem = models.FloatField(verbose_name=' Баланс Alem TV', default=0)
	b_telefon = models.FloatField(verbose_name='Баланс Телефон', default=0)
	b_slr = models.FloatField(verbose_name='Баланс СЛР', default=0)
	b_kod = models.FloatField(verbose_name='Баланс Код', default=0)
	b_zakaz = models.FloatField(verbose_name='Баланс Заказ', default=0)
	b_prochee = models.FloatField(verbose_name='Баланс Прочее', default=0)
	b_dop_uslugi = models.FloatField(verbose_name='Баланс Доп. Услуги', default=0)

	s_internet = models.FloatField(verbose_name=' Сальдо Интернет', default=0)
	s_kabel = models.FloatField(verbose_name=' Сальдо Кабель', default=0)
	s_alem = models.FloatField(verbose_name=' Сальдо Alem TV', default=0)
	s_telefon = models.FloatField(verbose_name='Сальдо Телефон', default=0)
	s_slr = models.FloatField(verbose_name='Сальдо СЛР', default=0)
	s_kod = models.FloatField(verbose_name='Сальдо Код', default=0)
	s_zakaz = models.FloatField(verbose_name='Сальдо Заказ', default=0)
	s_prochee = models.FloatField(verbose_name='Сальдо Прочее', default=0)
	s_dop_uslugi = models.FloatField(verbose_name='Сальдо Доп. Услуги', default=0)

	# дата добавления абонента в нашу БД (или дата активации номера) короче в MATB сами пишут эту дату
	addDate = models.DateField(verbose_name="Дата и время добавления абонента в базу данных", null=True, blank=True)

	# Дата востановления если есть
	wost_date = models.DateField(verbose_name="Дата и время востановления абонента", null=True, blank=True)

	snyat_bool = models.BooleanField(default=False, verbose_name='Снят?', blank=True)
	snyat_date = models.DateTimeField(verbose_name="Дата и время снятия", null=True, blank=True)

	intOnDate = models.DateField(verbose_name="Дата подключения интернета", null=True, blank=True)
	intOffDate = models.DateField(verbose_name="Дата отключения интернета", null=True, blank=True)

	class Meta:
		unique_together = ["number", "etrap"]
		verbose_name = 'Абонента'
		verbose_name_plural = 'Абоненты'
		ordering = ['-number']

	def __str__(self):
		return f"{self.number} {self.etrap}"



# Old Login Dogowor нужен при начислении по договору или логину. Если абонент сменил логин и на старый логин есть начисления будет начислен на номер
class OldLoginDogowor (models.Model):
	number = models.CharField(verbose_name='Номер', max_length=32, null=True, blank=True)
	etrap = models.CharField(verbose_name='Этрап', max_length=64, null=True, blank=True)
	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='Договор', blank=True)
	dogowor_alem = models.CharField(max_length=100, verbose_name='Договор Алем ТВ', blank=True)
	dogowor_telefoniya = models.CharField(max_length=100, verbose_name='Договор Телефония', blank=True)
	dogowor_belet = models.CharField(max_length=100, verbose_name='Договор Белет', blank=True)
	created_at = models.DateField(verbose_name='Дата сохранения', auto_now_add=True, null=True, blank=True)
	is_enterprises = models.BooleanField(default=False, verbose_name='Предприятия', blank=True)
	hb = models.CharField(max_length=20, verbose_name='H или B', blank=True)
	operator = models.CharField(verbose_name='Кто сохранял в old', max_length=500, blank=True)
	# Перекидка всех данных, Снятие, База, При сохранении в Old
	saved_in_action = models.CharField(verbose_name='Сохранено при действии', max_length=2000, blank=True)
	account = models.IntegerField(verbose_name='Счет №', blank=True, null=True)

	def __str__(self):
		return f"{self.number} {self.etrap} {self.login} {self.dogowor}"
	
	class Meta:
		verbose_name = 'Старые договоры и логины'
		verbose_name_plural = 'Старые договоры и логины'

		
# для отображения инфы о начислениях в кассе
class PerekidkaInfo(models.Model):
	# user = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Абонент')
	# for_akt_perekidka = models.BooleanField(default=False, verbose_name='Для акт перекидки (если перекидка с пр. на нас. и наоборот)', blank=True)

	user1Number = models.CharField(verbose_name='Перекинуто с абонента номер', max_length=255, null=True, blank=True)
	user1Etrap = models.CharField(verbose_name='Перекинуто с абонента этрап', max_length=255, null=True, blank=True)

	user2Number = models.CharField(verbose_name='Перекинуто на абонента номер', max_length=255, null=True, blank=True)
	user2Etrap = models.CharField(verbose_name='Перекинуто на абонента этрап', max_length=255, null=True, blank=True)

	# эти 2 поля нужны для удобства при печатании месячного отчета для Ашир
	user1_is_enterprises = models.BooleanField(default=False, verbose_name='Абонент 1 предпр')
	user2_is_enterprises = models.BooleanField(default=False, verbose_name='Абонент 2 предпр')

	internet1 = models.FloatField(verbose_name='Перекинуто с Интернет', default=0)
	kabel1 = models.FloatField(verbose_name=' Перекинуто с Кабель', default=0)
	alem1 = models.FloatField(verbose_name=' Перекинуто с Alem TV', default=0)
	telefon1 = models.FloatField(verbose_name='Перекинуто с Телефон', default=0)
	slr1 = models.FloatField(verbose_name='Перекинуто с СЛР', default=0)
	kod1 = models.FloatField(verbose_name='Перекинуто с Код', default=0)
	zakaz1 = models.FloatField(verbose_name='Перекинуто с Заказ', default=0)
	prochee1 = models.FloatField(verbose_name='Перекинуто с Прочее', default=0)
	dop_uslugi1 = models.FloatField(verbose_name='Перекинуто с Доп. Услуги', default=0)

	internet2 = models.FloatField(verbose_name='Перекинуто на Интернет', default=0)
	kabel2 = models.FloatField(verbose_name=' Перекинуто на Кабель', default=0)
	alem2 = models.FloatField(verbose_name=' Перекинуто на Alem TV', default=0)
	telefon2 = models.FloatField(verbose_name='Перекинуто на Телефон', default=0)
	slr2 = models.FloatField(verbose_name='Перекинуто на СЛР', default=0)
	kod2 = models.FloatField(verbose_name='Перекинуто на Код', default=0)
	zakaz2 = models.FloatField(verbose_name='Перекинуто на Заказ', default=0)
	prochee2 = models.FloatField(verbose_name='Перекинуто на Прочее', default=0)
	dop_uslugi2 = models.FloatField(verbose_name='Перекинуто на Доп. Услуги', default=0)

	comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
	operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Оператор', null=True, blank=True)
	createDate = models.DateField(verbose_name='Дата перекидки', auto_now_add=True) 
	
	def __str__(self):
		return f"c {self.user1Number} {self.user1Etrap} на {self.user2Number} {self.user2Etrap}"
	class Meta:
		verbose_name = 'Информация о перекидках'
		verbose_name_plural = 'Информация о перекидках'


class PerekidkaInfoNew(models.Model):
	user1Number = models.CharField(verbose_name='Номер абонента 1', max_length=64, blank=True)
	user1Etrap = models.CharField(verbose_name='Этрап абонента 1', max_length=64, blank=True)
	user1NameSurname = models.CharField(verbose_name='Фамилия и имя во время перекидки абонента 1', max_length=1000, null=True, blank=True)

	user2Number = models.CharField(verbose_name='Номер абонента 2', max_length=64, blank=True)
	user2Etrap = models.CharField(verbose_name='Этрап абонента 2', max_length=64, blank=True)
	user2NameSurname = models.CharField(verbose_name='Фамилия и имя во время перекидки абонента 2', max_length=512, null=True, blank=True)

	user1KabelNumber = models.CharField(verbose_name='Номер kabel абонента 1', max_length=64, blank=True)
	user1KabelNameSurname = models.CharField(verbose_name='Фамилия и имя во время перекидки kabel абонента 1', max_length=1000, null=True, blank=True)

	user1Ksurname = models.CharField(max_length=500, verbose_name='(Кабель1) Фамилия', blank=True)
	user1Kname = models.CharField(max_length=500, verbose_name='(Кабель1) Имя', blank=True)
	user1Kstreet = models.CharField(max_length=100, verbose_name='(Кабель1) Улица', blank=True)
	user1Khome = models.CharField(max_length=100, verbose_name='(Кабель1) Дом', blank=True)
	user1Kflat = models.CharField(max_length=100, verbose_name='(Кабель1) Квартира', blank=True)
	user1Ksotowyy = models.CharField(max_length=40, verbose_name='(Кабель1) Сотовый номер', blank=True)
	user1Kis_enterprises = models.BooleanField(default=False, verbose_name='(Кабель1) Предприятия')
	user1Kis_active = models.BooleanField(default=False, verbose_name='(Кабель1) Активный')
	user1Kbalance = models.FloatField(verbose_name='(Кабель1) Баланс', default=0)
	user1Kcount = models.IntegerField(verbose_name='(Кабель1) Кол-во точек', default=0)
	
	user2KabelNumber = models.CharField(verbose_name='Номер kabel абонента 2', max_length=64, blank=True)
	user2KabelNameSurname = models.CharField(verbose_name='Фамилия и имя во время перекидки kabel абонента 2', max_length=512, null=True, blank=True)

	user2Ksurname = models.CharField(max_length=500, verbose_name='(Кабель2) Фамилия', blank=True)
	user2Kname = models.CharField(max_length=500, verbose_name='(Кабель2) Имя', blank=True)
	user2Kstreet = models.CharField(max_length=100, verbose_name='(Кабель2) Улица', blank=True)
	user2Khome = models.CharField(max_length=100, verbose_name='(Кабель2) Дом', blank=True)
	user2Kflat = models.CharField(max_length=100, verbose_name='(Кабель2) Квартира', blank=True)
	user2Ksotowyy = models.CharField(max_length=40, verbose_name='(Кабель2) Сотовый номер', blank=True)
	user2Kis_enterprises = models.BooleanField(default=False, verbose_name='(Кабель2) Предприятия')
	user2Kis_active = models.BooleanField(default=False, verbose_name='(Кабель2) Активный')
	user2Kbalance = models.FloatField(verbose_name='(Кабель2) Баланс', default=0)
	user2Kcount = models.IntegerField(verbose_name='(Кабель2) Кол-во точек', default=0)

	operator = models.CharField(verbose_name='Кто делал перекидку', max_length=256, blank=True)
	comment = models.TextField(verbose_name='Комментарий', blank=True)
	date = models.DateTimeField(verbose_name='Дата и время перекидки', auto_now_add=True) 
	type_perekidka = models.CharField(verbose_name='"полная перекидка" или "перекидка баланса"', max_length=64, blank=True)

	internet1 = models.FloatField(verbose_name='Перекинуто с Интернет', default=0)
	kabel1 = models.FloatField(verbose_name=' Перекинуто с Кабель', default=0)
	alem1 = models.FloatField(verbose_name=' Перекинуто с Alem TV', default=0)
	telefon1 = models.FloatField(verbose_name='Перекинуто с Телефон', default=0)

	internet2 = models.FloatField(verbose_name='Получено на Интернет', default=0)
	kabel2 = models.FloatField(verbose_name=' Получено на Кабель', default=0)
	alem2 = models.FloatField(verbose_name=' Получено на Alem TV', default=0)
	telefon2 = models.FloatField(verbose_name='Получено на Телефон', default=0)

	def __str__(self):
		return f"c {self.user1Number} {self.user1Etrap} на {self.user2Number} {self.user2Etrap}"
	class Meta:
		verbose_name = 'Информация о перекидках New'
		verbose_name_plural = 'Информация о перекидках New'


class SnyatieInfo(models.Model):
	number = models.CharField(verbose_name='Номер', max_length=20, blank=True)
	etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)

	operator_galochka = models.CharField(verbose_name='Кто ставил галочку', max_length=500, blank=True)
	date_galochka = models.DateTimeField(verbose_name='Дата галочки', blank=True, null=True)
	namesurname1 = models.CharField(verbose_name='Абонент при галочки', max_length=1000, null=True, blank=True)

	operator_snyal = models.CharField(verbose_name='Кто снял абонента', max_length=500, blank=True)
	date_snyal = models.DateTimeField(verbose_name='Дата снятия', blank=True, null=True) 
	namesurname2 = models.CharField(verbose_name='Абонент при снятии', max_length=1000, null=True, blank=True)

	comment_galochka = models.TextField(verbose_name='Комментарий при галочки', blank=True, null=True)

	def __str__(self):
		return f"{self.number} {self.etrap}"
	class Meta:
		verbose_name = 'Информация о снятиях New'
		verbose_name_plural = 'Информация о снятиях New'


class PaysWithComment(models.Model):
    number = models.CharField(verbose_name='Номер', max_length=20, blank=True)
    etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)
    operator = models.CharField(verbose_name='Кто совершил платеж', max_length=256, blank=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    internet = models.FloatField(verbose_name='Платеж на Интернет', default=0)
    kabel = models.FloatField(verbose_name='Платеж на Кабель', default=0)
    alem = models.FloatField(verbose_name='Платеж на Alem TV', default=0)
    prochee = models.FloatField(verbose_name='Платеж на Телефон', default=0)
    date = models.DateTimeField(verbose_name='Когда сделали платеж', auto_now_add=True)
    date_pay = models.DateTimeField(verbose_name='на какую дату сделали платеж')
    pays_pk = models.CharField(verbose_name='pk платежа (для отмены)', max_length=256, blank=True)

    changed = models.BooleanField(default=False, verbose_name='Отменили?')
    when_changed = models.DateTimeField(verbose_name='когда отменили', blank=True, null=True)
    who_changed = models.CharField(verbose_name='Кто отменил', max_length=256, blank=True)
    changed_comment = models.TextField(verbose_name='Причина отмены', blank=True)

    def __str__(self):
        return f"Платеж {self.pays_pk} - {self.number} ({self.etrap})"

    class Meta:
        verbose_name = 'Платеж с комментарием'
        verbose_name_plural = 'Платежи с комментариями'


class NachWithComment(models.Model):
    number = models.CharField(verbose_name='Номер', max_length=20, blank=True)
    etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)
    operator = models.CharField(verbose_name='Кто сделал начисление', max_length=256, blank=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    internet = models.FloatField(verbose_name='Начислен на Интернет', default=0)
    kabel = models.FloatField(verbose_name='Начислен на Кабель', default=0)
    alem = models.FloatField(verbose_name='Начислен на Alem TV', default=0)
    prochee = models.FloatField(verbose_name='Начислен на prochee', default=0)
    telefon = models.FloatField(verbose_name='Начислен на telefon', default=0)
    slr = models.FloatField(verbose_name='Начислен на slr', default=0)
    kod = models.FloatField(verbose_name='Начислен на kod', default=0)
    zakaz = models.FloatField(verbose_name='Начислен на zakaz', default=0)
    dop_uslugi = models.FloatField(verbose_name='Начислен на dop_uslugi', default=0)

    date = models.DateTimeField(verbose_name='Когда сделали начисления', auto_now_add=True)
    year = models.CharField(max_length=100, verbose_name='Год')
    month = models.CharField(max_length=100, verbose_name='Месяц')

    def __str__(self):
        return f"Начисления {self.number} ({self.etrap})"

    class Meta:
        verbose_name = 'Начисления с комментарием'
        verbose_name_plural = 'Начисления с комментариями'

	
class CheckPaysWithKassirs(models.Model):
	etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)

	checked_kassir = models.CharField(verbose_name='Проверенный кассир', max_length=500, blank=True)

	# день проверки в формате '2024-01-01'
	checked_date = models.CharField(max_length=16, verbose_name='Какой день сверил', blank=True)

	day_is_closed = models.BooleanField(default=False, verbose_name='День Закрыт')
	who_close_the_day = models.CharField(verbose_name='Кто закрыл день', max_length=500, blank=True)

	operator = models.CharField(verbose_name='Кто Проверил', max_length=500, blank=True)
	date = models.DateTimeField(verbose_name='Когда проверил', auto_now_add=True) 
	comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

	total_telefon = models.FloatField(verbose_name='сумма телефонии', default=0)
	total_alem = models.FloatField(verbose_name='сумма Alem', default=0)
	total_internet = models.FloatField(verbose_name='сумма интернет', default=0)
	total_kabel = models.FloatField(verbose_name='сумма кабель', default=0)
	itogo_kassir = models.FloatField(verbose_name='itogo для этого кассира', default=0)

	total_telefon_when_closed_day = models.FloatField(verbose_name='сумма телефонии за весь день (при закрытии дня)', default=0)
	total_alem_when_closed_day = models.FloatField(verbose_name='сумма Alem за весь день (при закрытии дня)', default=0)
	total_internet_when_closed_day = models.FloatField(verbose_name='сумма интернет за весь день (при закрытии дня)', default=0)
	total_kabel_when_closed_day = models.FloatField(verbose_name='сумма кабель за весь день (при закрытии дня)', default=0)
	itogo_when_closed_day = models.FloatField(verbose_name='итого за весь день (при закрытии дня)', default=0)

	def __str__(self):
		return f"{self.etrap} {self.checked_date}"
	class Meta:
		verbose_name = 'Информация о сверках платежей'
		verbose_name_plural = 'Информация о сверках платежей'


# Сверка платежей Milli Billing - отдельная от CheckPaysWithKassirs (lanbilling), чтобы не путать источники
class CheckMilliBillingPaysWithKassirs(models.Model):
	etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)

	checked_kassir = models.CharField(verbose_name='Проверенный кассир', max_length=500, blank=True)

	# день проверки в формате '2024-01-01'
	checked_date = models.CharField(max_length=16, verbose_name='Какой день сверил', blank=True)

	day_is_closed = models.BooleanField(default=False, verbose_name='День Закрыт')
	who_close_the_day = models.CharField(verbose_name='Кто закрыл день', max_length=500, blank=True)

	operator = models.CharField(verbose_name='Кто Проверил', max_length=500, blank=True)
	date = models.DateTimeField(verbose_name='Когда проверил', auto_now_add=True)
	comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

	total_telefon = models.FloatField(verbose_name='сумма телефонии', default=0)
	total_alem = models.FloatField(verbose_name='сумма Alem', default=0)
	total_internet = models.FloatField(verbose_name='сумма интернет', default=0)
	total_kabel = models.FloatField(verbose_name='сумма кабель', default=0)
	itogo_kassir = models.FloatField(verbose_name='itogo для этого кассира', default=0)

	total_telefon_when_closed_day = models.FloatField(verbose_name='сумма телефонии за весь день (при закрытии дня)', default=0)
	total_alem_when_closed_day = models.FloatField(verbose_name='сумма Alem за весь день (при закрытии дня)', default=0)
	total_internet_when_closed_day = models.FloatField(verbose_name='сумма интернет за весь день (при закрытии дня)', default=0)
	total_kabel_when_closed_day = models.FloatField(verbose_name='сумма кабель за весь день (при закрытии дня)', default=0)
	itogo_when_closed_day = models.FloatField(verbose_name='итого за весь день (при закрытии дня)', default=0)

	def __str__(self):
		return f"{self.etrap} {self.checked_date}"

	class Meta:
		verbose_name = 'Информация о сверках платежей Milli Billing'
		verbose_name_plural = 'Информация о сверках платежей Milli Billing'


# таблица для сохранения инфы о том кто добавил платеж с Lan Billinga и кто ее начислил
class SaveInfoAboutWhoAddAndNachPaysFromBilling(models.Model):
	file_name = models.CharField(verbose_name='Название файла', max_length=500, blank=True)

	etrap_add = models.CharField(verbose_name='Этрап добавил', max_length=64, blank=True)
	who_add = models.CharField(verbose_name='Кто добавил', max_length=500, blank=True)
	when_add = models.DateTimeField(verbose_name='Когда добавил') 

	etrap_nach = models.CharField(verbose_name='Этрап начислили', max_length=64, blank=True)
	who_nach = models.CharField(verbose_name='Кто начислил', max_length=500, blank=True)
	when_nach = models.DateTimeField(verbose_name='Когда начислил', null=True, blank=True)


	# если удалю по их просьбе в CheckPays то вставить инфу о том что удалил
	is_delete = models.BooleanField(default=False, verbose_name='Удален')#
	comment = models.TextField(verbose_name='Комментарий по поводу удаления', null=True, blank=True)
	when_delete = models.DateTimeField(verbose_name='Когда удалил', null=True, blank=True)
	manager = models.CharField(verbose_name='manager платежей для удаления', max_length=500, blank=True)
	date_delete = models.CharField(verbose_name='Дата платежей для удаления', max_length=500, blank=True)

	def __str__(self):
		return f"{self.etrap_add} {self.who_add}"
	class Meta:
		verbose_name = 'Информация о том кто добавил и начислил платеж с LanBillinga'
		verbose_name_plural = 'Информация о том кто добавил и начислил платеж с LanBillinga'	



# class InfoAboutDeletedPaysFromCheckPaysPage(models.Model):
# 	file_name = models.CharField(verbose_name='Название файла', max_length=500, blank=True)
# 	when_delete = models.DateTimeField(verbose_name='Когда удалил', null=True, blank=True, auto_now_add=True)
# 	comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)


# 	def __str__(self):
# 		return f"{self.file_name}"
# 	class Meta:
# 		verbose_name = 'Информация о том какие платежи я удалил с страницы CheckPays'
# 		verbose_name_plural = 'Информация о том какие платежи я удалил с страницы CheckPays'	



	
# Тут будет инфо о сальдо и баланса на 31 декабря для отображения их в кассе если там выберится не текущий год (тогда можно будет не устанавливать программы за предыдущие годы а все будет в одном)
class SaldoBalancePoGodam(models.Model):
	etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)
	number = models.CharField(verbose_name='Номер', max_length=50, blank=True)
	year = models.CharField(max_length=4, verbose_name='Год', null=True, blank=True)

	surname = models.CharField(max_length=500, verbose_name='Фамилия/организация', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя/Отдел', blank=True)
	street = models.CharField(max_length=500, verbose_name='Улица', blank=True)
	home = models.CharField(max_length=500, verbose_name='Дом', blank=True)
	flat = models.CharField(max_length=500, verbose_name='Квартира', blank=True)

	service = models.ManyToManyField('AbonentService', verbose_name='Доп.Услуги (добавлять через ctrl)', blank=True)#
	abonplata = models.CharField(max_length=500,verbose_name='Абонплата', null=True, blank=True)#

	surname_k = models.CharField(max_length=500, verbose_name='Фамилия/организация Кабельное', blank=True)#
	name_k = models.CharField(max_length=500, verbose_name='Имя/Отдел Кабельное', blank=True)#
	street_k = models.CharField(max_length=500, verbose_name='Улица Кабельное', blank=True)#
	home_k = models.CharField(max_length=500, verbose_name='Дом Кабельное', blank=True)#
	flat_k = models.CharField(max_length=500, verbose_name='Квартира Кабельное', blank=True)#
	kabel_count = models.IntegerField(verbose_name='Кол-во точек', default=0)#
	is_active = models.BooleanField(default=False, verbose_name='Активный')#
	
	b_internet = models.FloatField(verbose_name=' Баланс Интернет', default=0)
	b_kabel = models.FloatField(verbose_name=' Баланс Кабель', default=0)
	b_alem = models.FloatField(verbose_name=' Баланс Alem TV', default=0)
	b_telefon = models.FloatField(verbose_name='Баланс Телефон', default=0)
	b_slr = models.FloatField(verbose_name='Баланс СЛР', default=0)
	b_kod = models.FloatField(verbose_name='Баланс Код', default=0)
	b_zakaz = models.FloatField(verbose_name='Баланс Заказ', default=0)
	b_prochee = models.FloatField(verbose_name='Баланс Прочее', default=0)
	b_dop_uslugi = models.FloatField(verbose_name='Баланс Доп. Услуги', default=0)

	s_internet = models.FloatField(verbose_name=' Сальдо Интернет', default=0)
	s_kabel = models.FloatField(verbose_name=' Сальдо Кабель', default=0)
	s_alem = models.FloatField(verbose_name=' Сальдо Alem TV', default=0)
	s_telefon = models.FloatField(verbose_name='Сальдо Телефон', default=0)
	s_slr = models.FloatField(verbose_name='Сальдо СЛР', default=0)
	s_kod = models.FloatField(verbose_name='Сальдо Код', default=0)
	s_zakaz = models.FloatField(verbose_name='Сальдо Заказ', default=0)
	s_prochee = models.FloatField(verbose_name='Сальдо Прочее', default=0)
	s_dop_uslugi = models.FloatField(verbose_name='Сальдо Доп. Услуги', default=0)

	def __str__(self):
		return f"{self.etrap} {self.number} {self.year}"
	class Meta:
		verbose_name = 'Информация о балансе и сальдо по годам'
		verbose_name_plural = 'Информация о балансе и сальдо по годам'


# Тут будет инфо о всех изменениях которые были в базе
class BazaChangeInfo(models.Model):
	etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)
	number = models.CharField(verbose_name='Номер', max_length=50, blank=True)
	comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
	operator = models.CharField(verbose_name='Кто изменил', max_length=500, blank=True)
	date = models.DateField(verbose_name='Дата изменения', auto_now_add=True) 
	akt_raport = models.CharField(verbose_name='Акт рапорт', max_length=1000, blank=True) 

	def __str__(self):
		return f"{self.etrap} {self.number}"
	class Meta:
		verbose_name = 'Информация об изменениях в База'
		verbose_name_plural = 'Информация об изменениях в База'


# Тут История перекидок начислений
class NachPerekidkaHistory(models.Model):
	user1Number = models.CharField(verbose_name='Номер абонента 1', max_length=64, blank=True)
	user1Etrap = models.CharField(verbose_name='Этрап абонента 1', max_length=64, blank=True)

	user2Number = models.CharField(verbose_name='Номер абонента 2', max_length=64, blank=True)
	user2Etrap = models.CharField(verbose_name='Этрап абонента 2', max_length=64, blank=True)

	operator = models.CharField(verbose_name='Кто делал перекидку', max_length=500, blank=True)
	comment = models.TextField(verbose_name='Комментарий', blank=True)
	date = models.DateTimeField(verbose_name='Дата и время перекидки', auto_now_add=True) 

	internet1 = models.FloatField(verbose_name='Перекинуто с Интернет', default=0)
	kabel1 = models.FloatField(verbose_name=' Перекинуто с Кабель', default=0)
	alem1 = models.FloatField(verbose_name=' Перекинуто с Alem TV', default=0)
	telefon1 = models.FloatField(verbose_name='Перекинуто с Телефон', default=0)
	slr1 = models.FloatField(verbose_name='Перекинуто с слр', default=0)
	kod1 = models.FloatField(verbose_name='Перекинуто с код', default=0)
	zakaz1 = models.FloatField(verbose_name='Перекинуто с заказ', default=0)
	prochee1 = models.FloatField(verbose_name='Перекинуто с прочее', default=0)
	dop_uslugi1 = models.FloatField(verbose_name='Перекинуто с доп услуги', default=0)

	internet2 = models.FloatField(verbose_name='Получено на Интернет', default=0)
	kabel2 = models.FloatField(verbose_name=' Получено на Кабель', default=0)
	alem2 = models.FloatField(verbose_name=' Получено на Alem TV', default=0)
	telefon2 = models.FloatField(verbose_name='Получено на Телефон', default=0)
	slr2 = models.FloatField(verbose_name='Перекинуто на слр', default=0)
	kod2 = models.FloatField(verbose_name='Перекинуто на код', default=0)
	zakaz2 = models.FloatField(verbose_name='Перекинуто на заказ', default=0)
	prochee2 = models.FloatField(verbose_name='Перекинуто на прочее', default=0)
	dop_uslugi2 = models.FloatField(verbose_name='Перекинуто на доп услуги', default=0)

	def __str__(self):
		return f"c {self.user1Number} {self.user1Etrap} на {self.user2Number} {self.user2Etrap} {self.operator}"
	class Meta:
		verbose_name = 'Информация о перекидках начислений New'
		verbose_name_plural = 'Информация о перекидках начислений New'

		
class AccountName(models.Model):
	etrap = models.CharField(max_length=32,verbose_name='Этрап', null=True, blank=True)
	account = models.CharField(max_length=500, verbose_name='Счёт', blank=True, null=True)
	accountName = models.CharField(max_length=1000,verbose_name='Имя счет №', null=True, blank=True)
	accountAdress = models.CharField(max_length=1000,verbose_name='Адрес счет №', null=True, blank=True)

	def __str__(self):
		return f"{self.etrap} {self.account} {self.accountName} {self.accountAdress}"
	class Meta:
		verbose_name = 'БД для Счет №'
		verbose_name_plural = 'БД для Счет №'


# чтобы не было повторных начислений и/или добовлений
# В DontRepeatYourself Начисления для  kodSlrFileNachisleniya нет так как инфа о их начислениях хранится в dbfNameList
class DontRepeatYourself(models.Model):

	# При добавлении с xlsx
	internetPlatejiXlsxName = models.CharField(max_length=500,verbose_name='Добавленный xlsx файл имени внешние интернет платежи в нашу БД', null=True, blank=True)
	internetNachisleniyaXlsxName = models.CharField(max_length=500,verbose_name='Добавленный xlsx файл имени интернет начисления в нашу БД', null=True, blank=True)
	alemNachisleniyaXlsxName = models.CharField(max_length=500,verbose_name='Добавленный xlsx файл имени alem начисления в нашу БД', null=True, blank=True)

	# '2023Март' Информация о том за какие месяцы былы начисления
	slrNachisleniyaYearMonth = models.CharField(max_length=500,verbose_name='Начисленный Год и Месяц для СЛР', null=True, blank=True)
	kodNachisleniyaYearMonth = models.CharField(max_length=500,verbose_name='Начисленный Год и Месяц для КОД', null=True, blank=True)

	# '2023МартDashoguz'
	dopUslugiNachisleniyaYearMonthEtrap = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц и этрап для Доп. Услуги', null=True, blank=True)
	KabelNachisleniaYearMonthEtrap = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц и этрап для Kabel TV', null=True, blank=True)
	abonplataNachisleniaYearMonthEtrap = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц и этрап для Абонплата', null=True, blank=True)
	# metrNachisleniaYearMonthEtrap = models.CharField(max_length=32,verbose_name='Начисленный Год, Месяц и этрап для Метров', null=True, blank=True)
	zakazNachisleniaYearMonthEtrap = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц и этрап для Заказных звонков', null=True, blank=True)

	# '2023МартDashoguzON' При начислении xlsx
	platejiNachisleniyaYearMonthEtrapONOFF = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц, Этрап  и ON/OFF Внешние платежи', null=True, blank=True)
	internetNachisleniyaYearMonthEtrapONOFF = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц, Этрап  и ON/OFF Интернет начисления', null=True, blank=True)
	alemNachisleniyaYearMonthEtrapONOFF = models.CharField(max_length=500,verbose_name='Начисленный Год, Месяц, Этрап  и ON/OFF Alem начисления', null=True, blank=True)

	# plateji s kassy kassirami
	platejiSkassyKassirami = models.CharField(max_length=500,verbose_name='гггг-мм-дд  Платежи с файла биллинга в нашу кассу кассирами', null=True, blank=True)
	
	def __str__(self):
		return f"{self.internetPlatejiXlsxName} {self.slrNachisleniyaYearMonth} {self.kodNachisleniyaYearMonth} {self.platejiNachisleniyaYearMonthEtrapONOFF} {self.internetNachisleniyaXlsxName} {self.internetNachisleniyaYearMonthEtrapONOFF} {self.dopUslugiNachisleniyaYearMonthEtrap} {self.alemNachisleniyaXlsxName} {self.KabelNachisleniaYearMonthEtrap} {self.abonplataNachisleniaYearMonthEtrap} {self.zakazNachisleniaYearMonthEtrap} {self.alemNachisleniyaYearMonthEtrapONOFF} {self.platejiSkassyKassirami}"
	
	class Meta:
		verbose_name = 'Чтобы не было повторных начислений и/или добовлений'
		verbose_name_plural = 'Чтобы не было повторных начислений и/или добовлений'

# class AbonentBeneficiary(models.Model):
# 	beneficiary = models.CharField(max_length=32, verbose_name='Льгота')
# 	percent = models.IntegerField(verbose_name='Скидка %')
# 	def __str__(self):
# 		return f"{self.beneficiary}; {str(self.percent)}%"

# 	class Meta:
# 		verbose_name = 'Льгота'
# 		verbose_name_plural = 'Льготы'


class HozOrBudjet(models.Model):
	name = models.CharField(max_length=1, verbose_name='Хоз/Бюджет?')
	percent = models.IntegerField(verbose_name='процент скидки')

	def __unicode__(self):
		return self.name

	def __str__(self):
		return f"{self.name} : {str(self.percent)} %"

	class Meta:
		verbose_name = 'Хоз или Бюджет'
		verbose_name_plural = 'Хоз или Бюджет'

"""#######################
   Основные таблицы END ##
"""#######################
"""##########
    Услуги ##
"""##########

class InternetTarif(models.Model):
	tarif = models.CharField(max_length=500, verbose_name='Скорость тарифа mb/s')
	price = models.FloatField(verbose_name='Цена тарифа manat', null=True, blank=True)

	def __str__(self):
		return f"{self.tarif}m/s; {str(self.price)} TMT"

	class Meta:
		verbose_name = 'Интернет тариф'
		verbose_name_plural = 'Интернет тарифы'


# class AbonentNumbersCount(models.Model):
# 	count_of_numbers = models.IntegerField(verbose_name='Количество номеров')
# 	price = models.FloatField(verbose_name='Цена')
# 	def __str__(self):
# 		return f"{str(self.count_of_numbers)} шт; {str(self.price)} TMT"

# 	class Meta:
# 		verbose_name = 'Кол-во номеров'
# 		verbose_name_plural = 'Кол-во номеров'


# class AbonLength(models.Model):
# 	metr = models.CharField(max_length=16, verbose_name='Метры')
# 	price = models.FloatField(verbose_name='Цена', null=True, blank=True)

# 	def __str__(self):
# 		return f"{self.metr} metr; {str(self.price)} TMT"

# 	class Meta:
# 		verbose_name = 'Кабель Метры'
# 		verbose_name_plural = 'Кабель Метры'


class AbonentService(models.Model):
	service = models.CharField(max_length=1024, verbose_name='Услуга')
	price = models.FloatField(verbose_name='Цена')
	def __str__(self):
		return str(self.pk) + ': ' + self.service + ' :' + str(self.price) + 'м'

	class Meta:
		verbose_name = 'Услуги'
		verbose_name_plural = 'Услуги'


class KabelCount(models.Model):
	kabel_count = models.IntegerField(verbose_name='Кол-во точек кабеля')
	price = models.FloatField(verbose_name='Цена', null=True, blank=True)
	def __str__(self):
		return f"{self.kabel_count} шт; {str(self.price)} TMT"

	class Meta:
		verbose_name = 'Кол-во кабель TV'
		verbose_name_plural = 'Кол-во кабель TV'


class AlemCount(models.Model):
	alem_count = models.IntegerField(verbose_name='Кол-во Alem TV')
	price = models.FloatField(verbose_name='Цена', null=True, blank=True)
	def __str__(self):
		return f"{self.alem_count} шт; {str(self.price)} TMT"

	class Meta:
		verbose_name = 'Кол-во Alem TV'
		verbose_name_plural = 'Кол-во Alem TV'

"""##############
    Услуги END ##
"""##############
"""#########
    Касса ##
"""#########

ilat_edara = (
        (None, 'ФЛ или ЮЛ'),
        ('ФЛ', 'ФЛ'),
        ('ЮЛ', 'ЮЛ'),
)

wn_or_default = (
        (None, 'Внешние платежи или default (кассир)'),
        ('Внешние платежи', 'Внешние платежи'),
        ('Default', 'Default'),
        ('MATB', 'MATB'),
)

# Квитанция (чек)
class PayHistory(models.Model):
	abonent = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Абонент')

	internet = models.FloatField(verbose_name='Интернет', default=0)
	kabel = models.FloatField(verbose_name='Кабель', default=0)
	alem = models.FloatField(verbose_name='Alem TV', default=0)
	telefon = models.FloatField(verbose_name='Телефон', default=0)
	slr = models.FloatField(verbose_name='СЛР', default=0)
	kod = models.FloatField(verbose_name='Код', default=0)
	zakaz = models.FloatField(verbose_name='Заказ', default=0)
	prochee = models.FloatField(verbose_name='Прочее', default=0)
	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)
	
	is_card = models.BooleanField(default=False, verbose_name='Карт?', blank=True)

	# кассир, банк, app toleg и т.п.
	kassir = models.CharField(max_length=500, verbose_name='Кассир')

	kassa = models.CharField(max_length=500, verbose_name='Касса №', null=True, blank=True)

	total = models.FloatField(verbose_name='Вклад', null=True, blank=True)

	date = models.DateTimeField(verbose_name="Дата и время оплаты")

	edara_ilat = models.CharField(max_length=8, verbose_name='ФЛ или ЮЛ', null=True, blank=True, choices=ilat_edara)

	# Внешние платежи или default (кассир)
	type = models.CharField(max_length=128, verbose_name='Внешние платежи или Default (кассир)', null=True, blank=True, choices=wn_or_default)

	# Кассир etrap
	kassir_etrap = models.CharField(max_length=32, verbose_name='etrap кассира', null=True, blank=True, choices=etraps)

	# Если начислено из MilliBillingPay - хранит file_name, для точного отката начисления
	milli_billing_file_name = models.CharField(max_length=500, verbose_name='Файл Milli Billing', blank=True, null=True)

	def __str__(self):
		return f"{self.abonent.number} {self.abonent.etrap} {self.abonent.name} {self.abonent.surname}"

	class Meta:
		verbose_name = 'История оплат'
		verbose_name_plural = 'История оплат'


"""#############
    Касса END ##
"""#############
"""############
    Interpay ##
"""############
class InterpayBilling(models.Model):
	pay_history = models.ForeignKey('PayHistory', on_delete=models.SET_NULL, verbose_name='Абонент', null=True)

	is_checked_internet = models.BooleanField(default=False, verbose_name='Переведено? Интернет', blank=True)
	is_checked_alem = models.BooleanField(default=False, verbose_name='Переведено? Alem TV', blank=True)
	is_checked_telefon = models.BooleanField(default=False, verbose_name='Переведено? Абонплата', blank=True)

	billing_date_total = models.DateTimeField(verbose_name='Дата перевода в биллинг все', null=True, blank=True)
	operator = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Оператор', null=True, blank=True)

	def __str__(self):
		return f"{str(self.billing_date_total)}"

	class Meta:
		verbose_name = 'Интернет биллинг'
		verbose_name_plural = 'Интернет биллинг'


class InterpayPerekidkaBilling(models.Model):
	# abonent = models.ForeignKey(UserTable, on_delete=models.SET_NULL, verbose_name='Абонент', null=True, blank=True)

	mtbUsername = models.CharField(max_length=500, verbose_name='MTB соотрудик', null=True, blank=True)
	mtbEtrap = models.CharField(max_length=64, verbose_name='MTB соотрудик этрап', choices= etraps, null=True, blank=True)

	number1 = models.CharField(max_length=16, verbose_name='Номер 1', null=True, blank=True)
	etrap1 = models.CharField(max_length=32, verbose_name='Этрап 1', choices= etraps, null=True, blank=True)
	name1 = models.CharField(max_length=500, verbose_name='Имя 1', null=True, blank=True)
	surname1 = models.CharField(max_length=500, verbose_name='Фамилия 1', null=True, blank=True)
	abonent1_pk = models.CharField(max_length=16, verbose_name='pk abonent1', null=True, blank=True)


	number2 = models.CharField(max_length=16, verbose_name='Номер 2', null=True, blank=True)
	etrap2 = models.CharField(max_length=32, verbose_name='Этрап 2', choices= etraps, null=True, blank=True)
	name2 = models.CharField(max_length=500, verbose_name='Имя 2', null=True, blank=True)
	surname2 = models.CharField(max_length=500, verbose_name='Фамилия 2', null=True, blank=True)
	abonent2_pk = models.CharField(max_length=16, verbose_name='pk abonent2', null=True, blank=True)

	internet1 = models.FloatField(verbose_name='Интернет1', default=0)
	kabel1 = models.FloatField(verbose_name='Кабель1', default=0)
	alem1 = models.FloatField(verbose_name='Alem TV1', default=0)
	telefon1 = models.FloatField(verbose_name='Телефон1', default=0)
	slr1 = models.FloatField(verbose_name='СЛР1', default=0)
	kod1 = models.FloatField(verbose_name='Код1', default=0)
	zakaz1 = models.FloatField(verbose_name='Заказ1', default=0)
	prochee1 = models.FloatField(verbose_name='Прочее1', default=0)
	dop_uslugi1 = models.FloatField(verbose_name='Доп. Услуги1', default=0)

	internet2 = models.FloatField(verbose_name='Интернет2', default=0)
	kabel2 = models.FloatField(verbose_name='Кабель2', default=0)
	alem2 = models.FloatField(verbose_name='Alem TV2', default=0)
	telefon2 = models.FloatField(verbose_name='Телефон2', default=0)
	slr2 = models.FloatField(verbose_name='СЛР2', default=0)
	kod2 = models.FloatField(verbose_name='Код2', default=0)
	zakaz2 = models.FloatField(verbose_name='Заказ2', default=0)
	prochee2 = models.FloatField(verbose_name='Прочее2', default=0)
	dop_uslugi2 = models.FloatField(verbose_name='Доп. Услуги2', default=0)


	is_checked_internet1 = models.BooleanField(default=False, verbose_name='Переведено? Интернет1', blank=True)
	is_checked_alem1 = models.BooleanField(default=False, verbose_name='Переведено? Alem TV1', blank=True)
	is_checked_abonplata1 = models.BooleanField(default=False, verbose_name='Переведено? Абонплата1', blank=True)

	is_checked_internet2 = models.BooleanField(default=False, verbose_name='Переведено? Интернет2', blank=True)
	is_checked_alem2 = models.BooleanField(default=False, verbose_name='Переведено? Alem TV2', blank=True)
	is_checked_abonplata2 = models.BooleanField(default=False, verbose_name='Переведено? Абонплата2', blank=True)

	date = models.DateTimeField(verbose_name='Дата перекидки в PyView', null=True, blank=True)

	perekidka_date = models.DateTimeField(verbose_name='Дата перекидки в биллинг', null=True, blank=True)
	operator = models.CharField(max_length=500, verbose_name='Оператор который перекинул в billing', null=True, blank=True)


	def __str__(self):
		return f"{self.number1} {self.etrap1} {self.name1} {self.surname1}"

	class Meta:
		verbose_name = 'Перекидка биллинг'
		verbose_name_plural = 'Перекидка биллинг'

# class DeletedPay(models.Model):
# 	abonent = models.ForeignKey(UserTable, on_delete=models.SET_NULL, verbose_name='Оператор', null=True, blank=True)

# 	internet = models.FloatField(verbose_name='Интернет', default=0)
# 	kabel = models.FloatField(verbose_name='Кабель', default=0)
# 	alem = models.FloatField(verbose_name='Alem TV', default=0)
# 	telefon = models.FloatField(verbose_name='Телефон', default=0)
# 	slr = models.FloatField(verbose_name='СЛР', default=0)
# 	kod = models.FloatField(verbose_name='Код', default=0)
# 	zakaz = models.FloatField(verbose_name='Заказ', default=0)
# 	prochee = models.FloatField(verbose_name='Прочее', default=0)
# 	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)

InternetTarifaction = (
        ('подключения итернета', 'подключения итернета'),
        ('отключения итернета', 'отключения итернета'),
        ('смена интернет тарифа', 'смена интернет тарифа'),

)

"""################
    Interpay END ##
"""################

"""#######
    DBF ##
"""#######

class LocalCall(models.Model):
	etrap = models.CharField(max_length=100,verbose_name='Этрап')
	SUB_A =  models.CharField(max_length=100,verbose_name='SUB_A номер')
	SUB_B = models.CharField(max_length=100,verbose_name='SUB_B номер')

	DATE = models.DateField(verbose_name="Дата звонка")
	START = models.CharField(max_length=100,verbose_name='Начало звонка')
	FIN = models.CharField(max_length=100,verbose_name='Конец звонка')
	DUR = models.CharField(max_length=100,verbose_name='Длительность звонка')
	MT = models.CharField(max_length=100,verbose_name='Общее минут разговора')

	file_name = models.CharField(max_length=500,verbose_name='Названия файла')

	edara = models.CharField(max_length=500,verbose_name='H, B, или I', blank=True)

	def __str__(self):
		return f"{self.etrap} {self.SUB_A} {self.SUB_B} {self.DATE} {self.START} {self.FIN} {self.DUR} {self.MT}"

	class Meta:
		verbose_name = 'Звонки локальные'
		verbose_name_plural = 'Звонки локальные'


class NonLocalCall(models.Model):
	SUB_A_etrap = models.CharField(max_length=500,verbose_name='SUB_A этрап')
	SUB_A = models.CharField(max_length=500,verbose_name='SUB_A номер')

	SUB_B_locations = models.CharField(max_length=500,verbose_name='SUB_B Город/Страна')
	SUB_B = models.CharField(max_length=500,verbose_name='SUB_B номер')

	type = models.CharField(max_length=16,verbose_name='Междугород или международный звонок')

	price = models.FloatField(verbose_name="Цена за минуту")

	DATE = models.DateField(verbose_name="Дата звонка")
	START = models.CharField(max_length=500,verbose_name='Начало звонка')
	FIN = models.CharField(max_length=500,verbose_name='Конец звонка')
	DUR = models.CharField(max_length=500,verbose_name='Длительность звонка')
	MT = models.CharField(max_length=500,verbose_name='Общее минут разговора')

	total_price = models.FloatField(verbose_name="Общая цена разговора")

	file_name = models.CharField(max_length=500,verbose_name='Названия файла')

	edara = models.CharField(max_length=500,verbose_name='H, B, или I', blank=True)

	def __str__(self):
		return f"{self.SUB_A_etrap} {self.SUB_A} {self.SUB_B_locations} {self.SUB_B} {self.type} {self.price} {self.DATE} {self.START} {self.FIN} {self.DUR} {self.MT} {self.total_price}"

	class Meta:
		verbose_name = 'Звонки междугородние и международные'
		verbose_name_plural = 'Звонки междугородние и международные'


# Для инфы о том начислен ли DBF файл или нет
class dbfNameList(models.Model):
	name = models.CharField(max_length=500, verbose_name='Названия DBF файла')
	is_nach = models.BooleanField(verbose_name='Начислен', default=False)

	def __str__(self):
		return f"{self.pk} {self.name} {self.is_nach}"
	
	class Meta:
		verbose_name = 'Список имен добавленных DBF файлов (для проверки начислен или нет)'
		verbose_name_plural = 'Список имен добавленных DBF файлов (для проверки начислен или нет)'


# Цены всех начислений для отчета
class NachisleniyaOtchet(models.Model):
	etrap = models.CharField(max_length=32, choices= etraps, null=True, blank=True)
	year = models.CharField(max_length=4, verbose_name='Год', null=True, blank=True)
	month = models.CharField(max_length=16, verbose_name='Месяц', null=True, blank=True)

	abonplataNachN = models.FloatField(verbose_name='Абонплата начисления для населения', default=0)
	abonplataNachP = models.FloatField(verbose_name='Абонплата начисления для Предприятия', default=0)

	kabelNachN = models.FloatField(verbose_name='Кабель начисления для населения', default=0)
	kabelNachP = models.FloatField(verbose_name='Кабель начисления для Предприятия', default=0)

	WneshniyePlatejiInternet  = models.FloatField(verbose_name='Внешние платежи Интернет', default=0)
	WneshniyePlatejiAlem = models.FloatField(verbose_name='Внешние платежи Alem TV', default=0)
	WneshniyePlatejiAbonplata = models.FloatField(verbose_name='Внешние платежи Абонплата (начислянтся в прочее, а потом распределяется)', default=0)
	# # Колонки оплаченные с прочее
	# fromProcheePay_abonplata = models.FloatField(verbose_name='Абонплата оплаченная с прочее', default=0)
	# fromProcheePay_slr = models.FloatField(verbose_name='Слр оплаченный с прочее', default=0)
	# fromProcheePay_kod = models.FloatField(verbose_name='Код оплаченный с прочее', default=0)
	# fromProcheePay_zakaz = models.FloatField(verbose_name='Заказ оплаченный с прочее', default=0)
	# fromProcheePay_uslugi = models.FloatField(verbose_name='Доп. услуги оплаченные с прочее', default=0)
	
	# WneshniyePlatejiSlr = models.FloatField(verbose_name='Внешние платежи СЛР', default=0)
	# WneshniyePlatejiKod = models.FloatField(verbose_name='Внешние платежи КОД', default=0)
	# WneshniyePlatejiZakaz = models.FloatField(verbose_name='Внешние платежи Заказ', default=0)
	# WneshniyePlatejiProchee = models.FloatField(verbose_name='Внешние платежи Прочее', default=0)
	# WneshniyePlatejiDop_uslugi = models.FloatField(verbose_name='Внешние платежи Доп. Услуги', default=0)


	# Начисления при удалении/окл/вкл кабель TV в Abon - отделе # Пока не надо
	# kabelServiceNachisleniya = models.FloatField(verbose_name='Кабель Начисления с абон-отдела или MATB при подключении', default=0)
	
	# kabelMatbNachisleniya = models.FloatField(verbose_name='Кабель Начисления при месячном начислении', default=0)

	# Плюс баланса при изменении кабель TV c большого тарифа на меланького
	# kabelServiceNachisleniya = models.FloatField(verbose_name='Кабель Начисления с абон-отдела', default=0)

	# №№№
	perek_edara_debit_plus = models.FloatField(verbose_name='Перекидка на edara Дебит (-)', default=0)
	perek_edara_kredit_plus = models.FloatField(verbose_name='Перекидка на edara Кредит (+)', default=0)

	perek_nasel_debit_plus = models.FloatField(verbose_name='Перекидка на населения Дебит (-)', default=0)
	perek_nasel_kredit_plus = models.FloatField(verbose_name='Перекидка на населения Кредит (+)', default=0)

	perek_edara_debit_minus = models.FloatField(verbose_name='Перекидка c edara Дебит (-)', default=0)
	perek_edara_kredit_minus = models.FloatField(verbose_name='Перекидка c edara Кредит (+)', default=0)

	perek_nasel_debit_minus = models.FloatField(verbose_name='Перекидка c населения Дебит (-)', default=0)
	perek_nasel_kredit_minus = models.FloatField(verbose_name='Перекидка c населения Кредит (+)', default=0)

	# perek_edaraPlus = models.FloatField(verbose_name='Перекидка edara плюс', default=0)
	# perek_naselPlus = models.FloatField(verbose_name='Перекидка населения плюс', default=0)
	# perek_edaraMinus = models.FloatField(verbose_name='Перекидка edara минус', default=0)
	# perek_naselMinus = models.FloatField(verbose_name='Перекидка населения минус', default=0)
	# №№№#

	intetnetNachisleniya = models.FloatField(verbose_name='Интернет начисления', default=0)
	alemNachisleniya = models.FloatField(verbose_name='Alem начисления', default=0)
	zakazNachisleniya = models.FloatField(verbose_name='Заказ начисления', default=0)
	# abonplataNachisleniya = models.FloatField(verbose_name='Абонплата начисления при месячном начислении', default=0)
	# metrNachisleniya = models.FloatField(verbose_name='Метры начисления при месячном начислении', default=0)
	kodNachisleniya = models.FloatField(verbose_name='Код начисления', default=0)
	slrNachisleniya = models.FloatField(verbose_name='Слр начисления', default=0)
	procheeNachisleniya = models.FloatField(verbose_name='Прочее начисления', default=0)
	# Тут начисления которые были начислены при добавлении услуг (начисляется по дням)
	serviceSeparateNachisleniya = models.FloatField(verbose_name='Доп услуги начисления (по дням) которые были добавлены в абон-отделе', default=0)
	# а тут обычное начисление
	serviceNachisleniya = models.FloatField(verbose_name='Доп услуги начисления', default=0)

	# Инфа о перекидках
	internetM = models.FloatField(verbose_name='Вычтено с Интернета', default=0)
	kabelM = models.FloatField(verbose_name='Вычтено с Кабель', default=0)
	alemM = models.FloatField(verbose_name='Вычтено с Alem TV', default=0)
	telefonM = models.FloatField(verbose_name='Вычтено с Телефон', default=0)
	slrM = models.FloatField(verbose_name='Вычтено с СЛР', default=0)
	kodM = models.FloatField(verbose_name='Вычтено с Код', default=0)
	zakazM = models.FloatField(verbose_name='Вычтено с Заказ', default=0)
	procheeM = models.FloatField(verbose_name='Вычтено с Прочее', default=0)
	dop_uslugiM = models.FloatField(verbose_name='Вычтено с Доп. Услуги', default=0)

	internetP = models.FloatField(verbose_name='Добавлено в Интернет', default=0)
	kabelP = models.FloatField(verbose_name='Добавлено в Кабель', default=0)
	alemP = models.FloatField(verbose_name='Добавлено в Alem TV', default=0)
	telefonP = models.FloatField(verbose_name='Добавлено в Телефон', default=0)
	slrP = models.FloatField(verbose_name='Добавлено в СЛР', default=0)
	kodP = models.FloatField(verbose_name='Добавлено в Код', default=0)
	zakazP = models.FloatField(verbose_name='Добавлено в Заказ', default=0)
	procheeP = models.FloatField(verbose_name='Добавлено в Прочее', default=0)
	dop_uslugiP = models.FloatField(verbose_name='Добавлено в Доп. Услуги', default=0)

	# При автоперекидке с прочего на минусные поля (абон, слр, код, заказ, прочее, доп.Услуги)
	sProWabon = models.FloatField(verbose_name='С прочего в абон (auto)', default=0)
	sProWslr = models.FloatField(verbose_name='С прочего в slr (auto)', default=0)
	sProWkod = models.FloatField(verbose_name='С прочего в kod (auto)', default=0)
	sProWzakaz = models.FloatField(verbose_name='С прочего в zakaz (auto)', default=0)
	sProWdop_uslugi = models.FloatField(verbose_name='С прочего в Доп Услуги (auto)', default=0)





	# # сколько манат минус с баланса при снятии абонента
	# internet_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Интернета при снятии', default=0)
	# kabel_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Кабель при снятии', default=0)
	# alem_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Alem TV при снятии', default=0)
	# telefon_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Телефон при снятии', default=0)
	# slr_minus_when_snyat = models.FloatField(verbose_name='Вычтено с СЛР при снятии', default=0)
	# kod_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Код при снятии', default=0)
	# zakaz_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Заказ при снятии', default=0)
	# prochee_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Прочее при снятии', default=0)
	# dop_uslugi_minus_when_snyat = models.FloatField(verbose_name='Вычтено с Доп. Услуги при снятии', default=0)

	# # сколько манат плюс в баланс при востановлении снятых номеров абонента
	# internet_plus_when_wost = models.FloatField(verbose_name='Добавлено в Интернет при востановлении номера', default=0)
	# kabel_plus_when_wost = models.FloatField(verbose_name='Добавлено в Кабель при востановлении номера', default=0)
	# alem_plus_when_wost = models.FloatField(verbose_name='Добавлено в Alem TV при востановлении номера', default=0)
	# telefon_plus_when_wost = models.FloatField(verbose_name='Добавлено в Телефон при востановлении номера', default=0)
	# slr_plus_when_wost = models.FloatField(verbose_name='Добавлено в СЛР при востановлении номера', default=0)
	# kod_plus_when_wost = models.FloatField(verbose_name='Добавлено в Код при востановлении номера', default=0)
	# zakaz_plus_when_wost = models.FloatField(verbose_name='Добавлено в Заказ при востановлении номера', default=0)
	# prochee_plus_when_wost = models.FloatField(verbose_name='Добавлено в Прочее при востановлении номера', default=0)
	# dop_uslugi_plus_when_wost = models.FloatField(verbose_name='Добавлено в Доп. Услуги при востановлении номера', default=0)



	def __str__(self):
		return f"{self.pk} {self.etrap} {self.year} {self.month} {self.WneshniyePlatejiInternet} {self.WneshniyePlatejiAlem} {self.year} {self.WneshniyePlatejiAbonplata} {self.intetnetNachisleniya} {self.kodNachisleniya} {self.slrNachisleniya} {self.procheeNachisleniya} {self.serviceSeparateNachisleniya}"	

	class Meta:
		unique_together = ["etrap", "year", "month"]
		verbose_name = 'Информация о всех начислений за месяц'
		verbose_name_plural = 'Информация о всех начислений за месяц'

# Каждый месяц 1-го числа во время 1-го открытия кассы сюда сохраняется текущий баланс
class MonthBalance(models.Model):
	year = models.CharField(max_length=4, verbose_name='Год')
	month = models.CharField(max_length=16, verbose_name='Месяц')
	etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап")

	internetPlus = models.FloatField(verbose_name='Интернет Plus', default=0)
	kabelPlus = models.FloatField(verbose_name='Кабель Plus', default=0)
	alemPlus = models.FloatField(verbose_name='Alem TV Plus', default=0)
	telefonPlus = models.FloatField(verbose_name='Телефон Plus', default=0)
	slrPlus = models.FloatField(verbose_name='СЛР Plus', default=0)
	kodPlus = models.FloatField(verbose_name='Код Plus', default=0)
	zakazPlus = models.FloatField(verbose_name='Заказ Plus', default=0)
	procheePlus = models.FloatField(verbose_name='Прочее Plus', default=0)
	dop_uslugiPlus = models.FloatField(verbose_name='Доп. Услуги Plus', default=0)

	internetMinus = models.FloatField(verbose_name='Интернет Minus', default=0)
	kabelMinus = models.FloatField(verbose_name='Кабель Minus', default=0)
	alemMinus = models.FloatField(verbose_name='Alem TV Minus', default=0)
	telefonMinus = models.FloatField(verbose_name='Телефон Minus', default=0)
	slrMinus = models.FloatField(verbose_name='СЛР Minus', default=0)
	kodMinus = models.FloatField(verbose_name='Код Minus', default=0)
	zakazMinus = models.FloatField(verbose_name='Заказ Minus', default=0)
	procheeMinus = models.FloatField(verbose_name='Прочее Minus', default=0)
	dop_uslugiMinus = models.FloatField(verbose_name='Доп. Услуги Minus', default=0)

	# internetPlusArhiw = models.FloatField(verbose_name='Интернет Plus Arhiw', default=0)
	# kabelPlusArhiw = models.FloatField(verbose_name='Кабель Plus Arhiw', default=0)
	# alemPlusArhiw = models.FloatField(verbose_name='Alem TV Plus Arhiw', default=0)
	# telefonPlusArhiw = models.FloatField(verbose_name='Телефон Plus Arhiw', default=0)
	# slrPlusArhiw = models.FloatField(verbose_name='СЛР Plus Arhiw', default=0)
	# kodPlusArhiw = models.FloatField(verbose_name='Код Plus Arhiw', default=0)
	# zakazPlusArhiw = models.FloatField(verbose_name='Заказ Plus Arhiw', default=0)
	# procheePlusArhiw = models.FloatField(verbose_name='Прочее Plus Arhiw', default=0)
	# dop_uslugiPlusArhiw = models.FloatField(verbose_name='Доп. Услуги Plus Arhiw', default=0)

	# internetMinusArhiw = models.FloatField(verbose_name='Интернет Minus Arhiw', default=0)
	# kabelMinusArhiw = models.FloatField(verbose_name='Кабель Minus Arhiw', default=0)
	# alemMinusArhiw = models.FloatField(verbose_name='Alem TV Minus Arhiw', default=0)
	# telefonMinusArhiw = models.FloatField(verbose_name='Телефон Minus Arhiw', default=0)
	# slrMinusArhiw = models.FloatField(verbose_name='СЛР Minus Arhiw', default=0)
	# kodMinusArhiw = models.FloatField(verbose_name='Код Minus Arhiw', default=0)
	# zakazMinusArhiw = models.FloatField(verbose_name='Заказ Minus Arhiw', default=0)
	# procheeMinusArhiw = models.FloatField(verbose_name='Прочее Minus Arhiw', default=0)
	# dop_uslugiMinusArhiw = models.FloatField(verbose_name='Доп. Услуги Minus Arhiw', default=0)

	class Meta:
		# unique_together = ["etrap", "year", "month"]
		verbose_name = 'Баланс каждого месяца за все время'
		verbose_name_plural = 'Баланс каждого месяца за все время'

# class MonthBalanceRezerw(models.Model):
# 	year = models.CharField(max_length=4, verbose_name='Год')
# 	month = models.CharField(max_length=16, verbose_name='Месяц')
# 	etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап")

# 	internetPlus = models.FloatField(verbose_name='Интернет Plus', default=0)
# 	kabelPlus = models.FloatField(verbose_name='Кабель Plus', default=0)
# 	alemPlus = models.FloatField(verbose_name='Alem TV Plus', default=0)
# 	telefonPlus = models.FloatField(verbose_name='Телефон Plus', default=0)
# 	slrPlus = models.FloatField(verbose_name='СЛР Plus', default=0)
# 	kodPlus = models.FloatField(verbose_name='Код Plus', default=0)
# 	zakazPlus = models.FloatField(verbose_name='Заказ Plus', default=0)
# 	procheePlus = models.FloatField(verbose_name='Прочее Plus', default=0)
# 	dop_uslugiPlus = models.FloatField(verbose_name='Доп. Услуги Plus', default=0)

# 	internetMinus = models.FloatField(verbose_name='Интернет Minus', default=0)
# 	kabelMinus = models.FloatField(verbose_name='Кабель Minus', default=0)
# 	alemMinus = models.FloatField(verbose_name='Alem TV Minus', default=0)
# 	telefonMinus = models.FloatField(verbose_name='Телефон Minus', default=0)
# 	slrMinus = models.FloatField(verbose_name='СЛР Minus', default=0)
# 	kodMinus = models.FloatField(verbose_name='Код Minus', default=0)
# 	zakazMinus = models.FloatField(verbose_name='Заказ Minus', default=0)
# 	procheeMinus = models.FloatField(verbose_name='Прочее Minus', default=0)
# 	dop_uslugiMinus = models.FloatField(verbose_name='Доп. Услуги Minus', default=0)

		
	class Meta:
		unique_together = ["etrap", "year", "month"]
		verbose_name = ' Резерв баланс каждого месяца за все время'
		verbose_name_plural = 'Резерв баланс каждого месяца за все время'

"""###########
    DBF END ##
"""###########

"""######################################
    Import Excell Data to Our DataBase ##
"""######################################

	
class ImportInternetPlateji(models.Model):
	type = models.CharField(max_length=32, verbose_name='Способ оплаты')
	pay_date = models.DateField(verbose_name='Дата платежа')
	dogowor = models.CharField(max_length=100, verbose_name='№ Договора')
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О')
	price = models.FloatField(verbose_name='Сумма платежа')
	etrap = models.CharField(max_length=32, choices= etraps)

	def __str__(self):
		return f"{self.pk} {self.etrap} {self.type} {self.FAO} {self.dogowor} {self.pay_date} {self.price}"
	
	class Meta:
		verbose_name = 'Интернет Внешние Платежи'
		verbose_name_plural = 'Интернет Внешние Платежи'

class ImportInternetPlatejiOFF(models.Model):
	type = models.CharField(max_length=32, verbose_name='Способ оплаты')
	pay_date = models.DateField(verbose_name='Дата платежа')
	dogowor = models.CharField(max_length=100, verbose_name='№ Договора')
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О')
	price = models.FloatField(verbose_name='Сумма платежа')
	etrap = models.CharField(max_length=32, choices= etraps)

	def __str__(self):
		return f"{self.pk} {self.etrap} {self.type} {self.FAO} {self.dogowor} {self.pay_date} {self.price}"
	
	class Meta:
		verbose_name = 'Интернет Внешние Платежи OFF'
		verbose_name_plural = 'Интернет Внешние Платежи OFF'


class ImportInternetNachisleniyaON(models.Model):
	year = models.CharField(max_length=100, verbose_name='Год', null=True, blank=True)
	month = models.CharField(max_length=16, verbose_name='Месяц', null=True, blank=True)
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О', null=True, blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='№ Договора', blank=True)
	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	price = models.FloatField(verbose_name='Сумма платежа')
	etrap = models.CharField(max_length=32, choices= etraps)

	def __str__(self):
		return f"{self.pk} {self.etrap} {self.FAO} {self.dogowor} {self.login} {self.price}"
	
	class Meta:
		verbose_name = 'Список Абонентов для Интернет Начислений ON'
		verbose_name_plural = 'Список Абонентов для Интернет Начислений ON'


class ImportInternetNachisleniyaOFF(models.Model):
	year = models.CharField(max_length=4, verbose_name='Год', null=True, blank=True)
	month = models.CharField(max_length=16, verbose_name='Месяц', null=True, blank=True)
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О', null=True, blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='№ Договора', blank=True)
	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	price = models.FloatField(verbose_name='Сумма платежа')
	etrap = models.CharField(max_length=32, choices= etraps)

	def __str__(self):
		return f"{self.pk} {self.etrap} {self.FAO} {self.dogowor} {self.login} {self.price}"
	
	class Meta:
		verbose_name = 'Список Абонентов для Интернет Начислений OFF'
		verbose_name_plural = 'Список Абонентов для Интернет Начислений OFF'


class ImportAlemNachisleniyaON(models.Model):
	year = models.CharField(max_length=4, verbose_name='Год', null=True, blank=True)
	month = models.CharField(max_length=16, verbose_name='Месяц', null=True, blank=True)
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О', null=True, blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='№ Договора', blank=True)
	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	price = models.FloatField(verbose_name='Сумма платежа')
	etrap = models.CharField(max_length=32, choices= etraps)

	def __str__(self):
		return f"{self.pk} {self.etrap} {self.FAO} {self.dogowor} {self.login} {self.price}"
	
	class Meta:
		verbose_name = 'Список Абонентов для Alem Начислений ON'
		verbose_name_plural = 'Список Абонентов для Alem Начислений ON'


class ImportAlemNachisleniyaOFF(models.Model):
	year = models.CharField(max_length=4, verbose_name='Год', null=True, blank=True)
	month = models.CharField(max_length=16, verbose_name='Месяц', null=True, blank=True)
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О', null=True, blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='№ Договора', blank=True)
	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	price = models.FloatField(verbose_name='Сумма платежа')
	etrap = models.CharField(max_length=32, choices= etraps)

	def __str__(self):
		return f"{self.pk} {self.etrap} {self.FAO} {self.dogowor} {self.login} {self.price}"
	
	class Meta:
		verbose_name = 'Список Абонентов для Alem Начислений OFF'
		verbose_name_plural = 'Список Абонентов для Alem Начислений OFF'
"""##########################################
    Import Excell Data to Our DataBase END ##
"""##########################################







# Начисления которые будут показаны в кассе (минус к балансу)
class NachMinus(models.Model):
	user = models.ForeignKey(UserTable, on_delete=models.CASCADE, verbose_name='Абонент')
	year = models.CharField(max_length=100, verbose_name='Год')
	month = models.CharField(max_length=100, verbose_name='Месяц')

	internet = models.FloatField(verbose_name='Интернет', default=0)
	belet = models.FloatField(verbose_name='Белет', default=0)
	kabel = models.FloatField(verbose_name='Кабель', default=0)
	alem = models.FloatField(verbose_name='Alem TV', default=0)
	telefon = models.FloatField(verbose_name='Телефон', default=0)
	slr = models.FloatField(verbose_name='СЛР', default=0)
	kod = models.FloatField(verbose_name='Код', default=0)
	zakaz = models.FloatField(verbose_name='Заказ', default=0)
	prochee = models.FloatField(verbose_name='Прочее', default=0)

	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)

	# Тут хранятся pk новых добавленных услуг для показа начислений которые произошли при добавлении в текущем (year-month) месяце
	# при первом добавлении начисляются и новые и старые
	# при втором добавлении начисляются только новые, старые уже начислены
	# {added: [['1','2','3','2023.04.24', 13.61], ['4','2023.04.26', 1.58]], }
	dop_usligi_added_Pk = models.CharField(max_length=2000, blank=True)

	is_enterprises = models.BooleanField(verbose_name='Эдара?', default=False)
	hb = models.CharField(max_length=4, verbose_name='Хоз или Бюд', blank=True)


	


	def __str__(self):
		return f"{self.user.number} {self.user.etrap} {self.user.name} {self.user.surname}"

	class Meta:
		verbose_name = 'Начисления минус'
		verbose_name_plural = 'Начисления минус'



zakazCallType = (
        ('', ''),
        ('бно', 'бно'),
        ('заказ подтвержден', 'заказ подтвержден'),
)

class NachislitWruchnuyuHistory(models.Model):
	user = models.CharField(max_length=500, verbose_name='Работник который начислил')
	date = models.DateTimeField(verbose_name='Дата начисления', auto_now_add=True)
	column = models.CharField(max_length=500, verbose_name='Начислил на')
	price = models.FloatField(verbose_name='Начисления на сумму')
	number = models.IntegerField(verbose_name='Номер абонента')
	etrap = models.CharField(max_length=32, choices= etraps, verbose_name='Этрап абонента')
	comment = models.CharField(max_length=2000, verbose_name='Комментарий', blank=True)

	def __str__(self):
		return f"{self.etrap} {self.number} {self.price} {self.column} {self.user}"

	class Meta:
		verbose_name = 'Начисления вручную история'
		verbose_name_plural = 'Начисления вручную история'


# Это нужно для вывода в excel формате об всех установленных и снятых услугах нигде в программе она не будет видна (нет необходимости)
class UstanowkaSnyatieDopUslugHistory(models.Model):
	user = models.CharField(max_length=500, verbose_name='Кто выполнил')
	date = models.DateTimeField(verbose_name='Дата выполнения', auto_now_add=True)
	# при снятии, при перекидке, в абон-отделе, при востановлении с архива, 
	which_action = models.CharField(max_length=1000, verbose_name='изменения при')
	# установлено, снято, снято и установлено
	which_type = models.CharField(max_length=1000, verbose_name='установлено/снято')
	number = models.IntegerField(verbose_name='Номер абонента')
	etrap = models.CharField(max_length=32, choices= etraps, verbose_name='Этрап абонента')
	comment = models.TextField(verbose_name='Комментарий', blank=True)
	perekidka_info_new_pk = models.IntegerField(verbose_name='id perekidka_info_new для быстрого поиска и отмены (востановления)', default=0)

	def __str__(self):
		return f"{self.number} {self.etrap}"

	class Meta:
		verbose_name = 'Информация об установленных и снятых услуг'
		verbose_name_plural = 'Информация об установленных и снятых услуг'


# class Zakaz(models.Model):
# 	DATE = models.DateTimeField(verbose_name='Дата и время звонка ')
# 	NUMBER_A = models.CharField(max_length=32, verbose_name='NUMBER_A')
# 	NUMBER_B = models.CharField(max_length=32, verbose_name='NUMBER_B')
# 	NUMBER_LOCATIONS = models.CharField(max_length=32, verbose_name='Страна/Город соединяемой стороны')
# 	etrap = models.CharField(max_length=32, choices= etraps, verbose_name='Этрап соединяющей стороны')
# 	DUR = models.CharField(max_length=16, verbose_name='DUR')
# 	MT = models.CharField(max_length=8, verbose_name='MT')
# 	price = models.CharField(max_length=8, verbose_name='цена за минуту без процента')
# 	priceProc = models.CharField(max_length=8, verbose_name='цена за минуту c процентом')
# 	total_price = models.CharField(max_length=16, verbose_name='Общая цена без процента')
# 	total_priceProc = models.CharField(max_length=16, verbose_name='Общая цена с процентом')
# 	CALL_TYPE = models.CharField(max_length=4, verbose_name='CALL_TYPE')
# 	action = models.CharField(max_length=32, choices= zakazCallType, verbose_name='бно/повторно/потдвержден')
# 	agent_id = models.CharField(max_length=4, verbose_name='agent_id', blank=True)

# 	def __str__(self):
# 		return f"{self.NUMBER_A} {self.NUMBER_B}"

# 	class Meta:
# 		verbose_name = 'Заказ'
# 		verbose_name_plural = 'Заказ'
# 		ordering = ['DATE']



class Zakaz(models.Model):
	DATE = models.DateTimeField(verbose_name='Дата и время звонка ')
	NUMBER_A = models.CharField(max_length=500, verbose_name='NUMBER_A')
	NUMBER_B = models.CharField(max_length=500, verbose_name='NUMBER_B')
	NUMBER_LOCATIONS = models.CharField(max_length=500, verbose_name='Страна/Город соединяемой стороны')
	etrap = models.CharField(max_length=500, choices= etraps, verbose_name='Этрап соединяющей стороны')
	DUR = models.CharField(max_length=500, verbose_name='DUR')
	MT = models.CharField(max_length=8, verbose_name='MT')
	price = models.CharField(max_length=500, verbose_name='цена за минуту без процента')
	# priceProc = models.CharField(max_length=8, verbose_name='цена за минуту c процентом')
	# total_price = models.CharField(max_length=16, verbose_name='Общая цена без процента')
	total_price = models.CharField(max_length=500, verbose_name='Общая цена с процентом')
	CALL_TYPE = models.CharField(max_length=500, verbose_name='CALL_TYPE')
	action = models.CharField(max_length=500, choices= zakazCallType, verbose_name='бно/повторно/потдвержден')
	agent_id = models.CharField(max_length=4, verbose_name='agent_id', blank=True)

	def __str__(self):
		return f"{self.NUMBER_A} {self.NUMBER_B}"

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказ'
		ordering = ['DATE']























	








# # таблица для хранения инфы о начислениях в ввиде foreign и m2m для обзора их на кассе в столбцах доп.услуги, алем, интернет (не используется вроде)
# class ShowNachService(models.Model):
# 	nach_minus = models.ForeignKey(NachMinus, on_delete=models.CASCADE, verbose_name='Начисления минус к балансу')

# 	alem = alem = models.BooleanField(default=False, verbose_name='Alem TV', blank=True)
# 	alem_connect_date = models.CharField(max_length=16, verbose_name='Дата подключения Alem TV', blank=True)
# 	alem_disconnect_date = models.CharField(max_length=16, verbose_name='Дата отключения Alem TV', blank=True)

# 	internet_tarif = models.ForeignKey(InternetTarif, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Интернет тариф')
# 	internet_connect_date = models.CharField(max_length=16, verbose_name='Дата подключения Интернет', blank=True)
# 	internet_disconnect_date = models.CharField(max_length=16, verbose_name='Дата отключения Интернет', blank=True)

# 	def __str__(self):
# 		return f"{self.nach_minus.user.number} {self.nach_minus.user.etrap} {self.nach_minus.user.name} {self.nach_minus.user.surname}"

# 	class Meta:
# 		verbose_name = 'Для показа инфы у начисленных услугах в кассе'
# 		verbose_name_plural = 'Для показа инфы у начисленных услугах в кассе'



staffsction = (
        ('Delete', 'Delete'),
        ('Update', 'Update'),
        ('Recover', 'Recover'),
        ('Снятие Номера', 'Снятие Номера'),
        ('Безвозвратное удаление номера', 'Безвозвратное удаление номера'),
        ('Востановление номера', 'Востановление номера'),
        ('Начисления СЛР', 'Начисления СЛР'),
        ('Начисления КОД', 'Начисления КОД'),
        ('Начисления КОД+СЛР', 'Начисления КОД+СЛР'),
        ('Начисления Интернет Платежей', 'Начисления Интернет Платежей'),
        ('Импорт с xlsx внешние платежи в БД', 'Импорт с xlsx внешние платежи в БД'),
		('Импорт с xlsx Интернет Начисления в БД', 'Импорт с xlsx Интернет Начисления в БД'),
		('Импорт с xlsx Alem Начисления в БД', 'Импорт с xlsx Alem Начисления в БД'),
        ('Another', 'Another'),
        ('Начисления Интернет', 'Начисления Интернет'),
        ('Начисления абонплата', 'Начисления абонплата'),
        ('Начисления метры', 'Начисления метры'),
        ('Начисления заказ', 'Начисления заказ'),
        ('Начисления Доп Услуг', 'Начисления Доп Услуг'),
        ('Изменение Услуг', 'Изменение Услуг'),
        ('Подключения/смена интернет тарифа', 'Подключения/смена интернет тарифа'),
        ('Подключения/смена метров', 'Подключения/смена метров'),
        ('Кабель TV действия', 'Кабель TV действия'),
        ('Alem TV действия', 'Alem TV действия'),
        ('Изменение данных абонента в MATB в базе данных', 'Изменение данных абонента в MATB в базе данных'),
        ('Добавление абонента в MATB в базе данных', 'Добавление абонента в MATB в базе данных'),
        ('Перекидка', 'Перекидка'),
        ('Old Login Dogowor Save', 'Old Login Dogowor Save'),
		('Old Login Dogowor Delete', 'Old Login Dogowor Delete'),
        ('Old Login Dogowor Update', 'Old Login Dogowor Update'),
        ('Добавления платежей в базу', 'Добавления платежей в базу'),
		('Пробитие платежей с базы данных', 'Пробитие платежей с базы данных'),
		('Ручное начисление', 'Ручное начисление'),
)


# сохраняем действие операторов
class StaffAction(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Оператор')
	comment = models.TextField(verbose_name='Комментарий')
	action = models.CharField(max_length=1000, choices= staffsction)
	date = models.DateTimeField(auto_now_add=True)
	akt_raport = models.CharField(max_length=1000, verbose_name="Акт, рапорт", blank=True)
	perekidka_info_new_pk = models.IntegerField(verbose_name='id perekidka_info_new для быстрого поиска и отмены (востановления)', default=0)

	def __str__(self):
		return f"{self.user.username} {self.comment[:50]} {self.date}"








































"""##########
    Rezerw ##
"""##########
# Если номер очищен, то перед очищением надо сохранить абонента со всеми его данными, для того чтобы он оплатил все долги
# class UserTableRezerw(models.Model):
# 	number = models.CharField(max_length=15, verbose_name='Номер телефона')
# 	etrap = models.CharField(max_length=32, choices= etraps)
# 	surname = models.CharField(max_length=40, verbose_name='Фамилия/организация', blank=True)
# 	name = models.CharField(max_length=40, verbose_name='Имя/Отдел', blank=True)
# 	street = models.CharField(max_length=40, verbose_name='Улица', blank=True)
# 	home = models.CharField(max_length=40, verbose_name='Дом', blank=True)
# 	flat = models.CharField(max_length=40, verbose_name='Квартира', blank=True)
	
# 	sotowyy = models.CharField(max_length=40, verbose_name='Сотовый номер', blank=True)
	
# 	is_enterprises = models.BooleanField(default=False, verbose_name='Предприятия', blank=True)

# 	alem = models.BooleanField(default=False, verbose_name='Alem TV', blank=True)
# 	alemCount = models.ForeignKey('AlemCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Alem TV точек', default=1)
# 	alem_connect_date = models.DateTimeField(verbose_name='Дата подсоединения Alem TV', null=True, blank=True)
# 	alem_on_date = models.DateTimeField(verbose_name='Дата включения Alem TV', null=True, blank=True)
# 	alem_off_date = models.DateTimeField(verbose_name='Дата отключения Alem TV', null=True, blank=True)
# 	alem_disconnect_date = models.DateTimeField(verbose_name='Дата отсоединения Alem TV', null=True, blank=True)

# 	account = models.IntegerField(verbose_name='Счёт', blank=True, null=True)
# 	hb = models.ForeignKey('HozOrBudjet', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Хоз/Бюджет?')


# 	internet_tarif = models.ForeignKey('InternetTarif', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Интернет тариф')
# 	internet_connect_date = models.DateTimeField(verbose_name='Дата подсоединения Интернет', null=True, blank=True)
# 	internet_disconnect_date = models.DateTimeField(verbose_name='Дата отсоединения Интернет', null=True, blank=True)

# 	abon_length = models.ForeignKey('AbonLength', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга Метры') # -
# 	abon_length_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения Метров', null=True, blank=True) # -

# 	count_of_numbers = models.ForeignKey('AbonentNumbersCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кол-во номеров')
# 	count_of_numbers_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения Количество номеров', null=True, blank=True) # -

# 	beneficiary = models.ForeignKey('AbonentBeneficiary', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Льгота')

# 	# кабель
# 	is_on = models.BooleanField(default=False, verbose_name='Кабель Включен?', blank=True)
# 	is_on_date = models.DateTimeField(verbose_name="Дата и время включения кабеля", null=True, blank=True)
# 	kabel_count = models.ForeignKey('KabelCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кол-во точек кабеля')
# 	connect_date = models.DateTimeField(verbose_name="Дата и время Подключения кабеля", null=True, blank=True)
# 	kabel_comments = models.TextField(verbose_name='Комментарии для кабеля', null=True, blank=True)
# 	# Для кабель TV
# 	ids = models.CharField(max_length=8, verbose_name='Кабель ID', blank=True)

# 	# M2M fields
# 	service = models.ManyToManyField('AbonentService', verbose_name='Доп.Услуги (добавлять через ctrl)', blank=True)
# 	# service_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения услуг', null=True, blank=True)

# 	login = models.CharField(max_length=40, verbose_name='Логин', blank=True)
# 	dogowor = models.CharField(max_length=40, verbose_name='Договор', blank=True)

# 	b_internet = models.FloatField(verbose_name=' Баланс Интернет', default=0)
# 	b_kabel = models.FloatField(verbose_name=' Баланс Кабель', default=0)
# 	b_alem = models.FloatField(verbose_name=' Баланс Alem TV', default=0)
# 	b_telefon = models.FloatField(verbose_name='Баланс Телефон', default=0)
# 	b_slr = models.FloatField(verbose_name='Баланс СЛР', default=0)
# 	b_kod = models.FloatField(verbose_name='Баланс Код', default=0)
# 	b_zakaz = models.FloatField(verbose_name='Баланс Заказ', default=0)
# 	b_prochee = models.FloatField(verbose_name='Баланс Прочее', default=0)
# 	b_dop_uslugi = models.FloatField(verbose_name='Баланс Доп. Услуги', default=0)

# 	# дата добавления абонента в нашу БД (или дата активации номера) короче в MATB сами пишут эту дату
# 	addDate = models.DateField(verbose_name="Дата и время добавления абонента в базу данных", null=True, blank=True)

# 	# Дата снятия абонента
# 	snyat_date = models.DateField(verbose_name="Дата и время снятия абонента", null=True, blank=True)


# 	class Meta:
# 		unique_together = ["number", "etrap"]
# 		verbose_name = 'Абонента Резерв'
# 		verbose_name_plural = 'Абоненты Резерв'
# 		ordering = ['-number']

# 	def __str__(self):
# 		return f"{self.number} {self.etrap}"


# class NachMinusRezerw(models.Model):
# 	user = models.ForeignKey(UserTableRezerw, on_delete=models.CASCADE, verbose_name='Абонент')
# 	year = models.CharField(max_length=4, verbose_name='Год')
# 	month = models.CharField(max_length=2, verbose_name='Месяц')

# 	internet = models.FloatField(verbose_name='Интернет', default=0)
# 	kabel = models.FloatField(verbose_name='Кабель', default=0)
# 	alem = models.FloatField(verbose_name='Alem TV', default=0)
# 	telefon = models.FloatField(verbose_name='Телефон', default=0)
# 	slr = models.FloatField(verbose_name='СЛР', default=0)
# 	kod = models.FloatField(verbose_name='Код', default=0)
# 	zakaz = models.FloatField(verbose_name='Заказ', default=0)
# 	prochee = models.FloatField(verbose_name='Прочее', default=0)

# 	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)

# 	# Тут хранятся pk новых добавленных услуг для показа начислений которые произошли при добавлении в текущем (year-month) месяце
# 	# при первом добавлении начисляются и новые и старые
# 	# при втором добавлении начисляются только новые, старые уже начислены
# 	# {added: [['1','2','3','2023.04.24', 13.61], ['4','2023.04.26', 1.58]], }
# 	dop_usligi_added_Pk = models.CharField(max_length=256, blank=True)

	


# 	def __str__(self):
# 		return f"{self.user.number} {self.user.etrap} {self.user.name} {self.user.surname}"

# 	class Meta:
# 		verbose_name = 'Начисления минус Резерв'
# 		verbose_name_plural = 'Начисления минус Резерв'



# class PayHistoryRezerw(models.Model):
# 	abonent = models.ForeignKey(UserTableRezerw, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Абонент')

# 	internet = models.FloatField(verbose_name='Интернет', default=0)
# 	kabel = models.FloatField(verbose_name='Кабель', default=0)
# 	alem = models.FloatField(verbose_name='Alem TV', default=0)
# 	telefon = models.FloatField(verbose_name='Телефон', default=0)
# 	slr = models.FloatField(verbose_name='СЛР', default=0)
# 	kod = models.FloatField(verbose_name='Код', default=0)
# 	zakaz = models.FloatField(verbose_name='Заказ', default=0)
# 	prochee = models.FloatField(verbose_name='Прочее', default=0)
# 	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)
	
# 	is_card = models.BooleanField(default=False, verbose_name='Карт?', blank=True)

# 	# кассир, банк, app toleg и т.п.
# 	kassir = models.CharField(max_length=32, verbose_name='Кассир')

# 	total = models.FloatField(verbose_name='Вклад', null=True, blank=True)

# 	date = models.DateTimeField(verbose_name="Дата и время оплаты")

# 	# def __str__(self):
# 	# 	return f"{self.abonent.number} {self.abonent.etrap} {self.abonent.name} {self.abonent.surname}"

# 	class Meta:
# 		verbose_name = 'История оплат Резерв'
# 		verbose_name_plural = 'История оплат Резерв'



# class MonthBalanceArhiw(models.Model):
# 	year = models.CharField(max_length=4, verbose_name='Год')
# 	month = models.CharField(max_length=16, verbose_name='Месяц')
# 	etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап")

# 	internetPlus = models.FloatField(verbose_name='Интернет Plus', default=0)
# 	kabelPlus = models.FloatField(verbose_name='Кабель Plus', default=0)
# 	alemPlus = models.FloatField(verbose_name='Alem TV Plus', default=0)
# 	telefonPlus = models.FloatField(verbose_name='Телефон Plus', default=0)
# 	slrPlus = models.FloatField(verbose_name='СЛР Plus', default=0)
# 	kodPlus = models.FloatField(verbose_name='Код Plus', default=0)
# 	zakazPlus = models.FloatField(verbose_name='Заказ Plus', default=0)
# 	procheePlus = models.FloatField(verbose_name='Прочее Plus', default=0)
# 	dop_uslugiPlus = models.FloatField(verbose_name='Доп. Услуги Plus', default=0)

# 	internetMinus = models.FloatField(verbose_name='Интернет Minus', default=0)
# 	kabelMinus = models.FloatField(verbose_name='Кабель Minus', default=0)
# 	alemMinus = models.FloatField(verbose_name='Alem TV Minus', default=0)
# 	telefonMinus = models.FloatField(verbose_name='Телефон Minus', default=0)
# 	slrMinus = models.FloatField(verbose_name='СЛР Minus', default=0)
# 	kodMinus = models.FloatField(verbose_name='Код Minus', default=0)
# 	zakazMinus = models.FloatField(verbose_name='Заказ Minus', default=0)
# 	procheeMinus = models.FloatField(verbose_name='Прочее Minus', default=0)
# 	dop_uslugiMinus = models.FloatField(verbose_name='Доп. Услуги Minus', default=0)

# 	class Meta:
# 		unique_together = ["etrap", "year", "month"]
# 		verbose_name = 'Архив Баланс каждого месяца за все время'
# 		verbose_name_plural = 'Архив Баланс каждого месяца за все время'



"""##############
    Rezerw END ##
"""##############





# class ShowNachServiceAfterClearNumber(models.Model):
# 	nach_minus = models.ForeignKey(NachMinusAfterClearNumber, on_delete=models.CASCADE, verbose_name='Начисления минус к балансу')

# 	alem = alem = models.BooleanField(default=False, verbose_name='Alem TV', blank=True)
# 	alem_connect_date = models.CharField(max_length=16, verbose_name='Дата подключения Alem TV', blank=True)
# 	alem_disconnect_date = models.CharField(max_length=16, verbose_name='Дата отключения Alem TV', blank=True)

# 	internet_tarif = models.ForeignKey(InternetTarif, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Интернет тариф')
# 	internet_connect_date = models.CharField(max_length=16, verbose_name='Дата подключения Интернет', blank=True)
# 	internet_disconnect_date = models.CharField(max_length=16, verbose_name='Дата отключения Интернет', blank=True)

# 	def __str__(self):
# 		return f"{self.nach_minus.abonent.number} {self.nach_minus.abonent.etrap} {self.nach_minus.abonent.name} {self.nach_minus.abonent.surname}"

# 	class Meta:
# 		verbose_name = 'Для показа инфы у начисленных услугах в кассе после удаления'
# 		verbose_name_plural = 'Для показа инфы у начисленных услугах в кассе после удаления'




"""#########
    Arhiw ##
"""#########

class UserTableArhiw(models.Model):
	# 37 полей
	number = models.CharField(max_length=15, verbose_name='Номер телефона')
	etrap = models.CharField(max_length=32, choices= etraps)
	surname = models.CharField(max_length=500, verbose_name='Фамилия/организация', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя/Отдел', blank=True)
	street = models.CharField(max_length=500, verbose_name='Улица', blank=True)
	home = models.CharField(max_length=500, verbose_name='Дом', blank=True)
	flat = models.CharField(max_length=500, verbose_name='Квартира', blank=True)



	sotowyy = models.CharField(max_length=40, verbose_name='Сотовый номер', blank=True)
	
	is_enterprises = models.BooleanField(default=False, verbose_name='Предприятия', blank=True)

	alem = models.BooleanField(default=False, verbose_name='Alem TV Активен', blank=True)
	alemCount = models.ForeignKey('AlemCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Alem TV точек')
	alem_connect_date = models.DateTimeField(verbose_name='Дата подсоединения Alem TV', null=True, blank=True)
	alem_on_date = models.DateTimeField(verbose_name='Дата включения Alem TV', null=True, blank=True)
	alem_off_date = models.DateTimeField(verbose_name='Дата отключения Alem TV', null=True, blank=True)
	alem_disconnect_date = models.DateTimeField(verbose_name='Дата отсоединения Alem TV', null=True, blank=True)

	account = models.IntegerField(verbose_name='Счёт', blank=True, null=True)
	accountName = models.CharField(max_length=1000, verbose_name='Имя Счет номера (edara name)', blank=True)
	accountAdress = models.CharField(max_length=1000, verbose_name='Адрес Счет номера (edara adress)', blank=True)

	hb = models.ForeignKey('HozOrBudjet', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Хоз/Бюджет?')

	internet_tarif = models.ForeignKey('InternetTarif', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Интернет тариф')
	internet_connect_date = models.DateTimeField(verbose_name='Дата подсоединения Интернет', null=True, blank=True)
	internet_disconnect_date = models.DateTimeField(verbose_name='Дата отсоединения Интернет', null=True, blank=True)

	# abon_length = models.ForeignKey('AbonLength', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга Метры')
	# abon_length_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения Метров', null=True, blank=True) # -

	abonplata = models.CharField(max_length=16,verbose_name='Абонплата', null=True, blank=True)


	# count_of_numbers = models.ForeignKey('AbonentNumbersCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кол-во номеров')
	# count_of_numbers_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения Количество номеров', null=True, blank=True) # -

	# beneficiary = models.ForeignKey('AbonentBeneficiary', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Льгота')
	beneficiary = models.BooleanField(default=False, verbose_name='Льготник', blank=True)

	# кабель
	is_on = models.BooleanField(default=False, verbose_name='Кабель Включен?', blank=True)
	is_on_date = models.DateTimeField(verbose_name="Дата и время включения кабеля", null=True, blank=True)
	kabel_count = models.ForeignKey('KabelCount', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кол-во точек кабеля')
	connect_date = models.DateTimeField(verbose_name="Дата и время Подключения кабеля", null=True, blank=True)
	kabel_comments = models.TextField(verbose_name='Комментарии для кабеля', null=True, blank=True)
	# Для кабель TV
	ids = models.CharField(max_length=8, verbose_name='Кабель ID', blank=True)

	# surname name street home flat sotowyy	is_enterprises alem alemCount alem_connect_date alem_on_date alem_off_date alem_disconnect_date
	# account hb internet_tarif internet_connect_date internet_disconnect_date abon_length abon_length_connect_date
	# count_of_numbers count_of_numbers_connect_date beneficiary is_on is_on_date kabel_count connect_date kabel_comments
	# ids service login dogowor b_internet b_kabel b_alem b_telefon b_slr b_kod b_zakaz b_prochee b_dop_uslugi addDate wost_date

	# M2M fields
	service = models.ManyToManyField('AbonentService', verbose_name='Доп.Услуги (добавлять через ctrl)', blank=True)
	# service_connect_date = models.CharField(max_length=16,verbose_name='Дата подключения услуг', null=True, blank=True)

	login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='Договор', blank=True)
	dogowor_alem = models.CharField(max_length=100, verbose_name='Договор Алем ТВ', blank=True)
	dogowor_telefoniya = models.CharField(max_length=100, verbose_name='Договор Телефония', blank=True)
	dogowor_belet = models.CharField(max_length=100, verbose_name='Договор Белет', blank=True)

	b_internet = models.FloatField(verbose_name=' Баланс Интернет', default=0)
	b_kabel = models.FloatField(verbose_name=' Баланс Кабель', default=0)
	b_alem = models.FloatField(verbose_name=' Баланс Alem TV', default=0)
	b_telefon = models.FloatField(verbose_name='Баланс Телефон', default=0)
	b_slr = models.FloatField(verbose_name='Баланс СЛР', default=0)
	b_kod = models.FloatField(verbose_name='Баланс Код', default=0)
	b_zakaz = models.FloatField(verbose_name='Баланс Заказ', default=0)
	b_prochee = models.FloatField(verbose_name='Баланс Прочее', default=0)
	b_dop_uslugi = models.FloatField(verbose_name='Баланс Доп. Услуги', default=0)

	s_internet = models.FloatField(verbose_name=' Сальдо Интернет', default=0)
	s_kabel = models.FloatField(verbose_name=' Сальдо Кабель', default=0)
	s_alem = models.FloatField(verbose_name=' Сальдо Alem TV', default=0)
	s_telefon = models.FloatField(verbose_name='Сальдо Телефон', default=0)
	s_slr = models.FloatField(verbose_name='Сальдо СЛР', default=0)
	s_kod = models.FloatField(verbose_name='Сальдо Код', default=0)
	s_zakaz = models.FloatField(verbose_name='Сальдо Заказ', default=0)
	s_prochee = models.FloatField(verbose_name='Сальдо Прочее', default=0)
	s_dop_uslugi = models.FloatField(verbose_name='Сальдо Доп. Услуги', default=0)

	# дата добавления абонента в нашу БД (или дата активации номера) короче в MATB сами пишут эту дату
	addDate = models.DateField(verbose_name="Дата и время добавления абонента в базу данных", null=True, blank=True)

	# Дата снятия
	snyat_bool = models.BooleanField(default=False, verbose_name='Снят?', blank=True)
	snyat_date = models.DateTimeField(verbose_name="Дата снятия абонента", null=True, blank=True)
	# (old в месяном отчете не учитываюся архивные и Востановленные номера учитываются в отчете) Востановленные номера не будут учитываться при месячном отчете, так же не будет возможности оплтить в архиве
	wost_date = models.DateTimeField(verbose_name="Дата и время востановления с таблицы снятых номеров в основнную таблицу абонента", null=True, blank=True)
	# (old в месяном отчете не учитываюся архивные и платежи в архиве запрещены) Закрывать в случае если абонент уже оплатил все долги и вернул (или перекинул) остатки  баланса. Если закрыть то он останется в архиве но возможности оплатить не будет, так же не будут учитываться при месячном отчете
	close_date = models.DateTimeField(verbose_name="Дата закрытия долгов абонента", null=True, blank=True)

	perekidka_info_new_pk = models.IntegerField(verbose_name='id perekidka_info_new для быстрого поиска и отмены (востановления)', default=0)


	class Meta:
		verbose_name = 'Архив абонентов'
		verbose_name_plural = 'Архив абонентов'
		ordering = ['-number']

	def __str__(self):
		return f"{self.number} {self.etrap}"
	


# class PayHistoryArhiw(models.Model):
# 	abonent = models.ForeignKey(UserTableArhiw, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Абонент')

# 	internet = models.FloatField(verbose_name='Интернет', default=0)
# 	kabel = models.FloatField(verbose_name='Кабель', default=0)
# 	alem = models.FloatField(verbose_name='Alem TV', default=0)
# 	telefon = models.FloatField(verbose_name='Телефон', default=0)
# 	slr = models.FloatField(verbose_name='СЛР', default=0)
# 	kod = models.FloatField(verbose_name='Код', default=0)
# 	zakaz = models.FloatField(verbose_name='Заказ', default=0)
# 	prochee = models.FloatField(verbose_name='Прочее', default=0)
# 	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)
	
# 	is_card = models.BooleanField(default=False, verbose_name='Карт?', blank=True)

# 	# кассир, банк, app toleg и т.п.
# 	kassir = models.CharField(max_length=32, verbose_name='Кассир')

# 	total = models.FloatField(verbose_name='Вклад', null=True, blank=True)

# 	date = models.DateTimeField(verbose_name="Дата и время оплаты")

# 	def __str__(self):
# 		return f"{self.abonent.number} {self.abonent.etrap} {self.abonent.name} {self.abonent.surname}"

# 	class Meta:
# 		verbose_name = 'Архив история оплат'
# 		verbose_name_plural = 'Архив история оплат'


# Начисления которые будут показаны в кассе (минус к балансу)
# class NachMinusArhiw(models.Model):
# 	user = models.ForeignKey(UserTableArhiw, on_delete=models.CASCADE, verbose_name='Абонент')
# 	year = models.CharField(max_length=4, verbose_name='Год')
# 	month = models.CharField(max_length=2, verbose_name='Месяц')

# 	internet = models.FloatField(verbose_name='Интернет', default=0)
# 	kabel = models.FloatField(verbose_name='Кабель', default=0)
# 	alem = models.FloatField(verbose_name='Alem TV', default=0)
# 	telefon = models.FloatField(verbose_name='Телефон', default=0)
# 	slr = models.FloatField(verbose_name='СЛР', default=0)
# 	kod = models.FloatField(verbose_name='Код', default=0)
# 	zakaz = models.FloatField(verbose_name='Заказ', default=0)
# 	prochee = models.FloatField(verbose_name='Прочее', default=0)

# 	dop_uslugi = models.FloatField(verbose_name='Доп. Услуги', default=0)

# 	# Тут хранятся pk новых добавленных услуг для показа начислений которые произошли при добавлении в текущем (year-month) месяце
# 	# при первом добавлении начисляются и новые и старые
# 	# при втором добавлении начисляются только новые, старые уже начислены
# 	# {added: [['1','2','3','2023.04.24', 13.61], ['4','2023.04.26', 1.58]], }
# 	dop_usligi_added_Pk = models.CharField(max_length=256, blank=True)

	


# 	def __str__(self):
# 		return f"{self.user.number} {self.user.etrap} {self.user.name} {self.user.surname}"

# 	class Meta:
# 		verbose_name = 'Архив начисления минус'
# 		verbose_name_plural = 'Архив начисления минус'



"""#############
    Arhiw END ##
"""#############



"""#######################
    saldo minth balance ##
"""#######################

months = (
        ('Январь', 'Январь'),
        ('Февраль', 'Февраль'),
        ('Март', 'Март'),
        ('Апрель', 'Апрель'),
        ('Май', 'Май'),
        ('Июнь', 'Июнь'),
        ('Июль', 'Июль'),
        ('Август', 'Август'),
        ('Сентябрь', 'Сентябрь'),
        ('Октябрь', 'Октябрь'),
        ('Ноябрь', 'Ноябрь'),
        ('Декабрь', 'Декабрь'),
)



class NachMonthDebetKredet(models.Model):
	edaraOrNasel = models.BooleanField(verbose_name='Edara', default=False)
	year = models.CharField(max_length=4, verbose_name='Год')
	month = models.CharField(max_length=16, verbose_name='Месяц', choices=months)
	etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап")
	number = models.CharField(max_length=32, verbose_name="Номер")
	debet = models.FloatField(verbose_name="debet", default=0)
	kredet = models.FloatField(verbose_name="kredet", default=0)
	def __str__(self):
		return f"{self.edaraOrNasel} {self.year} {self.month} {self.etrap} {self.number} {self.balance}"
	class Meta:
		verbose_name = 'Баланс для Дибит, Кредит'
		verbose_name_plural = 'Баланс для Дибит, Кредит'

class MonthPlatejiFromBilling(models.Model):
	manager = models.CharField(max_length=500, verbose_name='Менеджер')
	pay_date = models.DateField(verbose_name='Дата Платежа')
	dogowor = models.CharField(max_length=500, verbose_name='Договор')
	price = models.FloatField(verbose_name='Платеж')
	platejiType = models.CharField(max_length=500, verbose_name='Внешние платежи, default или Оплачено по карте', blank=True)
	date_price = models.CharField(max_length=500, verbose_name='Дата вместо цены', blank=True)
	kod_oplaty = models.CharField(max_length=500, verbose_name='Код оплаты', blank=True)
	YurOrFiz = models.CharField(max_length=500, verbose_name='Юридическое или Физическое лицо', blank=True)
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О', blank=True)

	def __str__(self):
		return f"{self.manager} {self.dogowor} {str(self.price)} {self.kod_oplaty}"

	class Meta:
		verbose_name = 'Платеж взятые с биллинга'
		verbose_name_plural = 'Платежи взятые с биллинга'


class MonthPlatejiOFFFromBilling(models.Model):
	manager = models.CharField(max_length=500, verbose_name='Менеджер')
	pay_date = models.DateField(verbose_name='Дата Платежа')
	dogowor = models.CharField(max_length=100, verbose_name='Договор')
	price = models.FloatField(verbose_name='Платеж')
	platejiType = models.CharField(max_length=100, verbose_name='Внешние платежи, default или Оплачено по карте', blank=True)
	date_price = models.CharField(max_length=100, verbose_name='Дата вместо цены', blank=True)
	kod_oplaty = models.CharField(max_length=100, verbose_name='Код оплаты', blank=True)
	YurOrFiz = models.CharField(max_length=100, verbose_name='Юридическое или Физическое лицо', blank=True)
	FAO = models.CharField(max_length=1000, verbose_name='Ф.И.О', blank=True)

	def __str__(self):
		return f"{self.manager} {self.dogowor} {str(self.price)} {self.kod_oplaty}"

	class Meta:
		verbose_name = 'Платеж OFF взятые с биллинга'
		verbose_name_plural = 'Платежи OFF взятые с биллинга'



class SagidDecemberDebetKredet(models.Model):
	number = models.CharField(max_length=32, verbose_name='Номер')
	debit = models.FloatField(max_length=32, verbose_name='Дебит', default=0)
	kredit = models.FloatField(max_length=32, verbose_name='Кредит', default=0)

	def __str__(self):
		return f"{self.number} {str(self.debit)} {str(self.kredit)}"

	class Meta:
		verbose_name = 'Сагид дебит кредит декабрь 2023'
		verbose_name_plural = 'Сагид дебит кредит декабрь 2023'


# 0=adyFam, 1=dogowor, 2=nomerPlateja,  3=price,  4=manager,  5=datePlatej,  6=datePlatejProweden,  7=account,    8=cartOrNo,    9=platejPorucheniye,   10=comment,   11=operator,   12=kodOplaty  

"""###########################
    saldo minth balance END ##
"""###########################

etraps_wn = (
        (None, 'Этрап'),
        ('Dashoguz', 'Dashoguz'),
        ('Akdepe', 'Akdepe'),
        ('Gorogly', 'Gorogly'),
        ('Ruhubelent', 'Ruhubelent'),
        ('S.A.Nyyazow', 'S.A.Nyyazow'),
        ('Turkmenbashy', 'Turkmenbashy'),
        ('Boldumsaz', 'Boldumsaz'),
        ('Koneurgench', 'Koneurgench'),
		('Garashsyzlyk', 'Garashsyzlyk'),
        ('Gubadag', 'Gubadag'),
        ('Внешние платежи', 'Внешние платежи'),
)

  # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
class PlatejiWhichAddKassirsEveryDay(models.Model):
	number = models.CharField(max_length=32, verbose_name='Номер', blank=True)
	user_etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап абонента", blank=True)
	kassir_etrap = models.CharField(max_length=32, choices=etraps_wn, verbose_name="Этрап кассира", blank=True)

	type_pay = models.CharField(max_length=50, verbose_name='Тип платежа (абонплата, итернет, ...)', blank=True)

	pay_category = models.CharField(max_length=256, verbose_name='Категория платежа (Внешние Платежи, Default или Оплата картой)', blank=True)
	manager = models.CharField(max_length=500, verbose_name='Менеджер', blank=True)
	date = models.DateField(verbose_name='Дата платежа', blank=True)
	kodOplaty = models.CharField(max_length=100, verbose_name='Код оплаты', blank=True, null=True)
	dogowor = models.CharField(max_length=100, verbose_name='Dogowor', blank=True)
	name = models.CharField(max_length=500, verbose_name='Ф.И.О', blank=True)
	is_enterprises = models.CharField(max_length=32, verbose_name='ЮЛ или ФЛ', blank=True)
	price = models.FloatField(verbose_name='Сумма платежа')
	file_name = models.CharField(max_length=500, verbose_name='Файл', blank=True)
	who_add_file = models.CharField(max_length=500, verbose_name='Кто добавил файл', blank=True)
	when_added_file=models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Когда файл добавлен в БД')
	file_is_nach = models.BooleanField(default=False, verbose_name='Платежи с этого файла начислены')
	

	# nomerPlateja = models.CharField(max_length=32, verbose_name='Номер платежа', blank=True)
	# datePlatejProweden = models.DateField(verbose_name='Дата проведения платежа', blank=True)
	# account = models.CharField(max_length=16, verbose_name='Счет №', blank=True)
	# is_cart = models.BooleanField(default=False)
	# payPorucheniye = models.CharField(max_length=32, verbose_name='Платежное поручение', blank=True)
	# comment = models.CharField(max_length=32, verbose_name='Комментарий', blank=True)
	# operator = models.CharField(max_length=32, verbose_name='Оператор', blank=True)
	


	def __str__(self):
		return f"{self.number} {str(self.user_etrap)} {str(self.dogowor)}"

	class Meta:
		verbose_name = 'Платежи c биллинга кассиров'
		verbose_name_plural = 'Платежи c биллинга кассиров'


# Платежи из выгрузки Milli Billing (пришёл на смену lanbilling), формат csv
class MilliBillingPay(models.Model):
	number = models.CharField(max_length=32, verbose_name='Номер абонента', blank=True)
	user_etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап абонента", blank=True)
	kassir_etrap = models.CharField(max_length=32, choices=etraps_wn, verbose_name="Этрап кассира", blank=True)

	type_pay = models.CharField(max_length=50, verbose_name='Тип платежа (Internet, Telefon, Alem, Kabel)', blank=True)
	is_matched = models.BooleanField(default=False, verbose_name='Абонент найден в базе')
	is_nach = models.BooleanField(default=False, verbose_name='Начислено в UserTable')

	payment_number = models.CharField(max_length=100, verbose_name='Номер платежа Milli Billing', blank=True)
	depository_name = models.CharField(max_length=200, verbose_name='Касса/терминал', blank=True)
	contract_code = models.CharField(max_length=100, verbose_name='Номер договора (contractCode)', blank=True)
	subscriber_full_name = models.CharField(max_length=300, verbose_name='ФИО абонента (из файла)', blank=True)
	tariff_group_name = models.CharField(max_length=100, verbose_name='Категория услуги (tariffGroupName)', blank=True)
	currency_name = models.CharField(max_length=50, verbose_name='Валюта', blank=True)
	description = models.CharField(max_length=500, verbose_name='Комментарий', blank=True)

	manager = models.CharField(max_length=500, verbose_name='Менеджер', blank=True)
	date = models.DateTimeField(verbose_name='Дата платежа', null=True, blank=True)
	price = models.FloatField(verbose_name='Сумма платежа', default=0)

	file_name = models.CharField(max_length=500, verbose_name='Файл', blank=True)
	who_add_file = models.CharField(max_length=500, verbose_name='Кто добавил файл', blank=True)
	when_added_file = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Когда файл добавлен в БД')

	def __str__(self):
		return f"{self.contract_code} {self.subscriber_full_name} {self.price}"

	class Meta:
		verbose_name = 'Платежи Milli Billing'
		verbose_name_plural = 'Платежи Milli Billing'


# class MonthPaysFromBillingToMyProgramm(models.Model):
# 	number = models.CharField(max_length=32, verbose_name='Номер', blank=True)
# 	etrap = models.CharField(max_length=32, choices=etraps, verbose_name="Этрап", blank=True)
# 	name = models.CharField(max_length=256, verbose_name='Ф.И.О', blank=True)
# 	dogowor = models.CharField(max_length=32, verbose_name='Dogowor', blank=True)
# 	nomerPlateja = models.CharField(max_length=32, verbose_name='Номер платежа', blank=True)
# 	price = models.FloatField(verbose_name='Сумма платежа')
# 	manager = models.CharField(max_length=64, verbose_name='Менеджер', blank=True)
# 	date = models.DateField(verbose_name='Дата платежа', blank=True)
# 	datePlatejProweden = models.DateField(verbose_name='Дата проведения платежа', blank=True)
# 	account = models.CharField(max_length=16, verbose_name='Счет №', blank=True)
# 	is_cart = models.BooleanField(default=False)
# 	payPorucheniye = models.CharField(max_length=32, verbose_name='Платежное поручение', blank=True)
# 	comment = models.CharField(max_length=32, verbose_name='Комментарий', blank=True)
# 	operator = models.CharField(max_length=32, verbose_name='Оператор', blank=True)
# 	kodOplaty = models.CharField(max_length=32, verbose_name='Код оплаты', blank=True)


# 	def __str__(self):
# 		return f"{self.number} {str(self.etrap)} {str(self.dogowor)}"

# 	class Meta:
# 		verbose_name = 'Платежи c биллинга кассиров'
# 		verbose_name_plural = 'Платежи c биллинга кассиров'
		


class ManagerNames(models.Model):
	etrap = models.CharField(max_length=32, choices=etraps_wn, verbose_name="Этрап", blank=True)
	name = models.CharField(max_length=500, verbose_name='Менеджер', blank=True)
	name2 = models.CharField(max_length=500, verbose_name='Логин Менеджера', blank=True)
	

	def __str__(self):
		return f"{self.etrap} {str(self.etrap)} {str(self.name)}"

	class Meta:
		verbose_name = 'Этрап и имена кассиров'
		verbose_name_plural = 'Этрап и имя кассира'

# Для сохранения excel файлов платежей которые добавляет Лена
class KassaExcelFiles(models.Model):
	operator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Соотрудник который добавил file')
	document = models.FileField(upload_to='documents/kassirs_pay_excel/%Y-%m-%d/', verbose_name='Файл')
	add_date=models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Когда файл добавлен в БД')
	def __str__(self):
		return f"{self.operator.username}"
	
	
# Не работает пока не нужен удалить потом если это сообщение все еще стоит
# Не большой хак для исправления разницы 10-50 манат между трафиком и bedit-kredit
class KodSumm(models.Model):
	year = models.CharField(max_length=4, verbose_name='Год')
	month = models.CharField(max_length=2, verbose_name='Месяц')

	internet = models.FloatField(verbose_name='Интернет', default=0)
	kabel = models.FloatField(verbose_name='Кабель', default=0)
	alem = models.FloatField(verbose_name='Alem TV', default=0)
	telefon = models.FloatField(verbose_name='Телефон', default=0)
	slr = models.FloatField(verbose_name='СЛР', default=0)
	kod = models.FloatField(verbose_name='Код', default=0)
	zakaz = models.FloatField(verbose_name='Заказ', default=0)
	prochee = models.FloatField(verbose_name='Прочее', default=0)
	dop_uslugi = models.FloatField(verbose_name='Доп услуги', default=0)



	def __str__(self):
		return f"{self.year} {self.month}"
	




class ExamGroup(models.Model):
	name = models.CharField(max_length=500, verbose_name='Название Группы', blank=True)
	def __str__(self):
		return f"{self.name}"

	class Meta:
		verbose_name = 'Экзаменационные группы вопросов'
		verbose_name_plural = 'Экзаменационная группа вопроса'



class ExamQuestions(models.Model):
	group = models.ManyToManyField(ExamGroup, verbose_name='Группа')
	question = models.TextField(verbose_name='Вопрос')
	answer1 = models.TextField(verbose_name='Ответ 1')
	answer2 = models.TextField(verbose_name='Ответ 2')
	answer3 = models.TextField(verbose_name='Ответ 3')
	# answer4 = models.TextField(verbose_name='Ответ 4')
	currect_answer = models.CharField(max_length=2, choices= ((None, '----'),('1', '1'),('2', '2'),('3', '3'),('4', '4')), verbose_name="Правильный ответ №: ")
	lang = models.CharField(max_length=16, choices= ((None, '----'),('Туркменский', 'Туркменский'),('Русский', 'Русский')), verbose_name="Язык вопросов", blank=True)
	def __str__(self):
		return f"{self.group}"
	
	class Meta:
		verbose_name = 'Экзаменационные вопросы'
		verbose_name_plural = 'Экзаменационный вопрос'


class Scores(models.Model):
	# user_name = models.CharField(max_length=128, verbose_name='Экзаменуемый')
	surname = models.CharField(max_length=500, verbose_name='Фамилия', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя', blank=True)
	sotowyy = models.CharField(max_length=32, verbose_name='Телефон', blank=True)
	q_lang = models.CharField(max_length=500, verbose_name='Язык вопросов', choices= ((None, '----'),('Туркменский', 'Туркменский'),('Русский', 'Русский')), blank=True)
	questions_count = models.IntegerField(verbose_name='Всего количество вопросов', default=0)
	currect_answer = models.IntegerField(verbose_name='Количество правильных ответов', default=0)
	error_answer = models.IntegerField(verbose_name='Количество не правильных ответов', default=0)
	scores = models.IntegerField(verbose_name='Баллы', null=True, blank=True)
	start_time = models.DateTimeField(verbose_name='дата и врема начало экзамена', null=True) 
	date_of_passing = models.DateTimeField(verbose_name='Дата сдачи теста', null=True, blank=True) 
	duration = models.TimeField(verbose_name='Длительность сдачи экзамена', null=True)
	etrap = models.CharField(max_length=64, verbose_name='Этрап', blank=True)
	
	class Meta:
		verbose_name = 'Экзаменационные баллы'
		verbose_name_plural = 'Экзаменационный балл'
	

class ExamHistory(models.Model):
	surname = models.CharField(max_length=500, verbose_name='Фамилия', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя', blank=True)
	Scores_id = models.CharField(max_length=16, verbose_name='Баллы ID')
	question = models.TextField(verbose_name='Вопрос')
	answer1 = models.TextField(verbose_name='Ответ 1')
	answer2 = models.TextField(verbose_name='Ответ 2')
	answer3 = models.TextField(verbose_name='Ответ 3')
	# answer4 = models.TextField(verbose_name='Ответ 4')
	choised_answer = models.IntegerField(verbose_name='Выбрал ответ №')
	currect_answer = models.IntegerField(verbose_name='Правильный вариант')
	is_currect_answer = models.BooleanField(verbose_name='Ответил правильно?')
	
	class Meta:
		verbose_name = 'Экзаменационные истории'
		verbose_name_plural = 'Экзаменационная история'



# class KabelTv(models.Model):
# 	etrap = models.CharField(max_length=32, choices=etraps_wn, verbose_name="Этрап", blank=True)
# 	name = models.CharField(max_length=256, verbose_name='Менеджер', blank=True)

# 	def __str__(self):
# 		return f"{self.etrap} {str(self.etrap)} {str(self.name)}"

# 	class Meta:
# 		verbose_name = 'Этрап и имена кассиров'
# 		verbose_name_plural = 'Этрап и имя кассира'

	
# 0=adyFam, 1=dogowor, 2=nomerPlateja,  3=price,  4=manager,  5=datePlatej,  6=datePlatejProweden,  7=account,    8=cartOrNo,    9=platejPorucheniye,   10=comment,   11=operator,   12=kodOplaty  


# Попросили баланс для счет номеров
class AccountBalance(models.Model):
	name = models.CharField(max_length=1000, verbose_name='Название Предприятия', blank=True, null=True)
	account = models.IntegerField(verbose_name='Счет номер', default=0)
	balance = models.IntegerField(verbose_name='Баланс', default=0)

	class Meta:
		verbose_name = 'Едара, счет, баланс'
		verbose_name_plural = 'Едара, счет, баланс'





# Kabel New ###########################################################################################################################################################################
class KabelTvNew(models.Model):
	number = models.IntegerField(verbose_name='Номер', unique=True)
	dogowor = models.CharField(max_length=100, verbose_name='Договор', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя', blank=True)
	surname = models.CharField(max_length=500, verbose_name='Фамилия', blank=True)
	street = models.CharField(max_length=500, verbose_name='Улица', blank=True)
	home = models.CharField(max_length=500, verbose_name='Дом', blank=True)
	flat = models.CharField(max_length=500, verbose_name='Квартира', blank=True)
	sotowyy = models.CharField(max_length=500, verbose_name='Сотовый номер', blank=True)
	is_enterprises = models.BooleanField(default=False, verbose_name='Предприятия')
	is_active = models.BooleanField(default=False, verbose_name='Активный')
	balance = models.FloatField(verbose_name='Баланс', default=0)
	count = models.IntegerField(verbose_name='Кол-во точек', default=0)
	user_add_date = models.DateTimeField(verbose_name='Дата добавления пользователя', auto_now_add=True)

	class Meta:
		verbose_name = 'КабельTVNew новая база'
		verbose_name_plural = 'КабельTVNew новая база'

	def __str__(self):
		return f"{self.number}"


class KabelComment(models.Model):
	user = models.ForeignKey(KabelTvNew, verbose_name='Абонент', on_delete=models.CASCADE)
	worker = models.CharField(max_length=500, verbose_name='Работник')
	action = models.CharField(max_length=500, verbose_name='Действие', choices=(('Изменения данных', 'Изменения данных'), ('Добавление абонента', 'Добавление абонента'), ('Удаление абонента', 'Удаление абонента'))) #default='Изменения данных'
	comment = models.TextField(verbose_name='Комментарий', blank=True)
	comment_add_date = models.DateTimeField(verbose_name='Дата добавления комментария', auto_now_add=True)
	perekidka_info_new_pk = models.IntegerField(verbose_name='id perekidka_info_new для быстрого поиска и отмены (востановления)', default=0)

	class Meta:
		verbose_name = 'КабельTVNew Комментарии'
		verbose_name_plural = 'КабельTVNew Комментарии'


class KabelTvPayHistory(models.Model):
	user = models.ForeignKey(KabelTvNew, verbose_name='Абонент', on_delete=models.CASCADE)
	pay = models.FloatField(verbose_name='Платеж', default=0)
	pay_date = models.DateTimeField(verbose_name='Дата платежа')
	pay_kassir = models.CharField(max_length=100, verbose_name='Платеж принял кассир', blank=True)
	card = models.BooleanField(default=False, verbose_name='Платеж корточкой?')

	# Если начислено из MilliBillingPay - хранит file_name, для точного отката начисления
	milli_billing_file_name = models.CharField(max_length=500, verbose_name='Файл Milli Billing', blank=True, null=True)

	class Meta:
		verbose_name = 'КабельTVNew Исторя платежей'
		verbose_name_plural = 'КабельTVNew Исторя платежей'


class KabelNach(models.Model):
	user = models.ForeignKey(KabelTvNew, verbose_name='Абонент', on_delete=models.PROTECT)
	year = models.CharField(max_length=4, verbose_name='Год')
	month = models.CharField(max_length=2, verbose_name='Месяц')
	nach = models.FloatField(verbose_name='Начисления Сумма', default=0)
	nach_date = models.DateTimeField(verbose_name='Дата выполнения начисления', auto_now_add=True)

	class Meta:
		verbose_name = 'КабельTVNew Начисления'
		verbose_name_plural = 'КабельTVNew Начисления'


class KabelTvNewDebitKredit(models.Model):
	year = models.CharField(max_length=4, verbose_name='Год')
	month = models.CharField(max_length=2, verbose_name='Месяц')
	number = models.IntegerField(verbose_name='Номер', unique=True)
	last_DT = models.IntegerField(verbose_name='Предыдущее Debit', default=0)
	last_KT = models.IntegerField(verbose_name='Предыдущее Kredit', default=0)
	nach = models.IntegerField(verbose_name='Начислено', default=0)
	perekidka_nach = models.IntegerField(verbose_name='Акт перекидки начислено', default=0)
	is_enterprises = models.BooleanField(default=False, verbose_name='Предприятия')
	current_DT = models.IntegerField(verbose_name='Текущий Debit', default=0)
	current_KT = models.IntegerField(verbose_name='Текущий Kredit', default=0)

	class Meta:
		verbose_name = 'КабельTVNew DT KT'
		verbose_name_plural = 'КабельTVNew DT KT'



class PayAndPayTypeForDebitKredit(models.Model):
	KabelTvNewDebitKredit_pk = models.ForeignKey(KabelTvNewDebitKredit, verbose_name='DT KT id (ForeignKey)', on_delete=models.PROTECT)
	pay = models.IntegerField(verbose_name='Оплачено', default=0)
	pay_type = models.CharField(max_length=500, verbose_name='Тип платежа (с кассы, TOLEG APP TMCELL, e-gov, и.т.п)')

	class Meta:
		verbose_name = 'КабельTVNew Pays for DT KT'
		verbose_name_plural = 'КабельTVNew Pays for DT KT'


# class KabelTVStaffAction(models.Model):
# 	worker = models.CharField(max_length=150, verbose_name='Работник')
# 	comment = models.CharField(max_length=150, verbose_name='Комментарий соотрудника')
# 	action = models.TextField(verbose_name='Действие')
# 	action_date = models.DateTimeField(verbose_name='Дата выполнения действия', auto_now_add=True)

# 	class Meta:
# 		verbose_name = 'История действий персонала для Кабель TV'
# 		verbose_name_plural = 'История действий персонала для Кабель TV'


# Kabel New ###########################################################################################################################################################################




class AlemNachFileNames(models.Model):
    file_name = models.CharField(max_length=500, verbose_name='Файл', blank=True)
    add_date = models.DateTimeField(verbose_name='Дата добавления Alem TV', null=True, blank=True)
    nach_date = models.DateTimeField(verbose_name='Дата начисления Alem TV', null=True, blank=True)
    who_add = models.CharField(max_length=500, verbose_name='Кто добавил', blank=True)
    who_nach = models.CharField(max_length=500, verbose_name='Кто начислил', blank=True)
    year = models.CharField(max_length=4, verbose_name='Год')
    month = models.CharField(max_length=2, verbose_name='Месяц')
    on_off = models.CharField(max_length=10, verbose_name='on_off', null=True, blank=True)
    etrap = models.CharField(max_length=500, choices=etraps, null=True, blank=True)
    
    def __str__(self):
        return f"{self.file_name} - {self.year}- {self.month}"


class AlemNachData(models.Model):
    number = models.CharField(max_length=500, verbose_name='Номер телефона', null=True, blank=True)
    etrap = models.CharField(max_length=500, choices=etraps, null=True, blank=True)
    year = models.CharField(max_length=4, verbose_name='Год')
    month = models.CharField(max_length=2, verbose_name='Месяц')
    name = models.CharField(max_length=1500, verbose_name="Пользователь", null=True, blank=True)
    dogowor = models.CharField(max_length=500, verbose_name="Договор", null=True, blank=True)
    account_name = models.CharField(max_length=500, verbose_name="Учетное имя", null=True, blank=True)
    tariff = models.CharField(max_length=1500, verbose_name="Тариф", null=True, blank=True)
    service = models.CharField(max_length=1000, verbose_name="Услуга", null=True, blank=True)
    tariff_charge = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Списание по тарифу", null=True, blank=True)
    service_charge = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Списание за услугу", null=True, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Кол-во (шт.)", null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Итого", null=True, blank=True)
    currency = models.CharField(max_length=50, verbose_name="Валюта", null=True, blank=True)
    on_off = models.CharField(max_length=10, verbose_name="on_off", null=True, blank=True)
    file_name = models.CharField(max_length=500, verbose_name='Файл', blank=True)
    is_nach = models.BooleanField(default=False, verbose_name='Начислен')




class ChangeBalanceWithComment(models.Model):
	CHANGE_TYPE_CHOICES = [
		('telefoniya', 'telefoniya'),
		('internet', 'internet'),
		('alem', 'alem'),
		('kabel', 'kabel'),
	]

	number = models.CharField(verbose_name='Номер', max_length=20, blank=True)
	etrap = models.CharField(verbose_name='Этрап', max_length=64, blank=True)
	surname = models.CharField(max_length=500, verbose_name='Фамилия/организация', blank=True)
	name = models.CharField(max_length=500, verbose_name='Имя/Отдел', blank=True)
	street = models.CharField(max_length=500, verbose_name='Улица', blank=True)
	home = models.CharField(max_length=500, verbose_name='Дом', blank=True)
	flat = models.CharField(max_length=500, verbose_name='Квартира', blank=True)
 
	operator = models.CharField(verbose_name='Кто изменил баланс', max_length=256, blank=True)
	operatorFK = models.ForeignKey(User, verbose_name='Кто изменил баланс (FK)', on_delete=models.PROTECT)
 
	comment = models.TextField(verbose_name='Комментарий', blank=True)
	old_balance = models.FloatField(verbose_name='Старый баланс', default=0)
	new_balance = models.FloatField(verbose_name='Новый баланс', default=0)
 
	change_type = models.CharField(
			verbose_name='Тип',
			max_length=20,
			choices=CHANGE_TYPE_CHOICES,
			default='telefoniya'
		)

	
	date = models.DateTimeField(verbose_name='Когда изменили баланс', auto_now_add=True)


	def __str__(self):
		return f"Начисления {self.number} ({self.etrap}) ({self.change_type})"

	class Meta:
		verbose_name = 'Изменение баланса с комментарием'
		verbose_name_plural = 'Изменение баланса с комментариями'


class YhlasIyul2026InternetNach(models.Model):
	fio = models.CharField(max_length=500, verbose_name='Пользователь (ФИО)', blank=True)
	dogowor = models.CharField(max_length=100, verbose_name='Договор', blank=True)
	login = models.CharField(max_length=100, verbose_name='Учетное имя', blank=True)
	arenda = models.FloatField(verbose_name='Аренда', default=0)
	etrap = models.CharField(max_length=64, verbose_name='Этрап', blank=True)
	number = models.CharField(max_length=32, verbose_name='Номер абонента', blank=True)
	is_enterprises = models.CharField(max_length=10, verbose_name='Предприятия', blank=True)
	is_nach = models.BooleanField(default=False, verbose_name='Начислено в NachMinus')

	created_at = models.DateTimeField(verbose_name='Когда добавлено', auto_now_add=True, null=True, blank=True)
	who_add = models.CharField(max_length=500, verbose_name='Кто добавил', blank=True)
	file_name = models.CharField(max_length=500, verbose_name='Файл', blank=True)

	who_nach = models.CharField(max_length=500, verbose_name='Кто начислил', blank=True)
	nach_at = models.DateTimeField(verbose_name='Когда начислено', null=True, blank=True)

	def __str__(self):
		return f"{self.dogowor} {self.fio} {self.arenda}"

	class Meta:
		verbose_name = 'Yhlas Iyul 2026 Интернет начисление'
		verbose_name_plural = 'Yhlas Iyul 2026 Интернет начисление'


class AdminBroadcastMessage(models.Model):
	text = models.TextField(verbose_name='Текст сообщения', blank=True)
	is_enabled = models.BooleanField(default=False, verbose_name='Показывать на всех страницах')

	updated_at = models.DateTimeField(auto_now=True, verbose_name='Когда изменено')
	updated_by = models.CharField(max_length=500, verbose_name='Кто изменил', blank=True)

	def __str__(self):
		return f"[{'ON' if self.is_enabled else 'off'}] {self.text[:50]}"

	class Meta:
		verbose_name = 'Сообщение админа (баннер на всех страницах)'
		verbose_name_plural = 'Сообщение админа (баннер на всех страницах)'

