import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mercado Familiar", page_icon="🛒", layout="wide")

st.title("🛒 Asistente de Compras - Cali/Yumbo")

# 1. Base de datos predeterminada con precios estimados de la región
PRODUCTOS_BASE = {
    "Granos y Despensa": [
        ("Arroz (1kg)", 4200), ("Aceite (1L)", 12500), ("Frijol (500g)", 6500), 
        ("Lentejas (500g)", 4000), ("Azúcar (1kg)", 4500), ("Café (250g)", 9000),
        ("Sal (1kg)", 2200), ("Pasta (500g)", 3800)
    ],
    "Proteínas (Carnes/Huevos)": [
        ("Huevos (Cubeta x30)", 18500), ("Pollo Entero (kg)", 14000), 
        ("Carne de Res (kg)", 28000), ("Carne de Cerdo (kg)", 22000),
        ("Pescado (kg)", 25000)
    ],
    "Lácteos y Desayuno": [
        ("Leche (6 pack)", 26000), ("Queso Cuajada", 12000), 
        ("Mantequilla (250g)", 8500), ("Chocolate (Pastillas)", 6000)
    ],
    "Aseo y Hogar": [
        ("Detergente (kg)", 11000), ("Jabón de Baño (3 Pack)", 12000), 
        ("Papel Higiénico (4 rollos)", 9500), ("Lavaloza", 5500),
        ("Suavizante", 13000)
    ],
    "Frutas y Verduras": [
        ("Papa (Libra)", 2000), ("Plátano (Unidad)", 1500), 
        ("Tomate (Libra)", 2500), ("Cebolla (Libra)", 2200),
        ("Fruta de temporada", 5000)
    ]
}

# Inicializar estados de sesión
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- SECCIÓN 1: AGREGAR PRODUCTOS ---
st.header("📋 Selecciona lo que necesitas")
col_cat, col_prod = st.columns(2)

with col_cat:
    categoria_sel = st.selectbox("Categoría:", list(PRODUCTOS_BASE.keys()))

with col_prod:
    lista_opciones = [p[0] for p in PRODUCTOS_BASE[categoria_sel]]
    producto_sel = st.selectbox("Producto:", lista_opciones)

if st.button("Añadir al carrito"):
    # Buscar el precio en la base de datos
    precio = next(p[1] for p in PRODUCTOS_BASE[categoria_sel] if p[0] == producto_sel)
    st.session_state.carrito.append({
        "Producto": producto_sel,
        "Categoría": categoria_sel,
        "Precio": precio
    })
    st.success(f"{producto_sel} agregado")

# --- SECCIÓN 2: CARRITO ACTUAL ---
st.divider()
st.header("🛒 Tu Lista Actual")

if st.session_state.carrito:
    df_carrito = pd.DataFrame(st.session_state.carrito)
    st.table(df_carrito)
    
    total = df_carrito["Precio"].sum()
    st.subheader(f"💰 Total Estimado: ${total:,.0f} COP")
    
    if st.button("Vaciar Carrito"):
        st.session_state.carrito = []
        st.rerun()
else:
    st.info("El carrito está vacío.")

# --- SECCIÓN 3: INFORMES POR JERARQUÍA ---
st.divider()
st.header("📊 Informe de Gastos")

if st.session_state.carrito:
    # Agrupar por categoría
    df_resumen = df_carrito.groupby("Categoría")["Precio"].sum().reset_index()
    df_resumen.columns = ["Jerarquía de Producto", "Gasto Total"]
    
    # Mostrar gráfico de barras simple
    st.bar_chart(df_resumen.set_index("Jerarquía de Producto"))
    
    # Mostrar tabla de resumen
    st.write("Resumen detallado por categoría:")
    st.dataframe(df_resumen.style.format({"Gasto Total": "${:,.0f}"}))
else:
    st.write("No hay datos suficientes para generar informes.")
