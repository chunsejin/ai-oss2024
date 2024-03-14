# Imports the convertion library
from moviepy.editor import VideoFileClip
import math
import os

# google cloud STT & etc...
from pydub import AudioSegment
from google.cloud import speech
from google.oauth2 import service_account
import glob



# 1. mp4 -> mp3 변환
####################################################################
# 동영상 파일 경로
video_path = "mp4 file 저장 경로"

# 저장할 폴더 경로
output_folder = "data/"

# 동영상 파일 로드
clip = VideoFileClip(video_path)

# 동영상의 총 길이(초)
duration = clip.duration

# 40초 간격으로 분할
interval = 40   # 40초

# 분할된 파일의 수 계산
num_clips = math.ceil(duration / interval)

# 분할 및 저장
for i in range(num_clips):
    # 시작 및 종료 시간 계산
    start_time = i * interval
    end_time = min((i + 1) * interval, duration)
    
    # 분할된 오디오 클립 생성
    audio_clip = clip.subclip(start_time, end_time).audio
    
    # WAV 파일로 저장
    output_path = f"{output_folder}output_segment_{i + 1}.wav"
    audio_clip.write_audiofile(output_path, codec='pcm_s16le')  # WAV 형식으로 저장

print(f"분할 완료: 총 {num_clips}개의 파일이 생성되었습니다.")

####################################################################



# 2. convert to STT
####################################################################
# 서비스 계정 키와 관련된 설정
service_account_file = 'google cloud API key [.json]'
credentials = service_account.Credentials.from_service_account_file(service_account_file)
client = speech.SpeechClient(credentials=credentials)

# WAV 파일들이 위치한 폴더
wav_folder = 'data/'

# 해당 폴더 내 모든 WAV 파일 찾기
wav_files = glob.glob(wav_folder + '*.wav')

for wav_file in wav_files:
    # WAV 파일을 로드하고 모노로 변환
    sound = AudioSegment.from_wav(wav_file)
    sound = sound.set_channels(1)  # 모노로 설정

    # 임시 파일로 저장
    temp_file = "temp_mono.wav"
    sound.export(temp_file, format="wav")
    
    # 임시 파일로부터 오디오 데이터 읽기
    with open(temp_file, "rb") as audio_file:
        content = audio_file.read()
        
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,  # 실제 샘플 레이트에 맞게 설정
        language_code="en-US",  # 언어를 영어로 설정
    )

    # STT 요청 및 응답 처리
    response = client.recognize(config=config, audio=audio)
    
    # 결과 출력
    print(f"파일: {wav_file}")
    for result in response.results:
        print(f"Transcription: {result.alternatives[0].transcript}")

# 임시 파일 제거
if os.path.exists(temp_file):
    os.remove(temp_file)
####################################################################