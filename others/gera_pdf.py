from fpdf import FPDF

model_data = [
    {
        "Categoria": "GPT-5 (última geração)",
        "Modelos": [
            ("gpt-5", "Tarefas complexas, agentes autônomos, programação", "$1,250/M", "$0,125/M", "$10,000/M"),
            ("gpt-5-mini", "Tarefas bem delimitadas", "$0,250/M", "$0,025/M", "$2,000/M"),
            ("gpt-5-nano", "Resumos, classificação, tarefas leves", "$0,050/M", "$0,005/M", "$0,400/M"),
        ]
    },
    {
        "Categoria": "GPT-4.1 (com ajuste fino)",
        "Modelos": [
            ("gpt-4.1", "Alta performance com ajuste fino", "$3,00/M", "$0,75/M", "$12,00/M", "$25,00/M"),
            ("gpt-4.1-mini", "Compacto, mais barato", "$0,80/M", "$0,20/M", "$3,20/M", "$5,00/M"),
            ("gpt-4.1-nano", "Resumos e classificação leves", "$0,20/M", "$0,05/M", "$0,80/M", "$1,50/M"),
        ]
    },
    {
        "Categoria": "o4-mini (ajuste fino de reforço)",
        "Modelos": [
            ("o4-mini", "Ajuste fino por reforço", "$4,00/M", "$1,00/M", "$16,00/M", "$100,00/hora"),
        ]
    }
]

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "Modelos OpenAI - GPT-5, GPT-4.1 e o4-mini (2025)", ln=True, align='C')

pdf.set_font("Arial", "", 12)

for section in model_data:
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, section["Categoria"], ln=True)
    pdf.set_font("Arial", "B", 12)

    headers = ["Modelo", "Indicação", "Entrada", "Cache Entrada", "Saída"]
    if len(section["Modelos"][0]) == 6:
        headers.append("Treinamento")
    col_widths = [30, 70, 25, 30, 25, 30]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1)
    pdf.ln()

    pdf.set_font("Arial", "", 12)
    for model in section["Modelos"]:
        for i, item in enumerate(model):
            pdf.cell(col_widths[i], 8, item, border=1)
        pdf.ln()

pdf.output("modelos_openai_2025.pdf")
