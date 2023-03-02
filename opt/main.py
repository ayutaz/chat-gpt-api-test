import os

import openai
openai.api_key = os.environ["OPEN_API_KEY"]
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "あなたは役に立つアシスタントです。"},
    {"role": "user", "content": "2021年の日本シリーズで優勝したのは?"},
    {"role": "assistant", "content": "2021年の日本シリーズで優勝したのは、東京ヤクルトスワローズです。"},
    {"role": "user", "content": "その球団の本拠地はどこですか?"}
  ]
)
print(response["choices"][0]["message"]["content"])