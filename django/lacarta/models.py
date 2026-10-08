from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Estas tablas las crea y gestiona Flask (SQLAlchemy).
# Django solo las lee y escribe: managed = False evita que las cree o modifique.
class Restaurante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(_('nombre'), max_length=120)
    ciudad = models.CharField(_('ciudad'), max_length=80)
    direccion = models.CharField(_('dirección'), max_length=200, blank=True, null=True)
    telefono = models.CharField(_('teléfono'), max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurantes'
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    id = models.AutoField(primary_key=True)
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name='platos'
    )
    nombre = models.CharField(_('nombre'), max_length=120)
    precio = models.DecimalField(
        _('precio'), max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    disponible = models.BooleanField(_('disponible'), default=True)

    class Meta:
        managed = False
        db_table = 'platos'
        verbose_name = 'Plato'
        verbose_name_plural = 'Platos'

    def __str__(self):
        return self.nombre