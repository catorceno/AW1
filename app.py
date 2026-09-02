import os # ¿qué hace os? ¿para qué sirve os?
from flask import Flask, jsonfy, abort, request, render_template, redirect, url_for
from flask_sqlachemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:abc@localhost:5432/lacarta'
) # ¿qué hace esto?
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # ¿qué hace esto?
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia-esta-clave-en-produccion') # ¿qué hace esto?

db = SQLAchemy(app) # ¿qué es exactamente db?¿por qué todo se accede mediante este?

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
    pass

@app.route('/restaurantes/crear', methods=['GET'])
def formulario_crear_restaurante():
    pass

@app.route('/restaurantes/crear', methods=['POST'])
def crear_restaurante():
    pass

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