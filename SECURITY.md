# 🔒 보안 가이드

## API 키 보안 설정

OpenAI API 키는 절대 코드에 하드코딩하지 마세요!

## 로컬 개발 환경 설정

### 방법 1: Streamlit Secrets 사용 (권장)

1. `.streamlit/secrets.toml` 파일 생성:
   ```bash
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. `secrets.toml` 파일 편집:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```

3. `.gitignore`에 이미 포함되어 있어 Git에 커밋되지 않습니다.

### 방법 2: 환경 변수 사용

```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
streamlit run app.py
```

## Streamlit Cloud 배포 시 설정

1. Streamlit Cloud 대시보드 접속
2. 앱 선택
3. "Settings" > "Secrets" 클릭
4. 다음 내용 추가:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```
5. "Save" 클릭

## 확인 사항

✅ API 키가 코드에 하드코딩되어 있지 않은지 확인
✅ `.streamlit/secrets.toml`이 `.gitignore`에 포함되어 있는지 확인
✅ GitHub에 푸시하기 전에 코드 검토

## 주의사항

⚠️ **절대 하지 말아야 할 것:**
- API 키를 코드에 직접 작성
- API 키를 GitHub에 커밋
- API 키를 공개 채팅이나 포럼에 공유

✅ **해야 할 것:**
- Streamlit Secrets 사용
- 환경 변수 사용
- `.gitignore`에 secrets 파일 추가 확인

