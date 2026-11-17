import cv2,numpy as np,sys
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import gaussian_filter1d
D='/tmp/claude-0/-home-user-oldyfans/156d809e-1f1a-5118-9555-6a24b416dda5/scratchpad/'
src=cv2.imread(D+'src.webp')
mask=cv2.imread(D+'mask.png',0)>0          # recolor mask (label excluded)
geo=mask.copy()
n,l,s,_=cv2.connectedComponentsWithStats((~geo).astype(np.uint8),4)
for i in range(1,n):
    if s[i,4]<20000 and s[i,0]>0 and s[i,1]>0: geo[l==i]=True
H=W=2000
VARIANTS={2:('charcoal',(102,103,108)),3:('military-green',(94,116,97)),4:('sport-grey',(151,153,155)),5:('navy',(38,49,71))}
MATCH_HEX = '--photo-color' not in sys.argv

def pmask(im):
    d=np.abs(im.astype(int)-252).sum(2)
    core=d>300 if np.median(d)<100 else d>45
    thr=0.45*np.median(d[d>200]); m=(d>thr).astype(np.uint8)
    n,l,s,_=cv2.connectedComponentsWithStats(m);b=1+np.argmax(s[1:,4]);mm=(l==b).astype(np.uint8)
    n2,l2,s2,_=cv2.connectedComponentsWithStats(1-mm,4)
    for k in range(1,n2):
        if s2[k,4]<50000: mm[l2==k]=1
    return mm
def fit(mm):
    small=cv2.resize(geo.astype(np.uint8),(500,500),interpolation=cv2.INTER_NEAREST)>0
    ys,xs=np.nonzero(mm); oy,_=np.nonzero(geo)
    def score(p):
        w=cv2.warpAffine(mm,np.array([[p[0]/4,0,p[1]/4],[0,p[0]*p[3]/4,p[2]/4]]),(500,500),flags=cv2.INTER_NEAREST)>0
        return (w&small).sum()/(w|small).sum()
    s=1.8; p=np.array([s,1000-s*(xs.min()+xs.max())/2,oy.min()-s*ys.min(),1.0]); st=np.array([0.05,20,20,0.02])
    cur=score(p)
    while st[0]>0.001:
        imp=False
        for k in range(4):
            for sg in (1,-1):
                q=p.copy();q[k]+=sg*st[k];q[3]=np.clip(q[3],0.92,1.0);sc=score(q)
                if sc>cur:p,cur,imp=q,sc,True
        if not imp: st/=2
    return p,cur
def extend(im,mm):
    # erode to drop white antialias, then push shirt colors outward into the background
    core=cv2.erode(mm,np.ones((5,5),np.uint8)).astype(np.float32)
    f=im.astype(np.float32)*core[...,None]; w=core.copy()
    out=f.copy(); have=core>0
    acc_f=f.copy(); acc_w=w.copy()
    for sig in [2,4,8,16,32,64,128]:
        bf=cv2.GaussianBlur(f,(0,0),sig); bw=cv2.GaussianBlur(w,(0,0),sig)
        val=bf/np.maximum(bw[...,None],1e-6)
        fillm=(~have)&(bw>1e-3)
        out[fillm]=val[fillm]; have|=fillm
    return out
