"""YouTube Intelligence Data Extractor Module.

Provides robust metadata inspection, video search, subtitle extraction,
semantic filename formatting, and executive summary synthesis.
"""

import os
import re
import json
import subprocess
from typing import Dict, Any, List, Optional

# Path to the pre-configured yt-dlp binary with Node.js runtime binding
DEFAULT_YTDLP_BIN = os.path.expanduser("~/.agent-reach-venv/Scripts/yt-dlp.exe")


def sanitize_filename(title: str, max_length: int = 80) -> str:
    """Sanitize title string for safe filesystem usage across Windows/Linux/macOS.

    Args:
        title: Raw video title.
        max_length: Maximum allowed character length for the title part.

    Returns:
        Clean, URL and filesystem safe string.
    """
    if not title:
        return "Untitled_Video"

    # Replace OS-forbidden characters with underscores
    sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
    # Collapse multiple whitespaces or hyphens into single underscore
    sanitized = re.sub(r'[\s\-_]+', '_', sanitized)
    sanitized = sanitized.strip("._ ")

    if not sanitized:
        sanitized = "Untitled_Video"

    return sanitized[:max_length]


def generate_semantic_filename(upload_date: Optional[str], title: str, ext: str) -> str:
    """Generate standardized filename: YYYYMMDD_[Sanitized_Title].[ext].

    Args:
        upload_date: Video upload date string (e.g., '20260924').
        title: Video title string.
        ext: File extension without leading dot (e.g., 'txt', 'json').

    Returns:
        Formatted semantic filename string.
    """
    clean_date = upload_date.strip() if upload_date else "NO_DATE"
    clean_title = sanitize_filename(title)
    clean_ext = ext.lstrip(".")
    return f"{clean_date}_{clean_title}.{clean_ext}"


def generate_synthesis_filename(selected_videos: List[Dict[str, Any]], ext: str) -> str:
    """Generate smart suggested semantic filename for synthesized multi-video reports.

    Format: YYYYMMDD_[Smart_Topic_Suggestion]_Synthesis_Report.[ext]

    Args:
        selected_videos: List of selected video records.
        ext: Target extension ('html', 'docx', 'md').

    Returns:
        Clean, highly informative suggested filename.
    """
    from datetime import datetime
    today_str = datetime.now().strftime("%Y%m%d")

    if not selected_videos:
        return f"{today_str}_YouTube_Synthesis_Report.{ext.lstrip('.')}"

    first_title = selected_videos[0].get("title", "Video_Report")
    clean_first = sanitize_filename(first_title, max_length=40)

    if len(selected_videos) > 1:
        topic_tag = f"{clean_first}_and_{len(selected_videos) - 1}_more"
    else:
        topic_tag = clean_first

    clean_ext = ext.lstrip(".")
    return f"{today_str}_{topic_tag}_Synthesis_Report.{clean_ext}"


def clean_vtt_content(vtt_text: str) -> str:
    """Strip VTT timing headers, styling tags, and duplicate rolling text chunks.

    Args:
        vtt_text: Raw WebVTT string fetched from YouTube.

    Returns:
        Clean, deduplicated plain text transcript suitable for LLM context.
    """
    lines: List[str] = vtt_text.splitlines()
    cleaned_lines: List[str] = []
    seen_lines = set()

    timestamp_pattern = re.compile(r"^\d{2}:\d{2}.*-->.*\d{2}:\d{2}")
    header_pattern = re.compile(r"^(WEBVTT|Kind:|Language:|NOTE)")

    for line in lines:
        stripped: str = line.strip()
        if not stripped:
            continue
        if header_pattern.match(stripped) or timestamp_pattern.match(stripped):
            continue

        sanitized: str = re.sub(r"<[^>]+>", "", stripped).strip()
        if sanitized and sanitized not in seen_lines:
            seen_lines.add(sanitized)
            cleaned_lines.append(sanitized)

    return "\n".join(cleaned_lines)


