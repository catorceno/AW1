import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedMixin(models.Model):
  # auto_now_add establecerá automáticamente la fecha de creación del registro
  created = models.DateTimeField(auto_now_add=True)
  # auto_now se modifica con cada actualización del registro
  modified = models.DateTimeField(auto_now=True)

  class Meta:
    # Este parámetro indica a Django que esta clase no es una representación de ta
    abstract = True

class UUIDMixin(models.Model):
  # Un modelo típico en Django usa un número como id. En tales situaciones el campo
  # Tú sin embargo tendrás que declarar explícitamente la primary key.
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  
  class Meta:
    abstract = True

class Genre(UUIDMixin, TimeStampedMixin):  
  # El primer argumento suele ser el nombre legible del campo
  name = models.CharField('name', max_length=255)
  
  # blank=True hace que el campo sea opcional para llenar.
  description = models.TextField('description', blank=True)

  class Meta:
    # Tus tablas están en un esquema no estándar. Esto hay que indicarlo en la cla
    db_table = "content\".\"genre"
  
    # Los siguientes dos campos son responsables del nombre del modelo en la inter
    verbose_name = 'Género'
    verbose_name_plural = 'Géneros'

  def __str__(self):
    return self.name

class Person(UUIDMixin, TimeStampedMixin):
  full_name = models.CharField('full_name', max_length=255)

  class Meta:
    db_table = "content\".\"person"
    verbose_name = 'Persona'
    verbose_name_plural = 'Personas'

  def __str__(self):
    return self.full_name
  
class FilmWork(UUIDMixin, TimeStampedMixin):
  class FilmType(models.TextChoices):
    MOVIE = 'movie', 'movie'
    TV_SHOW = 'tv_show', 'tv_show'

  title = models.CharField('title', max_length=255)
  description = models.TextField('description', blank=True)
  creation_date = models.DateField('creation_date', blank=True, null=True)
  rating = models.FloatField('rating', blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
  type = models.TextField('type', choices=FilmType.choices)
  
  genres = models.ManyToManyField(Genre, through='GenreFilmWork')
  persons = models.ManyToManyField(Person, through='PersonFilmWork')

  certificate = models.CharField(_('certificate'), max_length=512, blank=True)
  
  # El parámetro upload_to indica en qué subcarpeta se almacenarán los archivos subi
  # La carpeta base se indica en el archivo de configuración como MEDIA_ROOT
  file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

  class Meta:
    db_table = "content\".\"film_work"
    verbose_name = 'Película'
    verbose_name_plural = 'Películas'

  def __str__(self):
    return self.title

class GenreFilmWork(UUIDMixin):
  film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
  genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "content\".\"genre_film_work"

class PersonFilmWork(UUIDMixin):
  film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
  person = models.ForeignKey('Person', on_delete=models.CASCADE)
  role = models.TextField('role')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "content\".\"person_film_work"