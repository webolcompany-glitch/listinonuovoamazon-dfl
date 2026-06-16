import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Filtro articoli Amazon")

# Upload file
file_amazon = st.file_uploader(
    "Carica il file Amazon",
    type=["xlsx"]
)

file_fornitore = st.file_uploader(
    "Carica il file Fornitore",
    type=["xlsx"]
)

if file_amazon and file_fornitore:

    # ==========================
    # LETTURA FILE
    # ==========================

    amazon = pd.read_excel(file_amazon, dtype=str)
    fornitore = pd.read_excel(file_fornitore, dtype=str)

    # ==========================
    # CONTROLLO COLONNE
    # ==========================

    if "seller-sku" not in amazon.columns:
        st.error(
            "Nel file Amazon non esiste la colonna 'seller-sku'"
        )
        st.stop()

    if "CodiceArticolo" not in fornitore.columns:
        st.error(
            "Nel file Fornitore non esiste la colonna 'CodiceArticolo'"
        )
        st.stop()

    # ==========================
    # ESTRAZIONE CODICI AMAZON
    # ==========================

    codici_amazon = (
        amazon["seller-sku"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.split("_")
        .str[-1]
    )

    codici_amazon = set(codici_amazon)

    # ==========================
    # NORMALIZZAZIONE FORNITORE
    # ==========================

    fornitore["CodiceArticolo"] = (
        fornitore["CodiceArticolo"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ==========================
    # FILTRAGGIO
    # ==========================

    mask_presenti = fornitore["CodiceArticolo"].isin(codici_amazon)

    articoli_presenti = fornitore[mask_presenti].copy()
    articoli_da_caricare = fornitore[~mask_presenti].copy()

    # ==========================
    # REPORT
    # ==========================

    st.success("Elaborazione completata")

    st.write("### Report")

    st.write(
        {
            "Articoli Amazon unici": len(codici_amazon),
            "Articoli Fornitore": len(fornitore),
            "Già presenti su Amazon": len(articoli_presenti),
            "Da caricare": len(articoli_da_caricare),
        }
    )

    # ==========================
    # GENERAZIONE FILE EXCEL
    # ==========================

    output_filtrato = BytesIO()
    output_presenti = BytesIO()

    articoli_da_caricare.to_excel(
        output_filtrato,
        index=False
    )

    articoli_presenti.to_excel(
        output_presenti,
        index=False
    )

    # ==========================
    # DOWNLOAD
    # ==========================

    st.download_button(
        label="📥 Scarica articoli da caricare",
        data=output_filtrato.getvalue(),
        file_name="File_fornitore_filtrato.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        label="📥 Scarica articoli già presenti",
        data=output_presenti.getvalue(),
        file_name="Articoli_gia_presenti_amazon.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
