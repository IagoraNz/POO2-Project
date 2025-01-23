# 📄 Implementação do trabalho final da disciplina de Programação Orientada a Objetos II.

## 🔗 Objetivo
O objetivo deste projeto é implementar as operações de um sistema de aeroporto, onde gerenciamos as interações envolvendo gerentes e atendentes. O sistema oferece funcionalidades para o manuseio eficiente e seguro das tarefas relacionadas ao aeroporto.

<div align="center">
  <img src="https://github.com/user-attachments/assets/994d3b10-2937-4942-ba8e-3b1a428ecd71" alt="Descrição da imagem" width="500px">
</div>

## 🔗 Funcionalidades

### ⚙️ Cadastro
Ao acessar a tela de Cadastro, o usuário deverá preencher os campos com seu usuário, senha e função (gerente ou atendente). Após inserir um usuário, senha válidos e uma função válida, e clicar em Efetuar Cadastro, o sistema criará o cadastro do usuário, permitindo que ele realize o login posteriormente.

### ⚙️ Login
Na tela de Login, o usuário preencherá os campos de usuário e senha. Após clicar em Entrar, o sistema verificará as credenciais fornecidas. Com base no número de cadastro realizado, o usuário será direcionado para as funcionalidades específicas de gerente ou atendente, conforme sua função.

### ⚙️ Tela de Gerente
Se, após o login, o usuário for identificado como gerente, ele terá acesso às seguintes funcionalidades através dos botões na tela principal de gerente:

- Voo
- Aviões
- Chat
- Sair (para retornar ao menu principal)

#### 🔧 Tela de Voo

Na tela de Voos, o gerente terá diversas funcionalidades disponíveis para gerenciar o fluxo de operações aéreas. Ele poderá cadastrar novos voos, atualizar informações de voos existentes, remover voos quando necessário, listar todos os voos cadastrados para consulta e organização, além de marcar voos. Essas ações permitirão ao gerente manter um controle eficiente e organizado dos voos registrados no sistema.

#### 🔧 Tela de Aviões

Na tela de Aviões, o gerente terá à sua disposição diversas funcionalidades para gerenciar as informações relacionadas à frota de aviões. Ele poderá cadastrar novos aviões, atualizar dados de aviões já existentes, remover registros de aviões que não são mais necessários e listar todos os aviões cadastrados para facilitar a consulta e a organização. Essas funcionalidades garantirão um controle eficaz e atualizado da frota no sistema.

#### 🔧 Tela de Chat

Na tela de Chat, o gerente terá a possibilidade de se comunicar diretamente com os atendentes de maneira prática e em tempo real. Essa funcionalidade permitirá trocar informações, fornecer orientações, esclarecer dúvidas e acompanhar a execução das atividades, promovendo uma comunicação eficiente e colaborativa entre o gerente e a equipe de atendimento.

### ⚙️ Tela de Atendente

Se, após o login, o usuário for identificado como atendente, ele terá acesso às seguintes funcionalidades através dos botões na tela principal de atendente:

- Passageiros
- Reservas
- Chat
- Sair (para retornar ao menu principal)
  
#### 🔧 Tela de Passageiros

Na tela de Passageiros, o atendente terá acesso a funcionalidades essenciais para o gerenciamento de informações dos clientes. Ele poderá cadastrar novos passageiros no sistema, atualizar os dados de passageiros já existentes, remover registros de passageiros quando necessário e listar todos os passageiros cadastrados para facilitar a consulta e a organização. Essas ferramentas asseguram uma gestão eficiente e precisa das informações dos passageiros.

#### 🔧 Tela de Reservas

Na tela de Reservas, o atendente terá à disposição funcionalidades para gerenciar as reservas de voos de forma prática e eficiente. Ele poderá realizar a reserva de um voo para um cliente, garantindo o registro da viagem no sistema, ou remover reservas já existentes, caso haja cancelamentos ou alterações. Essas opções permitem um gerenciamento organizado e atualizado das reservas, atendendo às necessidades dos clientes de maneira ágil.

#### 🔧 Tela de Chat

Na tela de Chat, o atendente terá a possibilidade de se comunicar diretamente com os gerentes de maneira prática e em tempo real. Essa funcionalidade permitirá trocar informações, fornecer orientações, esclarecer dúvidas e acompanhar a execução das atividades, promovendo uma comunicação eficiente e colaborativa entre o gerente e a equipe de atendimento.
  
## 🔗 Aproveite a aplicação
Para que a aplicação funcione corretamente é necessário o Docker Desktop instalado, além da criação do conteiner Postgress(banco de dados utilizado). 

1. Clone o repositório
```
git clone https://github.com/IagoraNz/POO2-Project
```

2. Criação do container

Para criar o conteiner utilize o código abaixo no terminal do seu compilador com o Docker Desktop em execução.
``` 
docker run --name postgres -e POSTGRES_USER=poodois -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=credenciais -p 5432:5432 -d postgres
``` 

3. Iniciar o conteiner do Docker

Com o Docker Desktop em execução e após o contêiner ter sido criado, utilize o comando abaixo para iniciar o contêiner pelo terminal ou, se preferir, inicie-o manualmente pelo Docker Desktop.
``` 
docker start postgres
```

4. Rode o arquivo principal da aplicação
```
./main.py
``` 

## ⚠️ Notas
- Certifique-se de que você criou o contêiner.
- Certifique-se de que o Docker e o contêiner Docker estão em execução.
- Certifique-se de que seu sistema tenha recursos suficientes alocados para o Docker Desktop a fim de evitar problemas de desempenho.
