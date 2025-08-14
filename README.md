<h1>
 Proyecto Intranet
 <img src="/static/img/logo_2.png" alt="logo" width="50">
</h1>

Este proyecto lo estoy haciendo para mi trabajo final de grado superior *(Desarrollo de aplicaciones web)* y para la empresa en la que estoy de prácticas. Es un **CRM** *(Customer Relationship Management o Gestión de Relaciones con el Cliente)*.

## Tecnologías del proyecto:

### Frontend
 - HTML
 - CSS
 - JavaScript
 - Bootstrap
### Backend
 - Python
 - Django
### Sistema gestor de base de datos
 - Postgres

## Instalación

1. Se crea una carpeta en la cual se va a clonar el repositorio.
2. Abro una terminal en la carpeta y clono el repositorio:
```
git clone git@github.com:juanfher4/proyecto-intranet.git
```
3. Entro en la carpeta del repositorio:
```
cd .\proyecto-intranet\
```
4. Creo un entorno virtual llamado "venv":
```
python -m venv venv
```
5. Activo el entorno virtual:
```
.\venv\Scripts\activate
```
6. Hago las migraciones:
```
python manage.py makemigrations
python manage.py migrate
```
7. Creo el superusuario y le introduzco los valores:
```
python manage.py createsuperuser
```
8. Inicio el servidor:
```
python manage.py runserver
```
9. Entro a esta url: http://127.0.0.1:8000/
