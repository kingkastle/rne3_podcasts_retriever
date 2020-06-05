from collections import OrderedDict
from app.rne3_parser.rne3_parser import RNE3parser


def query_results(rne3, string_busqueda):
    results = {}
    for programa in rne3.informacion_programas.keys():
        for sesion_name in rne3.informacion_programas[programa]['sesiones'].keys():
            sesion = rne3.informacion_programas[programa]['sesiones'][sesion_name]
            if (string_busqueda.lower() in sesion['descripcion'].lower()) or\
                    (string_busqueda.lower() in sesion_name.lower()):
                if programa not in results.keys():
                    results[programa] = [sesion]
                else:
                    results[programa].append(sesion)
    results = OrderedDict(sorted([x for x in results.items()], key=lambda x: len(x[1]), reverse=True))
    return results


if __name__ == "__main__":

    rne3_data = RNE3parser()
    busqueda = 'billie holiday'
    resultados = query_results(rne3_data, busqueda)

