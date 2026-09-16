import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://restaurant:abc@localhost:5432/restaurant'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-de-desarrollo')

db = SQLAlchemy(app)

ORDENES_POR_PAGINA = 50


class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'content'}

    customer_id = db.Column(UUID(as_uuid=True), primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text, nullable=False)

    @property
    def nombre_completo(self):
        """Arma 'Nombre Apellido'; si falta alguno, usa lo que haya."""
        partes = [p for p in (self.first_name, self.last_name) if p]
        return ' '.join(partes) if partes else 'Cliente sin nombre registrado'


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'content'}

    order_id = db.Column(UUID(as_uuid=True), primary_key=True)
    customer_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('content.customers.customer_id'),
        nullable=False,
    )
    status = db.Column(db.Text, nullable=False)
    total = db.Column(db.Numeric(10, 2))
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False)

    cliente = db.relationship('Customer', backref='ordenes')


@app.route('/', methods=['GET'])
def salud():
    """GET / → comprobación rápida de que la conexión funciona."""
    total_ordenes = Order.query.count()
    return {'status': 'ok', 'ordenes_registradas': total_ordenes}


@app.route('/ordenes', methods=['GET'])
def listar_ordenes():
    """GET /ordenes → todas las órdenes, paginadas de a 50.
    Acepta ?page=N (por defecto 1)."""
    page = request.args.get('page', 1, type=int)
    if not page or page < 1:
        page = 1

    paginacion = (
        Order.query
        .order_by(Order.creation_date.desc())
        .paginate(page=page, per_page=ORDENES_POR_PAGINA, error_out=False)
    )

    return render_template(
        'ordenes/index.html',
        ordenes=paginacion.items,
        paginacion=paginacion,
    )


@app.errorhandler(404)
def no_encontrado(error):
    return render_template('errores/404.html'), 404


@app.errorhandler(500)
def error_interno(error):
    db.session.rollback()
    return render_template('errores/500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=False)
