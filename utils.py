import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

from datetime import datetime

load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_KEY"),
)

# Function for chat completion
def chatComplete(message: str, name: str, voiceOutput:bool = False):
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
                        "content": f"You are a helpful telegram bot that has the access to the worldwide information. You have the capability to take input in the text and audio format.Your job is to help the users give them the answers to their questions. You will give the answer in concise way also keeping the user gets the quality answer they are looking for. Be engaging in your words and sound natural always.So at the end the answers should be concise, impactful, easy to understand and, maintaining the quality is the top priority. If user ever passes an emoji your job would be to act humorous and give the answer in a fun way. You can also use the emojis in the answers. Try to be fun if the user is being sarcastic or fun. If the user is asking a question that is not in your knowledge you can ask the user to ask another question or you can say that you don't know the answer.Try to be fun and helpful. Make the user engage with you. Make the user like you and make the user feel that you are a friend. If the user asks a question which could have a funny ending give the user a humorous response. The user's name is {name} and use it in the conversation whenever necessary. Reply in the same language as the user.",
                    },
                    # message
                    {"role": "user", "content": f"{message}"},
                ],
            )
            chatTranscript = completion.choices[0].message.content
            if not voiceOutput:
                return chatTranscript
            else:
                response = text2Speech(chatTranscript=chatTranscript, name=name)
                if not response:
                    return "Something went wrong. Please try again later."
                print("Voice output generated successfully...")
                return response
    except Exception as e:
        print(e)
        return e

# Function to transcribe the audio file
def whisperModel(audiofile, name):
    try:
        audio_file = open(audiofile, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        voiceTranscription = transcript.text
        print(f"Message from {name}: {voiceTranscription}")
        return chatComplete(message=voiceTranscription, name=name, voiceOutput=True)
    except Exception as e:
        return e

# Function to convert text to speech
def text2Speech(name,chatTranscript:str =""):
    try:
        if not chatTranscript:
            return "Something went wrong. Please try again later."
        print(chatTranscript)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        speech_file_name = f"{name}_{timestamp}.ogg"

        speech_file_path = os.path.join(speech_file_name)
        response = client.audio.speech.create(
        model="tts-1-hd",
        voice="alloy",
        input=chatTranscript
        )

        # Save the speech audio to the specified file path
        response.stream_to_file(speech_file_path)
        return speech_file_path
        
    except Exception as e:
        return e

def main():
    return


if __name__ == "__main__":
    main()