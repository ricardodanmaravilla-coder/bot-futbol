import os
from playwright.sync_api import sync_playwright

def bot_analisis():
    # Tus credenciales desde los Secrets de GitHub
    user = os.getenv("FSTATS_USER")
    password = os.getenv("FSTATS_PASS")

    with sync_playwright() as p:
        # Lanzamos el navegador
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Login
        page.goto("https://fstats.mx/login")
        page.fill('input[type="email"]', user)
        page.fill('input[type="password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        # 2. Ir al comparador
        page.goto("https://fstats.mx/comparator")
        
        # 3. Selección de Ligas y Equipos
        # Estos son los selectores más probables. Si fallan, probaremos otros.
        page.select_option('select[name="league"]', label='Premier League')
        page.wait_for_timeout(3000) # Tiempo para que cargue la lista de equipos
        
        page.select_option('select[name="home_team"]', label='Arsenal')
        page.select_option('select[name="away_team"]', label='Liverpool')
        
        # 4. Clic en comparar
        page.click('button:has-text("Comparar")')
        page.wait_for_load_state("networkidle")
        
        # 5. Captura de resultados
        # Buscamos tablas o divs con clase 'stats'
        datos = page.inner_text('table')
        print(datos)
        
        browser.close()

if __name__ == "__main__":
    bot_analisis()

