# 🧾 Thermal Daily Checklist

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Printer](https://img.shields.io/badge/ESC%2FPOS-Compatible-success)
![Obsidian](https://img.shields.io/badge/Obsidian-Integration-purple)
![Weather](https://img.shields.io/badge/OpenWeatherMap-API-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Personal Project](https://img.shields.io/badge/Project-Personal-blueviolet)

Automatiza a geração de um **checklist diário impresso** com:

* 🏋️ Treino do dia
* 🧹 Tarefas da casa
* 📅 Agenda do Google Calendar
* 🌤️ Clima atual
* 🧠 Exportação para Obsidian
* 🖨️ Impressão em impressora térmica ESC/POS
* ✅ Evita duplicação de tarefas
* 📦 Baseado em JSON configurável

---

# ✨ Sobre o Projeto

Este é um **projeto pessoal** que desenvolvi para organizar minha rotina diária com mais foco e disciplina.
Decidi compartilhar porque acredito que pode **inspirar outras pessoas** a criarem seus próprios sistemas de produtividade e automação pessoal.

Ele integra múltiplas fontes de informação e gera automaticamente:

* Um checklist físico
* Uma nota diária no Obsidian
* Uma visão clara do dia

Tudo com **um único comando**.

---

# 🖨️ Exemplo do que é impresso

```
CHECKLIST DO DIA
26/03/2026
QUARTA-FEIRA
Céu limpo | 23°C | 65%

TREINO: COSTAS/BÍCEPS
[ ] Dead hang
[ ] Scap pull-ups
...

LIMPEZA E ORGANIZAÇÃO
[ ] Limpeza do dormitório
...

AGENDA DO DIA
[ ] 13:00 - Estudar Python
```

---

## ✨ Inspiração

Este projeto nasceu como uma adaptação pessoal após assistir ao vídeo que mostra como uma simples impressora térmica pode ajudar a combater a procrastinação e trazer mais clareza ao dia a dia:

🎥 https://www.youtube.com/watch?v=xg45b8UXoZI

A ideia original foi desenvolvida por CodingWithLewis, cujo repositório serviu como base conceitual para esta implementação:
🔗 https://github.com/CodingWithLewis/ReceiptPrinterAgent

Por sua vez, o conceito foi inspirado no artigo da Laurie Hérault, que relata como uma impressora térmica ajudou a transformar sua produtividade e organização pessoal:
📝 https://www.laurieherault.com/articles/a-thermal-receipt-printer-cured-my-procrastination

Este projeto é minha interpretação dessa ideia — expandindo o conceito com integrações e ajustes voltados à minha rotina. Compartilho aqui na esperança de que também inspire outras pessoas a criarem seus próprios sistemas de organização e produtividade.

---

# ⚙️ Funcionalidades

* Impressão automática em impressora térmica
* Integração com Google Calendar (via ICS)
* Integração com Obsidian (nota diária)
* Clima do dia via OpenWeatherMap
* Rotinas configuráveis via JSON
* Evita duplicação no Obsidian
* QR Code no final do checklist
* Suporte a múltiplos calendários
* Formatação para papel térmico 58mm

---

# 🧰 Tecnologias Utilizadas

* Python 3
* ESC/POS
* OpenWeatherMap API
* Google Calendar ICS
* Obsidian Markdown
* JSON
* Requests

---

# 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/thermal-daily-checklist.git
cd thermal-daily-checklist
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install python-escpos requests
```

---

# 🖨️ Configuração da Impressora

⚠️ É possível que você precise instalar o **driver da impressora térmica**.

Passos:

1. Conecte sua impressora térmica USB
2. Instale o driver do fabricante
3. Verifique o nome da impressora no Windows
4. Atualize no código:

```python
PRINTER_NAME = "NOME_DA_SUA_IMPRESSORA"
```

Exemplo:

```python
PRINTER_NAME = "POS-58"
```

---

# 🌤️ Configuração do Clima

Crie uma conta gratuita:

https://openweathermap.org/

Obtenha sua API Key e configure:

```python
CLIMA_API_KEY = "SUA_API_KEY"
LAT = -23.55052
LON = -46.63331
```

Para descobrir sua latitude e longitude:

https://www.latlong.net/

---

# 📅 Configuração do Google Calendar

Você precisa do link ICS do seu calendário.

Passos:

1. Abra Google Calendar
2. Configurações do calendário
3. "Integrar calendário"
4. Copie o link privado ICS
5. Adicione no código:

```python
GOOGLE_ICS_URLS = [
    "SEU_LINK_ICS_AQUI"
]
```

Você pode adicionar múltiplos calendários.

---

# 🧠 Configuração do Obsidian

Defina o caminho do seu Vault:

```python
OBSIDIAN_VAULT = r"D:\SeuVault\Daily"
```

O script criará automaticamente:

```
2026-03-27.md
```

Com template diário.

---

# 📄 Estrutura do JSON

Arquivo: `rotina.json`

Estrutura obrigatória:

```json
{
  "plano_mestre_casa_e_treino": {
    "rotina_diaria": {
      "segunda_feira": {
        "treino": {
          "tipo": "TREINO A",
          "exercicios": [
            "Flexão",
            "Agachamento"
          ]
        },
        "casa": [
          "Limpar quarto",
          "Organizar mesa"
        ]
      }
    }
  }
}
```

---

# 📌 Regras importantes do JSON

* Use exatamente:

  * `segunda_feira`
  * `terca_feira`
  * `quarta_feira`
  * `quinta_feira`
  * `sexta_feira`
  * `sabado`
  * `domingo`

* `treino.tipo` → título do treino

* `treino.exercicios` → lista de exercícios

* `casa` → tarefas domésticas

---

# ▶️ Executando

```bash
python main.py
```

O script irá:

1. Ler JSON
2. Ler Google Calendar
3. Buscar clima
4. Imprimir checklist
5. Criar nota no Obsidian

---

# 📂 Estrutura do Projeto

```
thermal-daily-checklist
│
├── main.py
├── rotina.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🔐 Privacidade

Este projeto não armazena:

* Senhas
* Tokens privados
* Dados pessoais

Todas as configurações são locais.

---

# 💡 Ideias futuras

* Integração com Notion
* Estatísticas semanais
* Suporte Linux
* Interface gráfica
* Impressão automática via agendador

---

# 🤝 Contribuições

Contribuições são bem-vindas!

Se você criou algo legal com este projeto, compartilhe 🚀

---

# ⭐ Motivação

Este projeto nasceu de uma necessidade pessoal de:

* Ter foco
* Criar disciplina
* Organizar rotina
* Reduzir decisões diárias

Se isso inspirar alguém a construir algo parecido, já valeu a pena.
