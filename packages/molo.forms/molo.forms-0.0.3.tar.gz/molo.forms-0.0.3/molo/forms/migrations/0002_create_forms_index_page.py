# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_forms_index(apps, schema_editor):
    from molo.core.models import Main
    from molo.forms.models import FormsIndexPage
    main = Main.objects.all().first()

    if main:
        forms_index = FormsIndexPage(title='Forms', slug='forms')
        main.add_child(instance=forms_index)
        forms_index.save_revision().publish()


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_forms_index),
    ]