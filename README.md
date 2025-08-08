<svg id="d50sy1MOlen" xmlns="http://www.w3.org/2000/svg" width="195.22185516357422" height="35" viewBox="0 0 195.22185516357422 35"><rect width="106.6111068725586" height="35" fill="#4a90e2"/><rect x="106.6111068725586" width="88.61074829101562" height="35" fill="#fce800"/><text x="53.3055534362793" y="17.5" font-size="12" font-family="'Roboto', sans-serif" fill="#FFFFFF" text-anchor="middle" alignment-baseline="middle" letter-spacing="2"></text><text x="150.9164810180664" y="17.5" font-size="12" font-family="'Montserrat', sans-serif" fill="#FFFFFF" text-anchor="middle" font-weight="900" alignment-baseline="middle" letter-spacing="2"></text></svg>
![made-with-python](https://github.com/user-attachments/assets/8cf469f7-b015-45e8-9997-c8de48fa1381)



Yourplaylist é um app desktop open-source para Windows, feito com o objetivo de ajudar os usuários a transferirem, sincronizarem e baixarem suas músicas entre o Spotify e o Youtube Music. 


# Table of contents

- [Requisitos](#Requisitos)
- [Guia](#Guia)
	- [Instalação](#Instalação)
	- [Desinstalar](#Desinstalar)
	- [Autenticação](#Autenticação)
	- [Uso](#Uso)
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


https://github.com/user-attachments/assets/d6e28fe7-5751-4664-b635-7ce6d44201e9





### Uso

Siga os passos do vídeo abaixo.


https://github.com/user-attachments/assets/23599e73-581c-42c1-924d-7667b68f793c






# Projeto
[(Voltar ao topo)](#table-of-contents)

### Sobre

Este projeto utiliza o **Flask** no backend para gerenciar os endpoints e renderizar os templates HTML. No frontend, faz uso do **HTMX** para facilitar a comunicação assíncrona entre cliente e servidor, permitindo atualizações dinâmicas da página sem a necessidade de recarregamento completo. Além disso, utiliza **PyWebView** para integrar a aplicação web em uma interface de desktop.
### Estrutura

```plaintext
YourPlaylist/
├── .gitignore                # Arquivos e pastas ignorados pelo Git
├── Yourplaylist.vbs          # Script para rodar “yourplaylist.bat” sem o terminal
├── init.py                   # Inicialização do pacote principal
├── app/                      # Diretório principal da aplicação
│   ├── __init__.py           # Inicialização do módulo Flask
│   ├── views.py              # Definição das rotas e lógica das views
│   ├── static/               # Arquivos estáticos (imagens, CSS, JS)
│   │   └── images/
│   │       ├── background.png
│   │       └── github-icon.png
│   ├── templates/            # Templates HTML renderizados pelo Flask
│   │   ├── base.html         # Template base para herança
│   │   ├── start.html        # Página inicial
│   │   ├── conexao_spotify.html  # Conexão com Spotify
│   │   ├── conexao_youtube.html  # Conexão com YouTube
│   │   ├── choose_playlists.html # Escolha de playlists para transferência
│   │   ├── sync.html         # Tela de sincronização
│   │   ├── transfer.html     # Tela de transferência de playlists
│   │   ├── erro.html         # Página de erro genérica
│   │   └── ... (outros templates)
│   ├── platforms/            # Módulo para integração com plataformas de streaming
│   │   ├── PlatformInterface.py  # Interface base para serviços de música
│   │   ├── SpotifyPlatform.py    # Implementação para Spotify
│   │   ├── YoutubePlatform.py    # Implementação para YouTube
│   │   ├── cache_script.py   # Script para login no terminal (Spotify)
│   │   ├── oauth_script.py   # Gerenciamento de autenticação OAuth no terminal (YouTube)
│   │   ├── platforms_module.py   # Módulo para manipulação das plataformas
│   │   └── __init__.py       # Inicialização do módulo
├── requirements.txt          # Dependências do projeto
├── run.py                    # Arquivo principal para execução do Flask
├── setup.py                  # Configuração para instalação do projeto
├── tests/                    # Diretório para testes
│   └── yt_test.py            # Testes para integração com YouTube
├── yourplaylist_config.bat   # Script de instalação
└── README.md                 # Documentação do projeto
```


# License
[(Voltar ao topo)](#table-of-contents)

MIT

