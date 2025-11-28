# GitHub 저장소 설정 가이드

## 1단계: GitHub에서 새 저장소 생성

1. https://github.com/new 접속
2. Repository name 입력 (예: `worksheet-generator`)
3. Description 입력 (선택사항)
4. **Public** 선택 (Streamlit Cloud는 Public 저장소만 지원)
5. **"Initialize this repository with a README" 체크 해제**
6. "Create repository" 클릭

## 2단계: 로컬 저장소와 GitHub 연결

터미널에서 다음 명령어 실행:

```bash
cd /Users/im_1511/Desktop/Worksheet_Generator_Complete

# GitHub 저장소 URL을 YOUR_USERNAME과 YOUR_REPO_NAME으로 변경
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 브랜치 이름을 main으로 설정
git branch -M main

# 코드 푸시
git push -u origin main
```

## 3단계: Streamlit Cloud에 배포

1. https://streamlit.io/cloud 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 다음 정보 입력:
   - **Repository**: 방금 만든 저장소 선택
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. "Deploy" 클릭

## 빠른 명령어 (한 번에 실행)

```bash
# GitHub 저장소 URL을 알려주시면 아래 명령어를 수정해드리겠습니다
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## 주의사항

⚠️ **중요**: OpenAI API 키가 코드에 하드코딩되어 있습니다. 
배포 전에 환경 변수로 변경하는 것을 권장합니다:

1. `.streamlit/secrets.toml` 파일 생성 (로컬 테스트용):
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

2. `app.py` 수정:
   ```python
   OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "default-key-if-not-set")
   ```

3. Streamlit Cloud의 Settings > Secrets에 추가:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

## 현재 커밋된 파일

✅ `app.py` - 메인 애플리케이션
✅ `requirements.txt` - 패키지 의존성
✅ `.streamlit/config.toml` - Streamlit 설정
✅ `DEPLOYMENT.md` - 배포 가이드
✅ `Procfile` - Heroku 배포용
✅ `railway.json` - Railway 배포용
✅ `Dockerfile` - Docker 배포용
✅ `.gitignore` - Git 제외 파일

## 다음 단계

1. GitHub에서 저장소 생성
2. 저장소 URL을 알려주시면 연결 명령어를 제공해드리겠습니다
3. 또는 위의 명령어를 직접 실행하세요

