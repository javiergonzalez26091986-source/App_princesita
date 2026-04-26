import streamlit as st

# Configuración de estilo
st.set_page_config(page_title="Lista de Mercar", page_icon="🛒")

st.title("🛒 Lista de Mercar")
st.write("¡Hola! Aquí puedes anotar lo que necesitemos.")

# Inicializar la lista si no existe
if 'market_list' not in st.session_state:
    st.session_state.market_list = []

# Entrada de texto
item = st.text_input("Producto nuevo:", placeholder="Ej: Arroz, leche...")

if st.button("Agregar a la lista"):
    if item:
        st.session_state.market_list.append(item)
        st.rerun()

st.divider()

# Mostrar los productos
if st.session_state.market_list:
    for i, producto in enumerate(st.session_state.market_list):
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(f"✅ {producto}")
        if col2.button("Eliminar", key=f"delete_{i}"):
            st.session_state.market_list.pop(i)
            st.rerun()
            
    if st.button("Limpiar toda la lista"):
        st.session_state.market_list = []
        st.rerun()
else:
    st.write("La lista está vacía.")
