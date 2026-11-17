import cv2,numpy as np
D='/tmp/claude-0/-home-user-oldyfans/156d809e-1f1a-5118-9555-6a24b416dda5/scratchpad/v2/'
out=[]
for i in [2,3,4,5]:
    im=cv2.imread(D+f'p{i}.jpg'); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    d=np.abs(im.astype(int)-252).sum(2)
    tex=cv2.blur(np.abs(g-cv2.GaussianBlur(g,(0,0),1.5)),(9,9))
    bgtex=np.median(tex[d<20])
    fabric=(tex>bgtex*3)&(d>45)
    fabric=cv2.morphologyEx(fabric.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    n,l,s,_=cv2.connectedComponentsWithStats(fabric);b=1+np.argmax(s[1:,4]);fg=(l==b).astype(np.uint8)
    n2,l2,s2,_=cv2.connectedComponentsWithStats(1-fg,4)
    for k in range(1,n2):
        if s2[k,4]<80000 and np.median(d[l2==k])>60: fg[l2==k]=1
    fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    # refine with grabcut
    gc=np.full(fg.shape,cv2.GC_PR_BGD,np.uint8)
    gc[cv2.dilate(fg,np.ones((25,25),np.uint8))==0]=cv2.GC_BGD
    gc[fg>0]=cv2.GC_PR_FGD
    gc[cv2.erode(fg,np.ones((31,31),np.uint8))>0]=cv2.GC_FGD
    bgm=np.zeros((1,65),np.float64);fgm=np.zeros((1,65),np.float64)
    cv2.grabCut(im,gc,None,bgm,fgm,4,cv2.GC_INIT_WITH_MASK)
    m=((gc==cv2.GC_FGD)|(gc==cv2.GC_PR_FGD)).astype(np.uint8)
    n,l,s,_=cv2.connectedComponentsWithStats(m);b=1+np.argmax(s[1:,4]);m=(l==b).astype(np.uint8)
    n2,l2,s2,_=cv2.connectedComponentsWithStats(1-m,4)
    for k in range(1,n2):
        if s2[k,4]<80000 and np.median(d[l2==k])>60: m[l2==k]=1
    m[(d<35)]=0
    md=np.median(d[m>0]); m[d<max(0.35*md,150)]=0
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    n,l,s_,_=cv2.connectedComponentsWithStats(m);b=1+np.argmax(s_[1:,4]);m=(l==b).astype(np.uint8)
    n2,l2,s2,_=cv2.connectedComponentsWithStats(1-m,4)
    for k in range(1,n2):
        if s2[k,4]<3000: m[l2==k]=1
    print(i,'md',md)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    cv2.imwrite(D+f'pm{i}.png',m*255)
    v=im.copy(); e=cv2.dilate(m,np.ones((3,3)))-m; v[e>0]=(0,0,255); v[(m==0)&(d>40)]=(0,255,255)
    out.append(cv2.resize(v,(800,640)))
cv2.imwrite(D+'pm.jpg',np.vstack([np.hstack(out[:2]),np.hstack(out[2:])]))
