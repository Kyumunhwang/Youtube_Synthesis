"""Database and Storage Synchronization Module for YouTube Intelligence.

Handles saving structured transcripts, full metadata JSON files, and managing
the central database.json index in local storage or synced Google Drive folders.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from extractor import generate_semantic_filename

# Default database storage path (supports environment variable override)
DEFAULT_STORAGE_DIR = os.path.abspath(
    os.environ.get("YOUTUBE_STORAGE_DIR") or os.path.join(os.path.dirname(__file__), "storage_db")
)


def get_database_path(storage_dir: Optional[str] = None) -> str:
    """Return the absolute path to database.json within the target directory."""
    raw = (storage_dir or "").strip()
    if not raw or raw.startswith("http://") or raw.startswith("https://") or "://" in raw:
        base_dir = DEFAULT_STORAGE_DIR
    else:
        base_dir = os.path.abspath(raw)

    try:
        os.makedirs(base_dir, exist_ok=True)
    except OSError:
        base_dir = DEFAULT_STORAGE_DIR
        os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, "database.json")


def load_database_records(storage_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load all indexed video records from the database.json file.

    Args:
        storage_dir: Base directory containing database.json.

    Returns:
        List of video record dictionaries ordered by save date descending.
    """
    db_path = get_database_path(storage_dir)
    if not os.path.exists(db_path):
        return []

    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("records", [])
    except (json.JSONDecodeError, OSError):
        return []


def save_video_to_storage(
    video_data: Dict[str, Any],
    target_dir: Optional[str] = None
) -> Dict[str, str]:
    """Save clean transcript .txt, full metadata .json, and update database.json.

    Filenames strictly adhere to YYYYMMDD_[Sanitized_Title].[ext].

    Args:
        video_data: Extracted video dictionary.
        target_dir: Destination folder (e.g. Google Drive local sync directory).

    Returns:
        Dictionary containing saved txt_path, json_path, and semantic_name.
    """
    raw = (target_dir or "").strip()
    if not raw or raw.startswith("http://") or raw.startswith("https://") or "://" in raw:
        base_dir = DEFAULT_STORAGE_DIR
    else:
        base_dir = os.path.abspath(raw)

    try:
        os.makedirs(base_dir, exist_ok=True)
    except OSError:
        base_dir = DEFAULT_STORAGE_DIR
        os.makedirs(base_dir, exist_ok=True)

    upload_date = video_data.get("upload_date") or datetime.now().strftime("%Y%m%d")
    title = video_data.get("title", "Untitled")

    # 1. Format Semantic Filenames
    txt_filename = generate_semantic_filename(upload_date, title, "txt")
    json_filename = generate_semantic_filename(upload_date, title, "json")

    txt_filepath = os.path.join(base_dir, txt_filename)
    json_filepath = os.path.join(base_dir, json_filename)

    # 2. Write Transcript (.txt)
    transcript_text = video_data.get("transcript", "")
    with open(txt_filepath, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    # 3. Write Full Metadata (.json)
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(video_data, f, ensure_ascii=False, indent=2)

    # 4. Upsert into database.json
    db_path = get_database_path(base_dir)
    records = load_database_records(base_dir)

    record_entry: Dict[str, Any] = {
        "id": video_data.get("id"),
        "url": video_data.get("url"),
        "title": title,
        "upload_date": upload_date,
        "uploader": video_data.get("uploader", ""),
        "duration": video_data.get("duration", 0),
        "subtitles_found": video_data.get("subtitles_found", False),
        "transcript_length": len(transcript_text),
        "executive_summary": video_data.get("executive_summary", ""),
        "txt_filename": txt_filename,
        "json_filename": json_filename,
        "txt_filepath": txt_filepath,
        "json_filepath": json_filepath,
        "saved_at": datetime.now().isoformat()
    }

    # Deduplicate: Replace if existing, else prepend
    existing_idx = next((i for i, r in enumerate(records) if r.get("id") == video_data.get("id")), None)
    if existing_idx is not None:
        records[existing_idx] = record_entry
    else:
        records.insert(0, record_entry)

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump({"records": records, "updated_at": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

    return {
        "txt_path": txt_filepath,
        "json_path": json_filepath,
        "semantic_name": f"{upload_date}_{title}"
    }


def generate_consolidated_markdown(records: List[Dict[str, Any]]) -> str:
    """Generate consolidated markdown summary of all saved database records."""
    if not records:
        return "# YouTube Intelligence Database\n\n_No video records saved in this database yet._"

    doc: List[str] = [
        "# Consolidated YouTube Intelligence Report",
        f"_Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_",
        f"_Total Videos Indexed: {len(records)}_",
        "\n---\n"
    ]

    for idx, r in enumerate(records, 1):
        duration_sec = r.get("duration", 0)
        mins = duration_sec // 60
        secs = duration_sec % 60
        duration_str = f"{mins:02d}:{secs:02d}"

        doc.append(f"## {idx}. {r.get('title')}")
        doc.append(f"- **Uploader:** {r.get('uploader')} | **Upload Date:** {r.get('upload_date')} | **Duration:** {duration_str}")
        doc.append(f"- **URL:** [{r.get('url')}]({r.get('url')})")
        doc.append(f"- **Stored Files:** `{r.get('txt_filename')}` | `{r.get('json_filename')}`")
        doc.append("\n### Executive Brief:")
        doc.append(r.get("executive_summary") or "_No brief available._")
        doc.append("\n---\n")

    return "\n".join(doc)


def delete_record_from_storage(
    video_id: str,
    storage_dir: Optional[str] = None
) -> bool:
    """Delete a video's txt, json files and remove its entry from database.json.

    Args:
        video_id: Target YouTube video ID.
        storage_dir: Target storage directory containing database.json.

    Returns:
        True if the record was found and deleted, False otherwise.
    """
    db_path = get_database_path(storage_dir)
    records = load_database_records(storage_dir)

    target_idx = next((i for i, r in enumerate(records) if r.get("id") == video_id), None)
    if target_idx is None:
        return False

    target_record = records.pop(target_idx)

    # 1. Clean up physical files on disk
    txt_path = target_record.get("txt_filepath")
    json_path = target_record.get("json_filepath")

    for path in (txt_path, json_path):
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

    # 2. Persist updated database.json
    try:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump({
                "records": records,
                "updated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def delete_multiple_records_from_storage(
    video_ids: List[str],
    storage_dir: Optional[str] = None
) -> int:
    """Delete multiple video records and their associated files in bulk.

    Args:
        video_ids: List of video IDs to delete.
        storage_dir: Target storage directory.

    Returns:
        Count of successfully deleted records.
    """
    if not video_ids:
        return 0

    deleted_count = 0
    for vid_id in video_ids:
        if delete_record_from_storage(vid_id, storage_dir):
            deleted_count += 1

    return deleted_count

