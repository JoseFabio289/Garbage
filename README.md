# Robô de Exclusão de Cards no Botnext CRM (Playwright + Pandas)

Automação em Python desenvolvida para ler códigos **CF** de uma planilha Excel e excluir os registros correspondentes no CRM Botnext (`https://botnext.wts.chat/chat2/sessions`).

## Requisitos e Instalação

1. **Instalar as dependências do projeto:**

   ```powershell
   pip install -r requirements.txt
   ```
2. **Garantir a instalação dos navegadores do Playwright:**

   ```powershell
   playwright install chromium
   ```



## Configurações no `main.py`

No topo do arquivo [main.py](file:///c:/Users/joao.oliveira/Documents/AutomaçãoCNPJ/Garbage/main.py), você pode ajustar as variáveis:

```python
CAMINHO_EXCEL = "Dados/Excluir BOT.xlsx"
NOME_ABA = "Planilha1"
COLUNA_CF = "Código"              # Coluna que contém os identificadores (ex: CF-8009)

MODO_SIMULACAO = True             # True: simula e não exclui nada | False: exclusão real
LIMITE_REGISTROS = None           # Ex: 1 para testar um único registro, ou None para todos
INTERVALO_ENTRE_REGISTROS = 1.5   # Pausa em segundos entre cada registro
HEADLESS = False                  # False permite ver a tela e fazer login manual
```



## Como Executar

### 1. Teste em Modo Simulação (Padrão e Recomendado Inicialmente)

Mantenha `MODO_SIMULACAO = True`.

```powershell
python main.py
```

- O robô abrirá o navegador.
- Caso não esteja autenticado, você pode fazer login manualmente e teclar `ENTER` no terminal.
- O robô navegará para CRM > Painéis > Lista, fará a busca de cada CF, abrirá o card, conferirá o código e fechará o card **sem excluir nada**.
- Ao final, exibirá o resumo com a lista exata dos itens que seriam excluídos e salvará um arquivo `relatorio_execucao_YYYYMMDD_HHMMSS.csv`.

### 2. Teste com 1 Registro Autorizado

Para validar a exclusão de verdade em apenas 1 registro antes de rodar os 242 da base:

1. Em `main.py`, defina:
   ```python
   MODO_SIMULACAO = False
   LIMITE_REGISTROS = 1
   ```
2. Execute:
   ```powershell
   python main.py
   ```
3. Acompanhe a exclusão do primeiro card e a confirmação no modal.

### 3. Execução Completa

Quando tiver validado com sucesso:

1. Ajuste `LIMITE_REGISTROS = None` e `MODO_SIMULACAO = False`.
2. Execute `python main.py`.
