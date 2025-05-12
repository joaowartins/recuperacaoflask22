# DOCUMENTAÇÃO **Web App de Gerenciamento de Projetos**

# Objetivo do projeto

Desenvolver um Web App de gerenciamento de projetos utilizando Flask, permitindo a criação e gerenciamento de projetos e suas tarefas. O sistema deve armazenar dados em arquivos, oferecendo funcionalidades para cadastrar, listar, editar e remover projetos e tarefas, além de permitir o upload de imagens, filtro de tarefas por status, e exibição de uma barra de progresso do projeto. No projeto eu utilizei o Flask, CSS (Tailwind) e HTML

# SEPARAÇÃO DO PROJETO

Na parte do Front-End, eu utilizei o Tailwind e Html, pois nos requisitos do projeto era necessário.

foi organizado como:

## FRONT-END

**criar_projeto.html -** onde o usuário poderia criar seus projetos, podendo adicionar descrição, titulo e até imagem

**editar_projeto.html -** lugar onde o usuário poderá editar o titulo e a descrição do projeto

**index.html -**  é a página inicial do meu sistema, onde são exibidos todos os projetos cadastrados. Ele mostra nome, descrição, imagem (se houver) e botões para ver tarefas, editar ou excluir cada projeto. Também tem um botão para criar um novo projeto. O visual é feito com Tailwind CSS.

**editar_tarefa.html -** Essa página permite editar uma tarefa com título, descrição e status, enviando as mudanças via POST. Usa Tailwind CSS para o estilo.

## BACK-END

O backend do projeto utiliza o framework Flask e gerencia projetos e tarefas usando arquivos CSV para armazenamento. Ele inclui funcionalidades CRUD para criar, editar, excluir e listar projetos, além de permitir o upload de imagens.

O código foi construído no app.py e cada linha do código foi comentada.

# COMO EXECUTAR

primeiro passo - clone meu repositorio git: 
git clone https://github.com/joaowartins/recuperacaoflask22.git

segundo passo - ativar o ambiente virtual

```powershell
venv/Scripts/Activate.ps1
```

terceiro passo - executar arquivo app.py

```powershell
python app.py
```

![image.png](https://github.com/joaowartins/recuperacaoflask22/blob/main/static/ex/image.png)

# IMAGENS DO PROJETO

pagina inicial - 

![image.png](https://github.com/joaowartins/recuperacaoflask22/blob/main/static/ex/image%20(1).png)

criar novo projeto - 

![image.png](https://github.com/joaowartins/recuperacaoflask22/blob/main/static/ex/image%20(2).png)

edição do projeto - 

![image.png](https://github.com/joaowartins/recuperacaoflask22/blob/main/static/ex/image%20(3).png)

ver tarefas - 

![image.png](https://github.com/joaowartins/recuperacaoflask22/blob/main/static/ex/image%20(4).png)

![image.png](https://github.com/joaowartins/recuperacaoflask22/blob/main/static/ex/image%20(5).png)
