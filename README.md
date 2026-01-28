---

# 📚 Anki-Ingles-Automator: PDF to Anki with AI Audio

Este projeto automatiza a criação de flashcards do **Anki** a partir de arquivos **PDF**. Ele utiliza o **GPT-4o-mini** para extrair e traduzir frases, e a API de **Text-to-Speech (TTS)** da OpenAI para gerar áudios naturais em inglês.

---

## 🚀 Funcionalidades

* 📄 **Extração Inteligente**
  Lê PDFs e identifica frases úteis para o aprendizado de idiomas.

* 🤖 **Processamento com IA**
  Traduz e estrutura os dados automaticamente via OpenAI.

* 🎙️ **Áudio Nativo**
  Gera arquivos de áudio para cada card usando modelos de voz avançados.

* 📦 **Pacote Pronto**
  Exporta diretamente um arquivo `.apkg` que pode ser importado em qualquer dispositivo com Anki.

---

## 🛠️ Pré-requisitos

Antes de começar, você precisará de:

* Python **3.8+**
* Uma **chave de API da OpenAI**
* Um arquivo **PDF** que deseja converter

---

## 📥 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Luan-Felipe-R-Sanches/Anki-Ingles-Automator.git
cd Anki-Ingles-Automator
```

2. Instale as dependências:

```bash
pip install pymupdf genanki openai
```

---

## ⚙️ Configuração

No arquivo `app.py`, configure as seguintes variáveis:

* `API_KEY`: Sua chave secreta da OpenAI
* `PDF_PATH`: O nome ou caminho do arquivo PDF de origem

---

## 📖 Como usar

1. Coloque o seu PDF na pasta raiz do projeto.
2. Execute o script:

```bash
python app.py
```

3. Um arquivo chamado `ingles_openai.apkg` será gerado.
4. Abra o **Anki** e vá em:

```
Arquivo > Importar
```

5. Selecione o arquivo `.apkg` gerado.

---

## 🧪 Tecnologias Utilizadas

* **PyMuPDF** – Extração de texto de PDFs
* **OpenAI API** – Inteligência Artificial e Text-to-Speech
* **Genanki** – Criação de decks do Anki

---

