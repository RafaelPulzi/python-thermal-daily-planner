"""
Thermal Daily Checklist Printer
--------------------------------
Features:
- JSON daily routine
- Google Calendar (ICS)
- Weather (OpenWeather)
- Obsidian integration
- QR Code with full payload
- Duplicate-safe daily notes

EDIT USER CONFIG SECTION BEFORE USING
"""

from escpos.printer import Win32Raw
from datetime import datetime
import requests
import json
import os

# =============================
# USER CONFIG
# =============================

# Printer name (Windows)
PRINTER_NAME = "YOUR_PRINTER_NAME"

# Routine JSON file
JSON_FILE = "rotina.json"

# OpenWeather API Key
CLIMA_API_KEY = "YOUR_API_KEY"

# Your city latitude / longitude
LAT = -23.5505
LON = -46.6333

# Obsidian Vault folder
OBSIDIAN_VAULT = r"PATH_TO_YOUR_OBSIDIAN_VAULT"

# Google Calendar public ICS links
GOOGLE_ICS_URLS = [
    # "https://calendar.google.com/calendar/ical/xxxx/basic.ics",
    # "https://calendar.google.com/calendar/ical/yyyy/basic.ics",
]

# =============================
# WEATHER
# =============================

def obter_clima():
    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={LAT}"
            f"&lon={LON}"
            "&units=metric"
            "&lang=pt_br"
            f"&appid={CLIMA_API_KEY}"
        )

        r = requests.get(url, timeout=5)
        data = r.json()

        temp = round(data["main"]["temp"])
        descricao = data["weather"][0]["description"].capitalize()
        umidade = data["main"]["humidity"]
        cidade = data["name"]

        return f"{cidade} | {descricao} | {temp}°C | {umidade}%"

    except Exception:
        return "Clima indisponível"


# =============================
# OBSIDIAN
# =============================

def exportar_para_obsidian(tarefas, data):
    """Create/update daily note without duplicating tasks"""

    clima = obter_clima()

    nome_arquivo = data.strftime("%Y-%m-%d") + ".md"
    caminho = os.path.join(OBSIDIAN_VAULT, nome_arquivo)

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    tarefas_md = [f"- [ ] {t}" for t in tarefas]

    # Avoid duplication
    if os.path.exists(caminho):

        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        existentes = set(
            linha.strip()
            for linha in conteudo.splitlines()
            if linha.strip().startswith("- [ ]")
        )

        novas = [t for t in tarefas_md if t not in existentes]

        if not novas:
            return

        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(novas) + "\n")

        return

    tarefas_str = "\n".join(tarefas_md)

    template = f"""---
date: {data.strftime("%Y-%m-%d")}
tags:
  - diario
---

# Notas Diarias

> {clima}

***

### Jornal
#### Manha

#### Tarde 

#### Noite 

***

### Atividades
{tarefas_str}
"""

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(template)


# =============================
# GOOGLE CALENDAR ICS
# =============================

def ler_ics_simples(url):
    tarefas = []

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        linhas = r.text.splitlines()
        hoje = datetime.now().strftime("%Y%m%d")

        titulo = None
        data = None
        hora = "00:00"

        for linha in linhas:

            linha = linha.strip()

            if linha.startswith("DTSTART"):
                data_raw = linha.split(":")[1]
                data = data_raw[:8]

                if "T" in data_raw:
                    hora = data_raw[9:11] + ":" + data_raw[11:13]
                else:
                    hora = "00:00"

            elif linha.startswith("SUMMARY"):
                titulo = linha.split(":", 1)[1]

            elif linha.startswith("END:VEVENT"):
                if data == hoje and titulo:
                    tarefas.append(f"{hora} - {titulo}")

                titulo = None
                data = None
                hora = "00:00"

        return tarefas

    except Exception:
        return []


def ler_todos_calendarios():
    todas = []

    for url in GOOGLE_ICS_URLS:
        todas.extend(ler_ics_simples(url))

    return sorted(todas)


