rne3web = {'web_url': 'https://www.rtve.es/alacarta/rne/radio-3/',
           'patron_programas_audios_re': r"https://www.rtve.es/alacarta/audios/(?:[a-zA-Z]|[0-9]|[. -])+/",
           'boton_de_la_A_a_la_Z': {'css_selector': 'li.noactive:nth-child(3) > a:nth-child(1)'},
           'boton_programas_next': {'css_selector': '.siguiente > a:nth-child(1)'},
           'boton_sesiones_next': {'css_selector': '.siguiente > a:nth-child(1)'},
           'paginas': {'css_selector': '.paginas'},
           'lista_programas': {'css_selector': '#tab2mini > div:nth-child(1)'},
           'num_programas': {'css_selector': '#tabladecontenidos > div:nth-child(1) > h2:nth-child(3) > span:nth-child(1)'}
           }
backup_file_path = '/app/_data/rne3_data.pkl'

