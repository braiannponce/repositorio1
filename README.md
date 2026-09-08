# Servidor HTTP con WSGI en python:

* **Verbos utilizados:**
* **GET:** Utilizado para consultar y devolvernos la información del servidor.
* **POST:** Utilizado para mandar datos y crear un nuevo recurso.
* **PATCH:** Nos permite modificar datos de nuestro recurso, parcialmente.
* **DELETE:** Elimina un recurso elegido.

### Por qué POST no es idempotente:
POST no es idempotente porque cada vez que creamos un recurso este se crea con un identificador distinto.