# =============================
# UTIL
# =============================

def carregar_dados():
    if not os.path.exists(JSON_FILE):
        print("rotina.json not found")
        return None

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def formatar_texto(texto, largura=32):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""

    for p in palavras:
        if len(linha_atual) + len(p) < largura:
            linha_atual += p + " "
        else:
            linhas.append(linha_atual)
            linha_atual = p + " "

    linhas.append(linha_atual)
    return "\n".join(linhas)


# =============================
# MAIN
# =============================

def imprimir_dia():

    dados = carregar_dados()
    eventos_google = ler_todos_calendarios()

    if not dados:
        return

    try:
        p = Win32Raw(PRINTER_NAME)
    except Exception as e:
        print("Printer error:", e)
        return

    agora = datetime.now()
    clima = obter_clima()

    dias = [
        "segunda_feira","terca_feira","quarta_feira",
        "quinta_feira","sexta_feira","sabado","domingo"
    ]

    dia_chave = dias[agora.weekday()]
    hoje = dados["plano_mestre_casa_e_treino"]["rotina_diaria"][dia_chave]

    tarefas_obsidian = []

    CENTRALIZAR = b'\x1b\x61\x01'
    ESQUERDA = b'\x1b\x61\x00'
    NEGRITO_ON = b'\x1b\x45\x01'
    NEGRITO_OFF = b'\x1b\x45\x00'
    DUPLO_ON = b'\x1d\x21\x11'
    DUPLO_OFF = b'\x1d\x21\x00'

    # HEADER
    p._raw(CENTRALIZAR + NEGRITO_ON + DUPLO_ON)
    p.text("CHECKLIST DO DIA\n")
    p._raw(DUPLO_OFF)
    p.text(f"{agora.strftime('%d/%m/%Y')}\n")
    p.text(dia_chave.replace("_", "-").upper() + "\n")
    p.text(clima + "\n")
    p._raw(NEGRITO_OFF)
    p.text("-" * 30 + "\n")

    # TREINO
    p._raw(ESQUERDA + NEGRITO_ON)
    p.text(f"TREINO: {hoje['treino']['tipo']}\n")
    p._raw(NEGRITO_OFF)

    for ex in hoje['treino']['exercicios']:
        p.text(formatar_texto(f"[ ] {ex}") + "\n")
        tarefas_obsidian.append(f"Treino: {ex}")

    p.text("\n")

    # CASA
    p._raw(NEGRITO_ON)
    p.text("LIMPEZA E ORGANIZACAO:\n")
    p._raw(NEGRITO_OFF)

    for tarefa in hoje['casa']:
        p.text(formatar_texto(f"[ ] {tarefa}") + "\n")
        tarefas_obsidian.append(f"Casa: {tarefa}")

    # GOOGLE
    if eventos_google:
        p._raw(NEGRITO_ON)
        p.text("\nAGENDA DO DIA\n")
        p._raw(NEGRITO_OFF)

        for evento in eventos_google:
            p.text(f"[ ] {evento}\n")
            tarefas_obsidian.append(f"Agenda: {evento}")

    # OBSIDIAN
    exportar_para_obsidian(tarefas_obsidian, agora)

    # QR CODE
    qr_payload = {
        "data": agora.strftime('%Y-%m-%d'),
        "dia": dia_chave,
        "clima": clima,
        "treino": hoje['treino']['tipo'],
        "exercicios": hoje['treino']['exercicios'],
        "tarefas_casa": hoje['casa'],
        "agenda": eventos_google
    }

    p.text("\n")
    p._raw(CENTRALIZAR)
    p.text("Scan for full details\n")

    p.qr(
        json.dumps(qr_payload, ensure_ascii=False),
        size=4
    )

    p.text("\n\n")
    p.cut()


# =============================
# START
# =============================

if __name__ == "__main__":
    imprimir_dia()
