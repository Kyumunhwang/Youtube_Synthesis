"""Modern YouTube Intelligence Studio Application.

Features:
- Video search with responsive thumbnail cards and 1-click extraction.
- Automatic semantic file naming: YYYYMMDD_[Sanitized_Title].[txt|json].
- One-click synchronization to Google Drive / local database.
- Consolidated database overview with Multi-Video Paragraph-by-Paragraph Synthesis.
- Modernized, high-density card UI with executive briefs.
"""

import os
import json
import importlib
import streamlit as st
from typing import Dict, Any, List

import extractor
import storage
import exporter
import ai_engine
importlib.reload(extractor)
importlib.reload(storage)
importlib.reload(exporter)
importlib.reload(ai_engine)

from extractor import (
    extract_youtube_data,
    search_youtube_videos,
    generate_semantic_filename,
    generate_synthesis_filename,
    synthesize_multi_video_summary
)
from storage import (
    DEFAULT_STORAGE_DIR,
    save_video_to_storage,
    load_database_records,
    generate_consolidated_markdown,
    delete_record_from_storage,
    delete_multiple_records_from_storage
)
from exporter import (
    markdown_to_styled_html,
    markdown_to_docx,
    launch_google_docs_autopaste
)
from ai_engine import (
    get_active_gemini_api_key,
    is_gemini_configured,
    generate_executive_briefing,
    generate_multi_video_synthesis
)

