from config.bd import app, db, ma

class pedidos(db.Model):
    __tablename__ = 'pedido'

    id  = db.Column(db.Integer, primary_key=True)
    idtienda = db.Column(db.Integer, db.ForeignKey('tienda.id'))
    idcliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    direccionpedido = db.Column(db.String(50))
    total = db.Column(db.String(50))

    def __init__(self, id, idtienda, idcliente, direccionpedido, total):
        self.id = id
        self.idtienda = idtienda
        self.idcliente = idcliente 
        self.direccionpedido = direccionpedido
        self.total = total

with app.app_context():
    db.create_all()

class pedidos(ma.Schema):
    class Meta:
        fields = ('id', 'idtienda', 'idcliente,', 'direccionpedido', 'total')