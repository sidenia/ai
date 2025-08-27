import requests
from openai import OpenAI

OPENAI_API_KEY = open("../auth/openai_key.txt").read()
WEATHER_API_KEY = open("../auth/weatherapi_key.txt").read()

client = OpenAI(api_key=OPENAI_API_KEY)

def get_weather(city: str) -> dict:
    """Consulta o clima na OpenWeather API"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
    response = requests.get(url)
    return response.json()

def identify_city(user_input: str) -> str | None:
    prompt = f"Extraia o nome da cidade da frase: '{user_input}'. Responda apenas com o nome da cidade, sem explicações."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    city = completion.choices[0].message.content.strip()
    return city if city else None

def agent_response(user_input: str) -> str:
    """Agente que usa IA para responder"""
    # Descobre se o usuário perguntou sobre clima
    if "clima" in user_input.lower() or "tempo" in user_input.lower():
        city = identify_city(user_input)
        weather = get_weather(city)
        
        if weather.get("cod") != 200:
            return "Não consegui encontrar o clima dessa cidade. Tente novamente."
        
        temp = weather["main"]["temp"]
        desc = weather["weather"][0]["description"]

        # IA formata a resposta
        prompt = f"O clima em {city} agora está {desc} com temperatura de {temp}°C. Responda de forma simpática e curta, inclua na resposta o clima em graus Celsius."
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()

    else:
        # Resposta genérica via IA
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}]
        )
        return completion.choices[0].message.content.strip()


# 🚀 Teste do agente
if __name__ == "__main__":
    while True:
        print("Agente: Olá! Pergunte-me sobre o clima em qualquer cidade ou diga 'sair' para encerrar.")
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Agente: Até mais! 👋")
            break
        resposta = agent_response(user_input)
        print("Agente:", resposta)
