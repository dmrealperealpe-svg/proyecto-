

import streamlit as st

st.title("correo")

# Credenciales (guárdalas de forma segura en proyectos reales)
USUARIO_CORRECTO = "admin"
CONTRASEÑA_CORRECTA = "1234"

# Formulario de login
usuario = st.text_input("Usuario")
contraseña = st.text_input("Contraseña", type="password")

if st.button("Iniciar sesión"):
    if usuario == USUARIO_CORRECTO and contraseña == CONTRASEÑA_CORRECTA:
        st.success("¡Login exitoso!")
        # Contenido de la app aquí
    else:
        st.error("Usuario o contraseña incorrectos")