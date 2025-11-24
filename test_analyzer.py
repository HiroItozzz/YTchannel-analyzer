import os
from analyzer import getPlaylistIds, getAllVideoIds
from dotenv import load_dotenv

VIDEO_IDS = ["-4cr9HQ0Uu0"]

load_dotenv()
API_KEY = os.environ["YOUTUBE_API_KEY"]
DEBUG = os.getenv("DEBUG", "False") == "True"


def test_getChannelIds():
    result = getPlaylistIds(VIDEO_IDS, API_KEY)

    assert len(result) > 0
    assert "playlist_id" in result.columns  # channel_id列がある
    assert result["playlist_id"].iloc[0] != ""  # 値が入っている


def test_getAllVideoIds():
    playlist_ids = getPlaylistIds(VIDEO_IDS, API_KEY)
    result = getAllVideoIds(playlist_ids["playlist_id"].to_list(), API_KEY)

    assert len(result) > 0
    assert "video_id" in result.columns  # video_id列がある
    assert result["video_id"].iloc[0] != ""  # 値が入っている


if __name__ == "__main__":
    test_getChannelIds()
    test_getAllVideoIds()
