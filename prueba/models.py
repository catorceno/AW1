import uuid
from django.db import models
class Genre(models.Model):
  # Un modelo típico en Django usa un número como id. En tales situaciones el campo
  # Tú sin embargo tendrás que declarar explícitamente la primary key.
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  
  # El primer argumento suele ser el nombre legible del campo
  name = models.CharField('name', max_length=255)
  
  # blank=True hace que el campo sea opcional para llenar.
  description = models.TextField('description', blank=True)
  
  # auto_now_add establecerá automáticamente la fecha de creación del registro
  created = models.DateTimeField(auto_now_add=True)
  
  # auto_now se modifica con cada actualización del registro
  modified = models.DateTimeField(auto_now=True)

  class Meta:
    # Tus tablas están en un esquema no estándar. Esto hay que indicarlo en la cla
    db_table = "content\".\"genre"
  
    # Los siguientes dos campos son responsables del nombre del modelo en la inter
    verbose_name = 'Género'
    verbose_name_plural = 'Géneros'