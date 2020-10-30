# Comandos para criar uma aplicação utilizando Postgres com Docker
* Para criar um novo projeto Django:
```bash
$ docker-compose run web django-admin startproject <project_name> .
```
* Se estiver no Linux, mudar permissões com o comando:
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
* Para testar o banco de dados, vamos criar usuários. O Django já vem com uma tabela de usuários implementada. Para modificá-la, vamos utilizar o modo *admin*. Para tal, precisamos criar um usuário super com o comando:
```bash
$ docker-compose run web python manage.py createsuperuser
```
* Escolha o nome e senha que desejar.
* Para testar, execute novamente:
```bash
$ docker-compose up
```
* Agora, abra <http://localhost:8000/admin> no browser para acessar o painel de administração.
* Adicione alguns usuários novos.
* Pare o servidor com <kbd>Ctrl</kbd>+<kbd>C</kbd>
* Para e destrua todos os contêineres com
```bash
$ docker-compose down
```
* Reinicie todos os serviços com:
```bash
$ docker-compose up
```
* E confira em <http://localhost:8000/admin> se todos os usuários estão lá.