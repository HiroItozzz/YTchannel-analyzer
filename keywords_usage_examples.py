"""
keywords.py の参照方法サンプル

このファイルでは keywords.py をインポートして使う基本的なパターンを示します。
"""

# ============================================
# 基本的なインポート方法
# ============================================

# 方法1: 関数をインポート
from keywords import classify_text, count_keywords_in_category, is_category

# 方法2: キーワード辞書をインポート
from keywords import (
    KEYWORD_CATEGORIES,
    medical_keywords,
    legal_keywords,
    daily_surprising_keywords,
)

# 方法3: モジュール全体をインポート
import keywords


# ============================================
# 使用例
# ============================================


def example_1_basic_check():
    """例1: テキストが医療関連かチェック"""
    text = "医師の診断により重症の病気が判明した"

    # 関数を使う方法
    if is_category(text, "medical"):
        print(f"✓ 医療関連: {text}")

    # キーワード辞書を直接使う方法
    if any(w in text for w in medical_keywords):
        print(f"✓ (直接チェック) 医療関連: {text}")


def example_2_count_keywords():
    """例2: キーワード出現回数をカウント"""
    text = "病気で入院して治療を受けた。医師の診断は重症だった。"

    # 医療キーワード数
    medical_count = count_keywords_in_category(text, "medical")
    print(f"医療キーワード: {medical_count}個出現")

    # 法律キーワード数
    legal_count = count_keywords_in_category(text, "legal")
    print(f"法律キーワード: {legal_count}個出現")


def example_3_classify():
    """例3: テキストを複数カテゴリで分類"""
    text = "医療裁判で患者が勝訴し、奇跡的に意識が戻った"

    result = classify_text(text)
    print(f"\nテキスト: {text}")
    print("分類結果:")
    for category, info in result.items():
        if info["matched"]:
            print(f"  - {category}: {info['count']}個マッチ ✓")
        else:
            print(f"  - {category}: マッチなし")


def example_4_loop_categories():
    """例4: 全カテゴリをループして確認"""
    text = "殺人犯の逮捕が奇跡的に行われた"

    print(f"\nテキスト: {text}")
    print("各カテゴリのマッチ状況:")

    for category_name, keywords_set in KEYWORD_CATEGORIES.items():
        count = count_keywords_in_category(text, category_name)
        if count > 0:
            print(f"  {category_name}: {count}個のキーワードマッチ")


def example_5_dataframe_analysis():
    """例5: pandas DataFrame を使った分析（analyzer で使う想定）"""
    import pandas as pd
    from keywords import KEYWORD_CATEGORIES

    # サンプルDF
    df = pd.DataFrame(
        {
            "video_id": ["vid001", "vid002", "vid003"],
            "transcript": [
                "医師が重症の病気を診断した",
                "殺人事件で容疑者が逮捕された",
                "行方不明だった人が奇跡的に見つかった",
            ],
        }
    )

    # 各カテゴリのキーワード出現数を列として追加
    for category in KEYWORD_CATEGORIES.keys():
        df[f"{category}_count"] = df["transcript"].apply(
            lambda t: count_keywords_in_category(t, category)
        )

    # 各カテゴリのマッチ判定も追加
    for category in KEYWORD_CATEGORIES.keys():
        df[f"is_{category}"] = df["transcript"].apply(
            lambda t: is_category(t, category)
        )

    print("\n=== DataFrame 分析結果 ===")
    print(df)


# ============================================
# analyzer.py での使い方（想定例）
# ============================================


def analyze_with_keywords_example():
    """
    analyzer.py で実際に使う想定例

    get_video_details() から DataFrame を受け取って
    キーワード分析を追加する
    """
    from keywords import count_keywords_in_category, is_category

    # 仮想的な DataFrame（実際には get_video_details から取得）
    df = pd.DataFrame(
        {
            "video_id": ["abc123"],
            "title": ["医師が奇跡的に回復した患者を診断"],
            "transcript": ["医師が重症の患者の診断を行った..."],
        }
    )

    # キーワード分析を追加
    for category in KEYWORD_CATEGORIES.keys():
        df[f"keyword_{category}_count"] = df["transcript"].apply(
            lambda t: count_keywords_in_category(t, category)
        )
        df[f"contains_{category}"] = df["transcript"].apply(
            lambda t: is_category(t, category)
        )

    return df


# ============================================
# test.py での使い方（想定例）
# ============================================


def test_keywords_example():
    """
    test.py で keywords をテストする想定例
    """
    from keywords import classify_text, KEYWORD_CATEGORIES

    test_cases = [
        ("医療関連", "医師が重症の病気を診断"),
        ("法律関連", "殺人容疑で逮捕された"),
        ("日常の意外", "行方不明だった人が奇跡的に見つかった"),
        ("複合", "医療裁判で患者が勝訴し奇跡的に回復"),
    ]

    for case_name, text in test_cases:
        result = classify_text(text)
        print(f"\n[{case_name}] {text}")
        for cat, info in result.items():
            if info["matched"]:
                print(f"  ✓ {cat}: {info['count']}個")


if __name__ == "__main__":
    print("=" * 60)
    print("keywords.py 参照方法サンプル")
    print("=" * 60)

    print("\n【例1】基本的なチェック")
    example_1_basic_check()

    print("\n【例2】キーワード出現回数")
    example_2_count_keywords()

    print("\n【例3】複数カテゴリ分類")
    example_3_classify()

    print("\n【例4】全カテゴリループ")
    example_4_loop_categories()

    print("\n【例5】DataFrame分析")
    example_5_dataframe_analysis()
