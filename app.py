import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

st.title("📊 Dilema del Vendedor de Periódicos")

# --- Entradas del usuario ---
n_sim = st.number_input("Cantidad de simulaciones (días)", min_value=10, max_value=10000, value=1000, step=10)
precio_venta = st.number_input("Precio de venta", min_value=0.1, value=0.50, step=0.01)
precio_compra = st.number_input("Precio de compra", min_value=0.1, value=0.33, step=0.01)
precio_reciclaje = st.number_input("Precio de reciclaje", min_value=0.0, value=0.05, step=0.01)

# --- Datos del problema ---
tipos_dia = ["Excelente", "Bueno", "Malo"]
prob_dia = [0.35, 0.45, 0.20]

tabla_demanda = {
    "Demanda": [40, 50, 60, 70, 80, 90, 100],
    "Excelente": [0.03, 0.05, 0.15, 0.20, 0.35, 0.15, 0.07],
    "Bueno":     [0.10, 0.18, 0.40, 0.20, 0.08, 0.04, 0.00],
    "Malo":      [0.44, 0.22, 0.16, 0.12, 0.06, 0.00, 0.00]
}
df_demanda = pd.DataFrame(tabla_demanda)

if st.button("Simular"):
    resultados = []

    for q in range(40, 101, 10):  # ofertas en bloques de 10
        ganancias = []

        for _ in range(n_sim):
            # Elegir tipo de día
            tipo = random.choices(tipos_dia, weights=prob_dia, k=1)[0]

            # Elegir demanda según distribución del día
            demanda = random.choices(df_demanda["Demanda"],
                                     weights=df_demanda[tipo],
                                     k=1)[0]

            # Calcular ganancia
            ventas = min(q, demanda)
            sobrante = max(0, q - demanda)
            ganancia = precio_venta * ventas - precio_compra * q + precio_reciclaje * sobrante
            ganancias.append(ganancia)

        resultados.append({"Oferta": q,
                           "Ganancia_promedio": np.mean(ganancias),
                           "Ganancias": ganancias})

    df_resultados = pd.DataFrame(resultados)

    # --- Gráfico de línea (ganancia promedio) ---
    fig1, ax1 = plt.subplots()
    ax1.plot(df_resultados["Oferta"], df_resultados["Ganancia_promedio"], marker="o")
    ax1.set_title("Ganancia promedio según cantidad de periódicos comprados")
    ax1.set_xlabel("Cantidad comprada")
    ax1.set_ylabel("Ganancia promedio")
    st.pyplot(fig1)

    # --- Gráfico de violín (distribución de ganancias) ---
    df_exploded = df_resultados.explode("Ganancias")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.violinplot(x="Oferta", y="Ganancias", data=df_exploded, inner="quartile", ax=ax2)
    ax2.set_title("Distribución de ganancias por cantidad comprada")
    ax2.set_xlabel("Cantidad comprada")
    ax2.set_ylabel("Ganancia")
    st.pyplot(fig2)

