from django.contrib import admin
from .models import Restaurante, Plato

class PlatoInline(admin.TabularInline):
    model = Plato
    extra = 1


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    inlines = (PlatoInline,)
    list_display = ('nombre', 'ciudad', 'telefono')
    list_filter = ('ciudad',)
    search_fields = ('nombre', 'direccion')


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'restaurante', 'precio', 'disponible')
    list_filter = ('disponible', 'restaurante')
    search_fields = ('nombre',)