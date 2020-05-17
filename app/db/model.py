from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def additem(busqueda, fecha, total):
    nueva_busqueda = BusquedasModel(busqueda=busqueda, fecha=fecha, resultados_obtenidos=total)
    db.session.add(nueva_busqueda)
    db.session.commit()


class BusquedasModel(db.Model):
    __tablename__ = 'busquedas'

    id = db.Column(db.Integer, primary_key=True)
    busqueda = db.Column(db.String())
    fecha = db.Column(db.Integer())
    resultados_obtenidos = db.Column(db.Integer())

    def __init__(self, busqueda, fecha, resultados_obtenidos):
        self.busqueda = busqueda
        self.fecha = fecha
        self.resultados_obtenidos = resultados_obtenidos

    def __repr__(self):
        return f"<Busquedas>"
