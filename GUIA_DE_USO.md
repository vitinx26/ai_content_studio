# Guia de Instalação e Uso - AI Content Studio

## Visão Geral

O **AI Content Studio** é uma aplicação web completa e gratuita que oferece funcionalidades similares a assistentes de IA premium, incluindo pesquisa inteligente, geração de imagens, criação de apresentações PowerPoint e produção de vídeos slideshow. Toda a aplicação utiliza apenas tecnologias open source e APIs gratuitas.

## Funcionalidades Principais

### 1. Pesquisa Inteligente
- Pesquisa por texto ou voz (usando reconhecimento de fala do navegador)
- Busca integrada no DuckDuckGo e Wikipedia
- Resultados organizados e formatados
- Suporte para português e outros idiomas

### 2. Gerador de Imagens
- Cria imagens a partir de descrições de texto
- Suporte para prompts negativos (o que evitar na imagem)
- Usa o modelo Stable Diffusion 2.1 via Hugging Face
- Sistema de fallback com imagens placeholder quando a API está sobrecarregada

### 3. Criador de Apresentações PowerPoint
- Gera apresentações .pptx automaticamente
- Dois modos de criação:
  - **A partir de Tópico**: Pesquisa conteúdo na Wikipedia e cria slides
  - **A partir de Texto**: Transforma seu texto em apresentação
- Controle do número de slides (3 a 10)
- Design profissional com cores e formatação

### 4. Criador de Vídeos Slideshow
- Cria vídeos a partir de imagens
- Adicione legendas personalizadas para cada imagem
- Controle da duração de cada frame (1 a 10 segundos)
- Exporta frames individuais para preview

## Instalação

### Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.9 ou superior**
- **Node.js 16 ou superior**
- **pnpm** (gerenciador de pacotes)
- **FFmpeg** (para processamento de vídeo)

### Instalação no Linux/Ubuntu

```bash
# Instalar Python e pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Instalar Node.js e pnpm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g pnpm

# Instalar FFmpeg
sudo apt install ffmpeg
```

### Instalação no Windows

