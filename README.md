# ✈️ POO2-Airport: Sistema de Gerenciamento de Aeroporto

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Required-2496ED)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)

Este repositório contém o trabalho final da disciplina de **Programação Orientada a Objetos II**, focado no desenvolvimento de um sistema completo de gerenciamento de operações aeroportuárias.

## 📄 Sobre o projeto

O objetivo deste projeto é implementar as operações de um sistema de aeroporto, onde gerenciamos as interações envolvendo gerentes e atendentes. O sistema oferece funcionalidades para o manuseio eficiente e seguro das tarefas relacionadas ao aeroporto, incluindo gestão de voos, aviões, passageiros, reservas e comunicação em tempo real.

<div align="center">
  <img src="https://github.com/user-attachments/assets/994d3b10-2937-4942-ba8e-3b1a428ecd71" alt="Sistema de Aeroporto" width="500px">
</div>

### 🎯 Objetivos específicos
- Implementar sistema de autenticação com diferentes níveis de acesso (Gerente e Atendente).
- Gerenciar operações de voos e frota de aviões.
- Controlar cadastro de passageiros e reservas.
- Facilitar comunicação em tempo real entre gerentes e atendentes via chat.
- Aplicar conceitos de Programação Orientada a Objetos (POO).

## 🛠️ Tecnologias utilizadas

O projeto foi desenvolvido em **Python** utilizando as seguintes tecnologias:

- **Python 3.9+**: Linguagem principal do projeto.
- **PostgreSQL**: Banco de dados relacional para armazenamento de dados.
- **Docker**: Containerização do banco de dados.
- **Tkinter/CustomTkinter**: Interface gráfica do usuário.
- **Poetry**: Gerenciamento de dependências.

## ⚙️ Funcionalidades

### 🔐 Sistema de autenticação

#### Cadastro
Ao acessar a tela de Cadastro, o usuário deverá preencher os campos com seu usuário, senha e função (gerente ou atendente). Após inserir credenciais válidas e clicar em Efetuar Cadastro, o sistema criará o cadastro do usuário.

#### Login
Na tela de Login, o usuário preencherá os campos de usuário e senha. O sistema verificará as credenciais e direcionará o usuário para as funcionalidades específicas de sua função.

---

### 👔 Funcionalidades do gerente

#### ✈️ Gestão de voos
- Cadastrar novos voos
- Atualizar informações de voos existentes
- Remover voos
- Listar todos os voos cadastrados
- Marcar status de voos

#### 🛩️ Gestão de aviões
- Cadastrar novos aviões na frota
- Atualizar dados de aviões existentes
- Remover aviões da frota
- Listar todos os aviões cadastrados

#### 💬 Chat com atendentes
Comunicação em tempo real com a equipe de atendimento para coordenação de atividades e esclarecimento de dúvidas.

---

### 👨‍💼 Funcionalidades do atendente

#### 👥 Gestão de passageiros
- Cadastrar novos passageiros
- Atualizar dados de passageiros
- Remover registros de passageiros
- Listar todos os passageiros cadastrados

#### 🎫 Gestão de reservas
- Realizar reservas de voos para clientes
- Remover reservas existentes
- Consultar reservas ativas

#### 💬 Chat com gerentes
Comunicação direta com gerentes para suporte e orientações.

## 🚀 Como executar

### Pré-requisitos
- Python 3.9 ou superior
- Docker Desktop instalado e em execução
- Git

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/IagoraNz/POO2-Project
   cd POO2-Project
   ```

2. Crie o container do PostgreSQL:
   ```bash
   docker run --name postgres -e POSTGRES_USER=poodois -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=credenciais -p 5432:5432 -d postgres
   ```

3. Inicie o container do Docker:
   ```bash
   docker start postgres
   ```

4. Execute o arquivo principal da aplicação:
   ```bash
   python src/main.py
   ```

## 📂 Estrutura do repositório

```
📂 POO2-Project/
├── 📂 src/
│   ├── 🐍 main.py              # Arquivo principal da aplicação
│   ├── 📂 POO2PROJECT/         # Módulos principais do sistema
│   ├── 📂 backend/             # Lógica de backend e banco de dados
│   ├── 📂 chat/                # Funcionalidade de chat
│   ├── 📂 fonts/               # Fontes customizadas
│   ├── 📂 images/              # Recursos visuais
│   ├── 📂 others/              # Utilitários diversos
│   └── 📂 test/                # Testes automatizados
├── 📄 pyproject.toml           # Configuração do Poetry
├── 📄 setup.py                 # Configuração de instalação
├── 📄 test_autenticar.py       # Testes de autenticação
└── 📄 README.md                # Documentação do projeto
```

## ⚠️ Notas importantes

> [!IMPORTANT]
> Certifique-se de que o Docker Desktop está instalado e em execução antes de iniciar a aplicação.

> [!WARNING]
> O container PostgreSQL deve estar ativo para que o sistema funcione corretamente. Verifique o status com `docker ps`.

> [!NOTE]
> Certifique-se de que seu sistema tenha recursos suficientes alocados para o Docker Desktop a fim de evitar problemas de desempenho.

## 📝 Licença

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de Programação Orientada a Objetos II.
