import time
import pandas as pd
from playwright.sync_api import sync_playwright

# ==========================================
# CONFIGURAÇÕES
# ==========================================
EXCEL_PATH = "Dados/Excluir BOT.xlsx"
SIMULACAO = True           # True = apenas simula | False = exclui de verdade
INTERVALO_ACAO = 1.0       # Intervalo de 1 segundo entre ações
INTERVALO_REGISTRO = 3.0   # Intervalo de 3 segundos entre mudança de registro

<<<<<<< HEAD
#for dado in df:
df.loc["Código"]
=======
# ==========================================
# 1. LEITURA DA PLANILHA
# ==========================================
df = pd.read_excel(EXCEL_PATH, dtype=str)
codigos = df["Código"].dropna().str.strip().unique().tolist()
codigos = [c for c in codigos if c]

sucessos = []
nao_encontrados = []
erros = []

# ==========================================
# 2. AUTOMAÇÃO PLAYWRIGHT
# ==========================================
with sync_playwright() as p:
    # Abre o Chrome maximizado e com sessão persistente
    browser = p.chromium.launch_persistent_context(
        "./sessao",
        headless=False,
        args=["--start-maximized"],
        no_viewport=True
    )
    page = browser.pages[0] if browser.pages else browser.new_page()

    page.goto("https://botnext.wts.chat/chat2/sessions")

    # 1. CRM -> Painéis
    crm = page.get_by_text("CRM", exact=True)
    crm.hover()
    time.sleep(INTERVALO_ACAO)
    crm.click()
    time.sleep(INTERVALO_ACAO)

    page.get_by_text("Painéis", exact=True).click()
    time.sleep(INTERVALO_ACAO)
    
    # Se estiver na tela de seleção de painéis, pesquisa e abre o painel
    try:
        campo_painel = page.get_by_placeholder("Pesquisar por painel")
        if campo_painel.is_visible(timeout=3000):
            campo_painel.fill("CRM Falavinha")
            time.sleep(INTERVALO_ACAO)
            page.locator("button:has-text('Abrir'), a:has-text('Abrir')").first.click()
            time.sleep(INTERVALO_ACAO)
    except Exception:
        pass

    # 3. Alterna para visualização em Lista (clique no switch da lista)
    switch_lista = page.locator('[data-cy="button-panel-view-list"]')
    switch_lista.wait_for(state="visible", timeout=20000)
    switch_lista.click()
    time.sleep(INTERVALO_ACAO)

    # Aguarda o campo de busca da lista estar visível
    campo_busca = page.locator('[data-cy="dashboard-filter-text"]').or_(page.get_by_placeholder("Pesquisar"))
    campo_busca.wait_for(state="visible", timeout=20000)

    # ==========================================
    # 4. PROCESSAMENTO DOS CÓDIGOS CF
    # ==========================================
    for cf in codigos:
        try:
            # Busca o código na lista
            busca = page.locator('[data-cy="dashboard-filter-text"]').or_(page.get_by_placeholder("Pesquisar"))
            busca.fill("")
            time.sleep(INTERVALO_ACAO)
            busca.fill(cf)
            busca.press("Enter")
            time.sleep(INTERVALO_ACAO)

            # Localiza correspondência exata do código
            celulas = page.get_by_text(cf, exact=True)
            if celulas.count() != 1:
                nao_encontrados.append(cf)
                time.sleep(INTERVALO_REGISTRO)
                continue

            # Abre o card
            celulas.first.click()
            page.wait_for_url("**/card/**")
            time.sleep(INTERVALO_ACAO)

            if SIMULACAO:
                # Fecha o card sem excluir
                page.keyboard.press("Escape")
                time.sleep(INTERVALO_ACAO)
                if "/card/" in page.url:
                    page.locator("button:has(svg)").first.click()
                    time.sleep(INTERVALO_ACAO)
                sucessos.append(cf)
            else:
                # Localiza a lixeira no rodapé do card
                lixeira = page.locator("button[title*='Excluir'], button[aria-label*='Excluir']").first
                if not lixeira.is_visible():
                    lixeira = page.locator("div:has-text('Configurar campos') button").nth(2)
                if not lixeira.is_visible():
                    lixeira = page.locator("button:has(svg)").filter(has=page.locator("path[d*='19'], path[d*='trash']")).first

                lixeira.click()
                time.sleep(INTERVALO_ACAO)

                # Confirma no modal "Excluir Card"
                btn_confirmar = page.locator("div:has-text('Excluir Card') button:has-text('Excluir')").first
                btn_confirmar.wait_for(state="visible", timeout=5000)
                btn_confirmar.click()
                btn_confirmar.wait_for(state="hidden", timeout=10000)
                time.sleep(INTERVALO_ACAO)

                sucessos.append(cf)

            time.sleep(INTERVALO_REGISTRO)

        except Exception as e:
            erros.append((cf, str(e)))
            page.keyboard.press("Escape")
            time.sleep(INTERVALO_REGISTRO)

    browser.close()

# ==========================================
# 5. RESUMO FINAL
# ==========================================
rotulo = "SIMULADAS" if SIMULACAO else "EXCLUÍDAS"
print("\n" + "=" * 55)
print("              RESUMO DA EXECUÇÃO")
print("=" * 55)
print(f"Modo:               {'SIMULAÇÃO' if SIMULACAO else 'EXCLUSÃO REAL'}")
print(f"Total na planilha:  {len(codigos)}")
print(f"{rotulo.capitalize()} com sucesso: {len(sucessos)}")
print(f"Não encontrados:    {len(nao_encontrados)}")
print(f"Erros:              {len(erros)}")
print("-" * 55)
print(f"LINHAS {rotulo} COM SUCESSO ({len(sucessos)}):")
for item in sucessos:
    print(f"- {item}")
print("=" * 55 + "\n")
>>>>>>> 710e31223ff3d7496ff04183ca710b49829ba480