1. Baixe e instale Python 3.9+ de [python.org](https://www.python.org/downloads/)
2. Baixe e instale Node.js de [nodejs.org](https://nodejs.org/)
3. Instale pnpm: `npm install -g pnpm`
4. Baixe FFmpeg de [ffmpeg.org](https://ffmpeg.org/download.html) e adicione ao PATH

### Instalação no macOS

```bash
# Usando Homebrew
brew install python3 node pnpm ffmpeg
```

## Configuração do Projeto

### 1. Extrair os arquivos

Extraia o arquivo `ai_content_studio.zip` para um diretório de sua escolha.

### 2. Configurar o Backend

```bash
cd ai_content_studio
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar o Frontend

```bash
cd ai-content-studio-frontend
pnpm install
```

### 4. Construir o Frontend

```bash
cd ai-content-studio-frontend
pnpm run build
```

### 5. Copiar o Build para o Backend

```bash
# No Linux/macOS
cp -r dist/* ../ai_content_studio/src/static/

# No Windows
xcopy /E /I dist ..\ai_content_studio\src\static
```

## Executando a Aplicação

### Modo de Desenvolvimento

```bash
cd ai_content_studio
source venv/bin/activate  # No Windows: venv\Scripts\activate
python src/main.py
```

A aplicação estará disponível em `http://localhost:5000`

### Modo de Produção

```bash
cd ai_content_studio
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

## Configuração Opcional: Token do Hugging Face

Para melhor desempenho na geração de imagens, você pode criar uma conta gratuita no Hugging Face e obter um token de acesso:

1. Acesse [huggingface.co](https://huggingface.co/) e crie uma conta
2. Vá em Settings → Access Tokens
3. Crie um novo token com permissão de leitura
4. Configure a variável de ambiente:

```bash
# Linux/macOS
export HF_API_TOKEN="seu_token_aqui"

# Windows
set HF_API_TOKEN=seu_token_aqui
```

**Nota**: A aplicação funciona sem o token, mas pode ter limitações de taxa. O sistema automaticamente usa imagens placeholder quando necessário.

## Como Usar

### Pesquisa Inteligente

1. Clique na aba **Pesquisa**
2. Digite sua pergunta no campo de texto ou clique no ícone do microfone para usar voz
3. Clique no botão de pesquisa ou pressione Enter
4. Veja os resultados da Wikipedia e da web

### Geração de Imagens

1. Clique na aba **Imagem**
2. Descreva a imagem que deseja criar (ex: "Um gato laranja usando óculos de sol, estilo cartoon")
3. Opcionalmente, adicione o que evitar (ex: "baixa qualidade, desfocado")
4. Clique em **Gerar Imagem**
5. Aguarde alguns segundos e baixe a imagem gerada

### Criação de Apresentações

**A partir de Tópico:**
1. Clique na aba **Apresentação**
2. Selecione **A partir de Tópico**
3. Digite o título e o tópico principal
4. Ajuste o número de slides (3-10)
5. Clique em **Gerar Apresentação**
6. Baixe o arquivo .pptx gerado

**A partir de Texto:**
1. Selecione **A partir de Texto**
2. Digite o título
3. Cole ou digite o conteúdo da apresentação
4. Clique em **Gerar Apresentação**
5. Baixe o arquivo .pptx

### Criação de Vídeos

1. Clique na aba **Vídeo**
2. Digite o título do vídeo
3. Ajuste a duração por imagem (1-10 segundos)
4. Clique na área de upload para adicionar imagens
5. Adicione legendas opcionais para cada imagem
6. Clique em **Gerar Vídeo**
7. Veja o preview dos frames gerados

## Solução de Problemas

### Erro ao gerar imagens

**Problema**: "Rate limit exceeded" ou "Model is loading"

**Solução**: A API gratuita do Hugging Face tem limites de taxa. A aplicação automaticamente oferece gerar uma imagem placeholder. Aguarde alguns minutos e tente novamente, ou configure um token de acesso.

### Erro ao criar vídeo

**Problema**: "FFmpeg not found"

**Solução**: Certifique-se de que o FFmpeg está instalado e no PATH do sistema.

```bash
# Verificar instalação
ffmpeg -version
```

### Erro ao instalar dependências

**Problema**: Erro ao instalar pacotes Python

**Solução**: Certifique-se de estar usando Python 3.9+ e que o ambiente virtual está ativado.

```bash
python --version
which python  # Deve mostrar o caminho do venv
```

### Porta 5000 já em uso

**Problema**: "Address already in use"

**Solução**: Mude a porta ou encerre o processo que está usando a porta 5000.

```bash
# Usar outra porta
gunicorn --bind 0.0.0.0:8080 src.main:app

# Ou encontrar e encerrar o processo
lsof -ti:5000 | xargs kill -9  # Linux/macOS
```

## Compatibilidade

### Navegadores Suportados

- Google Chrome 90+
- Mozilla Firefox 88+
- Microsoft Edge 90+
- Safari 14+

**Nota**: O reconhecimento de voz funciona melhor no Chrome e Edge.

### Dispositivos

- **Desktop**: Totalmente suportado
- **Tablet**: Totalmente suportado
- **Mobile**: Interface responsiva, mas algumas funcionalidades podem ter desempenho reduzido

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **DuckDuckGo Search**: API de pesquisa
- **Wikipedia**: API de conteúdo enciclopédico
- **Hugging Face**: API de geração de imagens
- **python-pptx**: Criação de apresentações
- **MoviePy**: Processamento de vídeo

### Frontend
- **React**: Biblioteca JavaScript
- **Vite**: Build tool
- **Tailwind CSS**: Framework CSS
- **shadcn/ui**: Componentes UI
- **Lucide React**: Ícones

## Limitações

- **Geração de Imagens**: Limitada pela API gratuita do Hugging Face (pode haver delays ou limites de taxa)
- **Vídeos**: Apenas formato slideshow (não gera vídeos com animações complexas)
- **Apresentações**: Design básico (pode ser personalizado editando o código)
- **Pesquisa**: Resultados limitados aos disponíveis no DuckDuckGo e Wikipedia

## Próximos Passos e Melhorias Possíveis

- Adicionar mais modelos de geração de imagem
- Implementar edição de imagens
- Adicionar templates de apresentação personalizáveis
- Suporte para transições de vídeo mais avançadas
- Sistema de usuários e histórico
- Deploy em nuvem (Heroku, Vercel, etc.)

## Suporte

Para problemas, sugestões ou dúvidas, você pode:
- Consultar a documentação no arquivo `README.md`
- Verificar os logs do servidor para erros específicos
- Revisar o código-fonte nos diretórios `src/`

## Licença

Este projeto utiliza tecnologias open source e APIs gratuitas. Consulte as licenças individuais de cada dependência para mais informações.

---

**Desenvolvido com tecnologias open source e APIs gratuitas**

