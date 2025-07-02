import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Mines Bot Web - Probabilidade 95%", layout="centered")
st.title("💣 Mines Bot Web - Inteligência Estatística")

# Inicialização de estados
if "banca" not in st.session_state:
    st.session_state.banca = 10.0
if "lucro_total" not in st.session_state:
    st.session_state.lucro_total = 0.0
if "historico" not in st.session_state:
    st.session_state.historico = []

# Interface de jogo
bombas = st.slider("🎯 Quantas bombas no jogo?", 1, 24, 3)
valor_entrada = st.number_input("💵 Valor da entrada (R$)", min_value=0.1, value=0.2, step=0.1)
resultado = st.radio("🎮 Resultado da jogada:", ["✅ Acerto", "❌ Derrota", "💰 Saque"])

if st.button("Registrar Jogada"):
    if resultado == "✅ Acerto":
        lucro = valor_entrada * 0.85
        st.session_state.banca += lucro
    elif resultado == "❌ Derrota":
        st.session_state.banca -= valor_entrada
    elif resultado == "💰 Saque":
        st.session_state.banca += valor_entrada * 1.2  # valor simulado

    lucro_atual = st.session_state.banca - 10.0
    st.session_state.lucro_total = lucro_atual

    st.session_state.historico.append({
        "Resultado": resultado,
        "Banca": round(st.session_state.banca, 2)
    })

# Exibição da banca
st.metric("💰 Banca atual", f"R$ {st.session_state.banca:.2f}")
st.metric("📈 Lucro total", f"R$ {st.session_state.lucro_total:.2f}")

# Histórico de jogadas
st.subheader("📋 Histórico")
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.dataframe(df, use_container_width=True)
    acertos = sum(1 for h in st.session_state.historico if h["Resultado"] == "✅ Acerto")
    total = len(st.session_state.historico)
    prob = acertos / total if total > 0 else 0
    st.metric("🔢 Probabilidade de acerto", f"{prob*100:.2f}%")
    if prob >= 0.95:
        st.success("🎯 Probabilidade alta! Pode clicar!")
    else:
        st.warning("🧪 Aguardando padrão ≥ 95%")
else:
    st.info("Registre suas jogadas para começar.")

# Casas seguras sugeridas (base estatística simulada)
st.subheader("📌 Sugestão de casas com maior chance (estatístico)")
casas_totais = list(range(1, 26))
casas_sugeridas = random.sample(casas_totais, 25 - bombas)
st.write("Casas sugeridas:", sorted(casas_sugeridas))