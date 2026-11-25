import numpy as np, wave
src=open('audio_h.py').read().split('# 写真スライド型')[0].replace('DUR=26.0','DUR=17.0')
exec(src)
# 得する話：明るい和音（C-G-Am-F）・少し速め。場面ごとに軽いポップ音
C3,G2,A2,F2,E3,G3,A3,C4,D4,E4,F3,B3,D3,F4,G4=130.8,98,110,87.3,164.8,196,220,261.6,293.7,329.6,174.6,246.9,146.8,349.2,392
prog=[(C3,G3,C4,E4,G4),(G2,D3,B3,D4,G4),(A2,E3,A3,C4,E4),(F2,C3,A3,C4,F4)]
bar=DUR/10
for k in range(10): put(pad(prog[k%4],bar+0.6),k*bar,0.15)
step=bar/4
for k in range(int(DUR/step)):
    ch=prog[int(k*step/bar)%4]; f=ch[[1,3,2,4][k%4]]*2
    put(tone(f,1.0,0.004,0.4),k*step,0.11,0.3+0.4*((k*5)%4)/3)
    if k%2==0: put(pop(0.05),k*step,1,0.5)
CUTS=(1.0,2.4,5.2,8.0,10.8,13.0,14.6)
for a in CUTS: put(swell(0.35,0.18),a-0.3,1); put(shimmer(0.5,0.06),a,1)
put(boom(0.5),0,0.6); put(chime(1046.5,0.16),0.02)
for i,a in enumerate((2.5,5.3,8.1)): put(chime([1046.5,1174.7,1318.5][i],0.18),a)
put(boom(0.4),10.9,0.6); put(chime(1568,0.16),13.3)
put(pop(0.15),15.4); put(pop(0.15),15.7); put(chime(2093,0.12),15.8)
x=np.stack([L,R],1); x=np.tanh(x*1.1)*0.86; f=int(0.6*SR); x[-f:]*=np.linspace(1,0,f)[:,None]
w=wave.open('new1125.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
print('peak',float(np.abs(x).max()))
