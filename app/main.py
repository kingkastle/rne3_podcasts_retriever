from flask import Flask, render_template, request
from app.rne3_parser.rne3_parser import RNE3parser
from app.rne3_parser.query_rne3 import query_results
from app.configuracion.config import postgres_string
from app.db.model import db, additem
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_string

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
    print(string_busqueda, len(rne3_data.informacion_programas))
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
