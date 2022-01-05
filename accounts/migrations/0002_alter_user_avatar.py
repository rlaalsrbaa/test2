# Generated by Django 4.0 on 2021-12-24 00:21
from ..models import User
from django.db import migrations, models

def gen_master(apps, schema_editor):
    for id in range(1, 4):
        username = f"user{id}"
        password = f"user{id}"
        first_name = f"이름{id}"
        last_name = f"성{id}"
        email = f"test{id}@test.com"
        gender = 'male'

        User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name,
                                 email=email, gender=gender)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_user_name_user_provider_accounts_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='100px * 100px 크기의 gif/png/jpg 이미지를 업로드해주세요.', upload_to='accounts/avatar/%Y/%m/%d', verbose_name='아바타'),
        ),
        migrations.RunPython(gen_master),
    ]
