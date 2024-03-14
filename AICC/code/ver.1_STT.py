# Imports the convertion library
from moviepy.editor import VideoFileClip
import os

# python STT library
import speech_recognition as sr



# 1. mp4 -> mp3 변환
####################################################################
# 파일 경로 
file_path = "mp4 file 저장 경로" 
# 파일 이름 추출 (확장자 제외)
file_name_without_ext = os.path.basename(file_path).rsplit('.', 1)[0]
# 출력 파일 경로 생성 - "data" 폴더 내에 mp4와 같은 파일 이름으로 .wav 확장자 사용
output_path = f"data/{file_name_without_ext}.wav"

# 비디오 파일 로드
clip = VideoFileClip(file_path)
# 오디오 추출 및 지정된 경로에 wav 파일로 저장
clip.audio.write_audiofile(output_path)
####################################################################



# 2. convert to STT
####################################################################
# WAV 파일 경로
wav_file_path = "wav파일로 변환된 파일 경로"

# 오디오 인식기 생성
recognizer = sr.Recognizer()

# WAV 파일 열기
with sr.AudioFile(wav_file_path) as source:
    # 오디오 파일을 읽고 음성 데이터 추출
    audio_data = recognizer.record(source)

    # Google 웹 API를 사용하여 음성을 텍스트로 변환
    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        print("Transcript: {}".format(text))
    except sr.UnknownValueError:
        print("Google 웹 API에서 음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print("Google 웹 API에 대한 요청이 실패했습니다.: {}".format(e))
####################################################################
