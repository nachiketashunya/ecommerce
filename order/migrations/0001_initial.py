# Generated by Django 3.0.1 on 2020-01-30 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
        ('cart', '0001_initial'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=120)),
                ('status', models.CharField(choices=[('created', 'Created'), ('shipped', 'Shipped'), ('paid', 'Paid'), ('refunded', 'Refunded')], default='created', max_length=50)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=100.0, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=100.0, max_digits=100)),
                ('active', models.BooleanField(default=True)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='address.Address')),
                ('billing_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='address.Address')),
            ],
        ),
    ]
