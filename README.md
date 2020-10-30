# Comandos para criar uma aplicação utilizando Redis com Docker
* Para criar um novo projeto Django:
```bash
$ docker-compose run web django-admin startproject <project_name> .
```
* Se estiver no Linux, mudar permissões com o comando:
```bash
sudo chown -R $USER:$USER .
```
* Vamos realizar as migrações de banco de dados, execute:
```bash
$ docker-compose run web python manage.py migrate
```
* Finalmente, executar:
```bash
$ docker-compose up
```
* Abrir <http://localhost:8000> e verificar se está rodando.
* Pare o servidor com <kbd>Ctrl</kbd>+<kbd>C</kbd>
* Criar a aplicação `pages` para o nosso projeto Django:
  * Executar
  ```bash
  $ docker-compose run web python manage.py startapp pages
  ```
  * E editar arquivo `<project_name>/settings.py`
  ```python
  # <project_name>/settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'pages', # new
    ]
  ```
* Configurar variáveis de configuração do Redis: inserir no final do arquivo `<project_name>/settings.py`
```python
# <project_name>/settings.py
REDIS_HOST = 'redis'
REDIS_PORT = 6379
```
* Lembrando que o fluxo do Django segue a lógica 
```
URL -> View -> Model (typically) -> Template
```
* Primeiramente, vamos criar a view (poderia ser em qualquer ordem). Edite o arquivo `pages/views.py`
```python
# pages/views.py
from django.shortcuts import HttpResponse
from django.conf import settings
import time
import redis

# connect to our Redis instance
cache = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def homePageView(request):
    count = get_hit_count()
    return HttpResponse('Hello World! I have been seen {} times.\n'.format(count))
```
* Agora, vamos editar a URL
  * Crie o arquivo `pages/urls.py` com o conteúdo
  ```python
  # pages/urls.py
  from django.urls import path
  from .views import homePageView

  urlpatterns = [
    path('', homePageView, name='home')
  ]
  ```
  * E edite o arquivo `<project_name>/urls.py`
  ```python
  # <project_name>/urls.py
  from django.contrib import admin
  from django.urls import path, include # new
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('pages.urls')), # new
  ]
  ```
  * Finalmente, executar:
```bash
$ docker-compose up
```
* Abrir <http://localhost:8000> e verificar se está rodando. A cada vez que recarregar a página, o contador deve aumentar.