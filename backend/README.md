<h1 align="center">Bem-vindo ao backend do Coffee Shop 👋</h1>
<p>
  <a href="../LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg" />
  </a>
</p>

> Esse diretório possui um backend REST API para servir o frontend da aplicação

## Principais Dependências

- [x] [Flask](http://flask.pocoo.org/) - Um framework de micro serviços leve que será responsável por lidar com os requests e responses da aplicação
- [x] [SQLAlchemy](https://www.sqlalchemy.org/) e [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Bibliotecas para lidar de forma fácil com banco de dados
- [x] [jose](https://python-jose.readthedocs.io/en/latest/) - Biblioteca de assinatura e criptografia de objeto JavaScript para JWTs

## Instruções de instalação e configuração

Baixe o repositório e navegue para a pasta `backend`

```bash
git clone https://github.com/zerocoolbr/Coffee-Shop.git
cd Coffee-Shop
cd backend
```

Instale as dependências

```bash
pip install -r requirements.txt
```

É necessário editar o arquivo `src/auth/auth.py` para incluir as informações do Auth0

### Auth0

O [Auth0](https://auth0.com/) é uma é um serviço de autenticação de usuários de aplicações (Third-Party Authentication). Usaremos ele para a autenticação e gerenciamento de permissões e roles dos usuários. Siga o seguinte **passo a passo** para configurar o Auth0.

1. Crie uma nova conta no [Auth0](https://auth0.com/)
2. Selecione um único domínio
3. Crie um novo Single Page Web Application
4. Crie uma nova API
   - nas configurações da API
     - Ative o RBAC (Role Based Access Control)
     - Habilite Adicionar Permissões nos tokens de acesso
5. Crie as seguintes permissões na API:
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Crie as roles para:
   - Barista
     - pode `get:drinks-detail`
   - Manager
     - pode realizar todas as ações
7. Teste as permissões com o [Postman](https://getpostman.com).
   - Registre 2 usuários - atribua um a role de Barista e o outro de Manager.
   - Logue em cada um dos usuários para gerar um JWT e o anote.
   - Importe o postman collection `coffee-shop.postman_collection.json`
   - Clique com o botão direito no diretório da collection de barista e manager, navegue até a tab de autorização e inclua o JWT que você anotou para cada um.
   - Rode todas as collections e verifique se tudo funcionou corretamente

## Instruções para uso

Primeiro é necessário setar a variável ambiente `FLASK_APP` para o arquivo `src/api.py`. No linux isso pode ser feito da seguinte maneira:

```bash
export FLASK_APP=api.py;
```

Para setar a variável ambiente no Windows via CMD:

```cmd
set FLASK_APP="api.py"
```

Para setar a variável ambiente no Windows via Powershell:

```powershell
$env:FLASK_APP="api.py"
```

Após setar a variável ambiente basta iniciar a aplicação Flask

```bash
flask run --reload
```

A flag `reload` faz com que a aplicação reinicie automáticamente caso houver alguma mudança no código (hot-reload).

## Autor

👤 **Marcos Santana**

- LinkedIn: [@marcosbrs](https://linkedin.com/in/marcosbrs)
- Medium: [@marcos.brs](https://medium.com/@marcos.brs)
- Twitter: [@mbrsantana](https://twitter.com/mbrsantana)

## 📝 License

Copyright © 2020 [Marcos Santana](https://github.com/zerocoolbr).<br />
This project is [MIT](../LICENSE) licensed.
