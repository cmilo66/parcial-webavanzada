from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Finca(db.Model):
    nit         = db.Column(db.String(30), primary_key = True, unique = True)
    nombre      = db.Column(db.String(30))
    contacto    = db.Column(db.String(30))
    direccion   = db.Column(db.String(30))
    correo      = db.Column(db.String(30))
    propietario = db.Column(db.String(30))

    def __init__(self, nit, nombre,contacto, direccion, correo , propietario) :
        self.nit         = nit
        self.nombre      = nombre
        self.contacto    = contacto
        self.direccion   = direccion
        self.correo      = correo
        self.propietario = propietario

class Lote(db.Model):
    id                   = db.Column(db.Integer, primary_key = True, unique = True)
    numero               = db.Column(db.String(15))
    nit_finca            = db.Column(db.String(30))
    cultivo              = db.Column(db.String(30))
    existencias          = db.Column(db.Integer)
    responsable          = db.Column(db.String(25))

    def __init__(self, id, numero, nit_finca,responsable , cultivo,existencias ) :
        self.id          = id
        self.numero      = numero
        self.nit_finca   = nit_finca
        self.cultivo     = cultivo
        self.existencias = existencias
        self.responsable = responsable
        

    def serialize(self):
        return {
        "id" : self.id ,
        "numero" : self.numero,
        "nit_finca" : self.nit_finca,
        "cultivo" : self.cultivo,
        "existencias" : self.existencias,
        "responsable" : self.responsable,
        
        }


with app.app_context():
    db.create_all()


class FincaSchema(ma.Schema):
    class Meta:
        fields = ("nit","nombre","contacto","direccion","correo","propietario")

class LoteSchema(ma.Schema):
    class Meta:
        fields = ("id","numero","nit_finca","responsable","cultivo","existencias")

class VentaSchema(ma.Schema):
    class Meta:
        fields = ("id","nit_finca","id_Lote","cantidad_Compra")


finca_schema  = FincaSchema()
fincas_schema = FincaSchema(many=True)

lote_schema   = LoteSchema()
lotes_schema  = LoteSchema(many=True)

venta_schema  = VentaSchema()
ventas_schema = VentaSchema(many=True)


@app.route('/finca', methods=['POST'])
def crear_finca():
    finca_data = request.json
    new_finca = Finca(**finca_data)
    db.session.add(new_finca)

    db.session.commit()
    return finca_schema.jsonify(new_finca)

@app.route('/fincas', methods=['GET'])
def obtener_Fincas():
    all_Fincas = Finca.query.all()
    result = fincas_schema.dump(all_Fincas)
    
    return jsonify(result)

@app.route('/finca/<nit>', methods=['GET'])
def obtener_Finca(nit):
    finca = Finca.query.get(nit)

    return finca_schema.jsonify(finca)

@app.route('/finca/<nit>', methods=['PUT'])
def agregar_Finca(nit):
    finca = Finca.query.get(nit)

    if not finca:
        return "la finca no se encuentra en el registro"

    finca.nombre      = request.json.get("nombre", finca.nombre)
    finca.contacto    = request.json.get("contacto", finca.contacto)
    finca.propietario = request.json.get("propietario", finca.propietario)
    finca.direccion   = request.json.get("direccion", finca.direccion)
    finca.correo      = request.json.get("correo", finca.correo)

    db.session.commit()

    return finca_schema.jsonify(finca)


@app.route('/finca/<nit>', methods=['DELETE'])
def eliminar_Finca(nit):
   finca = Finca.query.get(nit)
   db.session.delete(finca)
   db.session.commit()

   return finca_schema.jsonify(finca)


@app.route('/lote', methods=['POST'])
def crear_lote():
    try:
        lote_data = request.json

        # datos para nuevo lote
        numero      = lote_data["numero"]
        nit_finca   = lote_data["nit_finca"]
        responsable = lote_data["responsable"]
        cultivo     = lote_data["cultivo"]
        existencias = lote_data["existencias"]

       
        finca = Finca.query.filter_by(nit=nit_finca).first()
        if not finca:
            return f"El NIT de la finca asignada no es válido o no existe: {nit_finca}"

        # nuevo lote
        new_lote = Lote(numero=numero, nit_finca=nit_finca, responsable=responsable,
                        cultivo=cultivo, existencias=existencias)

        # Guardar nuevo lote 
        db.session.add(new_lote)
        db.session.commit()

        
        return lote_schema.jsonify(new_lote)

    except Exception as e:
        print(e)
        return "lote no registrado intentar de nuevo"

    
@app.route('/lotes', methods=['GET'])
def obtener_Lotes():
    all_Lotes = Lote.query.all()
    result = lotes_schema.dump(all_Lotes)
    
    return jsonify(result)

@app.route('/lote/<id>', methods=['GET'])
def obtener_Lote(id):
    lote = Lote.query.get(id)

    return lote_schema.jsonify(lote)

@app.route('/lote/<id>', methods=['PUT'])
def agregar_Lote(id):
    lote = Lote.query.get(id)

    numero      = request.json["numero"]
    nit_finca   = request.json["nit_finca"]
    cultivo     = request.json["cultivo"]
    existencias = request.json["existencias"]
    responsable = request.json["responsable"]
    

    lote.numero      = numero
    lote.nit_finca   = nit_finca
    lote.cultivo     = cultivo
    lote.existencias = existencias
    lote.responsable = responsable
    

    db.session.commit()

    return lote_schema.jsonify(lote)

@app.route('/lote/<id>', methods=['DELETE'])
def eliminar_Lote(id):
    lote = Lote.query.get(id)

    db.session.delete(lote)
    db.session.commit()

    return lote_schema.jsonify(lote)


@app.route('/Inventario/<nit>', methods=['GET'])
def obtener_Inventario(nit):
    finca = Finca.query.get(nit)

    if not finca:
        return "Esta Finca no se encuentra en el registro"

    lotes = Lote.query.filter_by(nit_finca=nit).all()

    inventario = []
    for lote in lotes:
        inventario.append(lote.serialize())

    return jsonify(inventario)


if __name__ == "__main__":
    app.run(debug=True)