# 🏫 API de Gestão Escolar

Uma **API RESTful** desenvolvida em **Python (Flask)** para gerenciar informações de **alunos, professores e turmas** de uma instituição de ensino.  
A API possui **documentação interativa via Swagger**, e está totalmente **containerizada com Docker e Docker Compose**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **Flask**
- **Flasgger** (Swagger UI para documentação)
- **Docker / Docker Compose**

---

## 📁 Estrutura do Projeto

meu-projeto/
├── app.py # Arquivo principal da API Flask
├── requirements.txt # Dependências do projeto
├── Dockerfile # Configuração do container Docker
├── docker-compose.yml # Orquestração com Docker Compose
└── README.md # Este arquivo


🐍 Rodar localmente (sem Docker)

Se quiser executar diretamente na sua máquina:

pip install -r requirements.txt
python app.py


Acesse:
👉 http://localhost:3000


-------------------------------------------------------------------------------------------------


🐳 Executar com Docker
🔧 Construir a imagem
docker build -t api-gestao-escolar .

▶️ Rodar o container
docker run -d -p 3000:3000 api-gestao-escolar


Acesse a API em:
👉 http://localhost:3000


-------------------------------------------------------------------------------------------------


🧱 Executar com Docker Compose

Se preferir usar o Compose, rode:

docker compose up --build


A API ficará disponível em:
👉 http://localhost:3000



🔒 Boas Práticas Implementadas

Estrutura REST organizada

Configuração completa via Docker e Docker Compose

Código simples e modular, pronto para integração com banco de dados