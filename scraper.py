from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configurar navegador Chrome en modo headless (sin interfaz)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
url = "https://www.bolsadecaracas.com/historicos/"

acciones = [
    "BANCO PROVINCIAL, S.A. BCO. UNIVERSAL",  # BPV
    # Agrega más nombres desde el dropdown de la página si lo deseas
]

data_total = []

for accion in acciones:
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    select = Select(wait.until(EC.presence_of_element_located((By.TAG_NAME, "select"))))
    select.select_by_visible_text(accion)

    buscar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Buscar en Histórico')]")))
    buscar_btn.click()

    table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(.,'Últimos Tres Movimientos')]")))
    rows = table.find_elements(By.TAG_NAME, "tr")
    headers = [th.text.strip() for th in rows[0].find_elements(By.TAG_NAME, "th")]

    for row in rows[1:]:
        cols = [td.text.strip().replace('.', '').replace(',', '.') for td in row.find_elements(By.TAG_NAME, "td")]
        if len(cols) == len(headers):
            record = dict(zip(headers, cols))
            record["Accion"] = accion
            data_total.append(record)
    time.sleep(1)

driver.quit()

df = pd.DataFrame(data_total)
df.to_csv("precios_acciones_bvc.csv", index=False)
print("✅ Archivo guardado: precios_acciones_bvc.csv")
