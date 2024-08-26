import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec  

import os

def draw_figure_from_file(ax,fname=""):
    img = plt.imread(fname)
    
    if ax is not None:
        ax.imshow(img,extent=(-0.5,0.5,-0.5,0.5))
    
    return img
    
def get_nxny_etc_for_regular_polygon(n: int,
                                    reference = (3,15), # reference_n, reference_ny number of sides and rows for the reference polygon
                                    paperwh=(11.69,8.27), # inches, a4
                                    min_margin = 0.4135, # minimal margin in inch
                                    space_between_subplots = 0., # space between subplots inches
                                    ):
    """
    so what we do is say, in references to reference_n (3?) the sidelengths have to be all the same. So the nx,ny and height andsoon change. 
    we calculate it here.

    Args:
        n (int): _description_
        a4 (_type_): _description_
        paperwh (_type_, optional): _description_. Defaults to (11.69,8.27)#inches.

    Returns:
        _type_: _description_
    """
    min_bot  = min_margin/paperwh[1] # 0.05 # min margin as fraction
    min_left = min_margin/paperwh[0] # 0.05 # min margin as fraction
    
    
    wspace = space_between_subplots/paperwh[0]
    hspace = space_between_subplots/paperwh[1]
    
    # We take n=3 as a reference
    # The reference suggested nx,ny = 6,4
    # reference_n = 3
    # reference_ny = 15
    reference_n, reference_ny = reference
    reference_height = (1.-2*min_bot-(reference_ny-1)*hspace)/reference_ny # 0.212 # height of subplot (normalised by paperwh)
    reference_w = 0.5*np.cos(2*np.pi*(180-360/reference_n)/360/2) # HALF width of the side of the figure, not the subplot oops
    
    if reference_height < 0:
        raise ValueError("reference_height<0, probably you have set a ludicrous space_between_subplots: %f in"%(space_between_subplots))
    
    # calc current
    int_angle = 2*np.pi*(180-360/n)/360
    h = 0.5*np.sin(int_angle/2)
    w = 0.5*np.cos(int_angle/2) # HALF width of the side of the  figure
    
    # rato
    ratio = reference_w/w#/reference_w
    height = ratio * reference_height
        
    # nxny and left,bot
    ny = int(1//height)+1
    bot = -1 # Initialize with something wrong ;<
    while bot < min_bot:
        ny += -1
        bot = (1.-ny*height-(ny-1)*hspace)/2. #0.076
    
    width = height*paperwh[1]/paperwh[0]
    nx = int(1//width)+1
    left = -1 # Initialize with something wrong ;<
    while left < min_left:
        nx += -1
        left = (1.-nx*width-(nx-1)*wspace)/2.
    
    nxny = (nx,ny)
    subplots_adjust_kwargs = { 'left':left, 'bottom':bot, 'right':1.-left, 'top':1.-bot, 'wspace':wspace/width, 'hspace':hspace/height}
    
    print("n:",n,"| Height in cm:",height*paperwh[1]*2.54,"| Side of figure in cm:",2.*w*height*paperwh[1]*2.54,"| Number of figures: (%i,%i)"%(nx,ny),nx*ny)
    return nxny, subplots_adjust_kwargs


    
def get_nxny_etc_from_paperwh_and_height(paperwh,
                                         subplot_height_inches,
                                         min_margin = 0.4135, # minimal margin in inch
                                         space_between_subplots = 0., # inch
                                         ):
    """
    height is the height of a single subfig.
    
    Args:
        paperwh (_type_): _description_
        subplot_height_inches (_type_): _description_
    """
    min_bot  = min_margin/paperwh[1] # 0.05 # min margin as fraction
    min_left = min_margin/paperwh[0] # 0.05 # min margin as fraction
    
    
    wspace = space_between_subplots/paperwh[0]
    hspace = space_between_subplots/paperwh[1]
    
    height = subplot_height_inches/paperwh[1]
    
    
    # nxny and left,bot
    ny = int(1//height)+1
    bot = -1 # Initialize with something wrong ;<
    while bot < min_bot:
        ny += -1
        bot = (1.-ny*height-(ny-1)*hspace)/2. #0.076
    
    width = height*paperwh[1]/paperwh[0]
    nx = int(1//width)+1
    left = -1 # Initialize with something wrong ;<
    while left < min_left:
        nx += -1
        left = (1.-nx*width-(nx-1)*wspace)/2.
    
    
    nxny = (nx,ny)
    subplots_adjust_kwargs = { 'left':left, 'bottom':bot, 'right':1.-left, 'top':1.-bot, 'wspace':wspace/width, 'hspace':hspace/height }
    
    print("Height in cm:",height*paperwh[1]*2.54,"| Number of figures: (%i,%i)"%(nx,ny),nx*ny)
    return nxny, subplots_adjust_kwargs


def get_nxny_etc_from_img_and_subplotheight(fname,
                                            paperwh,
                                            subplot_height_inches,
                                            min_margin = 0.4135, # minimal margin in inch
                                            space_between_subplots=0., # inches
                                            ):
    img = draw_figure_from_file(None,fname)
    
    imgshape = img.shape
    subplot_aspect = imgshape[0]/imgshape[1]
    
    min_bot  = min_margin/paperwh[1] # 0.05 # min margin as fraction
    min_left = min_margin/paperwh[0] # 0.05 # min margin as fraction
    
    wspace = space_between_subplots/paperwh[0]
    hspace = space_between_subplots/paperwh[1]
    
    height = subplot_height_inches/paperwh[1]
    
    # nxny and left,bot
    ny = int(1//height)+1
    bot = -1 # Initialize with something wrong ;<
    while bot < min_bot:
        ny += -1
        bot = (1.-ny*height-(ny-1)*hspace)/2. #0.076
    
    width = height*paperwh[1]/paperwh[0]/subplot_aspect
    nx = int(1//width)+1
    left = -1 # Initialize with something wrong ;<
    while left < min_left:
        nx += -1
        left = (1.-nx*width-(nx-1)*wspace)/2.

    
    nxny = (nx,ny)
    subplots_adjust_kwargs = { 'left':left, 'bottom':bot, 'right':1.-left, 'top':1.-bot, 'wspace':wspace/width, 'hspace':hspace/height }
    
    print("Height in cm:",height*paperwh[1]*2.54,"| Number of figures: (%i,%i)"%(nx,ny),nx*ny,"| Aspect ratio h/w:",subplot_aspect)
    return nxny, subplots_adjust_kwargs, subplot_aspect



def tst():
    for n in range(3,11):
        
        int_angle = 2*np.pi*(180-360/n)/360
        int_top_angle = 2*np.pi*(360/n)/360
        # print(int_angle,int_top_angle)
        
        # mid = (0.5,0.5)
        mid = (0,0)
        
        h = 0.5*np.sin(int_angle/2)
        w = 0.5*np.cos(int_angle/2) # half width!

        plt.plot([n],[w],marker='o')
    plt.show()
    

def draw_regular_polygon(ax,n=3):
    
    int_angle = 2*np.pi*(180-360/n)/360
    int_top_angle = 2*np.pi*(360/n)/360
    # print(int_angle,int_top_angle)
    
    # mid = (0.5,0.5)
    mid = (0,0)
    
    h = 0.5*np.sin(int_angle/2)
    w = 0.5*np.cos(int_angle/2) # half width!
    
    
    pt1 = (mid[0]-w,mid[1]-h)
    pt2 = (mid[0]+w,mid[1]-h)
    
    # ax.plot([0],[0],marker='x')
    
    xlist = [pt1[0],pt2[0]]
    ylist = [pt1[1],pt2[1]]
    
    for i in range(n):
        pt1 = ( (pt1[0]-mid[0])*np.cos(int_top_angle)-(pt1[1]-mid[1])*np.sin(int_top_angle)+mid[0], (pt1[0]-mid[0])*np.sin(int_top_angle)+(pt1[1]-mid[1])*np.cos(int_top_angle)+mid[1] )
        pt2 = ( (pt2[0]-mid[0])*np.cos(int_top_angle)-(pt2[1]-mid[1])*np.sin(int_top_angle)+mid[0], (pt2[0]-mid[0])*np.sin(int_top_angle)+(pt2[1]-mid[1])*np.cos(int_top_angle)+mid[1] )
        
        xlist.extend([pt1[0],pt2[0]])
        ylist.extend([pt1[1],pt2[1]])
        
        ax.plot([pt1[0],pt2[0]],[pt1[1],pt2[1]],c='k',ls='-')
    
        # ax.plot([pt1[0]],[pt1[1]],marker='o')
        # ax.plot([pt2[0]],[pt2[1]],marker='s')
        
    ax.plot(xlist,ylist,c='k',ls='-')
    
    # ax.plot([0,1],[0,0],c='k',ls='-')
    # ax.plot([0,0.5],[0,np.sqrt(3)/2],c='k',ls='-')
    # ax.plot([0.5,1],[np.sqrt(3)/2,0],c='k',ls='-')


def make_figure_with_shapes(fname,
                            paperwh,
                            nxny,
                            draw_func,draw_func_kwargs,
                            subplots_adjust_kwargs,
                            subplot_aspect='equal',
                            show_figure=True,
                            ):
    """
        nxny 6,4 works well for a4
    """
    fig = plt.figure()
    fig.set_size_inches(paperwh[0],paperwh[1])

    nx,ny = nxny
    axlist = []
    
    
    gs = gridspec.GridSpec(ny,nx)
    for i in range(nx*ny):
        axlist.append(plt.subplot(gs[i]))
        
        draw_func(axlist[-1],**draw_func_kwargs)
        
        axlist[-1].set_aspect(subplot_aspect)
        axlist[-1].axis('off')
        axlist[-1].set_xlim(-0.5,0.5)
        axlist[-1].set_ylim(-0.5,0.5)

    
    plt.subplots_adjust(**subplots_adjust_kwargs)

    savefig_kwargs = {'dpi':150}
    plt.savefig(fname,**savefig_kwargs)#,bbox_inches='tight',pad_inches=0.0)
    if show_figure:
        plt.show()

def outfname_from_imgfname(imgfname):
    if "penrose_P3" in imgfname:
        if "fat" in imgfname:
            out = "PenroseRhombiFat"
        if "slim" in imgfname:
            out = "PenroseRhombiSlim"
    elif "penrose_kite" in imgfname:
        out = "PenroseQuadKite"
    elif "penrose_dart" in imgfname:
        out = "PenroseQuadDart"
    elif "spectre_curve" in imgfname:
        out = "EinsteinSpectre"
    elif "spectre" in imgfname:
        out = "EinsteinSpectreStraight"
    elif "hat" in imgfname:
        out = "EinsteinHat"
    else:
        raise ValueError("Could not find name %s to convert imgname.."%(imgfname))
    return out

def main():
    # tst()
    
    # nxny = (6,4)
    # subplots_adjust_kwargs = { 'left':0.05, 'bottom':0.076, 'right':0.95, 'top':0.924, 'wspace':0, 'hspace':0 }
    
    # paperwh = (11.69,8.27) # a4, inches
    paperwh = (70/2.54,50/2.54) #  inches
    min_margin = 1/2.54# 0.4135 # minimal margin in inches
    space_between_subplots = 1/2.54 # wspace and hspace in inches
    ext = ".svg"#".png"# extension for output
    
    out_loc = "svg"
    
    show_figure = False # SHOW?
    

    
    ## Penrose   and aperiodic haha
    subplot_height = 5/2.54 # inch
    loc_in = "imgs"
    for image_fname in sorted(["penrose_P3_fat","penrose_P3_slim","spectre_curve_aspect","penrose_kite_aspect","penrose_dart_aspect","hat_aspect","spectre_aspect"]):#
        draw_func_kwargs = {'fname':os.path.join(loc_in,image_fname+".png")}
        draw_func = draw_figure_from_file

        # fname = "grid_of_%s%s"%(image_fname,ext)
        fname = "%s%s"%(outfname_from_imgfname(image_fname),ext)
        fname = os.path.join(out_loc,fname)
        print(">",fname,"| from image",image_fname)
        
        
        # nxny,subplots_adjust_kwargs = get_nxny_etc_from_paperwh_and_height(paperwh,subplot_height,min_margin=min_margin)
        nxny,subplots_adjust_kwargs,subplot_aspect = get_nxny_etc_from_img_and_subplotheight(draw_func_kwargs['fname'],paperwh,subplot_height,min_margin=min_margin,space_between_subplots=space_between_subplots)
        
        make_figure_with_shapes(fname,paperwh,nxny,draw_func,draw_func_kwargs,subplots_adjust_kwargs,subplot_aspect=subplot_aspect,show_figure=show_figure)
        
    
    ## Regular polygons
    # We use a reference, all other polygons will have sides with the same length as set by these two numbers.
    reference_n = 3
    reference_ny = 12#14
    reference = (reference_n,reference_ny)
    for i in range(3,13):# range(5,11,5):#
        draw_func_kwargs = {'n':i}
        draw_func = draw_regular_polygon
        
        fname = "poly_%i%s"%(i,ext)
        fname = os.path.join(out_loc,fname)
        print(">",fname)
        
        nxny,subplots_adjust_kwargs = get_nxny_etc_for_regular_polygon(i,reference=reference,paperwh=paperwh,min_margin=min_margin,space_between_subplots=space_between_subplots)
        
        make_figure_with_shapes(fname,paperwh,nxny,draw_func,draw_func_kwargs,subplots_adjust_kwargs,show_figure=show_figure)
        
        
    print("Done")


if __name__ == "__main__":
    main()

