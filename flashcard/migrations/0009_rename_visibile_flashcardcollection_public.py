# Generated by Django 4.2.16 on 2024-11-14 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0008_flashcardcollection_visibile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flashcardcollection',
            old_name='visibile',
            new_name='public',
        ),
    ]
