# 📝 Handwriting Practice Worksheet Generator

AI 기반 영어 따라쓰기 학습지 자동 생성 웹 애플리케이션

## ✨ 주요 기능

- 🤖 **AI 단어 생성**: OpenAI를 사용하여 주제에 맞는 단어 자동 생성
- 📊 **CEFR 레벨 지원**: A1부터 C2까지 6단계 영어 수준 선택
- 🎨 **10가지 폰트**: Arial, Times New Roman, Comic Sans MS 등
- 📝 **커스텀 단어**: 직접 단어 입력 가능
- 📥 **즉시 다운로드**: 생성된 워크시트를 바로 다운로드

## 🚀 빠른 시작

### 로컬 실행

```bash
# 패키지 설치
pip install -r requirements.txt

# 애플리케이션 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하세요.

### 웹 배포 (Streamlit Cloud)

1. GitHub에 코드 푸시
2. https://streamlit.io/cloud 접속
3. GitHub 계정으로 로그인
4. "New app" 클릭
5. Repository 선택 후 `app.py` 지정
6. "Deploy" 클릭

## 📋 사용 방법

1. **주제 입력**: 예) "animals", "fruits", "school"
2. **단어 생성**: "단어 생성" 버튼 클릭 (AI 사용 시)
3. **설정 조정**: 사이드바에서 폰트와 CEFR 레벨 선택
4. **워크시트 생성**: "워크시트 생성" 버튼 클릭
5. **다운로드**: 생성된 워크시트 다운로드

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: OpenAI GPT-3.5-turbo
- **Image Processing**: Pillow (PIL)

## 📦 필요한 패키지

- streamlit >= 1.28.0
- Pillow >= 10.0.0
- openai >= 1.0.0

## 🔧 환경 변수

OpenAI API 키를 환경 변수로 설정:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

또는 Streamlit Secrets 사용:
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-api-key-here"
```

## 📄 라이선스

이 프로젝트는 자유롭게 사용 가능합니다.

## 🤝 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.
