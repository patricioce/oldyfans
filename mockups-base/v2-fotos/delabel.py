import cv2,numpy as np
D='/tmp/claude-0/-home-user-oldyfans/156d809e-1f1a-5118-9555-6a24b416dda5/scratchpad/v2/'
B={2:(956,1031,235,300),3:(945,1020,249,305),4:(989,1063,238,299),5:(952,1028,227,291)}
rng=np.random.default_rng(1)
for i,(x0,x1,y0,y1) in B.items():
    im=cv2.imread(D+f'p{i}.jpg')
    m=np.zeros(im.shape[:2],np.uint8); p=5; m[y0-p:y1+p,x0-p:x1+p]=1
    out=im.astype(np.float32).copy()
    X0,X1,Y0,Y1=x0-p,x1+p,y0-p,y1+p
    sm=cv2.GaussianBlur(out,(0,0),2)
    for yy in range(Y0,Y1):
        L=sm[yy-2:yy+3,X0-8:X0-2].reshape(-1,3).mean(0); R=sm[yy-2:yy+3,X1+2:X1+8].reshape(-1,3).mean(0)
        t=np.linspace(0,1,X1-X0)[:,None]
        out[yy,X0:X1]=L*(1-t)+R*t
    out[Y0:Y1,X0:X1]=cv2.GaussianBlur(out[Y0-3:Y1+3,X0:X1],(1,7),0)[3:-3]
    # restore fabric grain inside the filled area using grain from neighbouring fabric
    g=im.astype(np.float32); hp=g-cv2.GaussianBlur(g,(0,0),3)
    h=y1-y0+2*p; w=x1-x0+2*p
    ring=(cv2.dilate(m,np.ones((15,15),np.uint8))>0)&(m==0)
    sd=np.median(np.abs(hp[ring].mean(1)))*1.0
    nz=rng.normal(0,1,(h,w)).astype(np.float32); nz=cv2.GaussianBlur(nz,(0,0),0.6); nz=(nz/nz.std()*sd)[...,None]
    src=nz
    a=cv2.GaussianBlur(m.astype(np.float32),(0,0),2)[...,None]
    out[y0-p:y1+p,x0-p:x1+p]+=src*a[y0-p:y1+p,x0-p:x1+p]*0.9
    cv2.imwrite(D+f'q{i}.png',np.clip(out,0,255).astype(np.uint8))
c=[cv2.imread(D+f'q{i}.png')[200:340,900:1080] for i in [2,3,4,5]]
cv2.imwrite(D+'labels2.jpg',cv2.resize(np.hstack(c),None,fx=2,fy=2))
