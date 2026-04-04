

# import streamlit as st

# st.title("correo")

# # Credenciales (guárdalas de forma segura en proyectos reales)
# USUARIO_CORRECTO = "admin"
# CONTRASEÑA_CORRECTA = "1234"

# # Formulario de login
# usuario = st.text_input("Usuario")
# contraseña = st.text_input("Contraseña", type="password")

# if st.button("Iniciar sesión"):
#     if usuario == USUARIO_CORRECTO and contraseña == CONTRASEÑA_CORRECTA:
#         st.success("¡Login exitoso!")
#         # Contenido de la app aquí
#     else:
#         st.error("Usuario o contraseña incorrectos")

import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Tienda de Ropa | Iniciar Sesión", page_icon="👕", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #ff3333;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATOS DE ACCESO (EN PROYECTOS REALES USA BASE DE DATOS) ---
USUARIO_CORRECTO = "admin"
CONTRASEÑA_CORRECTA = "1234"

# --- VARIABLE DE ESTADO PARA CONTROLAR SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- FORMULARIO DE INICIO DE SESIÓN ---
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">👕 Tienda de Ropa</h1>', unsafe_allow_html=True)
    
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        if usuario == USUARIO_CORRECTO and contraseña == CONTRASEÑA_CORRECTA:
            st.session_state.logged_in = True
            st.success("✅ Inicio de sesión exitoso!")
            st.rerun()  # Recarga para mostrar el contenido
        else:
            st.error("❌ Usuario o contraseña incorrectos")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- CONTENIDO PRINCIPAL DE LA TIENDA ---
else:
    st.title("👕 Bienvenido a nuestra Tienda de Ropa")
    st.subheader("Catálogo de productos")
    
    # Aquí iría el código para mostrar productos, categorías, carrito, etc.
    st.write("Aquí se mostrarán las prendas, precios y opciones de compra.")
    
    # Botón para cerrar sesión
    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()