import streamlit as st
from docx import Document
import os

st.set_page_config(page_title="Тарих Тест Платформасы", layout="wide")

# Word файлын оқу функциясы
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    
    doc = Document(file_path)
    quiz = {}
    current_topic = "Жалпы сұрақтар"
    
    temp_q = None
    temp_options = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text: continue
        
        # Тақырыпты анықтау (Егер § белгісі болса)
        if "§" in text:
            current_topic = text
            quiz[current_topic] = []
        
        # Сұрақты анықтау (Егер соңында "?" болса немесе санмен басталса)
        elif "?" in text or (text[0].isdigit() and "." in text[:3]):
            if temp_q:
                quiz[current_topic].append({"q": temp_q, "options": temp_options, "a": temp_options[0]})
            temp_q = text
            temp_options = []
        
        # Жауап нұсқалары (Сұрақтан кейінгі мәтіндер)
        else:
            if temp_q:
                temp_options.append(text)
                
    # Соңғы сұрақты қосу
    if temp_q:
        quiz[current_topic].append({"q": temp_q, "options": temp_options, "a": temp_options[0]})
        
    return quiz

# Файлды жүктеу
data = load_data("7 сынып джт.docx") # Файл аты осылай болуы керек

st.title("📚 Дүниежүзі тарихы: Интерактивті тест")

if data:
    topic = st.sidebar.selectbox("Тақырыпты таңдаңыз:", list(data.keys()))
    questions = data[topic]
    
    st.header(f"📍 {topic}")
    
    with st.form("quiz_form"):
        user_answers = {}
        for i, item in enumerate(questions):
            st.markdown(f"### {item['q']}")
            # Нұсқаларды араластырмай шығару
            user_answers[i] = st.radio("Жауапты таңдаңыз:", item['options'], key=f"q_{i}")
            st.write("---")
        
        submit = st.form_submit_button("Нәтижені тексеру")

    if submit:
        score = 0
        st.subheader("📝 Тексеру нәтижесі:")
        
        for i, item in enumerate(questions):
            if user_answers[i] == item['a']:
                score += 1
                st.success(f"✅ Сұрақ №{i+1}: Дұрыс!")
            else:
                # ҚАТЕ КЕТКЕН СҰРАҚТЫ ҚЫЗЫЛМЕН КӨРСЕТУ
                st.error(f"❌ Сұрақ №{i+1}: ҚАТЕ!")
                st.markdown(f"**Сұрақ:** {item['q']}")
                st.markdown(f"**Сіздің жауабыңыз:** :red[{user_answers[i]}]")
                st.markdown(f"**Дұрыс жауап:** :green[{item['a']}]")
                st.write("---")
        
        st.sidebar.metric("Жалпы балл", f"{score}/{len(questions)}")
else:
    st.error("Файл табылмады! '7 сынып джт.docx' файлын GitHub-қа жүктеңіз.")
