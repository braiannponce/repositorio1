import re
import json
from wsgiref.simple_server import make_server

#Memoria
tasks = {}
id_counter = 1

def parse_body(environ):
    
    try:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError, TypeError):
        content_length = 0

    if content_length > 0:
        cuerpo = environ['wsgi.input'].read(content_length).decode('utf-8')
        return json.loads(cuerpo)
    return {}

def app(environ, start_response):
    metodo = environ.get('REQUEST_METHOD')
    ruta = environ.get('PATH_INFO')

    if ruta == '/' and metodo == 'GET':
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response('200 OK', headers)
        return [b'Bienvenido a la API de Tareas. Usa /tasks para interactuar con las tareas.']
    elif ruta == '/tasks' and metodo == 'GET':
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response('200 OK', headers)
        return [json.dumps(list(tasks.values())).encode('utf-8')]
    elif ruta == '/tasks' and metodo == 'POST':
        global id_counter
        data = parse_body(environ)
        task = {"id": id_counter, "title": data.get("title", "Tarea sin título"), "done": data.get("done", False)}
        tasks[id_counter] = task
        id_counter += 1
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response('201 Created', headers)
        return [json.dumps(task).encode('utf-8')]
     
    else: 
        match = re.match(r'^/tasks/(\d+)$', ruta)
        if match:
            task_id = int(match.group(1))

            if task_id not in tasks:
                headers = [('Content-type', 'text/plain; charset=utf-8')]
                start_response('404 Not Found', headers)
                return [json.dumps({"mensaje": f"Tarea {task_id} no encontrada"}).encode('utf-8')]

            if metodo == 'GET':
                    headers = [('Content-type', 'application/json; charset=utf-8')]
                    start_response('200 OK', headers)
                    return [json.dumps(tasks[task_id]).encode('utf-8')]

            elif metodo == 'PATCH':
                data = parse_body(environ)
                task = tasks[task_id]
                if 'title' in data:
                    task['title'] = data['title']
                if 'done' in data:
                    task['done'] = data['done']
                headers = [('Content-type', 'application/json; charset=utf-8')]
                start_response('200 OK', headers)
                return [json.dumps(task).encode('utf-8')]
            
            elif metodo == 'DELETE':
                    del tasks[task_id]
                    headers = [('Content-type', 'text/plain; charset=utf-8')]
                    start_response('200 OK', headers)
                    return [json.dumps({"mensaje": f"Tarea {task_id} eliminada correctamente"}).encode('utf-8')]

    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response('404 Not Found', headers)
    return [b'Pagina no encontrada']


if __name__ == '__main__':
    with make_server('', 9292, app) as httpd:
        print("Servidor corriendo en http://localhost:9292/ (Ctrl+C para salir)...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print("\nServidor detenido correctamente.")
    