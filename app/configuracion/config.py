LOCAL_CONFIG = False

rne3web = {'web_url': 'https://www.rtve.es/alacarta/rne/radio-3/',
           'patron_programas_audios_re': r"https://www.rtve.es/alacarta/audios/(?:[a-zA-Z]|[0-9]|[. -])+/",
           'boton_de_la_A_a_la_Z': {'css_selector': 'li.noactive:nth-child(3) > a:nth-child(1)'},
           'boton_next': {'css_selector': '.siguiente > a:nth-child(1)'},
           'paginas': {'css_selector': '.paginas'},
           'lista_programas': {'css_selector': '#tab2mini > div:nth-child(1)'},
           'num_programas': {'css_selector': '#tabladecontenidos > div:nth-child(1) > h2:nth-child(3) > span:nth-child(1)'},
           'total_sesiones_programa': {'xpath': '//*[@id="tabladecontenidos"]/div[1]/h2/span'},
           'nombre_programa': {'xpath': '//*[@id="wrapper"]/div[2]/div/div/div[1]/h2/a/span'},
           }

if LOCAL_CONFIG:
    backup_file_path = '/home/rafa/Dropbox/BackupBeeva/pycharm/rne3/app/rne3_data.pkl'
    postgres = {
        'user': 'postgres',
        'pw': '',
        'db': 'rne3',
        'host': 'localhost',
        'port': '5432',
    }
    postgres_string = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % postgres
else:
    backup_file_path = '/app/app/rne3_data.pkl'
    postgres_string = 'postgres://khsdgjiougdhgp:4f3049a6b8fc8c59ccb850a67c7d9fc2c01f637254ddc2ba785e8a8ed9822f0a@ec2-46-137-84-140.eu-west-1.compute.amazonaws.com:5432/da1fo9uv5r5kba'



