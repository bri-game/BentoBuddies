import wave,math,struct,pathlib
out=pathlib.Path(__file__).resolve().parents[1]/'assets/resources/audio';sr=22050
notes={'tap':([660],.09),'place':([523,784],.19),'rotate':([587,740],.14),'error':([262,220],.28),'win':([523,659,784,1047],.72)}
for name,(freqs,duration) in notes.items():
 samples=[]
 for i in range(int(sr*duration)):
  t=i/sr;j=min(len(freqs)-1,int(t/duration*len(freqs)));u=t-duration*j/len(freqs);e=math.exp(-u*17)*min(1,u*150);v=(math.sin(t*freqs[j]*math.tau)+.2*math.sin(t*freqs[j]*2*math.tau))*e*.3;samples.append(int(v*32767))
 with wave.open(str(out/(name+'.wav')),'wb') as f:f.setparams((1,2,sr,0,'NONE','not compressed'));f.writeframes(struct.pack('<'+'h'*len(samples),*samples))
duration=16;melody=[523,659,784,659,587,698,880,698,523,659,784,1047,784,659,587,392];samples=[]
for i in range(sr*duration):
 t=i/sr;j=int(t);u=t-j;f=melody[j];v=math.sin(t*f*math.tau)*math.exp(-u*5)*.13+math.sin(t*(130.813 if j<8 else 174.614)*math.tau)*.025*math.sin(math.pi*(t%duration)/duration)**2
 v*=min(1,t*5,(duration-t)*5);samples.append(int(v*32767))
with wave.open(str(out/'music.wav'),'wb') as f:f.setparams((1,2,sr,0,'NONE','not compressed'));f.writeframes(struct.pack('<'+'h'*len(samples),*samples))
