import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ==========================================
# CONFIGURAÇÕES
# ==========================================
EXCEL_PATH = "Dados/Excluir BOT_teste.xlsx"
URL = "https://botnext.wts.chat/chat2/sessions"

SIMULACAO = True
TIMEOUT = 15000

# ==========================================
# LEITURA DOS DADOS
# ==========================================
df = pd.read_excel(EXCEL_PATH, dtype=str)

codigos = (
    df["Código"]
    .dropna()
    .str.strip()
    .loc[lambda x: x.ne("")]
    .drop_duplicates()
    .tolist()
)

sucessos = []
nao_encontrados = []
erros = []

# ==========================================
# AUTOMAÇÃO
# ==========================================
with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        "./sessao",
        headless=False,
        args=["--start-maximized"],
        no_viewport=True
    )

    page = browser.pages[0] if browser.pages else browser.new_page()
    page.set_default_timeout(TIMEOUT)

    try:
        page.goto(URL, wait_until="domcontentloaded")

        # CRM -> Painéis
        crm = page.get_by_text("CRM", exact=True)
        crm.hover()
        crm.click()

        page.get_by_text("Painéis", exact=True).click()

        # Seleção do painel
        campo_painel = page.get_by_placeholder(
            "Pesquisar por painel"
        )

        if campo_painel.count() > 0:
            campo_painel.fill("CRM Falavinha")

            page.locator(
                "button:has-text('Abrir'), a:has-text('Abrir')"
            ).first.click()

        # Alternar para lista
        switch_lista = page.locator(
            '[data-cy="button-panel-view-list"]'
        )

        switch_lista.click()

        # Campo de pesquisa
        busca = page.locator(
            '[data-cy="dashboard-filter-text"]'
        )

        busca.wait_for(state="visible")

        # ==========================================
        # PROCESSAMENTO
        # ==========================================
        for cf in codigos:

            try:
                busca.fill(cf)
                busca.press("Enter")

                # Aguarda o resultado específico aparecer
                celula = page.get_by_text(cf, exact=True)

                try:
                    celula.first.wait_for(
                        state="visible",
                        timeout=5000
                    )

                except PlaywrightTimeoutError:
                    nao_encontrados.append(cf)
                    print(f"[NÃO ENCONTRADO] {cf}")
                    continue

                # Segurança: não processar resultados ambíguos
                if celula.count() != 1:
                    erros.append((cf, "Múltiplas correspondências"))
                    continue

                celula.click()

                page.wait_for_url("**/card/**")

                if SIMULACAO:
                    print(f"[SIMULAÇÃO] {cf}")

                    page.keyboard.press("Escape")

                    page.wait_for_url(
                        lambda url: "/card/" not in url,
                        timeout=5000
                    )

                else:
                    # Localizador da lixeira
                    lixeira = page.locator(
                        'button:has(mat-icon[data-mat-icon-name="delete"])'
                    )

                    lixeira.click()

                    # Confirmação
                    confirmar = page.get_by_role(
                        "button",
                        name="Excluir",
                        exact=True
                    )

                    confirmar.click()

                    confirmar.wait_for(state="hidden")

                    print(f"[EXCLUÍDO] {cf}")

                sucessos.append(cf)

            except Exception as e:
                erros.append((cf, str(e)))
                print(f"[ERRO] {cf}: {e}")

                page.keyboard.press("Escape")

                # Recupera a navegação, se necessário
                if "/card/" in page.url:
                    page.goto(
                        URL,
                        wait_until="domcontentloaded"
                    )
                    # A navegação de recuperação precisa
                    # retornar ao painel/lista antes de continuar.
                    raise RuntimeError(
                        "Navegação perdida. "
                        "Reabra o painel antes de continuar."
                    )

    finally:
        browser.close()

# ==========================================
# RELATÓRIO
# ==========================================
print("\n" + "=" * 50)
print("RESUMO DA EXECUÇÃO")
print("=" * 50)

print(f"Total: {len(codigos)}")
print(f"Sucessos: {len(sucessos)}")
print(f"Não encontrados: {len(nao_encontrados)}")
print(f"Erros: {len(erros)}")

print("\nSTATUS POR CF:")

for cf in codigos:
    if cf in sucessos:
        status = "SIMULADO" if SIMULACAO else "EXCLUSÃO EXECUTADA"
    elif cf in nao_encontrados:
        status = "NÃO ENCONTRADO"
    elif any(codigo == cf for codigo, _ in erros):
        status = "ERRO"
    else:
        status = "NÃO PROCESSADO"