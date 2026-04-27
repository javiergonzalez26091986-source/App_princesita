import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mercado & Gestión Hogar", page_icon="🏡", layout="wide")

# --- 1. INICIALIZACIÓN DE DATOS ---
if 'productos' not in st.session_state:
    st.session_state.productos = [
        {"nombre": "Arroz", "precio_ref": 2100, "cat": "Granos", "unidad": "Libra", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Cilantro", "precio_ref": 1000, "cat": "Refrigerador", "unidad": "Manojo", "comprado": False, "stock": 0, "cant_comprada": 0},
        {"nombre": "Salchichas", "precio_ref": 8500, "cat": "Carnes frías", "unidad": "Paquete", "comprado": False, "stock": 0, "cant_comprada": 0},
    ]

if 'categorias' not in st.session_state:
    st.session_state.categorias = ["Granos", "Refrigerador", "Carnes frías", "Aseo", "Proteínas", "Lácteos"]

if 'historial_compras' not in st.session_state:
    st.session_state.historial_compras = []

st.title("🏡 Gestión de Mercado e Inventario")

# --- 2. CONFIGURACIÓN DE CATEGORÍAS Y PRODUCTOS NUEVOS ---
with st.expander("⚙️ Configurar Categorías y Productos"):
    col_cat1, col_cat2 = st.columns([2, 1])
    nueva_c = col_cat1.text_input("Nueva Categoría (ej: Pasillo 5, Congelados):")
    if col_cat2.button("Añadir Categoría") and nueva_c:
        if nueva_c not in st.session_state.categorias:
            st.session_state.categorias.append(nueva_c)
            st.rerun()
    
    st.divider()
    
    c1, c2, c3 = st.columns([2, 1, 1])
    n_prod = c1.text_input("Nombre del producto:")
    c_prod = c2.selectbox("Categoría:", st.session_state.categorias)
    u_prod = c3.text_input("Unidad (ej: Libra):", value="Libra")
    if st.button("➕ Crear Producto"):
        st.session_state.productos.append({
            "nombre": n_prod, "precio_ref": 0, "cat": c_prod, 
            "unidad": u_prod, "comprado": False, "stock": 0, "cant_comprada": 0
        })
        st.rerun()

# --- 3. LISTA DE MERCADO ORGANIZADA ---
st.header("📝 Lista de Mercado")
st.write("Configura tus compras por pasillos:")

# Filtrar productos que no están en el carrito
pendientes = [p for p in st.session_state.productos if not p["comprado"]]

if pendientes:
    # Agrupamos por categoría para que ella no de vueltas en el súper
    for cat in st.session_state.categorias:
        prods_cat = [i for i, p in enumerate(st.session_state.productos) if p["cat"] == cat and not p["comprado"]]
        
        if prods_cat:
            st.subheader(f"📍 {cat}")
            for idx in prods_cat:
                p = st.session_state.productos[idx]
                # Columnas con anchos fijos para forzar alineación
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                c1.write(f"**{p['nombre']}** ({p['unidad']})")
                cant = c2.number_input("Cant.", value=1.0, key=f"c_{idx}", step=0.5)
                prec = c3.number_input("Precio", value=float(p['precio_ref']), key=f"p_{idx}", step=100.0)
                
                if c4.button(f"🛒 ${cant*prec:,.0f}", key=f"b_{idx}"):
                    st.session_state.productos[idx].update({
                        "cant_comprada": cant, "precio_ref": prec, "comprado": True
                    })
                    st.rerun()
else:
    st.info("No hay productos pendientes.")

# --- 4. CARRITO ACTUAL ---
st.divider()
st.header("🛒 Carrito del Día")
comprados = [p for p in st.session_state.productos if p["comprado"]]
if comprados:
    for i, p in enumerate(st.session_state.productos):
        if p["comprado"]:
            col_a, col_b = st.columns([5, 1])
            total_item = p["precio_ref"] * p["cant_comprada"]
            col_a.write(f"✅ **{p['nombre']}**: {p['cant_comprada']} {p['unidad']} (${total_item:,.0f})")
            if col_b.button("❌", key=f"rem_{i}"):
                st.session_state.productos[i]["comprado"] = False
                st.rerun()
    
    if st.button("💰 Confirmar Compra Total"):
        for p in st.session_state.productos:
            if p["comprado"]:
                st.session_state.historial_compras.append({
                    "nombre": p["nombre"], "cat": p["cat"], 
                    "gasto": p["precio_ref"] * p["cant_comprada"],
                    "fecha": pd.Timestamp.now().strftime("%Y-%m-%d")
                })
                p["stock"] += p["cant_comprada"]
                p["comprado"] = False
        st.success("Inventario actualizado")
        st.rerun()

# --- 5. INVENTARIO (Lógica restaurada y segura) ---
st.divider()
st.header("📦 Inventario en Casa")
for i, p in enumerate(st.session_state.productos):
    if p["stock"] > 0:
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"**{p['nombre']}** ({p['stock']} {p['unidad']})")
        gasto = c2.number_input("Gastar:", value=0.0, max_value=float(p["stock"]), key=f"inv_{i}", step=0.1)
        if c3.button("Confirmar", key=f"ubtn_{i}"):
            st.session_state.productos[i]["stock"] -= gasto
            st.rerun()

# --- 6. INFORME ---
st.divider()
st.header("📊 Gastos por Categoría")
if st.session_state.historial_compras:
    df_hist = pd.DataFrame(st.session_state.historial_compras)
    st.bar_chart(df_hist.groupby("cat")["gasto"].sum())
    resumen = df_hist.groupby("cat")["gasto"].sum().reset_index()
    st.bar_chart(resumen.set_index("cat"))
    st.table(resumen.style.format({"gasto": "${:,.0f}"}))
