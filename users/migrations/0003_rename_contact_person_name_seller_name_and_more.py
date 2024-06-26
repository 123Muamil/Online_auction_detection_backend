# Generated by Django 4.2.7 on 2024-06-02 07:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_buyer_account_created_buyer_email_buyer_id_card_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='contact_person_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='seller',
            old_name='contact_person_phone',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='contact_person_email',
        ),
        migrations.AddField(
            model_name='seller',
            name='account_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='seller',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='id_card',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
