# Test Sensedata

This repo provide the management for property on a Flask API

There's some rules to follow when developing the API. These rules are:
- Qual critério de escolha do banco de dados? (a resposta não deve ultrapassar 255 caracteres);
  - The answer for this questions is simple: there's such no problem using Relational SGBD for such small application, and the comparision with
  NoSQL it's very far. The perfomance of both are good, but not crucial in this project.
- Script de criação do banco de dados ou template dos arquivos;
- As APIs devem estar funcionando e documentadas;
- Um arquivo Markdown com observações pertinentes sobre a estrutura do projeto, como executar o projeto e exemplos de chamadas das APIs.
- O projeto deve possuir um DockerFile/Compose expondo a sua aplicação na porta 8080;
- O analista do projeto deve conseguir clonar seu repositório, buildar a imagem e rodar a sua aplicação executando as chamadas das APIs com os exemplos apontados no arquivo MD;


And in the techinal side, these are the requisites:

- Repositório de dados, pode ser csv, xml, txt, banco de dados SQL, noSQL etc;
- O desenvolvimento deve ser realizado utilizando Flask/SqlAlchemy;
- As APIs devem ser padrão restFull e documentadas com Swagger;
- O código fonte deve ser armazenado em um repositório privado no github (https://github.com) compartilhado com usuário (cenforce).

## Basic Configuration

It's necessary Python 3.6+, and recomended virtualenv, or venv package.

First create a folder, and inside folder clone this repo thus create the virtualenv:

``` bash
# Create the folder
mkdir flask-project
cd flask-project

# Clone the repo
git clone https://github.com/gabrielbalog/test-enforce

# Create the virtualenv
python3 -m venv venv
source venv/bin/activate

# Install the packages
pip install -r requirements.txt
```
Next it's needed to declare some environment variables to run flask properly:

``` bash
export FLASK_APP=properties
export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI="postgresql://flask:flask123@localhost/flask"
export SECRET_KEY="dev"
```

Now it's just call flask with the command run:

``` bash
flask run
```

You should be able to access http://127.0.0.1:8080/properties, and see a dict with an empty array.

## Initializing and Droping the Database

For default the project it's configured to run on a PostgreSQL Database, so before access any page, run:

``` bash
flask init-db
```

It'll automatically create the database and add the tables and data.

If need, it's also possible to delete all the data:

``` bash
flask drop-db
```


## Running with Docker

There is a Dockerfile within the project if there is a need and desire to upload the system through the docker. The database and the Flask APP are already configured,
so just run it with docker-compose:

```bash
docker-compose up
```

If need, it's also possible to remove the Flask APP, just comment the web section on the YAML file.


## Documentation

The documentation can be access in the URL: http://localhost:5000/api/spec.html, there you'll find some example of data and return response.

## Choices made for this project

The first decision I made was taking the database into account. The initial idea was to use Mongo, but due to the project's need to use SQLAlchemy, it was not possible to use the connector available for mongo. In this case I was encountering an error when connecting, and later the module did not have good documentation, so I chose to use PostgreSQL.

Other decisions such as the swagger's quick documentation were due to the short time given for development. 24h seems enough but not so much.

There is no test presence due to the availability of time.