from django import template

register = template.Library()

@register.filter()
def censor(value):

   bad = ['понедельник', 'стране', 'песню', 'песня']
   for i in bad:
      if i.find(value):
         value = value.replace(i[1::], "*" * len(i))
   return f'{value}'