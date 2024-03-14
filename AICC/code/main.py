from moviepy.editor import VideoFileClip

# 1. mp4 -> mp3 변환
####################################################################
# 파일 경로
file_path = "C:/Users/win/Desktop/project/sampleVideo.mp4"

# 출력 파일 경로 (확장자를 제외한 파일 이름 + .mp3)
output_path = file_path.rsplit('.', 1)[0] + ".mp3"

# 비디오 파일 로드
clip = VideoFileClip(file_path)

# 오디오 추출 및 mp3 파일로 저장
clip.audio.write_audiofile(output_path)
####################################################################

