import os
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

### Settings ###
load_dotenv()
SUBTITLE_LANGS = os.getenv("SUBTITLE_LANGS")  # Default to Japanese subtitles


def parse_json3_subtitles(json_data: list) -> str:
    """
    Parse YouTube JSON3 subtitle format and extract text content
    """
    if not json_data:
        return ""

    text_parts = []
    for event in json_data:
        if "segs" in event:
            for seg in event["segs"]:
                if "utf8" in seg:
                    text_parts.append(seg["utf8"])

    return " ".join(text_parts).replace("\n", " ").strip()


def extract_from_subtitle_list(subtitle_list: list) -> list:
    """
    Extract text from list of subtitle format objects
    """
    texts = []
    for sub_format in subtitle_list:
        if sub_format["ext"] == "json3" and "data" in sub_format:
            text = parse_json3_subtitles(sub_format["data"])
            if text:
                texts.append(text)
    return texts


def extract_subtitles_from_info(info_dict: dict) -> str:
    """
    Extract subtitle text from yt-dlp info dictionary
    Prioritizes manual subtitles over auto-generated ones
    """
    subtitle_texts = []

    # Check for manual subtitles first
    for lang in SUBTITLE_LANGS:
        # Manual subtitles
        if lang in info_dict.get("subtitles", {}):
            subtitle_texts.extend(
                extract_from_subtitle_list(info_dict["subtitles"][lang])
            )
            break

        # Auto-generated subtitles (only if no manual subtitles found)
        elif lang in info_dict.get("automatic_captions", {}) and not subtitle_texts:
            subtitle_texts.extend(
                extract_from_subtitle_list(info_dict["automatic_captions"][lang])
            )
            break

    return " ".join(subtitle_texts) if subtitle_texts else ""


def download_subtitles(video_url: str, video_id: str) -> str:
    """
    Download subtitles from YouTube video using in-memory processing
    """
    ydl_opts = {
        "skip_download": True,  # Don't download video content
        "writesubtitles": True,  # Download subtitles
        "writeautomaticsub": True,  # Include auto-generated subtitles
        "subtitleslangs": SUBTITLE_LANGS,  # Preferred languages
        "subtitlesformat": "json3",  # Keep in memory as JSON format
        "quiet": True,  # Suppress output
        "no_warnings": True,  # Hide warnings
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Extract metadata only (no file saving)
            info = ydl.extract_info(video_url, download=False)
            # Get subtitle data directly from memory
            return extract_subtitles_from_info(info)

    except Exception as e:
        print(f"Subtitle download failed: {e}")
        return ""


if __name__ == "__main__":  # Example usage
    test_video_id = "3jiUMCoLgzI"
    test_video_url = f"https://www.youtube.com/watch?v={test_video_id}"
    subtitles = download_subtitles(test_video_url, test_video_id)
    print(
        f"Extracted Subtitles for {test_video_id}:\n{subtitles[:500]}..."
    )  # Print first 500 chars
