#!/usr/bin/env python3
"""
Handwriting Practice Worksheet Generator - Web Application
Streamlit 기반 웹 애플리케이션
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import platform
from openai import OpenAI
import io
import base64

def get_api_key():
    """API 키 가져오기 (Secrets 또는 환경 변수)"""
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.getenv("OPENAI_API_KEY", "")

# 페이지 설정
st.set_page_config(
    page_title="📝 Handwriting Practice Worksheet Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CEFR 레벨 정의
CEFR_LEVELS = {
    "A1 (Beginner)": {
        "description": "초급 - 기본적인 일상 단어",
        "examples": "cat, dog, apple, red, one, two"
    },
    "A2 (Elementary)": {
        "description": "기초 - 간단한 일상 표현",
        "examples": "kitchen, bedroom, morning, afternoon, happy, sad"
    },
    "B1 (Intermediate)": {
        "description": "중급 - 일반적인 주제의 단어",
        "examples": "environment, education, technology, experience, develop"
    },
    "B2 (Upper Intermediate)": {
        "description": "중상급 - 추상적 개념과 복잡한 단어",
        "examples": "philosophy, sophisticated, comprehensive, analyze, perspective"
    },
    "C1 (Advanced)": {
        "description": "고급 - 전문적이고 정교한 단어",
        "examples": "articulate, intricate, phenomenon, methodology, substantial"
    },
    "C2 (Proficient)": {
        "description": "최고급 - 원어민 수준의 고급 어휘",
        "examples": "ubiquitous, quintessential, juxtaposition, serendipity, ephemeral"
    }
}

# 페이지 설정 (A4 크기: 210mm x 297mm = 2480px x 3508px at 300 DPI)
PAGE_WIDTH = 2480
PAGE_HEIGHT = 3508
MARGIN_TOP = 300
MARGIN_BOTTOM = 200
MARGIN_LEFT = 200
MARGIN_RIGHT = 200

# 12개 단어 기준 레이아웃
MAX_WORDS = 12
TITLE_HEIGHT = 250
CONTENT_START_Y = MARGIN_TOP + TITLE_HEIGHT

# 폰트 옵션 정의
FONT_OPTIONS = {
    "Arial": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/Arial.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/Arial Bold.ttf",
        ]
    },
    "Times New Roman": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
            "/Library/Fonts/Times New Roman.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/Times New Roman.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
            "/Library/Fonts/Times New Roman Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/timesbd.ttf",
            "C:/Windows/Fonts/Times New Roman Bold.ttf",
        ]
    },
    "Comic Sans MS": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Comic Sans MS.ttf",
            "/Library/Fonts/Comic Sans MS.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/comic.ttf",
            "C:/Windows/Fonts/Comic Sans MS.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf",
            "/Library/Fonts/Comic Sans MS Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/comicbd.ttf",
            "C:/Windows/Fonts/Comic Sans MS Bold.ttf",
        ]
    },
    "Helvetica": {
        "mac": [
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Helvetica.ttc",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/arial.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Helvetica.ttc",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/arialbd.ttf",
        ]
    },
    "Verdana": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Verdana.ttf",
            "/Library/Fonts/Verdana.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/verdana.ttf",
            "C:/Windows/Fonts/Verdana.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
            "/Library/Fonts/Verdana Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/verdanab.ttf",
            "C:/Windows/Fonts/Verdana Bold.ttf",
        ]
    },
    "Courier New": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Courier New.ttf",
            "/Library/Fonts/Courier New.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/cour.ttf",
            "C:/Windows/Fonts/Courier New.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
            "/Library/Fonts/Courier New Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/courbd.ttf",
            "C:/Windows/Fonts/Courier New Bold.ttf",
        ]
    },
    "Georgia": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/Library/Fonts/Georgia.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/georgia.ttf",
            "C:/Windows/Fonts/Georgia.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/Library/Fonts/Georgia Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/georgiab.ttf",
            "C:/Windows/Fonts/Georgia Bold.ttf",
        ]
    },
    "Trebuchet MS": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Trebuchet MS.ttf",
            "/Library/Fonts/Trebuchet MS.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/trebuc.ttf",
            "C:/Windows/Fonts/Trebuchet MS.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Trebuchet MS Bold.ttf",
            "/Library/Fonts/Trebuchet MS Bold.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/trebucbd.ttf",
            "C:/Windows/Fonts/Trebuchet MS Bold.ttf",
        ]
    },
    "Palatino": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Palatino.ttc",
            "/Library/Fonts/Palatino.ttc",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/pala.ttf",
            "C:/Windows/Fonts/Palatino.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Palatino.ttc",
            "/Library/Fonts/Palatino.ttc",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/palab.ttf",
            "C:/Windows/Fonts/Palatino Bold.ttf",
        ]
    },
    "Impact": {
        "mac": [
            "/System/Library/Fonts/Supplemental/Impact.ttf",
            "/Library/Fonts/Impact.ttf",
        ],
        "linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        "windows": [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/Impact.ttf",
        ],
        "bold_mac": [
            "/System/Library/Fonts/Supplemental/Impact.ttf",
            "/Library/Fonts/Impact.ttf",
        ],
        "bold_linux": [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "bold_windows": [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/Impact.ttf",
        ]
    }
}

def load_font(font_name, size, bold=False):
    """폰트 로드"""
    system = platform.system()
    
    font_config = FONT_OPTIONS.get(font_name, FONT_OPTIONS["Arial"])
    
    if system == "Darwin":  # macOS
        font_paths = font_config["bold_mac"] if bold else font_config["mac"]
    elif system == "Windows":
        font_paths = font_config["bold_windows"] if bold else font_config["windows"]
    else:  # Linux
        font_paths = font_config["bold_linux"] if bold else font_config["linux"]
    
    # 폰트 로드 시도
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                if font_path.endswith('.ttc'):
                    font = ImageFont.truetype(font_path, size, index=1 if bold else 0)
                else:
                    font = ImageFont.truetype(font_path, size)
                return font
        except Exception as e:
            continue
    
    # 폰트 로드 실패 시 기본 폰트 사용
    return ImageFont.load_default()

def calculate_layout(num_words):
    """단어 개수에 따른 레이아웃 계산 (12개 기준)"""
    available_height = PAGE_HEIGHT - CONTENT_START_Y - MARGIN_BOTTOM
    
    # 12개 기준 단어당 높이
    word_height_12 = available_height / MAX_WORDS
    
    # 실제 단어 간격 (12개 기준 크기 유지)
    word_spacing = available_height / num_words
    
    return {
        'word_height': word_height_12,  # 12개 기준 고정
        'word_spacing': word_spacing,   # 실제 간격
        'line_height': word_height_12 * 0.6,  # 보조선 높이
        'font_size': int(word_height_12 * 0.35),  # 글자 크기
    }

def generate_words_with_ai(topic, num_words=12, cefr_level="A1 (Beginner)"):
    """OpenAI API를 사용하여 주제에 맞는 단어 생성"""
    # API 키 확인
    api_key = get_api_key()
    if not api_key:
        st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. 사이드바에서 설정해주세요.")
        return []
    
    try:
        client = OpenAI(api_key=api_key)
        
        level_info = CEFR_LEVELS.get(cefr_level, CEFR_LEVELS["A1 (Beginner)"])
        level_description = level_info["description"]
        level_examples = level_info["examples"]
        
        prompt = f"""Generate {num_words} English words related to the topic "{topic}" for handwriting practice.

