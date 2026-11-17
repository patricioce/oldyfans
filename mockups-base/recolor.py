import cv2, numpy as np, sys
D='/tmp/claude-0/-home-user-oldyfans/156d809e-1f1a-5118-9555-6a24b416dda5/scratchpad/'
im=cv2.imread(D+'src.webp')
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV).astype(int)
raw=((hsv[...,1]<90)&(hsv[...,2]<120)).astype(np.uint8)
raw=cv2.morphologyEx(raw,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(raw,8)
big=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); m=(lab==big).astype(np.uint8)
# fill holes inside shirt (except label), smooth
n2,l2,s2,_=cv2.connectedComponentsWithStats((1-m).astype(np.uint8),4)
for i in range(1,n2):
    if s2[i,cv2.CC_STAT_AREA]<3000: m[l2==i]=1
# label: bright pixels near collar
white=((hsv[...,2]>150)&(hsv[...,1]<60)).astype(np.uint8); white[:150]=0; white[450:]=0; white[:,:850]=0; white[:,1150:]=0
ys,xs=np.nonzero(white); print('label bbox',xs.min(),xs.max(),ys.min(),ys.max())
hull=cv2.convexHull(np.stack([xs,ys],1)); lm=np.zeros_like(m); cv2.fillConvexPoly(lm,hull,1)
lm=cv2.dilate(lm,np.ones((3,3),np.uint8))
m[lm>0]=0
print('mask px',m.sum(), 'cassette in mask?', m[1900,1800], m[1750,1950])
cv2.imwrite(D+'mask.png',m*255)

def s2l(x): x=x/255.0; return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
def l2s(x): x=np.clip(x,0,1); return np.where(x<=0.0031308,x*12.92,1.055*x**(1/2.4)-0.055)*255
lin=s2l(im[...,::-1].astype(np.float64))           # RGB linear
Y=lin@np.array([0.2126,0.7152,0.0722])
mb=m.astype(bool)
ref=np.median(Y[mb]); print('ref Y',ref)
ratio=Y/ref
# edge band: ratio there is contaminated by wood/fuzz -> fill from interior (normalized convolution)
inner=cv2.erode(m,np.ones((7,7),np.uint8)).astype(np.float64)
num=cv2.GaussianBlur(ratio*inner,(0,0),4); den=cv2.GaussianBlur(inner,(0,0),4)
fill=num/np.maximum(den,1e-6)
band=(m>0)&(inner==0) | (cv2.dilate(m,np.ones((3,3),np.uint8))>0)&(m==0)
ratio=np.where(band,np.minimum(ratio,fill),ratio)
# alpha: soft edge
a=cv2.GaussianBlur(m.astype(np.float32),(0,0),1.0)
a=np.clip(a,0,1)[...,None]
COLORS={'navy':(38,49,71),'sport-grey':(151,153,155),'military-green':(94,116,97)}
for name,rgb in COLORS.items():
    t=s2l(np.array(rgb,float))
    tY=t@np.array([0.2126,0.7152,0.0722])
    # lighter fabrics reflect more diffuse light: soften extreme contrast slightly
    k={'navy':1.0,'sport-grey':0.85,'military-green':0.92}[name]
    r=np.clip(ratio,0,None)**k
    hc={'navy':0.8,'sport-grey':0.55,'military-green':0.7}[name]
    r=np.where(r>1,1+(r-1)*hc,r)
    r=r/np.median(r[mb])
    if name=='sport-grey':
        r=cv2.bilateralFilter(r.astype(np.float32),5,0.08,3).astype(np.float64)
    r=r/np.median(r[mb]); col=t[None,None,:]*r[...,None]
    out_rgb=l2s(col)
    # heather speckle for 90/10
    if name=='sport-grey':
        rng=np.random.default_rng(7)
        nz=rng.normal(0,1,Y.shape).astype(np.float32)
        nz=cv2.GaussianBlur(nz,(0,0),0.7); nz=cv2.resize(cv2.GaussianBlur(nz,(0,0),0.5),None,fx=1,fy=1)
        nz=nz/nz.std()
        out_rgb=out_rgb+ (nz*3.0)[...,None]
    src=im[...,::-1].astype(np.float64)
    res=src*(1-a)+out_rgb*a
    res=np.clip(np.round(res),0,255).astype(np.uint8)[...,::-1]
    cv2.imwrite(D+f'oldyfans-mockup-{name}.png',res)
    print(name,'median in mask',np.median(res[mb][:,::-1],axis=0),'target',rgb)
