import openai

client = openai.OpenAI(api_key="sua_chave_aqui")

modelos = [
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "o4-mini"
]

prompt = "Explique brevemente a teoria da relatividade."

for modelo in modelos:
    print(f"\n🔷 Modelo: {modelo}")
    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}]
    )
    print(response.choices[0].message.content)
