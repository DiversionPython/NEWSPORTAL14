from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from news .models import *
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

@receiver(m2m_changed, sender=PostCategory)
def post(sender, instance, *args, **kwargs):
    us_c = Category.objects.all().values_list("subscribers", flat=True)
    cat = Category.objects.all().values_list('name', "subscribers")
    sub = instance.postCategory.values_list("name", flat=True)
    print(us_c)
    print(cat)
    print(sub)
    for n, m in cat:
        if m is not None:
            print('n:', n)
            print('m:', m)
            for c in sub:
                print('c:', c)
                if n == c:
                    send_mail(subject=f"{instance.title}",
                              message=f"Здравствуй,{User.objects.get(pk=m)}."
                                      f" Новая статья в разделе! {c} \n "
                                      f"Заголовок статьи: {instance.title} \n"
                                      f" Текст статьи: {instance.text[:50]}",
                              from_email=os.getenv('DEFF_EMAIL'),
                              recipient_list=[f'{User.objects.get(pk=m).email}'],
                              )