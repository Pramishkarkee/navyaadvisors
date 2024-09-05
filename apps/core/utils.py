from django.utils import timezone
from rest_framework.utils import model_meta

def update(instance, data):
    info = model_meta.get_field_info(instance)

    for attr, value in data.items():
        if attr in info.relations and info.relations[attr].to_many:
            field = getattr(instance, attr)
            field.set(value)
        else:
            setattr(instance, attr, value)
    instance.updated = timezone.now()
    instance.save()
