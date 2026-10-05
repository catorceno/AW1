import os # Permite hacer operaciones sobre el SO. En este caso se usa para leer las variables de entorno del SO. Con docker, este se encarga de leer el archivo .env e inyectarlas en el SO.
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# flask se ubica en la carpeta de este archivo
# al ejecutar desde terminal (ej: python app.py) __name__ es igual a __main__, de esta manera flask encuentra en el motor interno de Python la ruta absoluta donde se lanzó el archivo app.py
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:123@localhost:5432/lacarta') # connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva un sistema que emite señales cada vez que un objeto cambia. False por convención porque consume memoria y rendimiento innecesariamente.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret-key') # para cifrar y tener control de autenticación

db = SQLAlchemy(app) # instancia que conecta la app Flask con el ORM SQLAlchemy y por tanto la base de datos

# (db.Model): herencia en Python
class Restaurante(db.Model):
    __tablename__ = 'restaurantes' # cómo se llamará la tabla en PostgresSQL

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(30))

    platos = db.relationship(
        'Plato',
        backref='restaurante',
        cascade='all, delete-orphan',
        lazy=True
    )

    # representation, propio de Python: definir cómo se debe ver en texto un objeto cuando lo imprimes o inspeccionas, pensado especialmente para dev y debug
    def __repr__(self):
        return f'<Restaurante id={self.id} nombre={self.nombre}>'

class Plato(db.Model):
    __tablename__ = 'platos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id', ondelete='CASCADE'),  nullable=False)

    __table_args__ = (
        db.CheckConstraint('precio > 0', name='chk_platos_precio_positivo'),
    )

    def __repr__(self):
        return f'<Plato id={self.id} nombre={self.nombre}>'

@app.route('/restaurantes', methods=['GET'])
def listar_restaurantes():
    # request.args: es un diccionario de Flask que contiene los parámetros de consulta (query string) que el usuario envía en la URL, los valores que aparece después del signo de interrogación ? en la URL
    # request.args.get('ciudad'): busca la clave ciudad dentro de la URL
    # si se entra a la URL limpia sin parámetros, '' como segundo parámetro evita que strip() falle porque sin este se intentaría hace None.strip() lo que daría error
    ciudad = request.args.get('ciudad', '').strip()

    consulta = Restaurante.query

    if ciudad:
        consulta = consulta.filter(Restaurante.ciudad.ilike(f'%{ciudad}%'))

    restaurantes = consulta.order_by(Restaurante.nombre).all()

    # nombre plantilla html, variables clave-valor variable_jinja_html=variable_python
    return render_template(
        'restaurantes/index.html',
        restaurantes=restaurantes,
        ciudad_filtro=ciudad
    )

# <int:restaurante_id>: Path Parameter, no viene ni en los headers ni del query string ?
# asociación automática entre el Path Parameter y el parámetro de la función restaurante_id
@app.route('/restaurantes/<int:restaurante_id>', methods=['GET'])
def detalle_restaurante(restaurante_id):
    restaurante = Restaurante.query.get_or_404(restaurante_id) # get_or_404(): ejecuta la consulta y si no encuentra nada, Flask devuelve automáticamente una página de error 404
    return render_template('restaurantes/detalle.html', restaurante=restaurante)

@app.route('/restaurantes/crear', methods=['GET'])
def formulario_crear_restaurante():
    return render_template('restaurantes/formulario.html', restaurante=None)

@app.route('/restaurantes/crear', methods=['POST'])
def crear_restaurante():
    nombre = request.form.get('nombre', '').strip()
    ciudad = request.form.get('ciudad', '').strip()
    direccion = request.form.get('direccion', '').strip() or None
    telefono = request.form.get('telefono', '').strip() or None

    if not nombre or not ciudad:
        flash('Nombre y ciudad son obligatorios.', 'error')
        return redirect(url_for('formulario_crear_restaurante'))

    nuevo = Restaurante(nombre=nombre, ciudad=ciudad, direccion=direccion, telefono=telefono)

    try:
        db.session.add(nuevo)
        db.session.commit()
        flash(f'Restaurante "{nombre}" creado correctamente.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo crear el restaurante. Intenta de nuevo.', 'error')
    finally:
        db.session.close()

    return redirect(url_for('listar_restaurantes'))

