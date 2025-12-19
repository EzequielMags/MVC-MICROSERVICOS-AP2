# 🧩 API de Gestão com Arquitetura de Microsserviços

Projeto de criação de uma **API REST desenvolvida em Python**, utilizando **arquitetura de microsserviços**, com o objetivo de separar responsabilidades, facilitar a manutenção do sistema e simular um ambiente próximo ao utilizado no mercado de tecnologia.

A API é composta por múltiplos microsserviços independentes, responsáveis por **Gerenciamento**, **Reservas** e **Atividades/Notas**, que se comunicam por meio de requisições HTTP.

---

## 📚 Contexto Acadêmico

Este projeto foi desenvolvido para fins educacionais como parte das atividades da **Faculdade Impacta de Tecnologia**, com foco no aprendizado prático de:
- Arquitetura de microsserviços
- Desenvolvimento de APIs REST
- Programação em Python
- Separação de responsabilidades
- Comunicação entre serviços

---

## 🐍 Tecnologias Utilizadas

- **Python 3**
- **FastAPI** *(ou Flask, conforme implementação)*
- **Uvicorn**
- **JSON**
- **HTTP/REST**
- **Docker** *(opcional, se utilizado)*

---

## 🧱 Arquitetura de Microsserviços

A aplicação foi dividida em microsserviços independentes, cada um com sua própria responsabilidade:

### 🔧 Microsserviço de Gerenciamento
Responsável pelo gerenciamento de informações gerais do sistema, como:
- Cadastro e consulta de dados
- Atualização e remoção de registros
- Regras básicas de negócio

### 📅 Microsserviço de Reservas
Responsável pelo controle de reservas, incluindo:
- Criação de reservas
- Consulta de reservas existentes
- Cancelamento e atualização de reservas
- Validação de disponibilidade

### 📝 Microsserviço de Atividades e Notas
Responsável pelo controle de atividades e registro de notas, incluindo:
- Cadastro de atividades
- Registro e consulta de notas
- Organização e acompanhamento do desempenho

---

## 🌐 Padrão da API

- Arquitetura **REST**
- Comunicação via **HTTP**
- Dados trafegados em **JSON**
- Endpoints independentes por microsserviço

Exemplo de endpoints:
http
GET    /gerenciamento
POST   /reservas
GET    /atividades-notas


### ▶️ Como Executar o Projeto

Pré-requisitos:

Python 3.10+
Pip


Passos
1. Clone o repositório:
git clone https://github.com/EzequielMags/MVC-MICROSERVICOS-AP2.git

2. Acesse o diretório do projeto: 
cd MVC-MICROSERVICOS-AP2

3. Instale as dependências
pip install -r requirements.txt

4. Execute cada microsserviço em um terminal separado:
docker compose -up



### 🧠 Objetivo do Projeto

O principal objetivo deste projeto é compreender e aplicar o conceito de microsserviços, explorando:

Independência entre serviços

Escalabilidade

Organização de código

Boas práticas no desenvolvimento de APIs em Python



### 🏫 Instituição

Projeto desenvolvido para fins educacionais na
Faculdade Impacta de Tecnologia


### 👨‍💻 Autor

Ezequiel Magoga
Estudante de Tecnologia | Desenvolvimento Full Stack
