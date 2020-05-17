from flask import Flask, render_template, request
from app.rne3_parser.rne3_parser import RNE3parser
from app.rne3_parser.query_rne3 import query_results
from app.configuracion.config import postgres
from app.db.model import db, additem
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
# conf en local:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres

# conf heroku:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://khsdgjiougdhgp:4f3049a6b8fc8c59ccb850a67c7d9fc2c01f637254ddc2ba785e8a8ed9822f0a@ec2-46-137-84-140.eu-west-1.compute.amazonaws.com:5432/da1fo9uv5r5kba'

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def rne3_form():
    """ Pagina de bienvenida """

    return render_template('rne3.html')


@app.route('/resultados', methods=['POST'])
def form_submitted():
    """ Lanzar script para obtener ficheros"""
    rne3_data = RNE3parser()
    string_busqueda = request.form.get('artista')
    resultados = query_results(rne3_data, string_busqueda)
    total = sum([len(resultados[x]) for x in resultados.keys()])
    now = datetime.now()
    now = int(now.strftime("%Y%m%d"))
    additem(string_busqueda, now, total)
    return render_template('rne3_form_submitted.html', resultados=resultados,
                           programas=rne3_data.informacion_programas,
                           artista=string_busqueda,
                           total=total)


if __name__ == "__main__":
    app.run()
