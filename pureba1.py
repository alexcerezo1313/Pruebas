import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Visualización de una Onda Senoidal")

# Crear un rango de valores de 0 a 2π
x = np.linspace(0, 2 * np.pi, 1000)
y = np.sin(x)

# Crear la figura y el eje para la gráfica
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Onda Senoidal")
ax.set_xlabel("Ángulo (radianes)")
ax.set_ylabel("Amplitud")
ax.grid(True)

# Mostrar la gráfica en la aplicación web con Streamlit
st.pyplot(fig)
