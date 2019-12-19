from webcam.webcamCapture import webcam
from patrol.patrol import patrol
from slack.slack import slack

p = patrol()
p.start() #block
wc = webcam()
ret,frame = wc.capture()
frame = wc.resize(frame, 1920, 1080)
wc.save(frame, '.')

s = slack('ze', as_user=False, ask_confirmation=False)
s.upload()
