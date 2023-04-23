from django.template.defaulttags import register

@register.filter
def get_item(lst, index):
    return lst[index]