# your_app/migrations/0002_mapea_mes.py
from django.db import migrations

def forwards(apps, schema_editor):
    gazette = apps.get_model('website', 'gazette')
    mapping = {
        "Enero":       1,
        "Febrero":     2,
        "Marzo":       3,
        "Abril":       4,
        "Mayo":        5,
        "Junio":       6,
        "Julio":       7,
        "Agosto":      8,
        "Septiembre":  9,
        "Octubre":    10,
        "Noviembre":  11,
        "Diciembre":  12,
    }
    for doc in gazette.objects.all():
        # solo mapea si el valor actual está en el diccionario
        if doc.month in mapping:
            doc.month = mapping[doc.month]
            doc.save(update_fields=['month'])

def backwards(apps, schema_editor):
    gazette = apps.get_model('website', 'gazette')
    inv = {
        1:  "Enero",
        2:  "Febrero",
        3:  "Marzo",
        4:  "Abril",
        5:  "Mayo",
        6:  "Junio",
        7:  "Julio",
        8:  "Agosto",
        9:  "Septiembre",
       10:  "Octubre",
       11:  "Noviembre",
       12:  "Diciembre",
    }
    for doc in gazette.objects.all():
        if doc.month in inv:
            doc.month = inv[doc.month]
            doc.save(update_fields=['month'])

class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_alter_infosubgroup_group_alter_infosubgroup_name'),  # ajusta al nombre de tu última migración
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