CEFR Level: {cefr_level}
Level Description: {level_description}
Example words for this level: {level_examples}

Requirements:
- All words must be appropriate for {cefr_level} level
- Words should match the difficulty of the CEFR level
- Return only the words, one per line, without numbers or bullets
- Each word should be a single word (not phrases)

Example format:
Apple
Banana
Orange"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that generates educational words for handwriting practice. You must generate words appropriate for {cefr_level} level according to CEFR standards."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        words_text = response.choices[0].message.content.strip()
        words = [word.strip() for word in words_text.split('\n') if word.strip()]
        
        return words[:num_words]
    except Exception as e:
        st.error(f"AI 단어 생성 실패: {str(e)}")
        return []

def create_worksheet(topic, words, font_name="Arial"):
    """워크시트 생성"""
    # 이미지 생성
    img = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), 'white')
    draw = ImageDraw.Draw(img)
    
    # 폰트 로드
    title_font = load_font(font_name, 120, bold=True)
    word_font = load_font(font_name, 80, bold=False)
    
    # 레이아웃 계산
    layout = calculate_layout(len(words))
    
    # 제목 그리기
    title = f"{topic.title()} Handwriting Practice"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (PAGE_WIDTH - title_width) / 2
    draw.text((title_x, MARGIN_TOP), title, fill='black', font=title_font)
    
    # 각 단어별 보조선과 텍스트 그리기
    for i, word in enumerate(words):
        # Y 위치 계산
        y_pos = CONTENT_START_Y + (i * layout['word_spacing'])
        
        # 보조선 4개 그리기
        line_height = layout['line_height']
        
        # 상단 검정 실선
        draw.line([(MARGIN_LEFT, y_pos), 
                   (PAGE_WIDTH - MARGIN_RIGHT, y_pos)], 
                  fill='black', width=3)
        
        # 중간 청록색 점선 (2개)
        middle1_y = y_pos + line_height * 0.33
        middle2_y = y_pos + line_height * 0.67
        
        for x in range(MARGIN_LEFT, PAGE_WIDTH - MARGIN_RIGHT, 40):
            draw.line([(x, middle1_y), (x + 20, middle1_y)], 
                     fill='#00BFFF', width=2)
            draw.line([(x, middle2_y), (x + 20, middle2_y)], 
                     fill='#00BFFF', width=2)
        
        # 하단 검정 실선
        bottom_y = y_pos + line_height
        draw.line([(MARGIN_LEFT, bottom_y), 
                   (PAGE_WIDTH - MARGIN_RIGHT, bottom_y)], 
                  fill='black', width=3)
        
        # 단어 그리기 (보조선 안에 위치)
        word_y = y_pos + (line_height * 0.15)  # 약간 위에서 시작
        draw.text((MARGIN_LEFT + 50, word_y), word, fill='black', font=word_font)
    
    return img

