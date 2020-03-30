from django.contrib import admin
try:
    from django.apps import apps
except admin.sites.AlreadyRegistered:
    pass


# Tomamos todos los modelos
models = apps.get_models()

# Y los registramos (para no tener que añadirlos de uno en uno) 
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
# Register your models here.
