# Generated by Django 3.0.8 on 2021-03-23 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=6, unique=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='QRCodes',
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('qr_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='qrcode', serialize=False, to='qrcode.UniqueID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=80, null=True)),
                ('contact', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
    ]
