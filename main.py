import os
from dotenv import load_dotenv
import pandas as pd

import analyzer, fetch_transcripts

VIDEO_IDS = ["3jiUMCoLgzI"]

load_dotenv()
API_KEY = os.environ["YOUTUBE_API_KEY"]
SUBTITLE_LANGS = os.getenv("SUBTITLE_LANGS", "ja")  # default to Japanese
DEBUG = os.getenv("DEBUG", "False") == "True"

if __name__ == "__main__":
    # Get playlist IDs from video IDs
    playlist_data = analyzer.get_playlist_ids(VIDEO_IDS, API_KEY)
    if DEBUG:
        print("Playlist Data:")
        print(playlist_data)

    # Get all video IDs from playlist IDs
    playlist_ids = playlist_data["playlist_id"].tolist()
    all_videos_data = analyzer.get_all_video_ids(playlist_ids, API_KEY)
    if DEBUG:
        print("All Videos Data:")
        print(all_videos_data)

    # Get detailed video information
    all_video_ids = all_videos_data["video_id"].tolist()
    df_video_details = analyzer.get_video_details(all_video_ids, API_KEY)
    if DEBUG:
        print("Video Details:")
        print(df_video_details)

    df_subtitles = fetch_transcripts.extract_subtitles_from_video(all_video_ids)
    result = pd.merge(df_video_details, df_subtitles, on="video_id", how="outer")

    print("-" * 30)
    print(f"Final Result:\n{result[['video_id', 'title', 'subtitles']]}")
    print("-" * 30)