st.set_page_config(
    page_title="YouTube Intelligence Studio",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.dialog("📑 Synthesized Intelligence Report", width="large")
def show_browser_report_modal(report_md: str):
    """Render full report directly in browser modal without file download."""
    st.caption("Live In-Browser Document Viewer with One-Click Auto-Paste to Google Docs.")
    st.markdown(report_md)
    st.markdown("---")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        if st.button("🚀 Auto-Paste into Google Docs (자동 붙여넣기 실행)", key="modal_autopaste_btn", use_container_width=True, type="primary"):
            launch_google_docs_autopaste(report_md)
            st.toast("Opening Google Docs and auto-pasting content via OS robot! Please keep browser focused.", icon="🚀")
    with m_col2:
        if st.button("Close Viewer", use_container_width=True):
            st.rerun()

# Custom High-End Modern Styling (Glassmorphism & Responsive Cards)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8F00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .video-card {
        border-radius: 12px;
        padding: 12px;
        background-color: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 16px;
    }
    .video-card:hover {
        transform: translateY(-3px);
        border-color: #FF4B4B;
    }
    .badge-time {
        display: inline-block;
        background-color: #212529;
        color: #f8f9fa;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        margin-top: 4px;
    }
    .brief-container {
        background: rgba(255, 75, 75, 0.07);
        border-left: 4px solid #FF4B4B;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    .synthesis-box {
        background: rgba(255, 143, 0, 0.08);
        border: 1px solid rgba(255, 143, 0, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration: Target Storage & Google Drive Directory
with st.sidebar:
    st.markdown("### ⚙️ Storage & Sync Settings")
    target_storage = st.text_input(
        "Google Drive / Database Path",
        value=st.session_state.get("target_storage_dir", DEFAULT_STORAGE_DIR),
        help="Specify your local folder or mounted Google Drive directory (e.g., G:\\My Drive\\YouTube_DB)."
    )
    st.session_state["target_storage_dir"] = target_storage

    st.markdown("---")
    st.markdown("### 🤖 AI Engine Settings")

    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = get_active_gemini_api_key()
    if "show_key_editor" not in st.session_state:
        st.session_state["show_key_editor"] = False

    gemini_key = st.session_state["gemini_api_key"]
    is_ai_active = is_gemini_configured(gemini_key)

    if is_ai_active:
        st.success("🟢 Gemini 2.5 Flash: Active", icon="✨")
    else:
        st.info("⚪ Local Synthesizer (No API Key)", icon="ℹ️")

    if not st.session_state["show_key_editor"]:
        if st.button("🔑 Change Gemini API Key", use_container_width=True, key="btn_toggle_key_editor"):
            st.session_state["show_key_editor"] = True
            st.rerun()
    else:
        with st.expander("🔑 Update Gemini API Key", expanded=True):
            new_key_input = st.text_input(
                "New API Key",
                type="password",
                value="",
                placeholder="AIzaSy...",
                help="Enter a new Google AI Studio API key."
            )
            k_col1, k_col2 = st.columns(2)
            with k_col1:
                if st.button("💾 Apply", use_container_width=True, type="primary", key="btn_apply_key"):
                    if new_key_input.strip():
                        st.session_state["gemini_api_key"] = new_key_input.strip()
                        st.session_state["show_key_editor"] = False
                        st.success("API Key updated successfully!")
                        st.rerun()
                    else:
                        st.warning("Please enter a valid key.")
            with k_col2:
                if st.button("Cancel", use_container_width=True, key="btn_cancel_key"):
                    st.session_state["show_key_editor"] = False
                    st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Database Status")
    db_records = load_database_records(target_storage)
    st.metric("Total Indexed Videos", f"{len(db_records)} records")

    st.markdown("---")
    st.caption("Engine: yt-dlp + Gemini 2.5 Flash / High-Density Sectional Synthesizer")

# Main Header
st.markdown('<div class="main-header">YouTube Intelligence Studio</div>', unsafe_allow_html=True)
st.caption("Search, analyze, digest, and synchronize YouTube video intelligence directly to your Google Drive knowledge base.")

# Top Navigation Tabs
nav_search, nav_detail, nav_db = st.tabs([
    "🔍 Search & Thumbnail Grid",
    "⚡ Active Video & Brief",
    "📚 Consolidated Database Hub"
])

# -----------------------------------------------------------------------------
# TAB 1: Search & Interactive Thumbnail Cards
# -----------------------------------------------------------------------------
with nav_search:
    st.markdown("#### Search YouTube or Paste Direct Video Link")
    search_col1, search_col2, search_col3 = st.columns([5, 2, 2])
    with search_col1:
        query_input = st.text_input(
            "Search Keyword or URL",
            placeholder="e.g. AI Music generation YuE2 OR https://www.youtube.com/watch?v=...",
            label_visibility="collapsed"
        )
    with search_col2:
        lang_choice = st.selectbox("Subtitle Language", ["ko", "en", "ja", "zh-Hans"], index=0)
    with search_col3:
        btn_search = st.button("Explore YouTube", type="primary", use_container_width=True)

    # Perform Search Query or Direct Match
    if btn_search and query_input:
        is_direct_url = "youtube.com" in query_input or "youtu.be" in query_input
        if is_direct_url:
            st.session_state["active_url"] = query_input.strip()
            st.session_state["auto_extract"] = True
            st.info("Direct YouTube URL recognized. Switched to extraction pipeline.")
        else:
            with st.spinner("Searching YouTube candidates..."):
                search_results = search_youtube_videos(query_input.strip(), max_results=6)
                st.session_state["search_results"] = search_results

    # Render Thumbnail Cards Grid
    if "search_results" in st.session_state and st.session_state["search_results"]:
        st.markdown("---")
        st.markdown("##### Select a video thumbnail below to extract intelligence:")
        cards = st.session_state["search_results"]

        # 3-Column Responsive Grid
        cols = st.columns(3)
        for idx, item in enumerate(cards):
            col = cols[idx % 3]
            with col:
                st.image(item["thumbnail"], use_container_width=True)
                st.markdown(f"**{item['title']}**")
                st.markdown(f"<span class='badge-time'>⏱️ {item['duration_formatted']}</span> | 👤 `{item['uploader']}`", unsafe_allow_html=True)
                if st.button("⚡ Extract & Analyze", key=f"btn_card_{item['id']}", use_container_width=True):
                    st.session_state["active_url"] = item["url"]
                    st.session_state["auto_extract"] = True
                    st.rerun()

# -----------------------------------------------------------------------------
# TAB 2: Active Video Extraction & Executive Brief
# -----------------------------------------------------------------------------
with nav_detail:
    active_url = st.session_state.get("active_url", "")

    if not active_url:
        st.info("No active video selected. Enter a URL or choose a video from the 'Search & Thumbnail Grid' tab.")
    else:
        # Trigger Extraction if flagged or requested
        if st.session_state.get("auto_extract", False) or st.button("Re-Extract Active Video", type="secondary"):
            st.session_state["auto_extract"] = False
            with st.spinner("Deciphering player signature and parsing transcript..."):
                try:
                    video_info = extract_youtube_data(active_url, lang=lang_choice)
                    st.session_state["current_video_data"] = video_info
                    st.success("Extraction completed successfully!")
                except Exception as err:
                    st.error(f"Extraction Failed: {str(err)}")

        if "current_video_data" in st.session_state:
            curr = st.session_state["current_video_data"]

            # Video Header & Overview Metrics
            head_col1, head_col2 = st.columns([1, 4])
            with head_col1:
                st.image(curr.get("thumbnail"), use_container_width=True)
            with head_col2:
                st.subheader(curr.get("title"))
                st.markdown(f"👤 **Channel:** {curr.get('uploader')} | 📅 **Upload Date:** `{curr.get('upload_date')}` | ⏱️ **Duration:** `{curr.get('duration') // 60}m {curr.get('duration') % 60}s`")

                # Semantic Filename Preview
                txt_preview = generate_semantic_filename(curr.get("upload_date"), curr.get("title"), "txt")
                json_preview = generate_semantic_filename(curr.get("upload_date"), curr.get("title"), "json")
                st.caption(f"💾 Standard Filename: `{txt_preview}` / `{json_preview}`")

            # One-Click Sync to Google Drive / Database
            st.markdown("---")
            sync_col1, sync_col2 = st.columns([3, 1])
            with sync_col1:
                st.write(f"📁 Destination Folder: `{st.session_state['target_storage_dir']}`")
            with sync_col2:
                if st.button("💾 Save to Google Drive / DB", type="primary", use_container_width=True):
                    with st.spinner("Saving semantic files and updating database.json..."):
                        save_info = save_video_to_storage(curr, st.session_state["target_storage_dir"])
                        st.success(f"Saved: {os.path.basename(save_info['txt_path'])}")
                        st.rerun()

            # Executive Brief Card
            st.markdown('<div class="brief-container">', unsafe_allow_html=True)
            b_head_col1, b_head_col2 = st.columns([3, 1])
            with b_head_col1:
                st.markdown("### 📋 Executive Intelligence Brief")
            with b_head_col2:
                if is_ai_active and curr.get("transcript"):
                    if st.button("✨ Deep AI Brief (Gemini)", key="btn_gen_ai_brief", use_container_width=True):
                        with st.spinner("Generating neural executive brief via Gemini 2.5 Flash..."):
                            ai_brief = generate_executive_briefing(
                                curr.get("title", ""),
                                curr.get("uploader", ""),
                                curr.get("transcript", ""),
                                api_key=gemini_key
                            )
                            if ai_brief:
                                curr["executive_summary"] = ai_brief
                                st.session_state["current_video_data"] = curr
                                st.success("Gemini brief generated!")
                                st.rerun()

            st.markdown(curr.get("executive_summary") or "_No summary generated._")
            st.markdown('</div>', unsafe_allow_html=True)

            # Detail Tabs
            d_tab_sub, d_tab_chap, d_tab_raw = st.tabs(["Clean Transcript", "Timeline Chapters", "Raw Metadata"])

            with d_tab_sub:
                if curr.get("transcript"):
                    st.text_area("Plain Text Transcript", curr["transcript"], height=400)
                    dl1, dl2, _ = st.columns([2, 2, 4])
                    with dl1:
                        st.download_button(
                            label=f"Download {txt_preview}",
                            data=curr["transcript"],
                            file_name=txt_preview,
                            mime="text/plain",
                            use_container_width=True
                        )
                    with dl2:
                        json_str = json.dumps(curr, ensure_ascii=False, indent=2)
                        st.download_button(
                            label=f"Download {json_preview}",
                            data=json_str,
                            file_name=json_preview,
                            mime="application/json",
                            use_container_width=True
                        )
                else:
                    st.warning("No subtitles found for this video in the selected language.")

            with d_tab_chap:
                chapters = curr.get("chapters") or []
                if chapters:
                    for ch in chapters:
                        start_time = int(ch.get("start_time", 0))
                        st.write(f"⏱️ **`{start_time // 60:02d}:{start_time % 60:02d}`** — {ch.get('title')}")
                else:
                    st.info("No timeline chapters found.")

            with d_tab_raw:
                st.json(curr)

# -----------------------------------------------------------------------------
# TAB 3: Consolidated Database Hub & Multi-Video Sectional Synthesis
# -----------------------------------------------------------------------------
with nav_db:
    st.markdown("#### 📚 Consolidated Knowledge Database & Synthesis Studio")
    st.caption("Select one or more saved YouTube records to generate a comprehensive, paragraph-by-paragraph intelligence synthesis report.")

    records = load_database_records(st.session_state["target_storage_dir"])

    if not records:
        st.info("Your database is currently empty. Extract a video and click 'Save to Google Drive / DB' to start indexing.")
    else:
        # Aggregation Toolbar
        top_c1, top_c2 = st.columns([3, 2])
        with top_c1:
            st.write(f"Total Stored Videos: **{len(records)}**")
        with top_c2:
            consolidated_md = generate_consolidated_markdown(records)
            st.download_button(
                label="📥 Export All Records Report (.md)",
                data=consolidated_md,
                file_name="YouTube_Consolidated_Full_Report.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown("---")

        # Multi-Video Selection Panel
        st.markdown("##### 🎯 Step 1: Select Videos for Consolidated Synthesis")

        sel_all_col, sel_count_col = st.columns([2, 4])
        with sel_all_col:
            select_all = st.checkbox("Select All Available Videos", value=False)

        selected_records: List[Dict[str, Any]] = []

        # Render Checkbox Selection Grid
        for idx, record in enumerate(records):
            vid_id = record.get("id")
            default_val = select_all
            is_checked = st.checkbox(
                f"**[{record.get('upload_date')}]** {record.get('title')} (`{record.get('uploader')}`)",
                value=default_val,
                key=f"chk_vid_{vid_id}_{idx}"
            )
            if is_checked:
                # Ensure full transcript is attached for synthesis
                rec_copy = dict(record)
                if not rec_copy.get("transcript") and os.path.exists(rec_copy.get("txt_filepath", "")):
                    try:
                        with open(rec_copy["txt_filepath"], "r", encoding="utf-8") as f:
                            rec_copy["transcript"] = f.read()
                    except OSError:
                        pass
                selected_records.append(rec_copy)

        st.markdown("---")

        # Step 2: Synthesis & Management Trigger
        st.markdown("##### ⚡ Step 2: Intelligence Synthesis & Record Management")
        c_info1, c_info2 = st.columns([3, 2])
        with c_info1:
            st.write(f"Selected videos: **{len(selected_records)}** item(s)")
        with c_info2:
            if is_ai_active:
                st.caption("⚡ Engine: **Google Gemini 2.5 Flash** (Deep Neural Synthesis)")
            else:
                st.caption("⚙️ Engine: **Local Sectional Synthesizer** (Rule-based Fallback)")

        action_col1, action_col2 = st.columns([3, 1])
        with action_col1:
            btn_title = "🤖 Synthesize Selected Videos (Gemini 2.5 Flash)" if is_ai_active else "⚙️ Synthesize Selected Videos (Sectional Synthesis)"
            if st.button(btn_title, type="primary", disabled=(len(selected_records) == 0), use_container_width=True):
                with st.spinner(f"Analyzing and synthesizing {len(selected_records)} video intelligence sources..."):
                    synthesized_report = synthesize_multi_video_summary(
                        selected_records,
                        api_key=st.session_state.get("gemini_api_key")
                    )
                    st.session_state["multi_video_synthesis"] = synthesized_report
                    st.success("Consolidated sectional synthesis generated successfully!")

        with action_col2:
            if st.button("🗑️ Delete Selected", type="secondary", disabled=(len(selected_records) == 0), use_container_width=True, help="Permanently delete selected videos from database and disk."):
                del_ids = [r["id"] for r in selected_records if r.get("id")]
                with st.spinner(f"Deleting {len(del_ids)} record(s)..."):
                    deleted_num = delete_multiple_records_from_storage(del_ids, st.session_state["target_storage_dir"])
                    st.success(f"Deleted {deleted_num} video record(s) and files.")
                    st.rerun()

        # Display Synthesized Report with Multi-Format Export & In-Browser Viewer
        if "multi_video_synthesis" in st.session_state:
            report_content = st.session_state["multi_video_synthesis"]

            st.markdown('<div class="synthesis-box">', unsafe_allow_html=True)
            st.markdown("### 📑 Paragraph-by-Paragraph Consolidated Synthesis Report")
            st.markdown(report_content)
            st.markdown('</div>', unsafe_allow_html=True)

            # Toolbar 1: Direct Actions (In-Browser Modal & Google Docs Transfer)
            st.markdown("##### 🚀 Quick Actions & Cloud Integration")
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("👁️ View in Browser Modal (브라우저에서 바로 보기)", use_container_width=True, type="secondary"):
                    show_browser_report_modal(report_content)
            with act_col2:
                if st.button("🚀 Auto-Paste to Google Docs (구글닥스 자동 실행 & 자동 붙여넣기)", use_container_width=True, type="primary"):
                    launch_google_docs_autopaste(report_content)
                    st.toast("🚀 Auto-Paste Robot dispatched! Please keep the browser window focused...", icon="🚀")
                    st.info("🚀 Google Docs가 새 탭으로 열린 후 에디터 캔버스가 로드되면(약 4.5초) 로봇이 자동으로 내용을 붙여넣습니다. (클립보드에도 복사되어 있어 언제든 Ctrl+V로 즉시 삽입 가능합니다)")

                st.caption("💡 *Auto-Paste Robot: Injects clipboard, opens Google Docs, waits for editor, and fires Ctrl+V.*")

            # Toolbar 2: Multi-Format File Downloads with Smart Suggested Filenames
            suggested_md = generate_synthesis_filename(selected_records, "md")
            suggested_html = generate_synthesis_filename(selected_records, "html")
            suggested_docx = generate_synthesis_filename(selected_records, "docx")

            st.markdown("##### 📥 Multi-Format Downloads (Smart Suggested Names)")
            st.caption(f"🏷️ **Suggested Filename:** `{suggested_docx}`")

            dl_col1, dl_col2, dl_col3 = st.columns(3)
            with dl_col1:
                st.download_button(
                    label="📥 Download Markdown (.md)",
                    data=report_content,
                    file_name=suggested_md,
                    mime="text/markdown",
                    use_container_width=True
                )
            with dl_col2:
                html_payload = markdown_to_styled_html(report_content, title="YouTube Intelligence Synthesis Report")
                st.download_button(
                    label="🌐 Download HTML (.html)",
                    data=html_payload,
                    file_name=suggested_html,
                    mime="text/html",
                    use_container_width=True
                )
            with dl_col3:
                docx_stream = markdown_to_docx(report_content, title="YouTube Intelligence Synthesis Report")
                st.download_button(
                    label="📄 Download MS-Word (.docx)",
                    data=docx_stream.getvalue(),
                    file_name=suggested_docx,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

        st.markdown("---")
        st.markdown("##### 📂 Individual File Explorer")

        # Individual Records Detail View
        for record in records:
            with st.expander(f"📅 {record.get('upload_date')} | {record.get('title')} ({record.get('uploader')})"):
                exp_c1, exp_c2 = st.columns([3, 1])
                with exp_c1:
                    st.markdown(f"**Video URL:** [{record.get('url')}]({record.get('url')})")
                    st.markdown(f"**Stored Files:** `{record.get('txt_filename')}` | `{record.get('json_filename')}`")
                    st.markdown(f"**File Location:** `{record.get('txt_filepath')}`")
                    st.markdown("##### Executive Summary:")
                    st.markdown(record.get("executive_summary") or "_No summary_")
                with exp_c2:
                    st.metric("Transcript Length", f"{record.get('transcript_length', 0):,} chars")
                    if os.path.exists(record.get("txt_filepath", "")):
                        with open(record.get("txt_filepath"), "r", encoding="utf-8") as f:
                            file_txt = f.read()
                        st.download_button(
                            label="Download .txt",
                            data=file_txt,
                            file_name=record.get("txt_filename"),
                            key=f"dl_txt_single_{record.get('id')}",
                            use_container_width=True
                        )
                    if st.button("Load into Active View", key=f"btn_load_{record.get('id')}", use_container_width=True):
                        st.session_state["active_url"] = record.get("url")
                        st.session_state["auto_extract"] = True
                        st.rerun()

                    # Individual Delete Record Button
                    if st.button("🗑️ Delete Record", key=f"btn_del_single_{record.get('id')}", type="secondary", use_container_width=True, help="Delete this video and its files from storage."):
                        if delete_record_from_storage(record.get("id"), st.session_state["target_storage_dir"]):
                            st.success("Record and files deleted successfully.")
                            st.rerun()
                        else:
                            st.error("Failed to delete record.")
