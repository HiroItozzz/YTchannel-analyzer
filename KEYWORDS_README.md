"""
keywords.py クイックリファレンス

詳しくは README.md を参照してください。
"""

# インポート

from keywords import analyze_by_keywords, count_keywords_in_category, is_category
from keywords import KEYWORD_CATEGORIES

# 基本的な使い方

text = "医師が重症の病気を診断した"

# 1. カテゴリに含まれるか確認

if is_category(text, "medical"):
print("医療関連です")

# 2. キーワード出現回数

count = count_keywords_in_category(text, "medical")
print(f"医療キーワード: {count}個")

# 3. DataFrame 分析

import pandas as pd

df = pd.DataFrame({
'video_id': ['vid001'],
'transcript': ['医師が重症の病気を診断した'],
'duration': [900] # 秒
})

analyze_by_keywords(df, "medical", threshold=0.5)
print(df[['video_id', 'medical_per_min', 'is_medical']])

# 複数カテゴリ分析

for category in KEYWORD_CATEGORIES.keys():
analyze_by_keywords(df, category=category)
