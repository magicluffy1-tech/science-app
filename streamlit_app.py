import streamlit as st
import pandas as pd
import google.generativeai as genai
import database

# Initialize database
database.init_db()

st.set_page_config(page_title="과학 질문 방", page_icon="🔬", layout="wide")

st.title("🔬 과학 질문 유목화 도구")

# API Key handling
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# Sidebar for Teacher Settings
with st.sidebar:
    st.header("⚙️ 교사 설정")
    api_key_input = st.text_input("Gemini API 키 입력 (Teacher Only):", type="password", value=st.session_state.api_key)
    if api_key_input:
        st.session_state.api_key = api_key_input
        genai.configure(api_key=api_key_input)
    
    st.caption("AI 기반 유목화 기능을 사용하려면 API 키가 필요합니다.")

# Tabs for Student and Teacher
tab1, tab2 = st.tabs(["🎓 학생 질문 입력", "👨‍🏫 교사 질문 확인 및 유목화"])

# ---- TAB 1: Student View ----
with tab1:
    st.header("질문을 남겨주세요!")
    
    with st.form("question_form", clear_on_submit=True):
        student_name = st.text_input("이름 (또는 모둠명)")
        question_text = st.text_area("궁금한 점을 자세히 적어주세요", placeholder="ex) 밀도로 물질을 구별할 때, 온도가 달라지면 밀도도 바뀌니까 항상 똑같이 맞춰놓고 비교해야 하나요?")
        submit_button = st.form_submit_button("질문 등록하기")
        
        if submit_button:
            if student_name.strip() and question_text.strip():
                if database.add_question(student_name, question_text):
                    st.success("질문이 성공적으로 등록되었습니다!")
                else:
                    st.error("질문 등록에 실패했습니다. 다시 시도해주세요.")
            else:
                st.warning("이름과 질문을 모두 입력해주세요.")
                
    st.divider()
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("📝 등록된 질문 목록")
    with col2:
        if st.button("🔄 새로고침", key="student_refresh"):
            st.cache_data.clear()
            st.rerun()
            
    questions = database.get_all_questions()
    if questions:
        df = pd.DataFrame(questions)
        df = df[['timestamp', 'student_name', 'question_text']] # Reorder columns
        df.columns = ['등록 시간', '이름', '질문 내용']
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("아직 등록된 질문이 없습니다.")

# ---- TAB 2: Teacher View ----
with tab2:
    st.header("학생 질문 유목화 (AI 분류)")
    
    col_t1, col_t2 = st.columns([4, 1])
    with col_t1:
        st.write("학생들이 등록한 질문을 AI가 핵심 주제별로 분류합니다.")
    with col_t2:
        if st.button("🔄 새로고침", key="teacher_refresh"):
            st.cache_data.clear()
            st.rerun()
            
    questions = database.get_all_questions()
    
    if not questions:
        st.info("아직 등록된 질문이 없습니다.")
    else:
        st.write(f"**총 {len(questions)}개의 질문이 대기 중입니다.**")
        st.divider()
        
        # 1. AI Categorization Section (Moved to the top)
        if st.session_state.api_key:
            if st.button("✨ AI로 질문 유목화하기", type="primary", use_container_width=True):
                with st.spinner("AI가 질문을 분석하고 주제별로 분류하고 있습니다..."):
                    try:
                        # Prepare prompt (Now includes student names and explicit formatting instructions)
                        question_list_str = "\n".join([f"- [{q['student_name']}] {q['question_text']}" for q in questions])
                        prompt = f"""
                        다음은 중학교 과학 수업 시간에 학생들이 작성한 질문들입니다. 
                        이 질문들을 내용이 비슷한 것끼리 3~5개의 **핵심 주제**로 분류해 주세요.
                        또한, 학생들은 일상적인 언어로 질문하는 경향이 있으므로, 학생의 '원래 질문'을 보여준 뒤 이를 정확한 과학적 용어를 사용한 '과학적 질문'으로 변환하여 함께 제시해 주세요.

                        답변은 반드시 아래의 마크다운 형식을 엄격하게 지켜서 작성해 주세요:

                        ---
                        ### 📌 [주제명 1]
                        **주제 요약**: 이 주제에 포함된 질문들의 공통적인 의도나 핵심 내용을 1~2줄로 요약해 주세요.

                        **🙋‍♂️ 학생들의 질문:**
                        - **[학생이름]**: (원래 질문) 
                          💡 **과학적 질문**: (과학적 용어로 다듬어진 질문)
                        - **[학생이름]**: (원래 질문) 
                          💡 **과학적 질문**: (과학적 용어로 다듬어진 질문)

                        ---
                        ### 📌 [주제명 2]
                        **주제 요약**: ... (위와 동일한 형식)

                        **🙋‍♂️ 학생들의 질문:**
                        - **[학생이름]**: (원래 질문) 
                          💡 **과학적 질문**: (과학적 용어로 다듬어진 질문)
                        ...

                        [학생들의 질문 목록]
                        {question_list_str}
                        """
                        
                        # Call Gemini API
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content(prompt)
                        
                        st.subheader("✨ 분류 결과")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"AI 분류 중 오류가 발생했습니다: {e}")
        else:
            st.warning("👈 왼쪽 사이드바에서 Gemini API 키를 입력해야 AI 유목화 기능을 사용할 수 있습니다.")
            
        st.divider()

        # 2. Raw Data Section (Moved to the bottom inside an expander)
        df_teacher = pd.DataFrame(questions)
        with st.expander("📊 원본 질문 데이터 전체 보기 (클릭하여 펼치기)"):
            st.dataframe(df_teacher[['student_name', 'question_text', 'timestamp']], use_container_width=True, hide_index=True)
            
        st.divider()
        if st.button("🗑️ 모든 질문 삭제 (초기화)"):
            database.delete_all_questions()
            st.success("모든 질문이 삭제되었습니다. 페이지를 새로고침하면 반영됩니다.")
            st.rerun()
