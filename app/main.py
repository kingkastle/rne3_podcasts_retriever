from flask import Flask, render_template, request
from app.rne3_parser.rne3_parser import RNE3parser
from app.rne3_parser.query_rne3 import query_results

app = Flask(__name__)

# Linux: Ctrl+Shift+R

rne3_data = RNE3parser()

@app.route('/', methods=['GET'])
def rne3_form():
    """ Paguina de bienvenida """

    return render_template('rne3.html')


@app.route('/resultados', methods=['POST'])
def form_submitted():
    """ Lanzar script para obtener ficheros"""
    string_busqueda = request.form.get('artista')
    resultados = query_results(rne3_data, string_busqueda)
    total = sum([len(resultados[x]) for x in resultados.keys()])
    return render_template('rne3_form_submitted.html', resultados=resultados,
                           programas=rne3_data.informacion_programas,
                           artista=string_busqueda,
                           total=total)


if __name__ == "__main__":
    app.run()
