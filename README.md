
[![forthebadge](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOTUuMjUwMDE1MjU4Nzg5MDYiIGhlaWdodD0iMzUiIHZpZXdCb3g9IjAgMCAxOTUuMjUwMDE1MjU4Nzg5MDYgMzUiPjxyZWN0IHdpZHRoPSIxMDYuNjI1MDA3NjI5Mzk0NTMiIGhlaWdodD0iMzUiIGZpbGw9IiM0YTkwZTIiLz48cmVjdCB4PSIxMDYuNjI1MDA3NjI5Mzk0NTMiIHdpZHRoPSI4OC42MjUwMDc2MjkzOTQ1MyIgaGVpZ2h0PSIzNSIgZmlsbD0iI2UxZDAwNyIvPjx0ZXh0IHg9IjUzLjMxMjUwMzgxNDY5NzI2NiIgeT0iMjEuNSIgZm9udC1zaXplPSIxMiIgZm9udC1mYW1pbHk9IidSb2JvdG8nLCBzYW5zLXNlcmlmIiBmaWxsPSIjRkZGRkZGIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBsZXR0ZXItc3BhY2luZz0iMiI+TUFERSBXSVRIPC90ZXh0Pjx0ZXh0IHg9IjE1MC45Mzc1MTE0NDQwOTE4IiB5PSIyMS41IiBmb250LXNpemU9IjEyIiBmb250LWZhbWlseT0iJ01vbnRzZXJyYXQnLCBzYW5zLXNlcmlmIiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iOTAwIiBsZXR0ZXItc3BhY2luZz0iMiI+UFlUSE9OPC90ZXh0Pjwvc3ZnPg==)](https://forthebadge.com)


Yourplaylist é um app desktop open-source para Windows, feito com o objetivo de ajudar os usuários a transferirem, sincronizarem e baixarem suas músicas entre o Spotify e o Youtube Music. 


# Table of contents

- [Requisitos](#Requisitos)
- [Guia](#Guia)
	- [Instalação](#Guia#Instalação)
	- [Desinstalar](#Guia#Desinstalar)
	- [Autenticação](#Guia#Autenticação)
	- [Uso](#Guia#Uso)
- [Projeto](#Projeto)
	- [Estrutura](#Estrutura)
- [License](#license)

# Requisitos
[(Voltar ao topo)](#table-of-contents)

Sistemas operacional Windows 10 ou superior.
Python 3.10 ou superior instalado na máquina.
# Guia
[(Voltar ao topo)](#table-of-contents)


### Instalação 

- Faça o download do arquivo .zip.
- Extraia o arquivo no local desejado.
- Entre na pasta “yourplaylist” e execute o arquivo “yourplaylist.vbs”
- O processo de instalação inicial deve demorar 30s após rodar o arquivo

### Desinstalar
Apenas remova o diretório “yourplaylist” da sua máquina.
### Autenticação

Siga os passos do vídeo abaixo após clicar no botão “Começar”.

[Ver vídeo](https://github.com/seu-repositorio/caminho/video.mp4)

### Uso

Siga os passos do vídeo abaixo.

[Ver vídeo](https://github.com/seu-repositorio/caminho/video.mp4)
# Projeto
[(Voltar ao topo)](#table-of-contents)

### Sobre

Este projeto utiliza o **Flask** no backend para gerenciar os endpoints e renderizar os templates HTML. No frontend, faz uso do **HTMX** para facilitar a comunicação assíncrona entre cliente e servidor, permitindo atualizações dinâmicas da página sem a necessidade de recarregamento completo. Além disso, utiliza **PyWebView** para integrar a aplicação web em uma interface de desktop.
### Estrutura

YourPlaylist/
├── .gitignore                 # Arquivos e pastas ignorados pelo Git  
├── Yourplaylist.vbs           # Script para rodar “yourplaylist.bat” sem o terminal
├── __init__.py                # Inicialização do pacote principal  
│
├── app/                       # Diretório principal da aplicação  
│   ├── __init__.py            # Inicialização do módulo Flask  
│   ├── views.py               # Definição das rotas e lógica das views  
│   ├── static/                # Arquivos estáticos (imagens, CSS, JS)  
│   │   └── images/  
│   │       ├── background.png  
│   │       └── github-icon.png  
│   ├── templates/             # Templates HTML renderizados pelo Flask  
│   │   ├── base.html          # Template base para herança  
│   │   ├── start.html         # Página inicial  
│   │   ├── conexao_spotify.html   # Conexão com Spotify  
│   │   ├── conexao_youtube.html   # Conexão com YouTube  
│   │   ├── choose_playlists.html  # Escolha de playlists para transferência  
│   │   ├── sync.html          # Tela de sincronização  
│   │   ├── transfer.html      # Tela de transferência de playlists  
│   │   ├── erro.html          # Página de erro genérica  
│   │   └── ... (outros templates)  
│
├── platforms/                 # Módulo para integração com plataformas de streaming  
│   ├── PlatformInterface.py   # Interface base para serviços de música  
│   ├── SpotifyPlatform.py     # Implementação para Spotify  
│   ├── YoutubePlatform.py     # Implementação para YouTube  
│   ├── cache_script.py        # Script para login no terminal (spotify)
│   ├── oauth_script.py        # Gerenciamento de autenticação OAuth no terminal (youtube)
│   ├── platforms_module.py    # Módulo para manipulação das plataformas  
│   └── __init__.py            # Inicialização do módulo  
│
├── requirements.txt           # Dependências do projeto  
├── run.py                     # Arquivo principal para execução do Flask  
├── setup.py                   # Configuração para instalação do projeto  
├── tests/                     # Diretório para testes  
│   └── yt_test.py             # Testes para YouTube integration  
│
├── yourplaylist_config.bat     # Script de instalação
└── README.md                   # Documentação do projeto


# License
[(Voltar ao topo)](#table-of-contents)

MIT

