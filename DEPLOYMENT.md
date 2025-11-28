# 웹 애플리케이션 배포 가이드

## 로컬 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 자동 열립니다.

## 클라우드 배포

### Streamlit Cloud (추천 - 무료)

1. **GitHub에 코드 업로드**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Streamlit Cloud에 배포**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인
   - "New app" 클릭
   - Repository 선택
   - Main file path: `app.py`
   - "Deploy" 클릭

3. **완료!**
   - 자동으로 배포되고 공개 URL이 생성됩니다
   - 예: `https://your-app-name.streamlit.app`

### Heroku 배포

1. **Procfile 생성**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Heroku 배포**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Railway 배포

1. **railway.json 생성**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "streamlit run app.py --server.port $PORT --server.address 0.0.0.0",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

2. Railway에서 GitHub 연동 후 자동 배포

### Docker 배포

1. **Dockerfile 생성**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **빌드 및 실행**
   ```bash
   docker build -t worksheet-generator .
   docker run -p 8501:8501 worksheet-generator
   ```

## 환경 변수 설정

OpenAI API 키를 환경 변수로 설정하려면:

1. **로컬**: `.streamlit/secrets.toml` 파일 생성
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

2. **Streamlit Cloud**: Settings > Secrets에 추가
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

3. **코드 수정**: `app.py`에서
   ```python
   OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "default-key")
   ```

## 주의사항

- OpenAI API 키는 절대 공개 저장소에 커밋하지 마세요
- Streamlit Cloud는 무료 플랜에서 제한이 있을 수 있습니다
- 대용량 트래픽이 예상되면 유료 플랜 고려

