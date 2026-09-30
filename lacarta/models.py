import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurante(UUIDMixin, TimeStampedMixin):
    nombre = models.CharField(_('nombre'), max_length=120)
    ciudad = models.CharField(_('ciudad'), max_length=80)
    direccion = models.CharField(_('dirección'), max_length=200, blank=True)
    telefono = models.CharField(_('teléfono'), max_length=30, blank=True)

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'

    def __str__(self):
        return self.nombre


class Plato(UUIDMixin, TimeStampedMixin):
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
        verbose_name = 'Plato'
        verbose_name_plural = 'Platos'

    def __str__(self):
        return self.nombre