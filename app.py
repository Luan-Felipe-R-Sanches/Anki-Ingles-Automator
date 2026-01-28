import os
import json
import fitz
import genanki
from openai import OpenAI

# ================= CONFIGURAÇÕES =================
API_KEY = "SUA_CHAVE_AQUI" 
PDF_PATH = "NOME_DO_SEU_ARQUIVO.pdf"
NOME_DECK = "Inglês com OpenAI"
ARQUIVO_SAIDA = "ingles_openai.apkg"
# =================================================

client = OpenAI(api_key=API_KEY)

def extrair_texto_pdf(caminho):
    """Lê o PDF e retorna o texto bruto."""
    try:
        doc = fitz.open(caminho)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto
    except Exception as e:
        print(f"❌ Erro ao ler o PDF: {e}")
        return None

def processar_com_gpt(texto_bruto):
    """Usa o GPT para limpar o texto e criar pares Inglês-Português."""
    if not texto_bruto:
        return []

    print("🤖 Enviando texto para o GPT estruturar e traduzir...")
    
    prompt = f"""
    Analise o texto abaixo extraído de um PDF.
    1. Identifique frases úteis para aprender inglês.
    2. Ignore cabeçalhos, números de página ou lixo de formatação.
    3. Retorne APENAS um objeto JSON com uma lista chamada 'cards'.
    4. Cada item da lista deve ter: 'ingles' e 'portugues' (traduza se necessário).
    
    Texto:
    {texto_bruto[:4000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts language learning cards from text."},
                {"role": "user", "content": prompt}
            ]
        )
        
        dados = json.loads(response.choices[0].message.content)
        return dados.get('cards', [])
    except Exception as e:
        print(f"❌ Erro na API da OpenAI: {e}")
        return []

def gerar_audio_openai(texto, id_unico):
    """Gera áudio usando a API TTS da OpenAI."""
    nome_arquivo = f"audio_{id_unico}.mp3"
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=texto
    )
    
    # Grava o arquivo de áudio temporariamente
    response.stream_to_file(nome_arquivo)
    return nome_arquivo

def criar_anki_package(lista_cards):
    if not lista_cards:
        print("⚠️ Nenhuma carta para gerar.")
        return

    print(f"📦 Criando baralho Anki com {len(lista_cards)} cartas...")
    
    # ID fixo para o modelo e para o deck (podem ser números aleatórios)
    modelo_id = 1091735104
    deck_id = 2059400110

    # Definição do Modelo do Card (HTML/CSS)
    modelo = genanki.Model(
        modelo_id,
        'Modelo OpenAI Audio',
        fields=[
            {'name': 'Ingles'},
            {'name': 'Portugues'},
            {'name': 'Audio'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<div style="font-family: Arial; font-size: 24px; text-align: center;">{{Ingles}}</div><br><div style="text-align: center;">{{Audio}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div style="font-family: Arial; color: #666; text-align: center;">{{Portugues}}</div>',
            },
        ])
    
    meu_deck = genanki.Deck(deck_id, NOME_DECK)
    arquivos_de_midia = []

    for i, item in enumerate(lista_cards):
        ing = item['ingles']
        pt = item['portugues']
        
        print(f"   🎙️ [{i+1}/{len(lista_cards)}] Gerando áudio: {ing}")
        
        try:
            arquivo_audio = gerar_audio_openai(ing, i)
            arquivos_de_midia.append(arquivo_audio)
            
            # Adiciona a nota ao deck
            nota = genanki.Note(
                model=modelo,
                fields=[ing, pt, f'[sound:{arquivo_audio}]']
            )
            meu_deck.add_note(nota)
        except Exception as e:
            print(f"   ⚠️ Falha ao processar frase '{ing}': {e}")

    # Cria o pacote final
    pacote = genanki.Package(meu_deck)
    pacote.media_files = arquivos_de_midia
    pacote.write_to_file(ARQUIVO_SAIDA)
    
    # Limpeza dos arquivos mp3 locais
    for f in arquivos_de_midia:
        if os.path.exists(f):
            os.remove(f)

    print(f"\n✅ Sucesso! O arquivo '{ARQUIVO_SAIDA}' foi criado.")

# --- Execução Principal ---
if __name__ == "__main__":
    if os.path.exists(PDF_PATH):
        texto_pdf = extrair_texto_pdf(PDF_PATH)
        cartoes = processar_com_gpt(texto_pdf)
        criar_anki_package(cartoes)
    else:
        print(f"❌ Erro: O arquivo '{PDF_PATH}' não foi encontrado na pasta.")
