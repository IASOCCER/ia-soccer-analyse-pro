
import streamlit as st

st.set_page_config(page_title="IA Soccer Analyse Pro Web", layout="wide")
st.title("IA Soccer Analyse Pro Web")

st.markdown("## Avaliação Técnica do Jogador")
nome = st.text_input("Nome do jogador")
idade = st.number_input("Idade", min_value=8, max_value=18)

tempo_passe = st.number_input("Tempo médio de passe (s)")
precisao_passe = st.slider("Precisão do passe (%)", 0, 100, 94)

velocidade_remate = st.number_input("Velocidade do remate (km/h)", value=67.0)
acerto_remate = st.slider("Precisão do remate (%)", 0, 100, 60)

st.markdown("---")
st.markdown("## Avaliação Biométrica")

altura = st.number_input("Altura (cm)", min_value=100, max_value=220, value=140)
peso = st.number_input("Peso (kg)", min_value=20, max_value=150, value=40)
massa_muscular = st.slider("Massa muscular estimada (%)", 0, 100, 45)

# Cálculo de IMC
altura_m = altura / 100
imc = round(peso / (altura_m ** 2), 1)

if st.button("Gerar Relatório Completo"):
    st.success("Relatório gerado com sucesso!")

    st.markdown(f'''
**Jogador:** {nome}  
**Idade:** {idade} anos  

### 🟦 Dados Técnicos
- Tempo médio de passe: {tempo_passe} s  
- Precisão do passe: {precisao_passe}%  
- Velocidade do remate: {velocidade_remate} km/h  
- Precisão do remate: {acerto_remate}%

### 🟩 Análise Técnica Automática
''')

    if tempo_passe > 2.5:
        st.markdown("- **Passe:** ⚠️ Acima do ideal. Treinar reação sob pressão.")
    else:
        st.markdown("- **Passe:** ✅ Dentro do ideal.")

    if precisao_passe >= 85:
        st.markdown("- **Precisão:** ✅ Excelente.")
    else:
        st.markdown("- **Precisão:** ⚠️ Pode melhorar consistência.")

    if velocidade_remate >= 55:
        st.markdown("- **Remate:** ✅ Potente.")
    else:
        st.markdown("- **Remate:** ⚠️ Potência abaixo da média.")

    if acerto_remate >= 70:
        st.markdown("- **Finalização:** ✅ Boa direção.")
    else:
        st.markdown("- **Finalização:** ⚠️ Melhorar controle e pontaria.")

    st.markdown(f'''
### 🟨 Dados Biométricos
- Altura: {altura} cm  
- Peso: {peso} kg  
- Massa muscular: {massa_muscular}%  
- **IMC:** {imc}

### 🟥 Análise Física Automática
''')

    if imc < 14:
        st.markdown("- **IMC:** ⚠️ Muito abaixo do ideal — acompanhar crescimento.")
    elif 14 <= imc < 18:
        st.markdown("- **IMC:** ✅ Dentro da média saudável para a idade.")
    elif 18 <= imc < 21:
        st.markdown("- **IMC:** 🔎 Ligeiramente elevado — manter acompanhamento.")
    else:
        st.markdown("- **IMC:** ⚠️ Acima do ideal — atenção com alimentação e treino físico.")

    if massa_muscular < 40:
        st.markdown("- **Massa muscular:** ⚠️ Baixa — foco em treino físico funcional.")
    elif 40 <= massa_muscular < 60:
        st.markdown("- **Massa muscular:** ✅ Boa para a idade.")
    else:
        st.markdown("- **Massa muscular:** 🔝 Excelente desenvolvimento físico.")
