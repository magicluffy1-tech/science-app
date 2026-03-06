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
        question_text = st.text_area("궁금한 점을 자세히 적어주세요")
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
    st.subheader("📝 등록된 질문 목록")
    
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
    
    questions = database.get_all_questions()
    
    if not questions:
        st.info("아직 등록된 질문이 없습니다.")
    else:
        df_teacher = pd.DataFrame(questions)
        st.write(f"**총 {len(questions)}개의 질문이 등록되었습니다.**")
        
        # Display raw questions
        with st.expander("원본 질문 목록 보기"):
            st.dataframe(df_teacher[['student_name', 'question_text']], use_container_width=True, hide_index=True)
            
        st.divider()
        
        if st.session_state.api_key:
            if st.button("✨ AI로 질문 유목화하기", type="primary"):
                with st.spinner("AI가 질문을 분류하고 있습니다. 잠시만 기다려주세요..."):
                    try:
                        # Prepare prompt
                        question_list_str = "\n".join([f"- {q['question_text']}" for q in questions])
                        prompt = f"""
                        다음은 중학생들이 과학 수업 시간에 작성한 질문들입니다. 
                        이 질문들을 내용이 비슷한 것끼리 3~5개의 핵심 주제로 분류(유목화)해주세요.
                        각 주제별로 어떤 질문들이 포함되는지 요약해서 보여주세요.
                        출력 형식은 마크다운을 사용해서 깔끔하게 정리해주세요.

                        [질문 목록]
                        {question_list_str}
                        """
                        
                        # Call Gemini API
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        response = model.generate_content(prompt)
                        
                        st.subheader("분류 결과")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"AI 분류 중 오류가 발생했습니다: {e}")
        else:
            st.warning("왼쪽 사이드바에서 Gemini API 키를 입력해야 AI 유목화 기능을 사용할 수 있습니다.")
            
        st.divider()
        if st.button("🗑️ 모든 질문 삭제 (초기화)"):
            database.delete_all_questions()
            st.success("모든 질문이 삭제되었습니다. 페이지를 새로고침하면 반영됩니다.")
            st.rerun()
