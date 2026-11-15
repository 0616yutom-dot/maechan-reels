import numpy as np, wave
SR=44100; rng=np.random.default_rng(3); DUR=26.0; n=int(DUR*SR); L=np.zeros(n); R=np.zeros(n)
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


# 写真スライド型の音：落ち着いたピアノ風。ネタの雰囲気で和音(prog)・速さ(bar)を変えて作り分ける
F2,A2,C3,E3,G2,B2,D3,E2,G3,A3,B3,C4,D4,E4=87.3,110,130.8,164.8,98,123.5,146.8,82.4,196,220,246.9,261.6,293.7,329.6
prog=[(F2,C3,A3,C4,E4),(G2,D3,G3,B3,D4),(E2,B2,G3,B3,D4),(A2,E3,A3,C4,E4)]
bar=DUR/8
for k in range(8): put(pad(prog[k%4],bar+0.9),k*bar,0.18)
step=bar/6
for k in range(int(DUR/step)):
    ch=prog[int(k*step/bar)%4]; f=ch[[1,2,3,4,3,2][k%6]]*2
    put(tone(f,1.6,0.004,0.6),k*step,0.10,0.3+0.4*((k*7)%5)/4)
CUTS=(1.6,3.8,6.7,9.6,12.5,14.8,20.0,22.3)          # 場面の切り替わり
for a in CUTS: put(swell(0.6,0.22),a-0.5,1); put(shimmer(0.8,0.07),a,1)
put(boom(0.7),0,0.7); put(boom(0.5),13.2,0.7); put(boom(0.5),20.2,0.7)
for i,a in enumerate((4.0,6.9,9.8)): put(chime([880,987.8,1174.7][i],0.16),a)
for i,a in enumerate((15.8,16.8,17.8)): put(chime([1046.5,1174.7,1318.5][i],0.16),a)
put(chime(1318.5,0.18),20.2); put(pop(0.15),24.0); put(pop(0.15),24.3); put(pop(0.15),24.6); put(chime(1568,0.14),24.4)
x=np.stack([L,R],1); x=np.tanh(x*1.1)*0.86; f=int(0.8*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
w=wave.open('h.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('peak',float(np.abs(x).max()))
