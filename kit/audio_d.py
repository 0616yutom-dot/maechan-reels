import numpy as np, wave
SR=44100; rng=np.random.default_rng(3); DUR=29.0; n=int(DUR*SR); L=np.zeros(n); R=np.zeros(n)
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

A2,C3,E3,G3,B3,F2,A3,C4,E4,G2,D3,D4=110,130.8,164.8,196,246.9,87.3,220,261.6,329.6,98,146.8,293.7
prog=[(A2,E3,G3,B3,C4),(F2,C3,A3,C4,E4),(C3,G3,C4,E4,261.6),(G2,D3,G3,B3,D4)]
bar=DUR/8
for k in range(8): put(pad(prog[k%4],bar+0.9),k*bar,0.17)
step=bar/8
for k in range(int(DUR/step)):
    ch=prog[int(k*step/bar)%4]; f=ch[[1,2,3,4,3,2,4,3][k%8]]*2
    put(tone(f,1.2,0.004,0.45),k*step,0.085,0.3+0.4*((k*7)%5)/4)
for a,g in [(0,0.9),(1.3,0.7),(2.5,1.1),(4.8,0.7),(7.8,0.8),(10.0,0.9),(12.9,1.1),(15.4,0.9),(23.25,0.9)]: put(boom(g),a,0.75)
for a in (3.65,6.65,11.05,14.65,18.65,22.85,24.85): put(swell(),a-0.45,1); put(shimmer(),a,1)
for k in range(20): put(pop(0.07+0.006*k),1.5+k*0.05)          # 455のカウント
for k in range(13): put(chime(660*2**(k/12),0.10),11.6+k*0.1)   # 13年の目盛り
for a in (4.0,6.85,7.05,13.3,13.5,21.7,21.9): put(pop(),a)
for i,a in enumerate((19.5,20.25,21.0)): put(chime([880,987.8,1318.5][i]),a); put(boom(0.4),a,0.6)
for i in range(5): put(pop(0.2),25.0+i*0.1)
put(chime(1318.5),2.5,1.0); put(chime(1975.5,0.14),2.62); put(chime(1046.5),10.0); put(chime(1318.5),15.3)
put(chime(1046.5),23.1); put(pop(0.2),27.0); put(pop(0.2),27.32); put(chime(1318.5),27.7); put(chime(1975.5,0.13),27.85)
x=np.stack([L,R],1); x=np.tanh(x*1.1)*0.86; f=int(0.5*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
w=wave.open('d.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('peak',float(np.abs(x).max()))
