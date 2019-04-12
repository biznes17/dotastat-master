from django import template
register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def values(dict):
	return dict.values()

@register.filter
def dict_access(dict,key):
	return dict[key]

@register.filter
def imgpath(string,int):
	return string + '.item_' + int + '.img_path'