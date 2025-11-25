import fetch_transcripts
from pathlib import Path
import shutil

# テスト用一時ディレクトリ
tmp = Path("test_tmp")
tmp.mkdir(exist_ok=True)

try:
    # 1. テキスト抽出のテスト
    dummy_sub = tmp / "dummy.ja.srt"
    dummy_sub.write_text(
        "1\n00:00:00,000 --> 00:00:01,000\nHello\n\n"
        "2\n00:00:01,000 --> 00:00:02,000\nWorld\n"
    )

    text = fetch_transcripts.subtitle_file_to_text(dummy_sub)
    print(f"✓ 抽出テキスト: '{text}'")
    assert "Hello" in text and "World" in text, "テキスト抽出失敗"

    # 2. ファイル検出のテスト
    found = fetch_transcripts.find_downloaded_subfile("dummy", tmp)
    print(f"✓ ファイル検出: {found}")
    assert found is not None, "ファイル検出失敗"

    print("\n✅ 字幕取得部分のテスト全て成功")

finally:
    shutil.rmtree(tmp, ignore_errors=True)
