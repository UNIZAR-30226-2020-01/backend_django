from django.contrib.auth.models import User
from models import S7_user, User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Para añadir un usuario a s7_user cada vez que se añada a User de Django
# (no podemos modificar su metodo save)
# Fuente: https://books.agiliq.com/projects/django-orm-cookbook/en/latest/update_denormalized_fields.html
@receiver(pre_save, sender=User, dispatch_uid="add_s7_user")
def add_s7_user(sender, **kwargs):
    user = kwargs['instance']
    print('creating s7_user from', str(user))
    if user.pk: # si existe el usuario
        Category.objects.filter(pk=hero.category_id).update(hero_count=F('hero_count')+1)
        s7_user = S7_User.create_from_user(user)
        s7_user.save()
