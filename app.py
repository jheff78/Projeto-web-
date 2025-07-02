import streamlit as st
import pandas as pd

APOSTA = 0.20
META_LUCRO = 2.00
STOP_LOSS = 2.00

if "banca" not in st.session_state:
    st.session_state.banca = 10.0
    st.session_state.lucro_total = 0.0
    st.session_state.cliques = 0
    st.session_state.jogos = []

def calcular_probabilidade(cliques):
    prob = 1.0
    casas_seguras = 22
    casas_totais = 25
    for _ in range(cliques):
        prob *= casas_seguras / casas_totais
        casas_seguras -= 1
        casas_totais -= 1
    return round(prob * 100, 2)

st.title("🎮 Mines 1Win - Bot Manual (Web)")

st.markdown(f"**💰 Banca:** R${st.session_state.banca:.2f}  
"
            f"📈 Lucro Total: R${st.session_state.lucro_total:.2f}  
"
            f"🎯 Meta: R${META_LUCRO:.2f} / 🛑 Stop: R${STOP_LOSS:.2f}")

if st.session_state.lucro_total >= META_LUCRO:
    st.success("🎉 Meta de lucro atingida!")
    st.stop()

if st.session_state.lucro_total <= -STOP_LOSS:
    st.error("🛑 Stop Loss atingido!")
    st.stop()

st.header("🎲 Nova Rodada")
prob = calcular_probabilidade(st.session_state.cliques + 1)
st.metric("🧠 Probabilidade do próximo clique", f"{prob:.2f}%")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Acertou"):
        st.session_state.cliques += 1
        prob = calcular_probabilidade(st.session_state.cliques)
        st.success(f"Acertou {st.session_state.cliques}x - Prob: {prob:.2f}%")
with col2:
    if st.button("💰 Sacar"):
        ganho = APOSTA * (0.09 * st.session_state.cliques)
        st.session_state.banca += ganho
        st.session_state.lucro_total += ganho
        st.session_state.jogos.append(["VITÓRIA", st.session_state.cliques, prob, ganho, st.session_state.banca])
        st.success(f"✅ Vitória! Lucro: R${ganho:.2f}")
        st.session_state.cliques = 0
with col3:
    if st.button("❌ Perdeu"):
        st.session_state.banca -= APOSTA
        st.session_state.lucro_total -= APOSTA
        st.session_state.jogos.append(["DERROTA", st.session_state.cliques, prob, -APOSTA, st.session_state.banca])
        st.error(f"❌ Perdeu R${APOSTA:.2f}")
        st.session_state.cliques = 0

if st.session_state.jogos:
    df = pd.DataFrame(st.session_state.jogos, columns=["Status", "Cliques", "Prob (%)", "Lucro", "Banca"])
    st.subheader("📊 Histórico")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar log (.csv)", data=csv, file_name="log.csv", mime="text/csv")
