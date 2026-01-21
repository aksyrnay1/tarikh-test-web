import streamlit as st
from docx import Document
import os

st.set_page_config(page_title="Тарих Тест Порталы", layout="centered")

# --- ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .error-box {
        background-color: #ffebeb;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #ff4b4b;
        margin-bottom: 15px;
    }
    .correct-ans { color: #28a745; font-weight: bold; }
    .q-title { font-size: 18px; font-weight: 600; color: #1e3a8a; }
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
            if q_text:
                # Файлда бірінші тұрған жауапты дұрыс деп аламыз
                data[current_sec].append({"q": q_text, "o": options, "a": options[0] if options else ""})
            q_text = txt; options = []
        else:
            if q_text: options.append(txt)
            
    if q_text:
        data[current_sec].append({"q": q_text, "o": options, "a": options[0] if options else ""})
    return data

def main():
    st.markdown("# 🏛 Дүниежүзі тарихы: Онлайн тест")
    
    # Файл атын тексеріңіз: "7 сынып джт.docx"
    file_name = "7 сынып джт.docx"
    quiz = load_data(file_name)

    if not quiz:
        st.error(f"❌ '{file_name}' файлы табылмады. Оны GitHub-қа жүктеңіз.")
        return

    topic = st.sidebar.selectbox("📚 Тақырып таңдаңыз:", list(quiz.keys()))
    questions = quiz[topic]
    user_inputs = {}

    # СҰРАҚТАРДЫ ШЫҒАРУ
    for i, item in enumerate(questions):
        st.markdown(f"<p class='q-title'>{item['q']}</p>", unsafe_allow_html=True)
        
        # Көпжауапты (нұсқалар 5-тен көп болса)
        if len(item['o']) > 5:
            user_inputs[i] = []
            for opt in item['o']:
                if st.checkbox(opt, key=f"ch_{i}_{opt}"):
                    user_inputs[i].append(opt)
        # Бір жауапты (Radio)
        else:
            user_inputs[i] = st.radio("Жауапты таңдаңыз:", item['o'], key=f"r_{i}", index=None, label_visibility="collapsed")
        st.write("---")

    if st.button("🏁 ТЕСТТІ АЯҚТАУ"):
        st.write("### 🔍 Нәтижелер:")
        score = 0
        
        for i, item in enumerate(questions):
            ans = user_inputs[i]
            # Тексеру логикасы
            if isinstance(ans, list): # Checkbox болса
                is_correct = (item['a'] in ans) if ans else False
            else: # Radio болса
                is_correct = (ans == item['a'])

            if is_correct:
                st.success(f"✅ Сұрақ №{i+1}: Дұрыс!")
                score += 1
            else:
                # ҚАТЕ КЕТКЕН СҰРАҚТЫ ҚЫЗЫЛМЕН ШЫҒАРУ
                st.markdown(f"""
                <div class="error-box">
                    <p style="color: #ff4b4b; font-weight: bold; margin-bottom: 5px;">❌ Сұрақ №{i+1} ҚАТЕ!</p>
                    <p><b>Сұрақ:</b> {item['q']}</p>
                    <p><b>Сіздің жауабыңыз:</b> <span style="color: #ff4b4b;">{ans if ans else 'Белгіленбеген'}</span></p>
                    <p><b>Дұрыс жауап:</b> <span class="correct-ans">{item['a']}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        st.sidebar.metric("Ұпайыңыз", f"{score} / {len(questions)}")

if __name__ == "__main__":
    main()
