# 📧 Email Classifier

Um sistema inteligente de classificação de emails com interface web moderna, que utiliza IA e processamento de linguagem natural para categorizar mensagens em **Produtivo** ou **Improdutivo**.

![Status](https://img.shields.io/badge/status-ativo-brightgreen)
![Python](https://img.shields.io/badge/Python-3-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009485)
![HTML](https://img.shields.io/badge/html-orange)
![Tailwind](https://img.shields.io/badge/tailwind-cyan)

## ✨ Características

- 🤖 **Classificação com IA** - Utiliza modelos de linguagem avançados para análise inteligente
- 📄 **Suporte a múltiplos formatos** - Processa emails em PDF e TXT
- 🧠 **NLP em Português** - Processamento de linguagem natural otimizado para português
- 🎨 **Interface moderna** - Dashboard intuitivo com Tailwind CSS
- 📱 **Responsivo** - Funciona perfeitamente em desktop e mobile
- 📝 **Editor rich text** - Quill.js para composição de mensagens
- 💾 **Histórico** - Mantém registro das análises realizadas

## 🚀 Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderna e rápida
- **Pydantic** - Validação de dados com tipos
- **spaCy** - Processamento avançado de linguagem natural
- **HuggingFace** - Modelos de IA para classificação
- **PyPDF** - Extração de texto de PDFs
- **NLTK** - Ferramentas adicionais de NLP

### Frontend
- **HTML5/CSS3** - Markup semântico
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript** - Sem dependências pesadas
- **Quill.js** - Editor de texto rico

### DevOps
- **Docker** - Containerização


## 📋 Pré-requisitos

- Docker instalado
- Ou: Python 3.9+ (para desenvolvimento)
- Token do HuggingFace (para usar modelos IA)

## 🔧 Instalação e Uso

### Opção 1: Com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/Andra-sun/email.git
cd email/backend

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua HUGGINGFACE_TOKEN

# Inicie os serviços
cd ../
docker-compose up -d

# A API estará disponível em http://localhost:8000
# A interface web em http://localhost:3000 (se configurado)
```

Acesse a documentação interativa da API em: **http://localhost:8000/docs**

### Opção 2: Desenvolvimento Local

#### Backend

```bash
# Entre no diretório backend
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente (Windows)
venv\Scripts\activate

# Ative o ambiente (Linux/Mac)
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure .env
cp .env.example .env

# Execute o servidor
python run.py
```

#### Frontend

```bash
# Em outro terminal, entre no diretório frontend
cd frontend

# Abra o index.html em um servidor local
# Opção com Python:
python -m http.server 8001

# Ou use Live Server no VS Code
```

## 🎯 Como Usar

### Via Interface Web

1. **Acesse a aplicação** em `http://localhost:8001` ou pela rota que você ativou o frontend
2. **envie ou digite** o email que deseja classificar
3. **Clique em "Classificar"**
4. **Visualize o resultado** com a categoria (Produtivo/Improdutivo) e confiança
5. **Consulte o histórico** na barra lateral esquerda

### Via API REST
acesse a rota `http://localhost:8000/docs`

```bash
# Exemplo: Classificar um email
curl -X POST "http://localhost:8000/api/v1/email/classify" \
  -H "Content-Type: application/json" \
  -d {
    "sender": "boss@company.com",
    "subject": "Reunião importante",
    "message": "Podemos agendar uma reunião para discutir o projeto?"
  }

# Resposta esperada:
{
  "classification": "Produtivo",
  "confidence": 0.95,
  "processing_time": 0.234
}
```

## 📊 Endpoints da API

### Classificar Email

```
POST /api/v1/email/classify
```

**Request:**
```json
{
  "sender": "string (opcional)",
  "subject": "string (opcional)",
  "message": "string (obrigatório)"
}
```

**Response:**
```json
{
  "classification": "Produtivo | Improdutivo",
  "confidence": 0.95,
  "processing_time": 0.234,
  "explanation": "string (opcional)"
}
```

### Fazer Upload de Arquivo

```
POST /api/v1/email/upload
```

Aceita PDFs e arquivos de texto para análise.

### Health Check

```
GET /
```

Verifica se a API está operacional.



## 🐛 Troubleshooting

### A API não inicia
```bash
# Verifique os logs
docker-compose logs backend

# Verifique se a porta 8000 está disponível
netstat -an | grep 8000
```

### Erro de HuggingFace Token
```bash
# Certifique-se de ter configurado no .env
echo HF_TOKEN=seu_token >> .env

# Gere um token em: https://huggingface.co/settings/tokens
```



## 📈 Roadmap
futuras implementções

- [ ] Autenticação e login
- [ ] Suporte para múltiplos idiomas
- [ ] Integração com Gmail/Outlook
- [ ] Análise de sentimentos
- [ ] Relatórios e estatísticas
- [ ] Export de dados
- [ ] Temas dark/light
- [ ] Mobile app nativa
