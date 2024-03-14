from moviepy.editor import VideoFileClip
import os

# 1. mp4 -> mp3 변환
####################################################################
# 파일 경로
file_path = "you are 'sampleVideo.mp4' file path"
# 파일 이름 추출 (확장자 제외)
file_name_without_ext = os.path.basename(file_path).rsplit('.', 1)[0]
# 출력 파일 경로 생성 - "C:/Users/win/Desktop/data" 폴더 내에 같은 파일 이름으로 .mp3 확장자 사용
output_path = f"'save file path'/{file_name_without_ext}.mp3"

# 비디오 파일 로드
clip = VideoFileClip(file_path)
# 오디오 추출 및 지정된 경로에 mp3 파일로 저장
clip.audio.write_audiofile(output_path)
####################################################################



# 2. convert to STT
####################################################################


####################################################################
