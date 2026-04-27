import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mercado & Gestión Hogar", page_icon="🏡", layout="wide")

# --- 1. DATOS INICIALES (Intactos como los tenías) ---
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

# Lista de categorías dinámicas
if 'categorias_adicionales' not in st.session_state:
    st.session_state.categorias_adicionales = ["Granos", "Proteínas", "Lácteos", "Aseo", "Despensa"]

if 'historial_compras' not in st.session_state:
    st.session_state.historial_compras = []

st.title("🏡 Gestión de Mercado e Inventario")

# --- 2. GESTIÓN DE CATEGORÍAS (Nueva función solicitada) ---
with st.expander("📂 Crear y Organizar Categorías"):
    col_nueva1, col_nueva2 = st.columns([3, 1])
    nueva_cat = col_nueva1.text_input("Nombre de la nueva categoría (ej: Refrigerador):")
    if col_nueva2.button("Añadir") and nueva_cat:
        if nueva_cat not in st.session_state.categorias_adicionales:
            st.session_state.categorias_adicionales.append(nueva_cat)
            st.rerun()
    
    st.write("---")
    st.write("Mover producto a categoría:")
    c_p, c_c, c_b = st.columns([2, 2, 1])
    prod_a_mover = c_p.selectbox("Selecciona Producto", [p["nombre"] for p in st.session_state.productos])
    cat_destino = c_c.selectbox("Mover a:", st.session_state.categorias_adicionales)
    if c_b.button("Mover"):
        for p in st.session_state.productos:
            if p["nombre"] == prod_a_mover:
                p["cat"] = cat_destino
                st.rerun()

# --- 3. LISTA DE MERCADO (Organizada por la categoría que ella elija) ---
st.header("📝 Lista de Mercado")
for cat in st.session_state.categorias_adicionales:
    # Solo mostrar la categoría si tiene productos pendientes
    prods_en_cat = [i for i, p in enumerate(st.session_state.productos) if p["cat"] == cat and not p["comprado"]]
    
    if prods_en_cat:
        st.subheader(f"📍 {cat}")
        for idx in prods_en_cat:
            p = st.session_state.productos[idx]
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            col1.write(f"**{p['nombre']}**")
            # Unidad
            u_opciones = ["Libra", "Kilo", "Litro", "Bolsa", "Paquete", "Cubeta", "Unidad"]
            u_final = col2.selectbox("Unid.", u_opciones, index=u_opciones.index(p["unidad"]) if p["unidad"] in u_opciones else 0, key=f"u_{idx}")
            # Cantidad y Precio
            c_final = col3.number_input("Cant.", value=1.0, min_value=0.1, key=f"c_{idx}")
            p_final = col4.number_input("$/U", value=float(p["precio_ref"]), key=f"p_{idx}")
            
            if col5.button(f"🛒 ${(c_final*p_final):,.0f}", key=f"b_{idx}"):
                st.session_state.productos[idx].update({
                    "unidad": u_final, "cant_comprada": c_final, "precio_ref": p_final, "comprado": True
                })
                st.rerun()

# --- 4. CARRITO ACTUAL ---
st.divider()
st.header("🛒 Carrito del Día")
comprados = [p for p in st.session_state.productos if p["comprado"]]
if comprados:
    for i, p in enumerate(st.session_state.productos):
        if p["comprado"]:
            ca, cb = st.columns([5, 1])
            sub = p["precio_ref"] * p["cant_comprada"]
            ca.write(f"✅ **{p['nombre']}**: {p['cant_comprada']} {p['unidad']} (${sub:,.0f})")
            if cb.button("❌", key=f"rem_{i}"):
                st.session_state.productos[i]["comprado"] = False
                st.rerun()
    
    if st.button("💰 Confirmar Compra"):
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

# --- 5. INVENTARIO (Lógica original intacta) ---
st.divider()
st.header("📦 Inventario en Casa")
for i, p in enumerate(st.session_state.productos):
    if p["stock"] > 0:
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"**{p['nombre']}** ({p['stock']} {p['unidad']})")
        gasto = c2.number_input("Gastar:", value=0.0, max_value=float(p["stock"]), key=f"inv_{i}")
        if c3.button("Confirmar", key=f"ubtn_{i}"):
            st.session_state.productos[i]["stock"] -= gasto
            st.rerun()

# --- 6. INFORME ---
st.divider()
st.header("📊 Informe de Gastos")
if st.session_state.historial_compras:
    df_hist = pd.DataFrame(st.session_state.historial_compras)
    st.bar_chart(df_hist.groupby("cat")["gasto"].sum())
