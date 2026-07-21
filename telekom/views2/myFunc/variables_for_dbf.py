

import datetime
import sqlite3

mugut = ['8888888','111','119','01','02','071','05', '03','9938001211','04','003229938001211','0032213000','00322071','383217','993322071','383272','384129',
	'383988','00488803','003229938001211', '112']

etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

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
	
# Проверка не был ли начислен этот файл
def check_a_file_has_been_added(file_):
	conn = sqlite3.connect(r'C:\Apache24\\htdocs\Dashoguz_telekom\db.sqlite3')
	cur = conn.cursor()
	get_name = """SELECT * FROM telekom_dbfnamelist WHERE name=?"""
	cur.execute(get_name, (file_,))
	name_in_DB = cur.fetchone()
	if name_in_DB:
		return True
	return False