# 메인 UI
def main():
    st.title("📝 Handwriting Practice Worksheet Generator")
    st.markdown("주제를 입력하면 자동으로 따라쓰기 학습지를 생성합니다.")
    
    # 사이드바 - 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # API 키 확인 및 경고
        api_key = get_api_key()
        if not api_key:
            st.warning("⚠️ OpenAI API 키가 설정되지 않았습니다.")
            st.info("""
            **설정 방법:**
            1. 로컬: `.streamlit/secrets.toml` 파일 생성
            2. Streamlit Cloud: Settings > Secrets에 추가
            
            예시:
            ```toml
            OPENAI_API_KEY = "sk-..."
            ```
            """)
        
        use_ai = st.checkbox("AI로 단어 자동 생성 (OpenAI)", value=True)
        
        font_name = st.selectbox(
            "폰트",
            options=list(FONT_OPTIONS.keys()),
            index=0
        )
        
        cefr_level = st.selectbox(
            "CEFR 레벨",
            options=list(CEFR_LEVELS.keys()),
            index=0
        )
        
        if cefr_level in CEFR_LEVELS:
            st.caption(CEFR_LEVELS[cefr_level]["description"])
    
    # 메인 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("주제 입력")
        topic = st.text_input(
            "주제를 입력하세요",
            placeholder="예: animals, fruits, school 등",
            label_visibility="collapsed"
        )
        
        if use_ai:
            if st.button("🔍 단어 생성", type="primary", use_container_width=True):
                if not topic:
                    st.error("주제를 입력해주세요.")
                else:
                    with st.spinner("AI로 단어 생성 중..."):
                        words = generate_words_with_ai(topic, MAX_WORDS, cefr_level)
                        if words:
                            st.session_state['generated_words'] = words
                            st.success(f"✅ {len(words)}개 단어가 생성되었습니다!")
                        else:
                            st.error("단어 생성에 실패했습니다.")
            
            # 생성된 단어 미리보기
            if 'generated_words' in st.session_state and st.session_state['generated_words']:
                st.subheader("생성된 단어 미리보기")
                words = st.session_state['generated_words']
                words_text = "\n".join([f"{i+1}. {word}" for i, word in enumerate(words)])
                st.text_area("", words_text, height=200, disabled=True, label_visibility="collapsed")
        else:
            st.subheader("커스텀 단어 입력")
            custom_words = st.text_area(
                "단어를 쉼표로 구분하여 입력하세요",
                placeholder="예: Apple, Banana, Orange, Grape",
                height=100
            )
            
            if custom_words:
                words = [w.strip() for w in custom_words.split(',') if w.strip()]
                st.session_state['custom_words'] = words
    
    with col2:
        st.subheader("워크시트 생성")
        
        # 단어 확인
        if use_ai:
            words = st.session_state.get('generated_words', [])
        else:
            words = st.session_state.get('custom_words', [])
        
        if not words:
            st.info("먼저 단어를 생성하거나 입력해주세요.")
        else:
            if len(words) > MAX_WORDS:
                st.warning(f"⚠️ 단어가 {len(words)}개로 최대 {MAX_WORDS}개를 초과합니다. 처음 {MAX_WORDS}개만 사용됩니다.")
                words = words[:MAX_WORDS]
            
            if st.button("📄 워크시트 생성", type="primary", use_container_width=True):
                if not topic:
                    st.error("주제를 입력해주세요.")
                else:
                    with st.spinner("워크시트 생성 중..."):
                        try:
                            img = create_worksheet(topic, words, font_name)
                            
                            # 이미지를 바이트로 변환
                            img_buffer = io.BytesIO()
                            img.save(img_buffer, format='JPEG', quality=95)
                            img_buffer.seek(0)
                            
                            # 다운로드 버튼
                            st.download_button(
                                label="📥 워크시트 다운로드",
                                data=img_buffer,
                                file_name=f"{topic.replace(' ', '_')}_worksheet.jpg",
                                mime="image/jpeg",
                                use_container_width=True
                            )
                            
                            # 미리보기 표시
                            st.image(img, caption=f"{topic.title()} Handwriting Practice", use_container_width=True)
                            
                        except Exception as e:
                            st.error(f"워크시트 생성 실패: {str(e)}")

if __name__ == "__main__":
    main()
