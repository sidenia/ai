import os
import smtplib
from email.utils import formatdate
from email.header import Header
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httpx
import feedparser
from openai import OpenAI



# --- CONFIGS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # news/app
AUTH_DIR = os.path.join(BASE_DIR, "..", "..", "auth")

OPENAI_API_KEY = open(os.path.join(AUTH_DIR, "openai_key.txt")).read().strip()

with open(os.path.join(AUTH_DIR, "email_rem.txt")) as f:
    linhas = f.readlines()
    EMAIL_REM = linhas[0].strip()
    EMAIL_REM_PASS = linhas[1].strip()

with open(os.path.join(AUTH_DIR, "email_des.txt")) as f:
    EMAIL_DES = [linha.strip() for linha in f if linha.strip()]

# --- Fontes seguras de notícias (RSS) ---
FONTES_BRASIL = {
    "G1": "https://g1.globo.com/dynamo/rss2.xml",
    "Folha": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",
    "Estadão": "https://feeds.folha.uol.com.br/poder/rss091.xml",
    "O Globo": "https://oglobo.globo.com/rss.xml"
}

FONTES_MUNDO = {
    "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "Le Monde (França)": "https://www.lemonde.fr/rss/une.xml",
    "El País (Espanha)": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "The Guardian (UK)": "https://www.theguardian.com/world/rss",
    "Japan Times": "https://www.japantimes.co.jp/feed/",
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "Associated Press (AP News)": "https://apnews.com/apf-topnews?format=rss"
}

client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client(timeout=30))

def coletar_noticias(fontes, limite=3):
    noticias = []
    links_processados = set()

    for nome, url in fontes.items():
        feed = feedparser.parse(url)
        for entrada in feed.entries[:limite]:
            if entrada.link not in links_processados:  # Evita duplicatas
                noticias.append({
                    "fonte": nome,
                    "titulo": entrada.title,
                    "link": entrada.link,
                    "resumo": entrada.get("summary", "")
                })
                links_processados.add(entrada.link)  # Marca o link como processado

    return noticias

def resumir_noticias(noticias):
    resumos = []
    for n in noticias:
        prompt = f"""
        Resuma a seguinte notícia em no máximo 280 caracteres, em português, 
        de forma clara e objetiva (estilo tweet). Inclua contexto se for importante:

        Título: {n['titulo']}
        Resumo: {n['resumo']}
        Fonte: {n['fonte']}
        """
        print(f"🔎 Pedindo resumo de: {n['titulo'][:50]}...")
        response = client.chat.completions.create(
            model="gpt-4.1-mini", # "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "o4-mini", "gpt-4o-mini"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        print("✅ Resposta recebida")

        resumo = response.choices[0].message.content.strip()
        # resumo = response.choices[0].message["content"].strip()
        resumos.append(f"📰 {resumo}\n🔗 {n['link']}\n")
    return resumos

def enviar_email(assunto, corpo):
    data_str = datetime.now().strftime("%d/%m/%Y")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_REM
    msg["To"] = ", ".join(EMAIL_DES)
    msg["Date"] = formatdate(localtime=True)

    # ✅ força UTF-8 no Subject
    msg["Subject"] = str(Header(f"{assunto} - {data_str}", "utf-8"))

    corpo_formatado = f"🌎 Principais Notícias do Dia — {data_str}\n\n{corpo}"
    msg.attach(MIMEText(corpo_formatado, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_REM, EMAIL_REM_PASS)
        print("======= EMAIL RAW =======")
        print(msg.as_string())
        print("=========================")
        server.sendmail(EMAIL_REM, EMAIL_DES, msg.as_string())

def main():
    ini = datetime.now()
    print(f"🚀 Iniciando coleta de notícias às {ini.strftime('%H:%M:%S')}...")
    noticias_brasil = coletar_noticias(FONTES_BRASIL)
    noticias_mundo = coletar_noticias(FONTES_MUNDO)

    print("✅ Notícias coletadas com sucesso!")
    print(f'Número de notícias do Brasil: {len(noticias_brasil)}')
    print(f'Número de notícias do Mundo: {len(noticias_mundo)}')

    resumos_brasil = resumir_noticias(noticias_brasil)
    resumos_mundo = resumir_noticias(noticias_mundo)

    corpo_email = "🇧🇷 Brasil:\n\n" + "\n".join(resumos_brasil) + "\n\n"
    corpo_email += "🌍 Mundo:\n\n" + "\n".join(resumos_mundo)

    enviar_email("AI Agent: Resumo diário de notícias", corpo_email)
    # enviar_email("AI Agent: Resumo diário de notícias", "Teste de envio de email - corpo simples.")
    print("✅ Email enviado com sucesso!")
    fim = datetime.now() 
    print(f"⏱️ Processo finalizado em {(fim - ini).seconds} segundos.")
    tempo_processamento = (fim - ini).seconds
    print(f"⏱️ Tempo de processamento: {tempo_processamento} segundos.")

if __name__ == "__main__":
    main()