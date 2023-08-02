from django import template
class ApiException(Exception):
   pass

register = template.Library()

RestrSwords = ["жопа", "сволочь", "говно", "урод"]

@register.filter()
def censor(value):
   n = 0
   try:
      inSwordList = value.split()
      for sword_ in inSwordList:
         if sword_.lower() in RestrSwords:
            inSwordList[n] = sword_.replace(sword_[1:], '*' * len(sword_[1:]))
         n += 1
   except Exception as e:
      return f'Объект не является строкой!:\n{e}'
   return ' '.join(inSwordList)


