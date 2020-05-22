# rne3_podcasts_retriever
Aplicación web que descarga los podcasts de tu programa favorito de Radio3 

# Levantar servidor Flaks en local
```
# desde el directorio donde tengas app.py
source activate your_env
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
```

# Levantar postgres en heroku:
1. provisionar el recurso postgres
2. levantar la db:
 ```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
