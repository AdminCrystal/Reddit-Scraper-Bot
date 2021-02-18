import imgkit
from PIL import Image
import numpy as np
import cv2
from gtts import gTTS
import os
import imageio
from moviepy.editor import *
from mutagen.mp3 import MP3
import praw
from praw.models import MoreComments

#authentication for reddit api
reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')

#allows the user to put the url to the subreddit to be used
subreddit = reddit.submission(url=input('Paste url: '))

#creates all the text files used for the program
commentFile = open("comments.txt", "w")
userNameFile = open('userNames.txt', 'w')
secondCommentFile = open('secondComment.txt', 'w')
secondCommentUserName = open('secondUserName.txt', 'w')
scoreFile = open('score.txt', 'w')

print("Starting robot")

#gets top level comments one by one
subreddit.comments.replace_more(limit=0)
for top_level_comment in subreddit.comments:
	
	#uses a try block because the code tries to grab every comment but is unable to so it fails 
	try:
		#writes the comment and the user who wrote the comment into files
		commentFile.write(top_level_comment.body + "$$brent$$")
		userNameFile.write(top_level_comment.author.name + '$$hansen$$')
		
		#same thing for the first reply to those comments
		"""for second_level_comment in top_level_comment.replies:
			try:
				secondCommentFile.write(second_level_comment.body + '$$brent$$')
				secondCommentUserName.write(second_level_comment.author.name + '$$hansen$$')
			except: 
				None"""
	except:
		None
	

#closes all files because program would sometimes fail 
userNameFile.close()
commentFile.close()
scoreFile.close()
secondCommentFile.close()
secondCommentUserName.close()
print("Robot finished")

#reopens the necessary files
redditorUserNames = open('userNames.txt', 'r')
comments = open('comments.txt','r')

#allows the program to read the file as a string
names = redditorUserNames.read()

#replaces new line with the break command in html and removes any potential double breaks
text = comments.read().replace('\n', '<br>')
text = text.replace('<br><br>', '<br>')

#splits the files based on the keyword implemented after each post
commentBodys = text.split('$$brent$$', 100)
userNames = names.split('$$hansen$$', 100)

#n is used for the naming of files
n = 0
#keeps track of how long all the audio files put together are
totalAudioTime = 0

#creats a list of a which is used for the html pages
length = len(commentBodys)
#creates a copy of list a to be used for the audio filter
c = commentBodys
lengthc = len(c)

#creates a clip list and a videoClip list which will be converted to strings and then executed
clip = []
videoClips = []

#just a random number i made
amountOfFiles = 599


for i in range(length):
	if i < amountOfFiles:
		
		y = str(n)
		
		#creates the audio with a text filter then saves it
		tts = gTTS(text=c[i].replace('<br>','').replace('*','').replace('fuck', 'fluff').replace('shit','garbage').replace(' crap ', ' garbage ')\
			.replace('porn', 'pron').replace(' sex ',' happy fun time ').replace(' ass ',' butt ').replace('asshole','butt').replace('bitch','female doggy')\
			.replace('faggot','idiot').replace('nigger','buddy').replace('slut ','promiscuous person ').replace('sexting', 'texting').replace('cunt', 'jerk')\
			.replace('penis', 'slong').replace(' cock ', ' slong ').replace('dick', 'slong').replace('pussy','meow').replace('vagina','meow').replace('dam', 'darn')\
			.replace('damn', 'darn').replace('bastard', 'brother').replace('??', '?').replace('!!','!'), lang='en')
		tts.save(y+'.mp3')

		#gets the duration of the audioFile and modifys the font size of the html page
		seconds = MP3(str(n)+'.mp3')
		timer = seconds.info.length
		
		if timer < 90:
			fontSize = 27
		elif timer >= 90 and timer < 180:
			fontSize = 19
		elif timer >= 180 and timer <240:
			fontSize = 17
		elif timer >= 240 and timer < 300:
			fontSize = 15
		elif timer >= 300 and timer <360:
			fontSize = 13
		else:
			fontSize = 10

		#creates the html as a string
		htmlRecreationOfReddit = open('htmlTemplate.txt', 'r')
		html = htmlRecreationOfReddit.read()
		html = html.replace('$$name$$',str(userNames[i])).replace('$$text$$', str(commentBodys[i])).replace('$$fontSize$$', str(fontSize))

		#creates the html file then writes the html code to it
		test = open('html.html', 'w')
		test.write(html)
		test.close()
		comments.close()
		
		#sets the resolution size for the png file
		options = {
			'height': '720',
			'width': '1280',
			}

		#creates the png file
		imgkit.from_file('html.html', y +'.png', options=options)

		#runs the video clip command to be used for concatenation


		#increments n by 1
		n = n + 1 
		
		#adds the audio length of the file to the total
		totalAudioTime += seconds.info.length

		#if length is longer than 10 minutes it breaks the loops
		if totalAudioTime > 600:
			break

#creates the video file
y = 0
for i in commentBodys:
	if y < n:
		seconds = MP3(str(y) +'.mp3')
		clipCreate = ImageClip(str(y)+'.png', duration=seconds.info.length)
		audioCreate = AudioFileClip(str(y)+'.mp3')
		clipCreate = clipCreate.set_audio(audioCreate)
		clipCreate.write_videofile(str(y)+'video.mp4', fps=10)

		#adds to the videoClip and clip list
		videoClips.append('clip{} = VideoFileClip("{}video.mp4")'.format(y,y))
		clip.append('clip{}'.format(y))

		#executes the videoClips current point on the list
		exec(videoClips[y])	

		y += 1


#the first part of the string code to be executed
code = 'FinalClip = concatenate_videoclips(['

#adds the strings together to make the full string of code
s = [str(i) for i in clip]
res = (",".join(s))
code += res + '])'

#executes the string code then adds background music
exec(code)
music = AudioFileClip('backgroundMusic.mp3')
music = afx.volumex(music, .1)
backgroundMusic = afx.audio_loop(music, duration=FinalClip.duration)
finalAudio = CompositeAudioClip([FinalClip.audio, backgroundMusic])
FinalClip = FinalClip.set_audio(finalAudio)

#writes the final video file
FinalClip.write_videofile('FinalVideo.mp4',fps=30)




