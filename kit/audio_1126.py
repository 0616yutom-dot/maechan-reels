import numpy as np, wave
SR=44100; rng=np.random.default_rng(3); DUR=18.0; n=int(DUR*SR); L=np.zeros(n); R=np.zeros(n)
def put(x,at,g=1,pan=0.5):
    i=int(at*SR); j=min(n,i+len(x))
    if 0<=i<n: L[i:j]+=x[:j-i]*g*(1-pan)*2**0.5; R[i:j]+=x[:j-i]*g*pan*2**0.5
def lp(x,k): return np.convolve(x,np.ones(k)/k,mode='same')
def tone(f,dur,a=0.02,d=0.8,h=(1,0.35,0.12,0.05)):
    m=int(dur*SR); t=np.arange(m)/SR
    return sum(w*np.sin(2*np.pi*f*(k+1)*t)*np.exp(-t/(d/(k+1))) for k,w in enumerate(h))*np.minimum(t/a,1)
def pad(freqs,dur):
    m=int(dur*SR); t=np.arange(m)/SR; e=np.minimum(t/0.6,1)*np.minimum((dur-t)/0.8,1)
    return sum(np.sin(2*np.pi*f*t+0.3*np.sin(2*np.pi*0.25*t+i))+0.3*np.sin(2*np.pi*f*2.003*t) for i,f in enumerate(freqs))*e/len(freqs)
def boom(amp=1):
    m=int(1.4*SR); t=np.arange(m)/SR
    return amp*(np.sin(2*np.pi*np.cumsum(36+50*np.exp(-t/0.07))/SR)*np.exp(-t/0.38)+lp(rng.standard_normal(m),30)*np.exp(-t/0.12)*0.8)
def shimmer(dur=0.9,amp=0.12):
    m=int(dur*SR); t=np.arange(m)/SR; x=rng.standard_normal(m); x=x-lp(x,6)
    return amp*x*np.sin(np.pi*t/dur)**2
def swell(dur=0.5,amp=0.35):
    m=int(dur*SR); t=np.arange(m)/SR; x=lp(rng.standard_normal(m),50)
    return amp*4*x*(t/dur)**3
def chime(f,amp=0.22): return amp*tone(f,1.4,0.004,0.5,(1,0.5,0.25,0.12,0.06))
def pop(amp=0.25):
    m=int(0.09*SR); t=np.arange(m)/SR; return amp*np.sin(2*np.pi*(420+900*np.exp(-t/0.02))*t)*np.exp(-t/0.025)


# 11/26 冬のお風呂：あたたかく、ゆっくり。低めの和音（D→Bm→G→A）＋水滴のような高い音
D2,Fs2,A2,B1,G2,D3,Fs3,A3,B3,Cs4,D4,E4,Fs4,G3,E3,A1=73.4,92.5,110,61.7,98,146.8,185,220,246.9,277.2,293.7,329.6,370,196,164.8,55
prog=[(D2,A2,Fs3,A3,D4),(B1,Fs2,D3,Fs3,B3),(G2,D3,G3,B3,D4),(A1*2,E3,A3,Cs4,E4)]
bar=DUR/6
for k in range(6): put(pad(prog[k%4],bar+0.9),k*bar,0.20)
step=bar/4
for k in range(int(DUR/step)):
    ch=prog[int(k*step/bar)%4]; f=ch[[2,4,3,4][k%4]]*2
    put(tone(f,2.0,0.006,0.8),k*step,0.085,0.3+0.4*((k*3)%5)/4)
def drop(f,amp=0.14):
    m=int(0.5*SR); t=np.arange(m)/SR
    return amp*np.sin(2*np.pi*(f+f*0.5*np.exp(-t/0.03))*t)*np.exp(-t/0.12)
CUTS=(1.1,2.7,5.5,8.5,11.1,13.1,14.9)
for a in CUTS: put(swell(0.6,0.16),a-0.5,1); put(shimmer(0.8,0.05),a,1)
put(boom(0.5),0,0.7); put(chime(1174.7,0.14),0.05); put(boom(0.45),1.5,0.7)
for i,a in enumerate((2.9,5.7,8.7)): put(drop([1174.7,1318.5,1480][i]),a); put(chime([587.3,659.3,740][i],0.13),a+0.2)
put(chime(880,0.12),11.4); put(boom(0.4),13.3,0.7); put(chime(1174.7,0.16),13.3)
put(pop(0.15),16.2); put(pop(0.15),16.5); put(pop(0.15),16.8); put(chime(1480,0.12),16.9)
x=np.stack([L,R],1); x=np.tanh(x*1.1)*0.86; f=int(0.8*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
w=wave.open('new1126.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('peak',float(np.abs(x).max()))
