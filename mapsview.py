from flask import Flask, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)

class Localizacao(db.Model):
    __tablename__ = "localizacao"
    localId = db.Column(db.Integer, primary_key = True) 
    latitude = db.Column(db.String) 
    longitude = db.Column(db.String)

class Delito(db.Model):
    delitoId = db.Column(db.Integer, primary_key = True)
    tipo_delito = db.Column(db.String)

class Boletins(db.Model):
    __tablename__ = "boletins"
    boletimId = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String) 
    rg = db.Column(db.String) 
    sexo = db.Column(db.String) 
    data = db.Column(db.String) 
    descricao = db.Column(db.String) 
    quando = db.Column(db.String)
    onde = db.Column(db.String)
    delito = db.Column(db.Integer)


@app.route("/")
def home():
    return render_template('formulario.html')

@app.route("/ocorrencias", methods = ['GET'])
def ocorrencias():
    data = Localizacao.query.all()
    return jsonify({'data' : data })

@app.route("/boletim", methods = ['POST'])
def boletim():
    id_delito = request.form['delito']
    
    delito = Delito.query.get(int(id_delito))

    data = {
        "nome" : request.form['nome'],
        "rg" : request.form['rg'],
        "sexo" : request.form['genero'],
        "data" : request.form['data'],
        "descricao" : request.form['descricao'],
        "quando" : request.form['quando'],
        "onde" : request.form['endereco'],
        "delito" : {
            "id" : delito.delitoId,
            "tipo_delito" : delito.tipo_delito
        }
    }

    db.session.merge(Boletins(name=data['nome'], rg= data['rg'], sexo=data['sexo'], data=data['data'], descricao =  data['descricao'], quando = data['quando'], onde = data['onde'], delito = delito.delitoId))
    db.session.commit()

    return jsonify({"data" : data})
