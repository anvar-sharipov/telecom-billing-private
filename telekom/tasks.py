# # tasks.py
# import tablib
# from django.http import HttpResponse
# from django_q.tasks import async_task

# def generate_excel_report(start, end2, etrap):
#     from apps.telekom.models import NonLocalCall  # Импорт внутри функции чтобы избежать циклических импортов
    
#     calls = NonLocalCall.objects.filter(
#         DATE__range=[start[:10], end2[:10]], 
#         SUB_A_etrap=etrap, 
#         edara__in=['E', 'I']
#     )
    
#     headers = ("SUB_A_etrap", "SUB_A_number", "SUB_B_locations", "SUB_B_number", "TYPE", 
#                "1_MIN_PRICE", "DATE", "START", "FIN", "DUR", "MT", "total_price", "file_name")
    
#     data = tablib.Dataset(headers=headers)
    
#     for c in calls:
#         data.append((
#             c.SUB_A_etrap, c.SUB_A, c.SUB_B_locations, c.SUB_B, c.type, 
#             c.price, c.DATE, c.START, c.FIN, c.DUR, c.MT, 
#             c.total_price, c.file_name
#         ))
    
#     return data.xlsx