# 📚 API School Indicator 

Este projeto é uma API desenvolvida em Flask para gerenciar escolas e pais/responsáveis. Ele oferece endpoints para criar, ler, atualizar e deletar informações de escolas e pais/responsáveis. A API também inclui filtros avançados para localizar escolas com base em metodologia de ensino, preço, avaliação e localização.

## 🛠️ Tecnologias Utilizadas

- **Flask**: Framework web para Python
- **SQLAlchemy**: ORM para banco de dados
- **Flasgger**: Para documentação de API com Swagger
- **ViaCEP**: Serviço externo para busca de endereços por CEP

## Diagrama
 
 ![Diagrama do esquema ](https://github.com/isahsantos/school-indicator-interface/blob/main/src/assets/img/diagrama-aplication.png?raw=true)

## 📑 Endpoints da API

### Escolas

#### ➕ Criar Escola
- **POST** `/escolas`
- Cria uma nova escola.
  
#### 📝 Listar Escolas
- **GET** `/escolas`
- Lista todas as escolas cadastradas.
  
#### 🔍 Obter Detalhes de uma Escola
- **GET** `/escolas/{id}`
- Obtém os detalhes de uma escola específica por ID.
  
#### ✏️ Atualizar Escola
- **PUT** `/escolas/{id}`
- Atualiza os dados de uma escola existente.
  
#### ❌ Deletar Escola
- **DELETE** `/escolas/{id}`
- Deleta uma escola específica por ID.

#### 🔍 Filtrar Escolas
- **GET** `/escolas/filtro/metodologia`: Filtra escolas por metodologia de ensino.
- **GET** `/escolas/filtro/preco`: Filtra escolas por faixa de mensalidade.
- **GET** `/escolas/filtro/avaliacao`: Filtra escolas por avaliação mínima.
- **GET** `/escolas/filtro/localizacao`: Filtra escolas por proximidade (não implementado).

### Pais/Responsáveis

#### ➕ Criar Pai/Responsável
- **POST** `/pais`
- Cadastra um novo pai ou responsável.

#### 📝 Listar Pais/Responsáveis
- **GET** `/pais`
- Lista todos os pais ou responsáveis cadastrados.

#### 🔍 Obter Detalhes de um Pai/Responsável
- **GET** `/pais/{id}`
- Obtém os detalhes de um pai ou responsável por ID.

#### ✏️ Atualizar Pai/Responsável
- **PUT** `/pais/{id}`
- Atualiza os dados de um pai ou responsável.

#### ❌ Deletar Pai/Responsável
- **DELETE** `/pais/{id}`
- Deleta um pai ou responsável.

## 🗂️ Instalação

1. Clone o repositório:
   ```bash
   git clone  https://github.com/isahsantos/school-indicator-api
   cd school-indicator-api

2. Crie e ative o ambiente virtual do Python: 
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt


4. Excute a aplicação:
   ```bash
   flask run

## 🚀 Uso
Após a inicialização da API, você pode acessar a documentação dos endpoints via Swagger na seguinte URL:
    ```bash
   http://localhost:5000/apidocs



