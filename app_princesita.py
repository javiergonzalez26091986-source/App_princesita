import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mercado & Gestión Hogar", page_icon="🏡", layout="wide")

# --- 1. INICIALIZACIÓN DE DATOS (Misma estructura) ---
if 'productos' not in st.session_state:
    st.session_state.productos = [
        {"nombre": "Arroz", "precio_ref": 2100, "cat": "Granos", "unidad": "Libra", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Aceite", "precio_ref": 12500, "cat": "Granos", "unidad": "Litro", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Huevos", "precio_ref": 18500, "cat": "Proteínas", "unidad": "Cubeta", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Leche", "precio_ref": 4500, "cat": "Lácteos", "unidad": "Bolsa", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Pollo", "precio_ref": 7000, "cat": "Proteínas", "unidad": "Libra", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Detergente", "precio_ref": 11000, "cat": "Aseo", "unidad": "Bolsa", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Papel Higiénico", "precio_ref": 9500, "cat": "Aseo", "unidad": "Paquete", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Café", "precio_ref": 9000, "cat": "Despensa", "unidad": "250g", "comprado": False, "stock": 0, "cant_comprada": 0},
    ]

if 'historial_compras' not in st.session_state:
    st.session_state.historial_compras = []

st.title("🏡 Gestión de Mercado e Inventario")

# --- 2. LISTA DE MERCADO (Lógica de cantidades y unidades) ---
st.header("📝 Lista de Mercado")
with st.expander("Ver estantería de productos", expanded=True):
    for i, p in enumerate(st.session_state.productos):
        if not p["comprado"]:
            c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
            c1.write(f"**{p['nombre']}**")
            
            # Lógica de Unidad (Libra por defecto)
            unid_list = ["Libra", "Kilo", "Litro", "Bolsa", "Paquete", "Cubeta", "Unidad"]
            if p["unidad"] not in unid_list: unid_list.append(p["unidad"])
            nueva_unid = c2.selectbox("Unidad", unid_list, index=unid_list.index(p["unidad"]), key=f"u_{i}")
            
            # Lógica de Precio y Cantidad
            nuevo_p = c3.number_input("Precio/U", value=float(p["precio_ref"]), key=f"p_{i}", step=50.0)
            nueva_cant = c4.number_input("Cant.", value=1.0, min_value=0.1, key=f"c_{i}", step=0.5)
            
            if c5.button("🛒 Agregar", key=f"add_{i}"):
                st.session_state.productos[i].update({
                    "unidad": nueva_unid,
                    "precio_ref": nuevo_p,
                    "cant_comprada": nueva_cant,
                    "comprado": True
                })
                st.rerun()

# --- 3. CARRITO ACTUAL (Lógica para quitar productos) ---
st.divider()
st.header("🛒 Carrito del Día")
comprados_ahora = [p for p in st.session_state.productos if p["comprado"]]

if comprados_ahora:
    for i, p in enumerate(st.session_state.productos):
        if p["comprado"]:
            col_a, col_b = st.columns([4, 1])
            subtotal = p["precio_ref"] * p["cant_comprada"]
            col_a.write(f"✅ **{p['nombre']}**: {p['cant_comprada']} {p['unidad']} (${subtotal:,.0f})")
            
            # Opción para quitar por error
            if col_b.button("❌ Quitar", key=f"rem_{i}"):
                st.session_state.productos[i]["comprado"] = False
                st.rerun()
    
    total_hoy = sum(p["precio_ref"] * p["cant_comprada"] for p in st.session_state.productos if p["comprado"])
    st.metric("Total a pagar", f"${total_hoy:,.0f} COP")
    
    if st.button("💰 Finalizar y Cargar al Inventario"):
        for p in st.session_state.productos:
            if p["comprado"]:
                st.session_state.historial_compras.append({
                    "nombre": p["nombre"], "cat": p["cat"], 
                    "gasto": p["precio_ref"] * p["cant_comprada"],
                    "fecha": pd.Timestamp.now().strftime("%Y-%m-%d")
                })
                p["stock"] += p["cant_comprada"]
                p["comprado"] = False
        st.success("¡Compra registrada!")
        st.rerun()
else:
    st.write("Carrito vacío.")

# --- 4. INVENTARIO (Descontar lo gastado) ---
st.divider()
st.header("📦 Inventario en Casa")
for i, p in enumerate(st.session_state.productos):
    if p["stock"] > 0:
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"**{p['nombre']}**")
        c2.write(f"Stock: {p['stock']} {p['unidad']}")
        # Descontar cantidad específica
        uso = c3.number_input("Cantidad usada:", value=1.0, min_value=0.1, max_value=float(p["stock"]), key=f"use_{i}")
        if c3.button(f"Gastar {uso}", key=f"ubtn_{i}"):
            st.session_state.productos[i]["stock"] -= uso
            st.rerun()

# --- 5. INFORME POR JERARQUÍA (Se mantiene) ---
st.divider()
st.header("📊 Informe de Gastos")
if st.session_state.historial_compras:
    df_hist = pd.DataFrame(st.session_state.historial_compras)
    resumen = df_hist.groupby("cat")["gasto"].sum().reset_index()
    st.bar_chart(resumen.set_index("cat"))
    st.table(resumen.style.format({"gasto": "${:,.0f}"}))
