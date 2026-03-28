"""
Thermal Daily Checklist Printer
--------------------------------
Imprime checklist diário com:
- Rotina JSON
- Google Calendar (.ics)
- Clima (OpenWeather)
- Integração com Obsidian

CONFIGURE A SEÇÃO "USER CONFIG" ANTES DE USAR
"""

from escpos.printer import Win32Raw
from datetime import datetime
import requests
import json
import os

# =============================
# USER CONFIG  (EDITAR AQUI)
# =============================

# Nome da impressora térmica (Windows)
# Exemplo: "POS-58", "XP-80", "Thermal Printer"
PRINTER_NAME = "YOUR_PRINTER_NAME"

# Arquivo JSON com rotinas
JSON_FILE = "rotina.json"

# OpenWeather API Key
# https://openweathermap.org/api
CLIMA_API_KEY = "YOUR_OPENWEATHER_API_KEY"

# Latitude e Longitude da sua cidade
# https://www.latlong.net/
LAT = 0.0
LON = 0.0

# Caminho do Vault do Obsidian
# Exemplo Windows:
# r"C:\Users\SeuUsuario\Documents\ObsidianVault"
OBSIDIAN_VAULT = r"PATH_TO_YOUR_OBSIDIAN_VAULT"

# Links iCal públicos (Google Calendar)
# Exportar em:
# Google Calendar → Settings → Integrate Calendar → Public ICS
GOOGLE_ICS_URLS = [
    # "https://calendar.google.com/calendar/ical/xxxxx/basic.ics"
]

# =============================
# CLIMA
# =============================

def obter_clima():
    try:
        url = (
            "https://api.openweathermap.org/data/3.0/onecall"
            f"?lat={LAT}"
            f"&lon={LON}"
            "&units=metric"
            "&lang=pt_br"
            f"&appid={CLIMA_API_KEY}"
        )

        r = requests.get(url, timeout=5)
        data = r.json()

        temp = round(data["current"]["temp"])
        descricao = data["current"]["weather"][0]["description"].capitalize()
        umidade = data["current"]["humidity"]

        return f"{descricao} | {temp}C | {umidade}%"

    except Exception:
        return "Clima indisponível"

# =============================
# OBSIDIAN
# =============================

def exportar_para_obsidian(tarefas, data):

    clima = obter_clima()

    nome_arquivo = data.strftime("%Y-%m-%d") + ".md"
    caminho = os.path.join(OBSIDIAN_VAULT, nome_arquivo)

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    tarefas_md = [f"- [ ] {tarefa}" for tarefa in tarefas]

    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        existentes = set()
        for linha in conteudo.splitlines():
            if linha.strip().startswith("- [ ]"):
                existentes.add(linha.strip())

        novas = [t for t in tarefas_md if t not in existentes]

        if not novas:
            return

        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(novas) + "\n")

        return

    tarefas_str = "\n".join(tarefas_md)

    template = f"""# Notas Diarias

> {clima}

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

            if linha.startswith("DTSTART"):
                data_raw = linha.split(":")[1]
                data = data_raw[:8]

                if "T" in data_raw:
                    hora = data_raw[9:11] + ":" + data_raw[11:13]

            if linha.startswith("SUMMARY"):
                titulo = linha.split(":", 1)[1]

            if linha.startswith("END:VEVENT"):
                if data == hoje and titulo:
                    tarefas.append(f"{hora} - {titulo}")

                titulo = None
                data = None

        return tarefas

    except:
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
        print("rotina.json não encontrado")
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
        print("Erro impressora:", e)
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

    p.text("CHECKLIST DO DIA\n")
    p.text(agora.strftime("%d/%m/%Y") + "\n")
    p.text(clima + "\n")
    p.text("-" * 30 + "\n")

    for ex in hoje["treino"]["exercicios"]:
        p.text("[ ] " + ex + "\n")
        tarefas_obsidian.append("Treino: " + ex)

    for tarefa in hoje["casa"]:
        p.text("[ ] " + tarefa + "\n")
        tarefas_obsidian.append("Casa: " + tarefa)

    for evento in eventos_google:
        p.text("[ ] " + evento + "\n")
        tarefas_obsidian.append("Agenda: " + evento)

    exportar_para_obsidian(tarefas_obsidian, agora)

    p.cut()

# =============================
# START
# =============================

if __name__ == "__main__":
    imprimir_dia()
