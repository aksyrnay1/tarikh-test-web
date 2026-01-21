import streamlit as st
from docx import Document
import os

st.set_page_config(page_title="Тарих Платформасы", layout="centered")

# --- СТИЛЬДЕР (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    /* Сұрақ карточкасы */
    .question-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #4A90E2;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    /* Қате болғандағы стиль */
    .error-card {
        background-color: #fff5f5;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .correct-text { color: #28a745; font-weight: bold; margin-top: 10px; }
    .stRadio > div, .stCheckbox > div { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

def load_data(file_name):
    if not os.path.exists(file_name): return None
    doc = Document(file_name)
    data = {}; current_sec = "Тест"; q_text = None; options = []
    
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt: continue
        if "§" in txt:
            current_sec = txt; data[current_sec] = []
        elif txt[0].isdigit() and ("." in txt[:3] or ")" in txt[:3]):
            if q_text: data[current_sec].append({"q": q_text, "o": options, "a": options[0]})
            q_text = txt; options = []
        else:
            if q_text: options.append(txt)
    if q_text: data[current_sec].append({"q": q_text, "o": options, "a": options[0]})
    return data

def main():
    st.markdown("# 🏛 Дүниежүзі тарихы порталы")
    quiz = load_data("7 сынып джт.docx")

    if not quiz:
        st.error("Файл табылмады.")
        return

    topic = st.sidebar.selectbox("Тақырыпты таңдаңыз:", list(quiz.keys()))
    questions = quiz[topic]
    user_inputs = {}

    # Сұрақтарды көрсету
    for i, item in enumerate(questions):
        with st.container():
            st.markdown(f"### {item['q']}")
            
            # Егер нұсқалар 5-тен көп болса - Көпжауапты (Checkbox)
            if len(item['o']) > 5:
                user_inputs[i] = []
                for opt in item['o']:
                    if st.checkbox(opt, key=f"ch_{topic}_{i}_{opt}"):
                        user_inputs[i].append(opt)
            # Әйтпесе - Бір жауапты (Radio)
            else:
                user_inputs[i] = st.radio("", item['o'], key=f"r_{topic}_{i}", index=None, label_visibility="collapsed")
            st.write("---")

    if st.button("Нәтижені тексеру"):
        st.write("## 🔍 Тексеріс:")
        for i, item in enumerate(questions):
            # Бір жауапты тексеу
            if isinstance(user_inputs[i], str):
                is_correct = (user_inputs[i] == item['a'])
            # Көп жауапты тексеру (Біздің файлда бірінші тұрған жауап дұрыс деп есептейміз)
            else:
                is_correct = (item['a'] in user_inputs[i] and len(user_inputs[i]) >= 1)

            if is_correct:
                st.markdown(f"✅ **{item['q']}**")
            else:
                # ҚАТЕ КЕТКЕН ЖЕРДІ ҚЫЗЫЛМЕН БӨЛЕУ
                st.markdown(f"""
                <div class="error-card">
                    <p style="color: #d9534f; font-weight: bold;">❌ Сұрақ: {item['q']}</p>
                    <p style="color: #28a745; font-weight: bold;">Дұрыс жауап: {item['a']}</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
