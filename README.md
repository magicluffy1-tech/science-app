# 🔬 과학 질문 유목화 도구 (Science Question Categorizer)

이 애플리케이션은 학생들이 과학 시간에 생긴 질문을 스마트폰으로 쉽게 등록하고, 교사가 AI(Gemini)를 활용해 등록된 질문들을 핵심 주제로 분류(유목화)할 수 있도록 돕는 Streamlit 앱입니다.

## 파일 구성
- `streamlit_app.py`: Streamlit 화면 구성 및 메인 로직 (학생/교사 뷰 제공)
- `database.py`: SQLite 데이터베이스 연결 및 질문 데이터 저장/호출 로직
- `requirements.txt`: 앱 실행에 필요한 파이썬 패키지 목록
- `science_questions.db`: 질문이 저장되는 로컬 데이터베이스 파일 (앱 실행 시 자동 생성)

## 로컬에서 실행하는 방법
1. 터미널(명령 프롬프트)을 열고 `science` 폴더로 이동합니다.
2. 필요한 패키지를 설치합니다: `pip install -r requirements.txt`
3. 앱을 실행합니다: `streamlit run streamlit_app.py`

## 🚀 GitHub 및 Streamlit Community Cloud 배포 방법
이 앱을 학생들이 자신의 휴대폰으로 접속할 수 있도록 하려면 배포가 필요합니다.

### 1단계: GitHub 저장소(Repository)에 코드 올리기
1. [GitHub](https://github.com/)에 로그인하고 `science`라는 이름으로 새로운 Repository를 생성합니다.
2. 현재 제작된 코드(`streamlit_app.py`, `database.py`, `requirements.txt`)를 해당 Repository에 업로드(Commit & Push)합니다. (`science_questions.db` 파일은 업로드하지 않아도 됩니다.)

### 2단계: Streamlit Community Cloud에 배포하기
1. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 로그인합니다.
2. 우측 상단의 **"New app"** 버튼을 클릭합니다.
3. 배포할 앱의 정보를 입력합니다.
   - **Repository**: 방금 만든 `science` 저장소 선택
   - **Branch**: `main` (또는 `master`) 선택
   - **Main file path**: `streamlit_app.py` 입력
4. **"Deploy!"** 버튼을 클릭합니다.
5. 배포가 완료되면 생성된 고유의 URL(링크)가 부여됩니다!

### 3단계: 학생들에게 접속 안내
- Streamlit 배포로 얻은 **URL 주소** 또는 이를 변환한 **QR 코드**를 학생들에게 제공합니다!
- 선생님은 교사 설정 탭에서 본인의 Gemini API 키를 입력하면 AI 유목화 기능을 사용할 수 있습니다.