def contour_pts(m,step):
    cs,_=cv2.findContours(m.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    c=max(cs,key=len)[:,0,:].astype(float)
    return c[::step]
def lin(x): x=x/255.0; return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
def srgb(x): x=np.clip(x,0,1); return np.where(x<=0.0031308,x*12.92,1.055*x**(1/2.4)-0.055)*255

# low-frequency shading of the original scene on the shirt (vignette / light falloff)
Ysrc=lin(src[...,::-1].astype(float))@[0.2126,0.7152,0.0722]
gm=cv2.erode(mask.astype(np.uint8),np.ones((15,15),np.uint8)).astype(np.float32)
lowo=cv2.GaussianBlur((Ysrc*gm).astype(np.float32),(0,0),80)/np.maximum(cv2.GaussianBlur(gm,(0,0),80),1e-6)
lowo=np.clip(lowo/np.median(lowo[geo]),0.7,1.3)

a=np.clip(cv2.GaussianBlur(mask.astype(np.float32),(0,0),1.0),0,1)[...,None]
for i,(name,hexc) in VARIANTS.items():
    mm=(cv2.imread(D+f'v2/pm{i}.png',0)>127).astype(np.uint8); im=cv2.imread(D+f'v2/q{i}.png')
    # remove the brand label from the photo (it is replaced by the OLDY FANS label of the scene)
    hsvp=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    ys,xs=np.nonzero(mm); top=ys.min()
    p,sc=fit(mm); print(name,'fit',np.round(p,3),'iou',round(sc,4))
    M=np.array([[p[0],0,p[1]],[0,p[0]*p[3],p[2]]])
    ext=extend(im,mm)
    A=cv2.warpAffine(ext,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    Am=cv2.warpAffine(mm,M,(W,H),flags=cv2.INTER_NEAREST)
    from scipy.spatial import cKDTree
    xx,yy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
    oc=contour_pts(geo,4)
    keep=(oc[:,0]>2)&(oc[:,0]<W-3)&(oc[:,1]<H-3)&(oc[:,1]>2)
    dist=cv2.distanceTransform(geo.astype(np.uint8),cv2.DIST_L2,5)
    gy,gx=np.mgrid[0:H:100,0:W:100]; g=np.stack([gx.ravel(),gy.ravel()],1)
    inner=g[dist[g[:,1],g[:,0]]>200]
    dx=np.zeros((H,W),np.float32); dy=np.zeros((H,W),np.float32)
    cy,cx=np.mgrid[0:H:8,0:W:8]; cg=np.stack([cx.ravel(),cy.ravel()],1).astype(float)
    for it in range(4):
        Wm_=cv2.remap(Am.astype(np.float32),xx+dx,yy+dy,cv2.INTER_LINEAR)
        wc=contour_pts(Wm_>0.5,1)
        _,idx=cKDTree(wc).query(oc); q=wc[idx]
        qi=np.clip(np.round(q).astype(int),0,W-1)
        sq=np.stack([qi[:,0]+dx[qi[:,1],qi[:,0]],qi[:,1]+dy[qi[:,1],qi[:,0]]],1)
        oi=np.clip(np.round(oc).astype(int),0,W-1)
        cur=np.stack([dx[oi[:,1],oi[:,0]],dy[oi[:,1],oi[:,0]]],1)
        disp=sq-oc
        disp=cur+ (disp-cur)*1.0
        disp[:,0]=gaussian_filter1d(disp[:,0],5,mode='wrap'); disp[:,1]=gaussian_filter1d(disp[:,1],5,mode='wrap')
        iv=np.stack([dx[inner[:,1],inner[:,0]],dy[inner[:,1],inner[:,0]]],1)
        oi2=np.clip(np.round(oc).astype(int),0,W-1)
        uncov=Wm_[oi2[:,1],oi2[:,0]]<0.5
        k2=keep|uncov
        P=np.vstack([oc[k2][::2],inner]); V=np.vstack([disp[k2][::2],iv])
        rbf=RBFInterpolator(P,V,kernel='thin_plate_spline',smoothing=np.array([30.0]*len(oc[k2][::2])+[3000.0]*len(inner)))
        dd=rbf(cg).reshape(cy.shape+(2,)).astype(np.float32)
        dx=cv2.resize(dd[...,0],(W,H),interpolation=cv2.INTER_CUBIC); dy=cv2.resize(dd[...,1],(W,H),interpolation=cv2.INTER_CUBIC)
        Wm_=cv2.remap(Am.astype(np.float32),xx+dx,yy+dy,cv2.INTER_LINEAR)
        print('   iter',it,'uncovered',int((geo&(Wm_<0.5)).sum()))
    from scipy.ndimage import distance_transform_edt
    coreA=cv2.erode(Am,np.ones((11,11),np.uint8))
    _,(iy,ix)=distance_transform_edt(coreA==0,return_indices=True)
    sx=np.clip(xx+dx,0,W-1); sy=np.clip(yy+dy,0,H-1)
    rx=np.round(sx).astype(int); ry=np.round(sy).astype(int)
    out_=coreA[ry,rx]==0
    qx=ix[ry,rx].astype(np.float32); qy=iy[ry,rx].astype(np.float32)
    mx=2*qx-sx; my=2*qy-sy
    mxi=np.clip(np.round(mx).astype(int),0,W-1); myi=np.clip(np.round(my).astype(int),0,H-1)
    okm=coreA[myi,mxi]>0
    sx=np.where(out_&okm,mx,np.where(out_,qx,sx)); sy=np.where(out_&okm,my,np.where(out_,qy,sy))
    print('  clamped px in shirt:',int((out_&geo).sum()))
    Wimg=cv2.remap(A,sx.astype(np.float32),sy.astype(np.float32),cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    Wm=cv2.remap(Am.astype(np.float32),xx+dx,yy+dy,cv2.INTER_LINEAR)
    cv2.imwrite(D+f'v2/wm{i}.png',(Wm*255).astype(np.uint8))
    WimgN=cv2.remap(A,xx+dx,yy+dy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    cv2.imwrite(D+f'v2/wimg{i}.png',np.clip(WimgN,0,255).astype(np.uint8))
    cover=(Wm>0.5)&geo
    print('  coverage of old shirt by new shirt (pre-fill):',round(cover.sum()/geo.sum(),4))
    np.save(D+f'v2/disp{i}.npy',np.stack([dx,dy]))
    L=lin(Wimg[...,::-1].astype(float))
    L=L*(lowo[...,None]**0.6)
    out=srgb(L)
    if MATCH_HEX:
        tgt=cv2.cvtColor((np.array([[hexc]],np.float32)/255),cv2.COLOR_RGB2LAB)[0,0]
        lab=cv2.cvtColor((out/255).astype(np.float32),cv2.COLOR_RGB2LAB)
        for it in range(4):
            o8=np.clip(cv2.cvtColor(lab,cv2.COLOR_LAB2RGB)*255,0,255)
            med=np.median(o8[mask],0)
            mlab=cv2.cvtColor((med/255).astype(np.float32)[None,None],cv2.COLOR_RGB2LAB)[0,0]
            lab=(lab+(tgt-mlab)).astype(np.float32)
        out=np.clip(cv2.cvtColor(lab,cv2.COLOR_LAB2RGB)*255,0,255)
    # edge zones the photo cannot reach: use the original shirt's own folds/edges, tinted with the local photo colour
    good=(~out_).astype(np.float32)*geo
    wgt=cv2.GaussianBlur(cv2.erode(good,np.ones((9,9),np.uint8)),(0,0),5)
    wgt=np.minimum(wgt,good)[...,None]
    olin=lin(out); gm2=cv2.erode(good,np.ones((9,9),np.uint8))
    num=cv2.GaussianBlur((olin*gm2[...,None]).astype(np.float32),(0,0),25); den=cv2.GaussianBlur(gm2,(0,0),25)
    for sg in (60,150):
        nb=cv2.GaussianBlur((olin*gm2[...,None]).astype(np.float32),(0,0),sg); db=cv2.GaussianBlur(gm2,(0,0),sg)
        weak=den<0.05; num[weak]=nb[weak]; den=np.where(weak,db,den)
    loc=num/np.maximum(den[...,None],1e-6)
    det=(Ysrc/np.maximum(cv2.GaussianBlur(Ysrc.astype(np.float32),(0,0),25),1e-6))
    det=np.clip(det,0,3)**0.85
    v1=srgb(loc*det[...,None])
    out=out*wgt+v1*(1-wgt)
    res=src[...,::-1].astype(float)*(1-a)+out*a
    res=np.clip(np.round(res),0,255).astype(np.uint8)[...,::-1]
    suf='' if MATCH_HEX else '-color-foto'
    cv2.imwrite(D+f'v2/oldyfans-mockup-{name}{suf}.png',res)
    cv2.imwrite(D+f'v2/raw{i}.jpg',Wimg)
    print('  median',np.median(res[mask][:,::-1],0),'target',hexc)
