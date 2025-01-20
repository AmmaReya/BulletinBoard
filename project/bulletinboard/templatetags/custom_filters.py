from django import template

register = template.Library()

censor_list = ['дурак', 'дурочка', 'дура']


@register.filter()
def censor(value):
    for i in censor_list:
        value = value.replace(i, '*' * len(i))
    return value
