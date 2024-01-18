from django import template

register = template.Library()


bad_words = ['редиска',
             'овощь',
             'футбол',
             'музыка',
             'Редиска',
             ]


@register.filter()
def censor(value):
    list = value.split()
    censor_list = []
    for word in list:
        if word in bad_words:
            word = "*" * len(word)
            censor_list.append(word)
        else:
            censor_list.append(word)
    return ' '.join(censor_list)