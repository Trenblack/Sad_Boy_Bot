import moviepy.editor as mpe
import moviepy.video as mpv
from random import randint
from math import floor
from words import word_list



class Generator:
    def __init__(self, filename, audioname):
        self.total_duration = 0
        self.clip_list = []
        self.clip = mpe.VideoFileClip(filename)
        self.audio = mpe.AudioFileClip(audioname)
        self.overlay = mpe.VideoFileClip('overlay.mov').subclip().resize(self.clip.size).set_opacity(0.40)

    def audi_test(self):
        f = self.clip.set_audio(self.audio)
        f.write_videofile('out.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
    def create(self, desired_length):
        self.random_word_screen()
        while self.total_duration < desired_length:
            self.add_clip()
        final = mpe.concatenate_videoclips(self.clip_list)
        image = mpe.ImageClip('blue.png').resize(self.clip.size).set_opacity(0.35).set_duration(self.total_duration)
        final = mpe.CompositeVideoClip([final, image])
        self.audio = self.audio.set_duration(self.total_duration)
        final = final.set_audio(self.audio)
        final.write_videofile('output_file.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    def add_clip(self):
        r = randint(0, floor(self.clip.duration-10))
        subclip = self.clip.subclip(r, r+(r%10))
        merged = mpe.CompositeVideoClip([subclip, self.overlay.subclip(2, 2+r%10)])
        if r%2==0: #adds a fade_in transition if r is even.
            merged = mpv.fx.all.fadein(merged, 3)
        self.clip_list.append(merged)
        self.total_duration += r%10

    def random_word_screen(self):
        r = randint(0, len(word_list))
        word = word_list[r]
        spaced_word = '  '.join([e for e in word])
        clip = mpe.TextClip(spaced_word, fontsize = 70, color = 'white',size=self.clip.size,bg_color = 'black',method='caption',align='center').set_duration(2)
        self.clip_list.append(clip)
        self.total_duration += 2
    
movie_name = input("Filename of Movie?")
music = input("Filename of music?")
desired_duration = int(input("Desired edit duration in seconds?"))

g = Generator(movie_name, music)
g.create(desired_duration)
