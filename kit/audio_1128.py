import numpy as np, wave
SR=44100; rng=np.random.default_rng(28); DUR=19.0; n=int(DUR*SR); L=np.zeros(n); R=np.zeros(n)
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
# 11/27 お金の掛け算：少し速め・低めの響きで始まり、明るい和音で終わる（A小調→C）
A1,E2,A2,C3,E3,F2,G2,D3,G3,A3,B3,C4,D4,E4,F3,C2=55,82.4,110,130.8,164.8,87.3,98,146.8,196,220,246.9,261.6,293.7,329.6,174.6,65.4
D2,Fs2,B2,Fs3,Cs4,Fs4=73.4,92.5,123.5,185,277.2,370
prog=[(D2,A2,D3,A3,Fs4),(B2/2*2,Fs3,B3,D4,Fs4),(G2,D3,G3,B3,D4),(A2,E3,A3,Cs4,E4)]
bar=DUR/8
for k in range(8): put(pad(prog[k%4],bar+0.8),k*bar,0.17)
step=bar/4
for k in range(int(DUR/step)):
    ch=prog[int(k*step/bar)%4]; f=ch[[4,2,3,2][k%4]]*2
    put(tone(f,1.2,0.004,0.45),k*step,0.09,0.3+0.4*((k*5)%4)/3)
for k in range(8): put(tone(prog[k%4][0],1.6,0.01,0.9,(1,0.5,0.2)),k*bar,0.16)
CUTS=(1.1,2.6,5.8,8.6,12.4,14.4,16.2)
for a in CUTS: put(swell(0.5,0.2),a-0.45,1); put(shimmer(0.7,0.06),a,1)
put(boom(0.8),0,0.7); put(boom(0.6),2.7,0.7); put(boom(0.4),14.5,0.7)
for k in range(10): put(pop(0.08),2.8+k*0.09)
put(chime(1174.7,0.22),3.7); put(chime(1480,0.14),3.9)
put(chime(880,0.14),6.2)
for i,a in enumerate((9.5,10.5)): put(chime([987.8,1174.7][i],0.16),a)
put(chime(1480,0.16),14.6)
put(pop(0.15),17.3); put(pop(0.15),17.6); put(chime(1760,0.14),17.7)
x=np.stack([L,R],1); x=np.tanh(x*1.1)*0.86; f=int(0.8*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
w=wave.open('new1128.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('peak',float(np.abs(x).max()))
