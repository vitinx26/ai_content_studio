# AI Content Studio

O AI Content Studio é uma aplicação web completa que permite aos usuários realizar pesquisas na web por texto e voz, e gerar conteúdo de IA, incluindo imagens, apresentações e vídeos, utilizando tecnologias de código aberto e APIs gratuitas.

## Funcionalidades

- **Pesquisa Inteligente**: Realiza pesquisas na web utilizando DuckDuckGo e busca artigos na Wikipedia. Suporta entrada de texto e voz (usando a API de Reconhecimento de Fala do navegador).
- **Gerador de Imagens**: Cria imagens a partir de descrições de texto (prompts) usando a API do Hugging Face Inference. Inclui suporte para prompts negativos e um modo de fallback com placeholders.
- **Criador de Apresentações**: Gera apresentações em formato PowerPoint (.pptx) a partir de um tópico (com busca na Wikipedia para o conteúdo) ou de um texto fornecido pelo usuário.
- **Criador de Vídeos**: Cria vídeos no estilo slideshow a partir de uma sequência de imagens e legendas fornecidas pelo usuário.

## Arquitetura

A aplicação é dividida em duas partes principais:

1.  **Backend (Flask)**: Uma API RESTful construída com Flask que serve o frontend, lida com a lógica de negócio e se integra com as APIs externas para geração de conteúdo.
2.  **Frontend (React)**: Uma Single-Page Application (SPA) responsiva construída com React e Vite, utilizando a biblioteca de componentes `shadcn/ui` para uma interface moderna e amigável.

### Estrutura do Backend (`/ai_content_studio`)

```
/ai_content_studio
├── src
│   ├── services
│   │   ├── search_service.py
│   │   ├── image_service.py
│   │   ├── presentation_service.py
│   │   └── video_service.py
│   ├── routes
│   │   └── api.py
│   ├── static/         # Frontend build
│   └── main.py         # Ponto de entrada
├── venv/               # Ambiente virtual
└── requirements.txt    # Dependências
```

### Estrutura do Frontend (`/ai-content-studio-frontend`)

```
/ai-content-studio-frontend
├── src
│   ├── components
│   │   ├── SearchComponent.jsx
│   │   ├── ImageGenerator.jsx
│   │   ├── PresentationCreator.jsx
│   │   └── VideoCreator.jsx
│   ├── App.jsx
│   └── main.jsx
├── public/
└── package.json
```

## Tecnologias Utilizadas

- **Backend**: Python, Flask, Gunicorn
- **Frontend**: React, Vite, Tailwind CSS, shadcn/ui, Lucide React
- **APIs e Bibliotecas**:
    - **Pesquisa**: `duckduckgo-search`, `wikipedia`
    - **Geração de Imagem**: Hugging Face Inference API (modelo `stabilityai/stable-diffusion-2-1`)
    - **Geração de Apresentação**: `python-pptx`, `wikipedia`
    - **Geração de Vídeo**: `moviepy`

## Configuração e Instalação

**Pré-requisitos**:
- Python 3.9+
- Node.js 16+ e pnpm
- FFmpeg (necessário para `moviepy`)

**Instalação do Backend**:

```bash
cd /home/ubuntu/ai_content_studio
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Instalação do Frontend**:

```bash
cd /home/ubuntu/ai-content-studio-frontend
pnpm install
```

## Executando a Aplicação

1.  **Construir o Frontend**:

    ```bash
    cd /home/ubuntu/ai-content-studio-frontend
    pnpm run build
    ```

2.  **Copiar os arquivos do build para o backend**:

    ```bash
    cp -r dist/* ../ai_content_studio/src/static/
    ```

3.  **Iniciar o Servidor Backend**:

    ```bash
    cd /home/ubuntu/ai_content_studio
    source venv/bin/activate
    gunicorn --bind 0.0.0.0:5000 src.main:app
    ```

4.  Acesse a aplicação em `http://localhost:5000` no seu navegador.

## Detalhes das APIs

- **Hugging Face API**: Para a geração de imagens, é necessário um token de acesso do Hugging Face. Este token deve ser configurado como uma variável de ambiente `HF_API_TOKEN`. A aplicação lida de forma inteligente com os limites de taxa da API, oferecendo uma imagem de placeholder se o modelo principal estiver carregando ou indisponível.

