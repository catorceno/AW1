import os # ¿qué hace os? ¿para qué sirve os?
from flask import Flask, jsonify, abort, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:abc@localhost:5432/lacarta'
) # ¿qué hace esto?
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # ¿qué hace esto?
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esta-clave-en-produccion') # ¿qué hace esto?

db = SQLAlchemy(app) # ¿qué es exactamente db?¿por qué todo se accede mediante este?
migrate = Migrate(app, db)

# MODELOS
# --------------------------------------------------
class Restaurante(db.Model): # una clase con parámetro?
    __tablename__ = 'restaurantes'

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
    ) # ¿qué hace esto?

    # ¿tiene algo de diferente o especial este método?
    def __repr__(self):
        return f'<Restaurante id={self.id} nombre={self.nombre}>'

class Plato(db.Model):
    __tablename__ = 'platos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        db.CheckConstraint('precio > 0', name='chk_platos_precio_positivo'),
    ) # ¿table args = constraints?¿qué más puede entrar aquí?

    def __repr__(self):
        return f'<Plato id={self.id} nombre={self.nombre}>'

# ENDPOINTS
# --------------------------------------------------
@app.route('/restaurantes', methods=['GET'])
def listar_restaurantes():
    ciudad = request.args.get('ciudad', '').strip()

    consulta = Restaurante.query
    if ciudad:
        consulta = consulta.filter(Restaurante.ciudad.ilike(f'%{ciudad}%'))

    restaurantes = consulta.order_by(Restaurante.nombre).all()

    return render_template(
        'restaurantes/index.html',
        restaurantes=restaurantes,
        ciudad_filtro=ciudad
    )

# ¿parámetro de la función viene por el header? ¿o por la url? nunca entendí bien este punto
@app.route('/restaurantes/<int:restaurante_id>', methods=['GET'])
def detalle_restaurante(restaurante_id):
    restaurante = Restaurante.query.get_or_404(restaurante_id)
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
    """Requisito 6: formulario precargado; al guardar, actualiza y redirige al detalle."""
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

    return redirect(url_for('detalle_restaurante', restaurante_id=restaurante_id))


@app.route('/restaurantes/<int:restaurante_id>/eliminar', methods=['POST'])
def eliminar_restaurante(restaurante_id):
    """Requisito 7: elimina el restaurante y sus platos en cascada. Solo POST."""
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
    """Requisito 8: agrega un plato al restaurante desde el formulario del detalle."""
    restaurante = Restaurante.query.get_or_404(restaurante_id)

    nombre = request.form.get('nombre', '').strip()
    precio_raw = request.form.get('precio', '').strip()
    disponible = request.form.get('disponible') == 'on'

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
    return redirect(url_for('listar_restaurantes'))

# ERRORES
# --------------------------------------------------
@app.errorhandler(404)
def no_encontrado(error):
    return render_template('errores/404.html'), 404

@app.errorhandler(500)
def no_encontrado(error):
    db.session.rollback() # ¿session?
    return render_template('errores/500.html'), 500

# MAIN
# --------------------------------------------------
if __name__ == '__main__':
    with app.app_context(): # ¿qué es y qué hace el context?
        db.create_all() # ¿qué hace esto?

    puerto = int(os.environ.get('PORT', 1028)) # ¿qué hace esto?
    app.run(host='0.0.0.0', port=puerto, debug=False)