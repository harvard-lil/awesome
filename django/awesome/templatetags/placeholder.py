from django.template import Library
import re

register = Library()

def placeholder(value, token):
	value.field.widget.attrs["placeholder"] = token
	return value

register.filter(placeholder)