<!-- 
* Baseado em <https://mattsegal.dev/django-react.html>
* Também baseado em <https://pypi.org/project/django-webpack-loader/>
* Atenção para o erro <https://github.com/jazzband/django-webpack-loader/issues/227>
* README em construção... -->
# Comandos para criar uma aplicação Django utilizando React com Docker
* Para criar um novo projeto Django
```bash
$ docker-compose run web django-admin startproject <project_name> .
```
* Se estiver no Linux, mudar permissões com o comando
```bash
sudo chown -R $USER:$USER .
```
* Primeiro devemos configurar o banco de dados. Para tal, edite o arquivo `<project_name>/settings.py`
```python
# <project_name>/settings.py
import os # new

...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
    }
}
```
* Vamos realizar as migrações de banco de dados. Primeiro, vamos rodar o container do Postgres:
```bash
$ docker-compose up -d database
```
* Depois, execute:
```bash
$ docker-compose run web python manage.py migrate
```
* Finalmente, executar:
```bash
$ docker-compose up
```
* Abrir <http://localhost:8000> e verificar se está rodando.
* Pare o servidor com <kbd>Ctrl</kbd>+<kbd>C</kbd>
* Agora podemos configurar o Webpack. No arquivo `<project_name>/settings.py`, adicione
```python
# <project_name>/settings.py
import os # new
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATICS_DIR = os.path.join(BASE_DIR, os.environ['STATICFILES_DIRNAME']) # new

...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader', # new
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(STATICS_DIR, 'bundles/webpack-stats.json'),
    }
}

...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ( STATICS_DIR,) # new
```
* Para testar, vamos criar a aplicação `pages` para o nosso projeto Django
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
        'webpack_loader',
        'pages', # new
    ]

    ...

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')], # new
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
  ```
* Lembrando que o fluxo do Django segue a lógica 
```
URL -> View -> Model (typically) -> Template
```
* Primeiramente, vamos criar a view (poderia ser em qualquer ordem). Edite o arquivo `pages/views.py`
```python
# pages/views.py
from django.shortcuts import render
from django.conf import settings

def homePageView(request):
    return render(request, "index.html", context={})
```
* Como estamos utilizando o template `index.html`, devemos criar o arquivo `templates/index.html` com o conteúdo
```html
<!-- templates/index.html -->
{% load render_bundle from webpack_loader %}

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Web site created using create-react-app"
    />
    <title>React App</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
  <!--
    This HTML file is a template.
    If you open it directly in the browser, you will see an empty page.

    You can add webfonts, meta tags, or analytics to this file.
    The build step will place the bundled scripts into the <body> tag.

    To begin the development, run `npm start` or `yarn start`.
    To create a production bundle, use `npm run build` or `yarn build`.
  -->
  {% render_bundle 'main' %}
</body>
</html>
```
* O arquivo Javascript com o código React deve ser criado em `assets/js/index.js` com o conteúdo
```js
import React from 'react'
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types'

const Hello = props => (
    <div>Hello {props.name}!</div>
)

Hello.defaultProps = {
    name: 'World'
}

Hello.propTypes = {
    name: PropTypes.string
}

ReactDOM.render(
    <React.StrictMode>
        <Hello name="Seu nome" />
    </React.StrictMode>,
    document.getElementById('root')
);
```
* Agora, vamos editar as URL. Primeiro, crie o arquivo `pages/urls.py` com o conteúdo
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
$ docker-compose up -d
```
* Antes de testar, devemos instalar a biblioteca `prop-types`, que foi utilizada no `assets/js/index.js`. Para tal, execute
```bash
$ docker-compose exec webpack npm install prop-types
```
* Abrir <http://localhost:8000> e verificar se está rodando. Modificar o atributo `name` do compoente React `Hello` em `assets/js/index.js` e recarregue para verificar o que foi mudado.