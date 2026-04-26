import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mercado & Gestión Hogar", page_icon="🏡", layout="wide")

# --- 1. INICIALIZACIÓN DE DATOS ---
if 'productos' not in st.session_state:
    st.session_state.productos = [
        {"nombre": "Arroz (1kg)", "precio": 4200, "cat": "Granos", "comprado": False, "stock": 0},
        {"nombre": "Aceite (1L)", "precio": 12500, "cat": "Granos", "comprado": False, "stock": 0},
        {"nombre": "Huevos (x30)", "precio": 18500, "cat": "Proteínas", "comprado": False, "stock": 0},
        {"nombre": "Leche (6 pack)", "precio": 26000, "cat": "Lácteos", "comprado": False, "stock": 0},
        {"nombre": "Pollo (kg)", "precio": 14000, "cat": "Proteínas", "comprado": False, "stock": 0},
        {"nombre": "Detergente", "precio": 11000, "cat": "Aseo", "comprado": False, "stock": 0},
        {"nombre": "Papel Higiénico", "precio": 9500, "cat": "Aseo", "comprado": False, "stock": 0},
        {"nombre": "Café (250g)", "precio": 9000, "cat": "Despensa", "comprado": False, "stock": 0},
    ]

# Historial permanente para los informes
if 'historial_compras' not in st.session_state:
    st.session_state.historial_compras = []

st.title("🏡 Gestión de Mercado e Inventario")

# --- 2. LISTA DISPONIBLE (Ajuste de Precios y Compra) ---
st.header("📝 Lista de Mercado")
with st.expander("Ver lista completa para marcar", expanded=True):
    for i, p in enumerate(st.session_state.productos):
        if not p["comprado"]:
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"**{p['nombre']}** ({p['cat']})")
            # Precio editable
            nuevo_p = col2.number_input(f"Precio", value=p["precio"], key=f"pre_{i}", step=100)
            if col3.button("✅ Al Carrito", key=f"btn_{i}"):
                st.session_state.productos[i]["precio"] = nuevo_p
                st.session_state.productos[i]["comprado"] = True
                st.rerun()

# --- 3. CARRITO DEL DÍA ---
st.divider()
st.header("🛒 Carrito Actual")
comprados_ahora = [p for p in st.session_state.productos if p["comprado"]]

if comprados_ahora:
    df_carro = pd.DataFrame(comprados_ahora)
    st.table(df_carro[["nombre", "cat", "precio"]])
    
    if st.button("💰 Finalizar y Registrar Compra"):
        for p in st.session_state.productos:
            if p["comprado"]:
                # 1. Guardar en el historial permanente
                st.session_state.historial_compras.append({
                    "nombre": p["nombre"],
                    "cat": p["cat"],
                    "precio": p["precio"],
                    "fecha": pd.Timestamp.now().strftime("%Y-%m-%d")
                })
                # 2. Sumar al inventario (stock)
                p["stock"] += 1
                # 3. Quitar del carrito
                p["comprado"] = False
        st.success("¡Mercado registrado exitosamente!")
        st.rerun()
else:
    st.info("No hay productos en el carrito.")

# --- 4. INVENTARIO (Consumo en casa) ---
st.divider()
st.header("📦 Inventario en Casa")
cols = st.columns(3)
for i, p in enumerate(st.session_state.productos):
    if p["stock"] > 0:
        with st.container():
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{p['nombre']}** (Stock: {p['stock']})")
            if c2.button("➖ Usar", key=f"use_{i}"):
                st.session_state.productos[i]["stock"] -= 1
                st.rerun()

# --- 5. INFORME PERMANENTE POR JERARQUÍAS ---
st.divider()
st.header("📊 Informe Histórico de Gastos")
if st.session_state.historial_compras:
    df_historial = pd.DataFrame(st.session_state.historial_compras)
    
    # Agrupar por categoría (Jerarquía)
    informe_jerarquia = df_historial.groupby("cat")["precio"].sum().reset_index()
    informe_jerarquia.columns = ["Categoría", "Inversión Total"]
    
    col_inf1, col_inf2 = st.columns([1, 1])
    
    with col_inf1:
        st.subheader("Gasto por Categoría")
        st.bar_chart(informe_jerarquia.set_index("Categoría"))
        
    with col_inf2:
        st.subheader("Detalle Económico")
        st.dataframe(informe_jerarquia.style.format({"Inversión Total": "${:,.0f} COP"}), use_container_width=True)
        st.metric("Gasto Acumulado Total", f"${df_historial['precio'].sum():,.0f} COP")
else:
    st.write("Aún no hay compras registradas para generar informes.")
