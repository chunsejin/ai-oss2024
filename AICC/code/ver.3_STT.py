# Imports the convertion library
from moviepy.editor import VideoFileClip
import math
import os
import time
from pydub import AudioSegment
import boto3
import urllib.parse
import glob



# 1. mp4 -> mp3 변환
####################################################################
# 동영상 파일 경로
video_path = "your media file path in local"
# 저장할 폴더 경로
output_folder = "your local folder to save converted audio file "

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
# boto3를 사용하여 S3 클라이언트 생성
s3_client = boto3.client('s3', region_name='region',
                             aws_access_key_id='your aws access key id',
                             aws_secret_access_key='your key'
                             )
# AWS Transcribe 클라이언트 생성
transcribe = boto3.client('transcribe', region_name='region',
                          aws_access_key_id='your aws access key id',
                          aws_secret_access_key='your key'
                          )

# WAV 파일들이 위치한 폴더
wav_folder = 'WAV files were saved folder path'

# 해당 폴더 내 모든 WAV 파일 찾기
wav_files = glob.glob(wav_folder + '*.wav')

for wav_file in wav_files:
    # WAV 파일을 로드하고 모노로 변환
    sound = AudioSegment.from_wav(wav_file)
    sound = sound.set_channels(1)  # 모노로 설정

    # 임시 파일로 저장
    temp_file = "temp_mono.wav"

    # 업로드할 파일의 경로와 S3 버킷 및 객체 키 이름 지정
    bucket_name = 'your bucket name'
    object_name = 'Path to the file within the bucket to upload from a local wav file.' # S3 내에서의 파일 경로 및 이름

    # 파일을 S3 버킷으로 업로드
    s3_client.upload_file(temp_file, bucket_name, object_name)
    print(f"File {temp_file} uploaded to {bucket_name}/{object_name}")

    # 변환할 오디오 파일의 S3 버킷 URL
    file_uri = 'bucket URL'

    # Transcribe 작업 이름 (유니크해야 함)
    job_name = "aicc_transcribe-" + str(int(time.time()))

    # 작업 시작
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav', # 오디오 파일 형식
        LanguageCode='en-US' # 사용하는 언어 코드. 예: 'en-US', 'ko-KR' 등
    )

    # 작업 상태 확인을 위한 대기
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Waiting for transcription to complete...")
        time.sleep(15)

    # 작업 완료 후 결과 처리
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # 결과 파일을 처리하기 위한 코드를 여기에 추가합니다.
        print(f"Transcription completed. Transcript file: {transcript_file_uri}")
    else:
        print("Transcription failed.")

# 임시 파일 제거
if os.path.exists(temp_file):
    os.remove(temp_file)
####################################################################

