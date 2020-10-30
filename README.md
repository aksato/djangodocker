# Comandos para execução
* Instruções retiradas de <https://docs.docker.com/compose/django/>
* Para criar um novo projeto Django:
```bash
$ docker-compose run web django-admin startproject <project_name> .
```
* Se estiver no Linux, mudar permissões com o comando:
```bash
sudo chown -R $USER:$USER .
```
* Abrir `<project_name>/settings.py` e substituir:
```python
# settings.py
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
* Finalmente, executar:
```bash
$ docker-compose up
```
* Abrir <http://localhost:8000>