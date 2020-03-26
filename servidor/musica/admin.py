from django.contrib import admin
try:
    from django.apps import apps
except admin.sites.AlreadyRegistered:
    pass

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
# Register your models here.
