import pafy
import vlc
import time

url = "https://www.youtube.com/watch?v=G-T3qKl6y-c"            
video = pafy.new(url)
media = vlc.MediaPlayer(video.streams[0].url)
media.play()
print('Opened Video')
time.sleep(2000)