import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

# ======================
# CONFIGURACIÓN DE LA APP
# ======================
st.set_page_config(page_title="Proyecto 2", layout="wide")
st.title("📊 Proyecto 2: Recaudo Municipal")

# ======================
# CARGA DE DATOS
# ======================
data = pd.read_csv("datos2p.csv")
gdf = gpd.read_parquet("datos2p.parquet")

# ======================
# SELECCIÓN DE MUNICIPIO
# ======================
munis = sorted(data["entidad"].unique().tolist())
mun = st.selectbox("🏙️ Seleccione un municipio:", munis)

filtro = data[data["entidad"] == mun]

# ======================
# AGRUPACIÓN GENERAL
# ======================
gen = (filtro.groupby("clas_gen")["total_recaudo"].sum())
total_gen = gen.sum()
gen = (gen / total_gen).round(2)

# AGRUPACIÓN DETALLADA
det = (filtro.groupby("clasificacion_ofpuj")["total_recaudo"].sum())
total_det = det.sum()
det = (det / total_det).round(3)

# ======================
# GRÁFICO 1 - PIE GENERAL
# ======================
colores_general = ["#2E86AB", "#F6C90E", "#A23B72"]

fig1 = px.pie(
    names=gen.index,
    values=gen.values,
    title="📌 Distribución General de Recursos",
    color_discrete_sequence=colores_general,
    hole=0.4
)
fig1.update_traces(textinfo="percent+label")
st.plotly_chart(fig1, use_container_width=True)

# ======================
# GRÁFICO 2 - PIE DETALLE
# ======================
colores_detalle = px.colors.sequential.Tealgrn

fig2 = px.pie(
    names=det.index,
    values=det.values,
    title="📌 Detalle de Recursos",
    color_discrete_sequence=colores_detalle,
    hole=0.3
)
fig2.update_traces(textinfo="percent+label")
st.plotly_chart(fig2, use_container_width=True)

# ======================
# TREE MAP
# ======================
fin = (
    filtro.groupby(["clas_gen", "clasificacion_ofpuj"])["total_recaudo"]
    .sum()
    .reset_index()
)

fig3 = px.treemap(
    fin,
    path=[px.Constant("Total"), "clas_gen", "clasificacion_ofpuj"],
    values="total_recaudo",
    color="total_recaudo",
    color_continuous_scale="Viridis"
)
fig3.update_layout(title="🌳 Estructura Jerárquica del Recaudo")
st.plotly_chart(fig3, use_container_width=True)

# ======================
# MAPA GEOREFERENCIADO
# ======================
filtro2 = gdf[gdf["entidad"] == mun][["codigo_alt", "geometry"]]

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
filtro2.plot(ax=ax, color="#2E86AB", edgecolor="black", alpha=0.7)

ax.set_axis_off()
ax.set_title(f"🗺️ Mapa georreferenciado de {mun}", fontsize=12, fontweight="bold")
st.pyplot(fig)
