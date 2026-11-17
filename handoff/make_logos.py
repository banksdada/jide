import math, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

import os
HERE=os.path.dirname(os.path.abspath(__file__))
FD=os.path.join(HERE,'node_modules/@fontsource/bodoni-moda/files/')
def font(w,s='normal'): return TTFont(FD+'bodoni-moda-latin-%d-%s.woff'%(w,s))

def text_path(f, txt, size, x, y, track=0, anchor='start'):
    gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; sc=size/upm
    adv=[f['hmtx'][cmap[ord(c)]][0]*sc+track for c in txt]
    total=sum(adv)-track
    if anchor=='middle': x-=total/2
    d=''; cx=x
    for c,a in zip(txt,adv):
        pen=SVGPathPen(gs, ntos=lambda v:('%.2f'%v).rstrip('0').rstrip('.'))
        tp=TransformPen(pen,(sc,0,0,-sc,cx,y))
        gs[cmap[ord(c)]].draw(tp); d+=pen.getCommands(); cx+=a
    return d,total

GOLD='#c9a24b'; BRASS='#e6c987'; INK='#0e0a07'
f500=font(500); f600=font(600); f500i=font(500,'italic')

def defs(uid):
    return ('<defs><linearGradient id="g%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1dba0"/>'
            '<stop offset=".55" stop-color="#c9a24b"/><stop offset="1" stop-color="#a8832f"/></linearGradient></defs>')%uid

# ---------- Logo 1: monogram with circular sound ring ----------
def monogram(bg=True, ticks=48, size=240, uid='m'):
    cx=cy=120
    heights=[]
    for i in range(ticks):
        t=i/ticks
        h=.5+.5*abs(math.sin(t*math.pi*5.0))*abs(math.cos(t*math.pi*1.5+.4))
        heights.append(h)
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" aria-label="Jide Arowolo">',defs(uid)]
    if bg: out.append('<rect width="240" height="240" rx="52" fill="%s"/>'%INK)
    out.append('<g class="logo-ring">')
    r0=86
    for i,h in enumerate(heights):
        a=2*math.pi*i/ticks-math.pi/2
        L=5+h*17
        x1=cx+r0*math.cos(a); y1=cy+r0*math.sin(a)
        x2=cx+(r0+L)*math.cos(a); y2=cy+(r0+L)*math.sin(a)
        out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#d6b45f" stroke-width="3.2" stroke-linecap="round"/>'%(x1,y1,x2,y2))
    out.append('<circle cx="120" cy="120" r="78" fill="none" stroke="%s" stroke-opacity=".55" stroke-width="1.2"/>'%GOLD)
    out.append('</g>')
    dj,wj=text_path(f600,'J',104,0,0); da,wa=text_path(f600,'A',104,0,0)
    tot=wj+wa-10
    x0=120-tot/2
    dj,_=text_path(f600,'J',104,x0,152); da,_=text_path(f600,'A',104,x0+wj-10,152)
    out.append('<path class="logo-ja" d="%s%s" fill="url(#g%s)"/>'%(dj,da,uid))
    out.append('</svg>')
    return ''.join(out)

# ---------- Logo 2: wordmark with waveform underline ----------
def wordmark(uid='w', bg=False):
    SZ=64; TR=10; GAP=30
    d1,w1=text_path(f500,'JIDE',SZ,0,0,track=TR)
    d2,w2=text_path(f500,'AROWOLO',SZ,0,0,track=TR)
    total=w1+GAP+w2; W=round(total+40); H=130
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Jide Arowolo">'%(W,H),defs(uid)]
    if bg: out.append('<rect width="%d" height="%d" fill="%s"/>'%(W,H,INK))
    x0=(W-total)/2
    d1,_=text_path(f500,'JIDE',SZ,x0,62,track=TR)
    d2,_=text_path(f500,'AROWOLO',SZ,x0+w1+GAP,62,track=TR)
    out.append('<path d="%s%s" fill="url(#g%s)"/>'%(d1,d2,uid))
    n=69; cx=W/2; span=total
    for i in range(n):
        t=(i-(n-1)/2)/((n-1)/2)
        env=math.cos(t*math.pi/2)**1.3
        wob=.5+.5*abs(math.sin(i*.9)*math.cos(i*.37))
        h=2.5+30*env*wob
        x=cx+t*span/2
        out.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#d6b45f" stroke-width="1.8" stroke-linecap="round"/>'%(x,100-h/2,x,100+h/2))
    out.append('</svg>')
    return ''.join(out)

# favicon: JA on ink, thin wave under
def favicon():
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="%s"/>'%INK]
    dj,wj=text_path(f600,'J',38,0,0); 
    tot=wj+text_path(f600,'A',38,0,0)[1]-3; x0=32-tot/2
    dj,_=text_path(f600,'J',38,x0,40); da,_=text_path(f600,'A',38,x0+wj-3,40)
    out.append('<path d="%s%s" fill="%s"/>'%(dj,da,GOLD))
    for i,h in enumerate([4,8,12,8,14,9,5,10,6,3]):
        x=12+i*4.4
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" stroke-linecap="round"/>'%(x,52-h/2,x,52+h/2,GOLD))
    out.append('</svg>')
    return ''.join(out)

if __name__=='__main__':
    O=os.path.join(HERE,'..','logo')+os.sep
    open(O+'ja-monogram.svg','w').write(monogram(bg=True,uid='a'))
    open(O+'ja-monogram-transparent.svg','w').write(monogram(bg=False,uid='b'))
    open(O+'ja-monogram-nav.svg','w').write(monogram(bg=False,ticks=32,uid='n'))
    open(O+'jide-arowolo-wordmark.svg','w').write(wordmark(uid='c'))
    open(O+'favicon.svg','w').write(favicon())
