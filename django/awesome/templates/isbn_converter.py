from django import template

register = template.Library()

import string, sys

@register.filter
def isbn_converter(isbn_13):
    """
        Given a 13 digit ISBN, return a 10 digit ISBN
    """
    if len(isbn_13) != 13:
        return isbn_13
    isbn_13 = string.replace(isbn_13,"-","")
    isbn_10 = isbn_13[3:12]
    sum = 0
    for i in range(9):
        digit = string.atoi(isbn_10[i])
        sum += (10-i)*digit
    gap_num = 11 - sum%11
    if gap_num == 11: gap_num = 0
    if gap_num == 10: gap_num = "X"
    isbn_10 += str(gap_num)
    return isbn_10