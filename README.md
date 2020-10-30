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
* Finalmente, executar:
```bash
$ docker-compose up
```
* Abrir <http://localhost:8000>