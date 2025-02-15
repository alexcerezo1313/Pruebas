import streamlit as st
import pandas as pd
import json

# --- Cargar datos desde el archivo JSON ---
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    st.error(f"Error al cargar el archivo JSON: {e}")
    st.stop()

# Convertir la lista de registros a un DataFrame
df = pd.DataFrame(data)

# Depuración: mostrar las columnas detectadas antes de normalizar
st.write("Columnas detectadas (original):", df.columns.tolist())

# Normalizar nombres de columnas: quitar espacios extra y pasar a minúsculas
df.columns = df.columns.str.strip().str.lower()
st.write("Columnas normalizadas:", df.columns.tolist())

# Definir los nombres de columnas a usar (en minúsculas, de acuerdo a la normalización)
col_pluma = "pluma"                        # Antes "pluma instalada"
col_alcance = "alcance deseado"
col_carga_deseada = "carga deseada"
col_modelo = "modelo de grúa torre"         # Con acento en "grúa"
col_carga_punta = "carga punta pluma"       # Antes "carga en punta"

# Lista de columnas requeridas
required_columns = [col_pluma, col_alcance, col_carga_deseada, col_modelo, col_carga_punta]

# Verificar que todas las columnas requeridas estén presentes
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    st.error(f"Las siguientes columnas no se encontraron en el JSON: {missing_cols}")
    st.stop()

# --- Título de la aplicación ---
st.title("Selector de Modelo de Grúa Torre")

# --- Panel de filtros en la barra lateral ---
st.sidebar.header("Filtros de búsqueda")

# Slider para filtrar por la longitud de la pluma
min_pluma_val = df[col_pluma].min()
max_pluma_val = df[col_pluma].max()
pluma_range = st.sidebar.slider(
    "Pluma (longitud)",
    float(min_pluma_val), 
    float(max_pluma_val),
    (float(min_pluma_val), float(max_pluma_val))
)

# Slider para filtrar por el alcance deseado
min_alcance_val = df[col_alcance].min()
max_alcance_val = df[col_alcance].max()
alcance_range = st.sidebar.slider(
    "Alcance deseado",
    float(min_alcance_val),
    float(max_alcance_val),
    (float(min_alcance_val), float(max_alcance_val))
)

# Slider para filtrar por la carga deseada
min_carga_deseada_val = df[col_carga_deseada].min()
max_carga_deseada_val = df[col_carga_deseada].max()
carga_deseada_range = st.sidebar.slider(
    "Carga deseada",
    float(min_carga_deseada_val),
    float(max_carga_deseada_val),
    (float(min_carga_deseada_val), float(max_carga_deseada_val))
)

# Slider para filtrar por la carga punta pluma mínima
min_carga_punta_val = df[col_carga_punta].min()
max_carga_punta_val = df[col_carga_punta].max()
carga_punta_min = st.sidebar.slider(
    "Carga punta pluma mínima",
    float(min_carga_punta_val),
    float(max_carga_punta_val),
    float(min_carga_punta_val)
)

# --- Filtrado de la base de datos ---
filtered_df = df[
    (df[col_pluma] >= pluma_range[0]) & (df[col_pluma] <= pluma_range[1]) &
    (df[col_alcance] >= alcance_range[0]) & (df[col_alcance] <= alcance_range[1]) &
    (df[col_carga_deseada] >= carga_deseada_range[0]) & (df[col_carga_deseada] <= carga_deseada_range[1]) &
    (df[col_carga_punta] >= carga_punta_min)
]

# --- Mostrar resultados ---
st.subheader("Modelos de Grúa Recomendados")
if not filtered_df.empty:
    st.write("Se han encontrado los siguientes modelos de grúa que cumplen con los filtros seleccionados:")
    st.dataframe(filtered_df[[col_modelo, col_pluma, col_alcance, col_carga_deseada, col_carga_punta]])
else:
    st.write("No se encontraron resultados con los filtros aplicados. Intenta modificar los parámetros.")
