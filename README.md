# 📄 Implementação do Trabalho Final da disciplina de Programação Orientada á Objetos 2.

## 🔗 **Objetivo**
O objetivo deste projeto é implementar as operações de um sistema de aeroporto, onde gerenciamos as interações envolvendo gerentes e atendentes. O sistema oferece funcionalidades para o manuseio eficiente e seguro das tarefas relacionadas ao aeroporto.

## 🔗 **Funcionalidades**

1. Cadastro
Ao acessar a tela de Cadastro, o usuário deverá preencher os campos com seu usuário, senha e função (gerente ou atendente). Após inserir um usuário, senha válidos e uma função válida, e clicar em Efetuar Cadastro, o sistema criará o cadastro do usuário, permitindo que ele realize o login posteriormente.

2. Login
Na tela de Login, o usuário preencherá os campos de usuário e senha. Após clicar em Entrar, o sistema verificará as credenciais fornecidas. Com base no número de cadastro realizado, o usuário será direcionado para as funcionalidades específicas de gerente ou atendente, conforme sua função.

3. Tela de Gerente
Se, após o login, o usuário for identificado como gerente, ele terá acesso às seguintes funcionalidades através dos botões na tela principal de gerente:

- Voo
- Aviões
- Chat
- Sair (para retornar ao menu principal)

3.1 Tela de Voo

Na tela de Voos, o gerente poderá cadastrar novos voos, alterar voos, remover voos, listar voos e marcar voos.

3.2 Tela de Aviões

Na tela de Aviões, o gerente poderá cadastrar aviões, alterar aviões, remover aviões e listar os aviões.


3.3 Tela de Chat

Na tela de Chat, o gerente poderá se comunicar diretamente com os atendentes em tempo real.

4. Tela de Atendente

Se, após o login, o usuário for identificado como atendente, ele terá acesso às seguintes funcionalidades através dos botões na tela principal de atendente:

- Passageiros
- Reservas
- Chat
- Sair (para retornar ao menu principal)
  
4.1 Tela de Passageiros

Na tela de passageiros, o atendente poderá cadastrar passageiros, alterar passageiros, remover passageiros e listar passageiros.

4.2 Tela de Reservas

Na tela de reserva, o atendente poderá reservar um voo ou remover a reserva de um voo.

4.3 Tela de Chat

Na tela de Chat, o atendente poderá se comunicar diretamente com os gerentes em tempo real.
  
## 🔗 Requisitos da Aplicação
Para que a aplicação funcione corretamente é necessário o Docker Desktop instalado, além da criação do conteiner Postgress(banco de dados utilizado). 

1. Criação do Conteiner.

Para criar o conteiner utilize o código abaixo no terminal do seu compilador com o Docker Desktop em execução.
``` 
docker run --name postgres -e POSTGRES_USER=poodois -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=credenciais -p 5432:5432 -d postgres
``` 

2. Iniciar o conteiner do Docker Desktop

Com o Docker Desktop em execução e após o contêiner ter sido criado, utilize o comando abaixo para iniciar o contêiner pelo terminal ou, se preferir, inicie-o manualmente pelo Docker Desktop.


``` 
docker start postgres
```

3. Inicializar os Pré-Requisitos.
   
Uma vez que o contêiner esteja em execução, você pode prosseguir para usar o aplicativo conectando-se ao banco de dados PostgreSQL através das credenciais e da porta especificadas acima. Certifique-se de que todas as dependências ou configurações necessárias para o sistema de gerenciamento do aeroporto estejam devidamente configuradas.

Notas
Certifique-se de que você criou o contêiner.
Certifique-se de que o Docker e o contêiner Docker estão em execução.
Certifique-se de que seu sistema tenha recursos suficientes alocados para o Docker Desktop a fim de evitar problemas de desempenho.
