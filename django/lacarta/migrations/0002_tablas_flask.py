from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lacarta', '0001_initial'),
    ]

    operations = [
        # 1) Elimina las tablas propias de Django (lacarta_plato y lacarta_restaurante)
        migrations.DeleteModel(name='Plato'),
        migrations.DeleteModel(name='Restaurante'),
        # 2) Declara los modelos sobre las tablas de Flask.
        #    managed=False: Django no crea ni altera estas tablas.
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120, verbose_name='nombre')),
                ('ciudad', models.CharField(max_length=80, verbose_name='ciudad')),
                ('direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='dirección')),
                ('telefono', models.CharField(blank=True, max_length=30, null=True, verbose_name='teléfono')),
            ],
            options={
                'verbose_name': 'Restaurante',
                'verbose_name_plural': 'Restaurantes',
                'db_table': 'restaurantes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120, verbose_name='nombre')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='precio')),
                ('disponible', models.BooleanField(default=True, verbose_name='disponible')),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platos', to='lacarta.restaurante')),
            ],
            options={
                'verbose_name': 'Plato',
                'verbose_name_plural': 'Platos',
                'db_table': 'platos',
                'managed': False,
            },
        ),
    ]