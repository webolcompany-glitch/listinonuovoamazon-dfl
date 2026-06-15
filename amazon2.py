import pandas as pd
from pathlib import Path

# =====================================
# CONFIGURAZIONE FILE
# =====================================

FILE_AMAZON = "Offerte attive amazon.xlsx"
FILE_FORNITORE = "File fornitore input.xlsx"

OUTPUT_FILTRATO = "File_fornitore_filtrato.xlsx"
OUTPUT_PRESENTI = "Articoli_gia_presenti_amazon.xlsx"

# =====================================
# CONTROLLI ESISTENZA FILE
# =====================================

if not Path(FILE_AMAZON).exists():
    raise FileNotFoundError(f"File non trovato: {FILE_AMAZON}")

if not Path(FILE_FORNITORE).exists():
    raise FileNotFoundError(f"File non trovato: {FILE_FORNITORE}")

print("Lettura file Excel...")

# =====================================
# LETTURA FILE
# =====================================

amazon = pd.read_excel(FILE_AMAZON, dtype=str)
fornitore = pd.read_excel(FILE_FORNITORE, dtype=str)

# =====================================
# CONTROLLO COLONNE
# =====================================

if "seller-sku" not in amazon.columns:
    raise ValueError(
        "Nel file Amazon non esiste la colonna 'seller-sku'"
    )

if "CodiceArticolo" not in fornitore.columns:
    raise ValueError(
        "Nel file Fornitore non esiste la colonna 'CodiceArticolo'"
    )

# =====================================
# ESTRAZIONE CODICI AMAZON
# DFL_100144 -> 100144
# =====================================

codici_amazon = (
    amazon["seller-sku"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.split("_")
    .str[-1]
)

# Elimina eventuali duplicati
codici_amazon = set(codici_amazon)

# =====================================
# NORMALIZZAZIONE CODICI FORNITORE
# =====================================

fornitore["CodiceArticolo"] = (
    fornitore["CodiceArticolo"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# =====================================
# FILTRAGGIO
# =====================================

mask_presenti = fornitore["CodiceArticolo"].isin(codici_amazon)

articoli_presenti = fornitore[mask_presenti].copy()
articoli_da_caricare = fornitore[~mask_presenti].copy()

# =====================================
# SALVATAGGIO
# =====================================

articoli_da_caricare.to_excel(
    OUTPUT_FILTRATO,
    index=False
)

articoli_presenti.to_excel(
    OUTPUT_PRESENTI,
    index=False
)

# =====================================
# REPORT
# =====================================

tot_amazon = len(codici_amazon)
tot_fornitore = len(fornitore)
tot_presenti = len(articoli_presenti)
tot_da_caricare = len(articoli_da_caricare)

print("\n======================================")
print("REPORT FINALE")
print("======================================")
print(f"Articoli Amazon unici      : {tot_amazon:,}")
print(f"Articoli Fornitore         : {tot_fornitore:,}")
print(f"Già presenti su Amazon     : {tot_presenti:,}")
print(f"Da caricare               : {tot_da_caricare:,}")
print("======================================")

print("\nFILE GENERATI:")
print(f"✓ {OUTPUT_FILTRATO}")
print(f"✓ {OUTPUT_PRESENTI}")

print("\nOperazione completata.")