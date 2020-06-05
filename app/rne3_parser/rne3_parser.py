import re
import time
import os
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, \
    NoSuchElementException, TimeoutException
import requests
from app.configuracion.config import rne3web, backup_file_path
from app.rne3_parser.navegador import Navigator


class RNE3parser(Navigator):
    """
    Clase destinada a parsear la web de radio3 y buscar los programas y sus correspondientes audios
    """

    def __init__(self):
        self.web_url = rne3web['web_url']
        self.patron_programas_audios_re = rne3web['patron_programas_audios_re']
        self.boton_de_la_A_a_la_Z = rne3web['boton_de_la_A_a_la_Z']
        self.boton_next = rne3web['boton_next']
        self.paginas = rne3web['paginas']
        self.lista_programas = rne3web['lista_programas']
        self.backup_file_path = backup_file_path
        self.informacion_programas = self._load()

    def _load(self):
        if os.path.isfile(self.backup_file_path):
            return pickle.load(open(self.backup_file_path, "rb"))
        else:
            print("New file generated...")
            return {}

    def _save_rne3_data(self):
        f = open(self.backup_file_path, "wb")
        pickle.dump(self.informacion_programas, f)
        f.close()

    def obtener_lista_programas(self, max_iteraciones=20):
        driver = self.launch_driver(self.web_url)
        self.presionar_boton(driver, self.boton_de_la_A_a_la_Z)
        while max_iteraciones > 0:
            programas = self._extraer_programas(driver, self.lista_programas, self.patron_programas_audios_re)
            for programa in programas:
                if (self.informacion_programas is None) or (programa not in self.informacion_programas.keys()):
                    self.informacion_programas[programa] = programas[programa]
            self.presionar_siguiente(driver, sleep=0.5)
            max_iteraciones -= 1
        self._save_rne3_data()
        driver.close()
        return

    @staticmethod
    def _extraer_programas(driver, elemento, patron_programas_audios):
        element = driver.find_element_by_css_selector(elemento['css_selector'])
        elems = element.find_elements_by_tag_name('a')
        path_programas = [elem.get_attribute('href') for elem in elems if
                          re.fullmatch(patron_programas_audios, elem.get_attribute('href')) is not None]
        return {x.split("/")[-2]: {'url': x} for x in path_programas}

    @staticmethod
    def _informacion_sesion(Tag):
        informacion = {}
        try:
            informacion['descripcion'] = Tag.find("span", itemprop="description").get('content')
            informacion['nombre'] = Tag.find("span", itemprop="name").get('content')
            informacion['duracion'] = Tag.find("span", itemprop="timeRequired").get('content')
            informacion['fecha_publicacion'] = Tag.find("span", itemprop="datePublished").get('content')
            informacion['enlace_mp3'] = Tag.find('span', {'class': 'col_tip'}).find('a').get('href')
        except:
            return {}
        return informacion

    def obtener_sesiones(self, retransmision, sleep=0.5, max_sessions=120):
        if 'sesiones' not in self.informacion_programas[retransmision].keys():
            self.informacion_programas[retransmision]['sesiones'] = {}
        self.informacion_programas[retransmision]['num_sesiones'] = len(self.informacion_programas[retransmision]['sesiones'])
        url_programa = self.informacion_programas[retransmision]['url']
        driver = self.launch_driver(url_programa)
        print("\nProcesando: {0} con sesiones incluidas: {1}".format(retransmision, len(self.informacion_programas[retransmision]['sesiones'])))
        pag_previa = 0
        while max_sessions > 0:
            liTags = self.extraer_litags(driver.page_source)
            for Tag in liTags:
                Tag.location_once_scrolled_into_view
                sesion = self._informacion_sesion(Tag)
                if len(sesion) == 0:
                    continue
                if (self.informacion_programas[retransmision] is None) or \
                        (sesion['nombre'] not in self.informacion_programas[retransmision]['sesiones'].keys()):
                    self.informacion_programas[retransmision]['sesiones'][sesion['nombre']] = sesion

            if len(self.informacion_programas[retransmision]['sesiones']) > self.informacion_programas[retransmision]['num_sesiones']:
                print("{0}".format(len(self.informacion_programas[retransmision]['sesiones'].keys())), end="..", flush=True)
                self.informacion_programas[retransmision]['num_sesiones'] = len(self.informacion_programas[retransmision]['sesiones'])
            try:
                pagina_activa = self._pagina_activa(driver, rne3web['paginas']['css_selector'])
                if pagina_activa is None or pagina_activa == pag_previa:
                    break
                else:
                    pag_previa = pagina_activa
                self.presionar_siguiente(driver, sleep)
            except (StaleElementReferenceException, ElementNotInteractableException, TimeoutException, NoSuchElementException) as e:
                print(e)
                break
            max_sessions -= 1
        print("\n   Completado! parseadas paginas: {0} y un total de {1} sesiones incluidas\n".format(pag_previa, len(self.informacion_programas[retransmision]['sesiones'])))
        self._save_rne3_data()
        driver.close()
        return

    def presionar_siguiente(self, driver, sleep):
        self.presionar_boton(driver, self.boton_next, timeout=200)
        time.sleep(sleep)
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_UP)

    def descargar_sesiones(self, dest_folder):
        for nombre in self.sesiones.keys():
            mp3 = requests.get(self.sesiones[nombre]['enlace_mp3'])
            with open('{0}/{1}.mp3'.format(dest_folder, nombre), 'wb') as f:
                f.write(mp3.content)


if __name__ == "__main__":

    parseo_web = RNE3parser()
    parseo_web.obtener_lista_programas()
    start_parsing = False
    for programa in parseo_web.informacion_programas.keys():
        # if programa != 'musicas-posibles': continue
        if programa == 'notas-confusas':
            start_parsing = True
            continue
        if start_parsing:
            parseo_web.obtener_sesiones(programa)