@app.route('/restaurantes/<int:restaurante_id>/editar', methods=['GET', 'POST'])
def editar_restaurante(restaurante_id):
    restaurante = Restaurante.query.get_or_404(restaurante_id)

    if request.method == 'GET':
        return render_template('restaurantes/formulario.html', restaurante=restaurante)

    nombre = request.form.get('nombre', '').strip()
    ciudad = request.form.get('ciudad', '').strip()
    direccion = request.form.get('direccion', '').strip() or None
    telefono = request.form.get('telefono', '').strip() or None

    if not nombre or not ciudad:
        flash('Nombre y ciudad son obligatorios.', 'error')
        return redirect(url_for('editar_restaurante', restaurante_id=restaurante_id))

    try:
        restaurante.nombre = nombre
        restaurante.ciudad = ciudad
        restaurante.direccion = direccion
        restaurante.telefono = telefono
        db.session.commit()
        flash('Restaurante actualizado correctamente.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo actualizar el restaurante.', 'error')
    finally:
        db.session.close()

    return redirect(url_for('detalle_restaurante', restaurante_id=restaurante_id)) # se para restaurante_id para que url_for construya la URL, para que se utilizado como Path Parameter luego

@app.route('/restaurantes/<int:restaurante_id>/eliminar', methods=['POST'])
def eliminar_restaurante(restaurante_id):
    restaurante = Restaurante.query.get_or_404(restaurante_id)
    nombre = restaurante.nombre

    try:
        db.session.delete(restaurante)
        db.session.commit()
        flash(f'Restaurante "{nombre}" eliminado.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo eliminar el restaurante.', 'error')
    finally:
        db.session.close()

    return redirect(url_for('listar_restaurantes'))

@app.route('/restaurantes/<int:restaurante_id>/platos', methods=['POST'])
def agregar_plato(restaurante_id):
    restaurante = Restaurante.query.get_or_404(restaurante_id)

    nombre = request.form.get('nombre', '').strip()
    precio_raw = request.form.get('precio', '').strip()
    disponible = request.form.get('disponible') == 'on' # funcionamiento nativo de elemento de formulario checkbox de html

    error = None
    precio = None

    if not nombre:
        error = 'El nombre del plato es obligatorio.'
    else:
        try:
            precio = float(precio_raw)
            if precio <= 0:
                error = 'El precio debe ser mayor que cero.'
        except ValueError:
            error = 'El precio debe ser un número válido.'

    if error:
        flash(error, 'error')
        return redirect(url_for('detalle_restaurante', restaurante_id=restaurante_id))

    nuevo_plato = Plato(
        nombre=nombre,
        precio=precio,
        disponible=disponible,
        restaurante_id=restaurante.id,
    )

    try:
        db.session.add(nuevo_plato)
        db.session.commit()
        flash(f'Plato "{nombre}" agregado.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo agregar el plato.', 'error')
    finally:
        db.session.close()

    return redirect(url_for('detalle_restaurante', restaurante_id=restaurante_id))

@app.route('/', methods=['GET'])
def raiz():
    # url_for: construcción dinámica de URLs, devuelve el texto de la URL asociada a esa función
    return redirect(url_for('listar_restaurantes'))

# capturar errores globales de HTTP en Flask
# cuando ocurre un problema en cualquier parte de la aplicación, Flask interrumpe la ejecución normal y envía la petición a estas funciones
@app.errorhandler(404)
def no_encontrado(error):
    return render_template('errores/404.html'), 404 # cuando ejecutas get_or_404()

@app.errorhandler(500)
def error_servidor(error):
    db.session.rollback()
    return render_template('errores/500.html'), 500

# __variable__: dunder (double underscore) para atributos especiales de configuración interna
# al ejecutar desde terminal (ej: python app.py), Python asigna __main__ a su variable __name__
# la condicional sirve para que el main no se ejecute si el archivo es utilizado mediante un import en otro lado
if __name__ == '__main__':

    # with: activa Context Manager, equivale a un try/finally PENDIENTE
    # en peticiones web se activa el context automáticamente, aquí no se está haciendo ninguna petición entonces se debe activar de manera manual
    with app.app_context():
        db.create_all() # crea todas las tablas

    puerto = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=puerto, debug=False)