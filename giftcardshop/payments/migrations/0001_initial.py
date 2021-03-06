# Generated by Django 3.0.8 on 2020-07-06 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intent_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('confirmedAt', models.DateTimeField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.Order')),
            ],
        ),
    ]
