"""AI Intelligence Engine for YouTube Knowledge Extraction.

Handles interactions with Google Generative AI (Gemini) SDK, providing
single-video executive briefings and deep multi-video sectional synthesis.
Features a resilient Multi-Model Fallback Chain (gemini-2.5-flash -> gemini-2.5-flash-lite -> gemini-flash-latest)
with automatic retry on 503 UNAVAILABLE / 429 spikes.
"""

import os
import time
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Automatically load local .env if available
load_dotenv()

# Priority fallback models supported by Google GenAI v2
FALLBACK_MODELS: List[str] = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest"
]


def get_active_gemini_api_key(explicit_key: Optional[str] = None) -> str:
    """Resolve Gemini API key in order of priority:
    1. Explicit key passed from UI session state
    2. Streamlit Cloud Secrets (st.secrets["GEMINI_API_KEY"])
    3. Environment variable (.env or OS: GEMINI_API_KEY / GOOGLE_API_KEY)

    Returns:
        Resolved API key string or empty string if not configured.
    """
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()

    # Try Streamlit secrets if running inside Streamlit
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            sec_key = st.secrets["GEMINI_API_KEY"]
            if sec_key and str(sec_key).strip():
                return str(sec_key).strip()
    except Exception:
        pass

    # Try environment variables
    env_key = os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("GOOGLE_API_KEY", "").strip()
    return env_key


def is_gemini_configured(api_key: Optional[str] = None) -> bool:
    """Check if a valid Gemini API key is available."""
    key = get_active_gemini_api_key(api_key)
    return bool(key and len(key) >= 20)


def _call_gemini_with_resilience(client: Any, prompt: str) -> Optional[str]:
    """Execute Gemini prompt across candidate models with automatic retry on 503/429 spikes.

    Args:
        client: google.genai.Client instance.
        prompt: User/system prompt string.

    Returns:
        Generated text or None if all models failed.
    """
    last_error: Optional[str] = None

    for model_name in FALLBACK_MODELS:
        for attempt in range(2):  # Try up to 2 attempts per model
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as err:
                err_str = str(err)
                last_error = err_str
                # If high-demand spike (503) or rate limit (429), back off and retry
                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                    time.sleep(1.2)
                    continue
                else:
                    # Model not supported or permanent error, skip to next candidate model
                    break

    return None


def generate_executive_briefing(
    title: str,
    channel: str,
    transcript: str,
    api_key: Optional[str] = None
) -> str:
    """Generate a high-density, professional executive brief for a single video.
    Uses multi-model fallback chain to ensure high availability even under Google cloud spikes.

    Args:
        title: Video title.
        channel: Channel/uploader name.
        transcript: Full or partial text transcript.
        api_key: Optional explicit Gemini API key.

    Returns:
        Markdown-formatted executive brief with core thesis, key insights, and recommendations.
    """
    key = get_active_gemini_api_key(api_key)
    if not key:
        return ""

    try:
        from google import genai
        client = genai.Client(api_key=key)

        prompt = (
            f"You are a Senior Technology Intelligence Analyst and Technical Architecture Expert. "
            f"Analyze the following video content/transcript and generate a structured executive brief in professional Korean.\n\n"
            f"**Video Title:** {title}\n"
            f"**Channel/Uploader:** {channel}\n\n"
            f"**Transcript / Context:**\n{transcript[:8000]}\n\n"
            "Format the output strictly as follows in Korean:\n"
            "### 🎯 핵심 어젠다 및 총평 (Executive Overview)\n"
            "(2~3 paragraphs explaining the core thesis, significance, and context)\n\n"
            "### 💡 핵심 기술 인사이트 & 논점 (Key Technical Insights)\n"
            "(Detailed bullet points with bold headings, citing specific models, frameworks, and benchmarks)\n\n"
            "### 🛠️ 실무 적용 포인트 (Actionable Recommendations)\n"
            "(Practical takeaways and adoption steps for architects and developers)"
        )

        output = _call_gemini_with_resilience(client, prompt)
        if output:
            return output
    except Exception as err:
        return f"> ⚠️ AI Briefing Generation Error: {str(err)}"

    # Graceful fallback brief if all AI models are temporarily busy
    fallback_paras = [p.strip() for p in transcript.split("\n\n") if len(p.strip()) > 30]
    excerpt = " ".join(fallback_paras[:3])[:300] if fallback_paras else transcript[:300]
    return (
        "### 🎯 핵심 어젠다 (Local Fallback Summary)\n"
        f"본 영상은 **{channel}** 채널의 **{title}**에 관한 자료입니다. "
        "일시적인 AI 모델 서버 과부하로 인해 로컬 고밀도 다이제스트로 생성되었습니다.\n\n"
        f"> \"{excerpt}...\"\n\n"
        "### 💡 알림\n"
        "- Google AI 서버 일시적 지연으로 로컬 요약이 대체 표시되었습니다. 잠시 후 'Deep AI Brief' 버튼을 다시 누르면 최신 신경망 분석이 갱신됩니다."
    )


def generate_multi_video_synthesis(
    selected_videos: List[Dict[str, Any]],
    api_key: Optional[str] = None
) -> str:
    """Synthesize multiple YouTube video intelligence records into a deep,
    paragraph-by-paragraph report using resilient multi-model fallback.

    Args:
        selected_videos: List of video dictionaries with transcript/summary data.
        api_key: Optional explicit Gemini API key.

    Returns:
        Comprehensive Markdown synthesis report.
    """
    key = get_active_gemini_api_key(api_key)
    if not key:
        return ""

    try:
        from google import genai
        client = genai.Client(api_key=key)

        context_blocks: List[str] = []
        for idx, v in enumerate(selected_videos, 1):
            t_snippet = (v.get("transcript") or v.get("executive_summary") or "")[:4500]
            context_blocks.append(
                f"### [Video {idx}] {v.get('title')}\n"
                f"- Channel: {v.get('uploader')} | Date: {v.get('upload_date')} | Duration: {v.get('duration', 0)}s\n"
                f"- Transcript/Content:\n{t_snippet}\n"
            )

        prompt = (
            "You are a Chief Technology Research Architect. "
            "Analyze the following selected video intelligence sources and produce a comprehensive, "
            "paragraph-by-paragraph intelligence synthesis report in Korean.\n\n"
            "Structure Requirements:\n"
            "# 📑 Multi-Video Consolidated Intelligence Report\n"
            "## 1. 📌 Executive Overview (핵심 총괄 요약)\n"
            "3~4 solid paragraphs summarizing the unified tech landscape, industry trends, and overarching consensus.\n\n"
            "## 2. 📑 Sectional Breakdown by Source (영상별 단락별 심층 분석)\n"
            "For EACH video source, provide:\n"
            "- Core thesis and problem statement\n"
            "- Detailed technological or business methodology\n"
            "- Key data points, quotes, or practical demonstrations\n\n"
            "## 3. 💡 Comparative Synthesis & Synergy (교차 분석 및 상호 보완점)\n"
            "Compare where the sources align, differ, or complement one another. Highlight combined synergies.\n\n"
            "## 4. 🛠️ Actionable Takeaways & Next Steps (실무 적용 로드맵)\n"
            "Step-by-step practical guide and implementation recommendations for practitioners.\n\n"
            "--- Source Materials ---\n"
            + "\n\n".join(context_blocks)
        )

        output = _call_gemini_with_resilience(client, prompt)
        if output:
            return output
    except Exception as err:
        return f"> ⚠️ Gemini Synthesis Error: {str(err)}\n\n_Falling back to sectional synthesizer..._"

    return ""
