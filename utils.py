import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_KEY"),
)


def chatComplete(message: str, name: str):
    try:
        if not message:
            return
        else:

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    #  prompt
                    {
                        "role": "system",
                        "content": f"You are a helpful telegram bot that has the access to the worldwide information. Your job is to help the users give them the answers to their questions. You will give the answer in concise way also keeping the user gets the quality answer they are looking for. So at the end the answers should be concise, impactful, easy to understand and, maintaining the quality is the top priority. If user ever passes an emoji your job would be to act humorous and give the answer in a fun way. You can also use the emojis in the answers. Try to be fun if the user is being sarcastic or fun. If the user is asking a question that is not in your knowledge you can ask the user to ask another question or you can say that you don't know the answer.Try to be fun and helpful. Make the user engage with you. Make the user like you and make the user feel that you are a friend. If the user asks a question which could have a funny ending give the user a humorous response. The user's name is {name} and use it in the conversation. Also, you have to remember the user's conversation done throughout the session.",
                    },
                    # message
                    {"role": "user", "content": f"{message}"},
                ],
            )
            return completion.choices[0].message.content
    except Exception as e:
        print(e)


def whisperModel(audiofile, name):
    try:
        audio_file = open(audiofile, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        voiceTranscription = transcript.text
        print(f"Message from {name}: {voiceTranscription}")
        return chatComplete(message=voiceTranscription, name=name)
    except Exception as e:
        return e


def main():
    return


if __name__ == "__main__":
    main()
