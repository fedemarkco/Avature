# Deployment
Para correr el servidor localmente se debe clonar el repositorio.
```
git clone git@github.com:fedemarkco/Avature.git
```
Y correr los siguientes comandos:
```
cd Avature
python3 -m venv project
source project/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
# Endpoint
Para agregar un job posting, primero hay que agregar los skills, a través del método POST:
```
http://localhost:8000/api/skill/
```
y el json del body sería, por ejemplo:
```
{
    "skill": "OOP"
}
```
También se puede ver los skills agregados, a través del método GET:
```
http://localhost:8000/api/skill/
```
Una vez agregado el skill, ahora podremos agregar un job posting, a través del método POST:
```
http://localhost:8000/api/job-posting/
```
y el json del body sería, por ejemplo:
```
{
    "name": "SSr Java Developer",
    "salary": 32000,
    "country": "Argentina",
    "skill": [1]
}
```
También se puede ver los job postings agregados, a través del método GET:
```
http://localhost:8000/api/job-posting/
```
Tenemos la posibilidad de agregar una alerta para cuando se agregue un job posting, a través del método POST:
```
http://localhost:8000/api/job-alert/
```
y el json del body sería, por ejemplo:
```
{
    "email": "fedemarkco2@gmail.com",
    "name": "Java", 
    "country": "Argentina",
    "salary_min": 30000,
    "salary_max": 35000
}
```
Las keys name, country, salary_min, salary_max son opcionales.

Las notificaciones se envían por correo, para que funcione el correo, es necesario crear un archivo .env y realizar las configuraciones necesarias, hay un ejemplo de este archivo con el nombre .env_example, en mi caso, las pruebas del envío de correo lo he hecho utilizando Mailtrap.

Para que el código interprete de dónde leer la url para las fuentes externas, también hay que configurarlo en el archivo .env, hay un ejemplo en .env_example. Este es para el caso del repositorio entregado para este fin que es JobberwockyExteneralJobs.

Para los test, se utilizó pytest. Se puede chequear ejecutando el comando:
```
pytest app/tests/
```
También se ha utilizado coverage para cubrir los testeos. Esto se puede comprobar ejecutando el comando:
```
pytest --cov=app
---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
app/__init__.py                            0      0   100%
app/admin.py                               1      0   100%
app/apps.py                                4      0   100%
app/constants.py                           4      0   100%
app/filters.py                            10      0   100%
app/migrations/0001_initial.py             5      0   100%
app/migrations/0002_modeljobalert.py       4      0   100%
app/migrations/__init__.py                 0      0   100%
app/models.py                             32      0   100%
app/notifications.py                      19      0   100%
app/serializers.py                        19      0   100%
app/services.py                           15      0   100%
app/tests/__init__.py                      0      0   100%
app/tests/test_services.py                30      0   100%
app/tests/test_views.py                   84      0   100%
app/urls.py                                8      0   100%
app/views.py                              49      0   100%
----------------------------------------------------------
TOTAL                                    284      0   100%
```

Para el código se ha utilizado isort y flake8.
