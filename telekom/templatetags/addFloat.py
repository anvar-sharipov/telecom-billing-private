from django import template

register = template.Library()

@register.simple_tag
def add(a, b=0, c=0, d=0, e=0, f=0, g=0, h=0, i=0):
    return a+b+c+d+e+f+g+h+i


@register.simple_tag
def mul_add(a,b):
    return a + b


# @register.filter
# def custom_math(value, arg):
#     print('gggg',value, arg)
#     # count, balance = map(int, args.split(','))
#     # return 10 + (count - 1) * 5 + balance
#     return eval(f"{value} + (({arg} - 1) * 5)")


# @register.filter
# def custom_math(value, args):
#     print('ggg',args)
#     count, balance = map(int, args.split(','))
#     return 10 + (count - 1) * 5 + balance


# @register.filter
# def custom_math(value, args):
#     print(args)
#     # balance, count = map(int, args.split(','))
#     # return eval(f"{value} + (({count} - 1) * 5) + {balance}")
#     return None


