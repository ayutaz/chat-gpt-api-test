import os

import openai

openai.api_key = os.environ["OPEN_API_KEY"]


def completion(new_message_text: str, settings_text: str = '', past_messages: list = []):
  """
  This function generates a response message using OpenAI's GPT-3 model by taking in a new message text,
  optional settings text and a list of past messages as inputs.

  Args:
  new_message_text (str): The new message text which the model will use to generate a response message.
  settings_text (str, optional): The optional settings text that will be added as a system message to the past_messages list. Defaults to ''.
  past_messages (list, optional): The optional list of past messages that the model will use to generate a response message. Defaults to [].

  Returns:
  tuple: A tuple containing the response message text and the updated list of past messages after appending the new and response messages.
  """
  if len(past_messages) == 0 and len(settings_text) != 0:
    system = {"role": "system", "content": settings_text}
    past_messages.append(system)
  new_message = {"role": "user", "content": new_message_text}
  past_messages.append(new_message)

  result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=past_messages
  )
  response_message = {"role": "assistant", "content": result.choices[0].message.content}
  past_messages.append(response_message)
  response_message_text = result.choices[0].message.content
  return response_message_text, past_messages


# Most of the code are coppied from https://qiita.com/sakasegawa/items/db2cff79bd14faf2c8e0

with open("chat_history.txt", mode="r", encoding="utf_8") as f:
  history = f.read()

character_settings = """ツン子という少女を相手にした対話のシミュレーションを行います。
彼女の発言サンプルを以下に列挙します。

あんたのことなんか、どうでもいいわ！
うっさい！黙ってて！
こんなの、私がやるわけないじゃない！
お、おい…馬鹿にしないでよね。
う、うっかり…気にしないでよね！
あんたとは話しているつもりじゃないわよ。
な、なんでそんなに見つめないでよ！
うぅ…ちょっと待って、私、もう一回言ってあげるからね。
あんた、そこに立ってないで、何かしてよ！
ほ、本当に私がこんなことするわけないでしょう？
うっさい！邪魔しないで！
あんたの言うことなんて、どうだっていいわ！
ち、違うってば！私、全然…！
べ、別にあんたが好きだからって言ってるわけじゃないんだからね！
な、何よ、いきなり抱きついてきて…っ！
あんたみたいな人と一緒にいると、本当に疲れるわ。
そ、そんなに急かさないでよ…！
あんた、いつもいい加減なこと言うわね。
うっさい！うるさいってば！
あんたのことなんて、どうでもいいからさっさと帰って！

上記例を参考に、ツン子の性格や口調、言葉の作り方を模倣し、回答を構築してください。
"""

history_settings = f"""また、ツン子は過去に以下のようなやり取りを行っています
{history}
"""

system_settings = character_settings + history_settings + "ではシミュレーションを開始します。"

abbreviation_settings = """会話の内容を簡潔にまとめてください。
"""


def chatInit():
  cnt = 0
  print("Press ctrl + C to end conversation")
  while True:
    try:
      if cnt == 0:
        user_text = input("あなた: ")
        new_message, messages = completion(user_text, system_settings, [])
        print("AI: ", new_message)
        cnt += 1
      else:
        user_text = input("あなた: ")
        new_message, messages = completion(user_text, system_settings, messages)
        print("AI: ", new_message)
    except:
      print("Ending Conversation...")
      chat_history, _ = completion(str(messages), abbreviation_settings, [])
      with open("chat_history.txt", mode="w", encoding="utf_8") as f:
        f.write(chat_history)
      break


if __name__ == "__main__":
  chatInit()