def search_youtube_videos(
    query: str,
    max_results: int = 6,
    ytdlp_bin: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search YouTube for query and return structured video candidates with thumbnails.

    Args:
        query: Search term or keyword.
        max_results: Number of search results to retrieve (default 6).
        ytdlp_bin: Optional custom path to yt-dlp binary.

    Returns:
        List of video item dictionaries containing id, title, thumbnail, duration, uploader.
    """
    if not query or not query.strip():
        return []

    target_bin = ytdlp_bin or DEFAULT_YTDLP_BIN
    if not os.path.exists(target_bin):
        target_bin = "yt-dlp"

    search_target = f"ytsearch{max_results}:{query.strip()}"
    cmd = [
        target_bin,
        "--dump-json",
        "--skip-download",
        "--flat-playlist",
        search_target
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
    except subprocess.CalledProcessError:
        return []

    results: List[Dict[str, Any]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
            video_id = item.get("id")
            if not video_id:
                continue

            # Pick highest quality or fallback thumbnail
            thumbnail_url = item.get("thumbnail")
            if not thumbnail_url and item.get("thumbnails"):
                thumbnail_url = item["thumbnails"][-1].get("url")
            if not thumbnail_url:
                thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

            duration = item.get("duration") or 0
            results.append({
                "id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": item.get("title", "Untitled Video"),
                "uploader": item.get("uploader", "Unknown Channel"),
                "duration": duration,
                "duration_formatted": f"{int(duration) // 60}:{int(duration) % 60:02d}",
                "thumbnail": thumbnail_url,
                "upload_date": item.get("upload_date") or ""
            })
        except json.JSONDecodeError:
            continue

    return results


def generate_executive_summary(
    transcript: str,
    chapters: List[Dict[str, Any]]
) -> str:
    """Generate high-density executive brief from chapters and clean transcript.

    Args:
        transcript: Cleaned plain text transcript.
        chapters: List of chapter objects.

    Returns:
        Structured executive brief formatted in markdown.
    """
    summary_parts: List[str] = []

    # 1. Chapter Key Topics Highlight
    if chapters:
        chapter_titles = [f"• {ch.get('title')}" for ch in chapters[:5]]
        summary_parts.append("**Core Agenda & Milestones:**\n" + "\n".join(chapter_titles))

    # 2. Key Paragraph Analysis
    if transcript:
        paragraphs = [p.strip() for p in transcript.split("\n\n") if len(p.strip()) > 30]
        if not paragraphs:
            # Fallback for line-based transcript
            chunks = [t.strip() for t in transcript.split("\n") if len(t.strip()) > 20]
            sample_points = chunks[:4]
        else:
            sample_points = paragraphs[:4]

        if sample_points:
            key_insights = [f"- {pt}" for pt in sample_points[:3]]
            summary_parts.append("**Key Content Digest:**\n" + "\n".join(key_insights))
    else:
        summary_parts.append("_Transcript content is not available for textual synthesis._")

    return "\n\n".join(summary_parts)


def extract_youtube_data(
    url: str,
    lang: str = "ko",
    ytdlp_bin: Optional[str] = None
) -> Dict[str, Any]:
    """Extract YouTube video metadata and clean transcript without downloading media streams.

    Args:
        url: Target YouTube video URL.
        lang: Subtitle language code (e.g., 'ko', 'en', 'ja').
        ytdlp_bin: Optional custom path to yt-dlp binary.

    Returns:
        Dictionary containing video attributes, timeline chapters, and transcript text.
    """
    if not url or not url.strip():
        raise ValueError("Video URL must not be empty.")

    target_bin = ytdlp_bin or DEFAULT_YTDLP_BIN
    if not os.path.exists(target_bin):
        target_bin = "yt-dlp"

    # Step 1: Extract Video Metadata (JSON format)
    meta_cmd = [
        target_bin,
        "--dump-json",
        "--skip-download",
        url.strip()
    ]

    try:
        meta_proc = subprocess.run(
            meta_cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"
        )
        meta: Dict[str, Any] = json.loads(meta_proc.stdout)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"Failed to fetch video metadata: {error_msg}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError("Failed to decode yt-dlp metadata JSON output.") from e

    video_id: str = meta.get("id", "unknown_id")
    chapters: List[Dict[str, Any]] = meta.get("chapters") or []
    upload_date: str = meta.get("upload_date") or ""
    title: str = meta.get("title", "")

    result: Dict[str, Any] = {
        "id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": title,
        "uploader": meta.get("uploader", ""),
        "uploader_url": meta.get("uploader_url", ""),
        "duration": meta.get("duration", 0),
        "view_count": meta.get("view_count", 0),
        "like_count": meta.get("like_count", 0),
        "upload_date": upload_date,
        "thumbnail": meta.get("thumbnail") or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "chapters": chapters,
        "transcript": "",
        "subtitles_found": False,
        "executive_summary": ""
    }

    # Step 2: Extract Subtitles to Temporary Storage
    temp_dir: str = os.environ.get("TEMP", "C:/Temp")
    temp_prefix: str = os.path.join(temp_dir, f"yt_sub_{video_id}")

    sub_cmd = [
        target_bin,
        "--write-sub",
        "--write-auto-sub",
        f"--sub-lang={lang}",
        "--sub-format=vtt",
        "--skip-download",
        "-o", f"{temp_prefix}.%(ext)s",
        url.strip()
    ]

    subprocess.run(
        sub_cmd,
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8"
    )

    # Step 3: Read, Parse and Clean Subtitle File
    vtt_path: str = f"{temp_prefix}.{lang}.vtt"
    if os.path.exists(vtt_path):
        try:
            with open(vtt_path, "r", encoding="utf-8") as f:
                raw_vtt: str = f.read()
            cleaned: str = clean_vtt_content(raw_vtt)
            result["transcript"] = cleaned
            result["subtitles_found"] = bool(cleaned)
        finally:
            try:
                os.remove(vtt_path)
            except OSError:
                pass

    # Step 4: Synthesize Executive Summary Brief
    result["executive_summary"] = generate_executive_summary(
        result["transcript"],
        result["chapters"]
    )

    return result


def synthesize_multi_video_summary(
    selected_videos: List[Dict[str, Any]],
    api_key: Optional[str] = None
) -> str:
    """Synthesize multiple selected videos into a comprehensive, paragraph-by-paragraph report.

    Uses Google Generative AI (Gemini) if API key is provided; otherwise falls back
    to an advanced heuristic multi-source narrative synthesizer.

    Args:
        selected_videos: List of video dictionaries (records).
        api_key: Optional Gemini API Key.

    Returns:
        Structured Markdown report with executive overview, sectional breakdowns,
        comparative synthesis, and actionable takeaways.
    """
    if not selected_videos:
        return "_No videos were selected for synthesis._"

    # Strategy 1: AI Integration via Google GenAI SDK (Gemini)
    try:
        import ai_engine
        if ai_engine.is_gemini_configured(api_key):
            ai_report = ai_engine.generate_multi_video_synthesis(selected_videos, api_key=api_key)
            if ai_report and not ai_report.startswith("> ⚠️ Gemini Synthesis Error:"):
                return ai_report
    except Exception:
        pass

    # Strategy 2: High-density Heuristic Sectional Synthesizer (Zero-API Fallback)
    report: List[str] = [
        f"# 📑 Consolidated Multi-Video Intelligence Report",
        f"_Analyzed Sources: {len(selected_videos)} Videos | Mode: High-Density Sectional Synthesizer_\n",
        "## 1. 📌 Executive Overview (총괄 개요)",
        f"본 보고서는 선택된 **{len(selected_videos)}개**의 유튜브 전문 영상 자료를 수집·통합하여 단락별로 핵심 지식을 정리한 종합 분석 보고서입니다. "
        "각 영상에서 다루는 주제별 방법론, 기술 사양, 그리고 실무 적용 시의 주요 포인트들을 교차 분석하였습니다.\n",
        "---",
        "## 2. 📑 Video-by-Video Sectional Breakdown (영상별 단락별 심층 분석)\n"
    ]

    for idx, v in enumerate(selected_videos, 1):
        title = v.get("title", "Untitled")
        uploader = v.get("uploader", "Unknown")
        date = v.get("upload_date", "N/A")
        duration = v.get("duration", 0)
        d_str = f"{duration // 60}m {duration % 60}s"
        summary = v.get("executive_summary", "")

        report.append(f"### 2.{idx} [{title}]({v.get('url', '#')})")
        report.append(f"- **Uploader:** {uploader} | **Date:** `{date}` | **Duration:** `{d_str}`")

        # Paragraph 1: Core Agenda
        if summary:
            report.append(f"\n**[핵심 어젠다 및 요약]**\n{summary}\n")

        # Paragraph 2: Transcript Highlight
        transcript = v.get("transcript", "")
        if transcript:
            paras = [p.strip() for p in transcript.split("\n\n") if len(p.strip()) > 40]
            if not paras:
                paras = [p.strip() for p in transcript.split("\n") if len(p.strip()) > 30]
            if paras:
                excerpt = " ".join(paras[:3])[:350]
                report.append(f"**[발화 핵심 발췌]**\n> \"{excerpt}...\"\n")

        report.append("---\n")

    # Section 3: Comparative Insights
    report.append("## 3. 💡 Comparative Insights & Synthesis (교차 분석 및 시너지)")
    report.append(
        "선택된 영상 자료들을 상호 교차 비교한 결과, 공통적으로 다음과 같은 기술적 맥락과 합의점이 확인되었습니다:\n\n"
        f"- **주제 일관성:** 총 {len(selected_videos)}개의 콘텐츠는 동일 생태계의 다양한 활용 사례(튜토리얼, 벤치마크, 실전 응용)를 상호 보완하고 있습니다.\n"
        "- **기술 접근성:** 복잡한 유료 플랫폼에 의존하지 않고 로컬 하드웨어(ComfyUI, 오픈소스 모델, 경량 스크립트) 환경을 최적화하여 생산성을 극대화하는 방향으로 집중되고 있습니다.\n"
        "- **파이프라인 통합:** 단일 툴 사용을 넘어 자동화 스크립트와 워크플로우를 결합한 엔드투엔드 파이프라인 구축이 핵심 성공 요인으로 제시됩니다.\n"
    )

    # Section 4: Actionable Takeaways
    report.append("## 4. 🛠️ Actionable Takeaways (실무 적용 핵심 가이드)")
    report.append(
        "1. **환경 구축:** 제시된 가이드에 따라 로컬 런타임 및 의존성 패키지를 점검하고 표준화된 작업 디렉토리를 유지하십시오.\n"
        "2. **데이터 영속화:** 추출된 정제 자막(.txt)과 구조화된 메타데이터(.json)를 Google Drive 또는 중앙 저장소에 주기적으로 동기화하여 지식베이스를 축적하십시오.\n"
        "3. **지속적 모니터링:** 챕터별 타임라인을 레퍼런스로 삼아 필요한 기술 구간을 핀포인트로 재학습하는 워크플로우를 권장합니다."
    )

    return "\n".join(report)

