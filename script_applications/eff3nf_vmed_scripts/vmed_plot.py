from matplotlib import pyplot as plt

from pmod import ioparse as iop

# fig_num = 12 # 12 or 13
# nxlo    = 2  # 2 or 3

'''
To run this script naming conventions must be observed:

The input data takes the form: 

'nxlo_3nf_yy.txt' : where x = name of chiral order, yy = figure (12 or 13)

(e.g.) 

'n2lo_3nf_12.txt' is a valid name for an input file 

fig_num = 12 # 12 or 13
nxlo    = 2  # 2 or 3

'''

def fig_file(nxlo,fig_num):
    table_file_name = 'n'+str(nxlo)+'lo_3nf_'+str(fig_num)+'.txt'
    return table_file_name


def get_file_12(nxlo = 'x'):
    if(nxlo == 'x'):
        xxx = iop.flat_file_intable(fig_file(2,12))
        yyy = iop.flat_file_intable(fig_file(3,12))
        return xxx, yyy
    elif(nxlo == 2):
        xxx = iop.flat_file_intable(fig_file(2,12))
        return xxx
    elif(nxlo == 3):
        yyy = iop.flat_file_intable(fig_file(3,12))   
        return yyy
    else:
        return None

    
def get_file_13(nxlo = 'x'):
    if(nxlo == 'x'):
        xxx = iop.flat_file_intable(fig_file(2,13))
        yyy = iop.flat_file_intable(fig_file(3,13))
        return xxx, yyy
    elif(nxlo == 2):
        xxx = iop.flat_file_intable(fig_file(2,13))
        return xxx
    elif(nxlo == 3):
        yyy = iop.flat_file_intable(fig_file(3,13))   
        return yyy
    else:
        return None
    
def nxdata_4split(nxlo):
    return [(nxlo[0],nxlo[1]),(nxlo[0],nxlo[2]),(nxlo[0],nxlo[3]),(nxlo[0],nxlo[4])]


def nxdata_16split(nxlo,xylo):
    return [(nxlo[0],nxlo[1],xylo[0],xylo[1]),
            (nxlo[0],nxlo[2],xylo[0],xylo[2]),
            (nxlo[0],nxlo[3],xylo[0],xylo[3]),
            (nxlo[0],nxlo[4],xylo[0],xylo[4])]


def one_plotter(kf, pwave, ylim = None, xlim = None, save = False, save_name = 'plot.txt'):
    plt.plot(kf, pwave)
    plt.ylabel('V (fm)', fontsize = 20)
    plt.xlabel('kf (fm)', fontsize = 20)
    if(ylim != None):
        plt.ylim(ylim[0],ylim[1])
    if(xlim != None):
        plt.xlim(xlim[0],xlim[1])
    if(save):
        plt.savefig(save_name)        
            
    
def four_plotter(tl_data, tr_data, bl_data, br_data, fig_num, nxlo='x', save = False):

    fig, axs = plt.subplots(2, 2, sharex=False, sharey=False)
    
    if(fig_num == 12):
        label = ['1S0','3S1','3D1','3S1 - 3D1']
    elif(fig_num == 13):
        label = ['1P1','3P0','3P1','3P2']
    else:
        label = [' ',' ',' ',' ']
    
    axs[0, 0].plot(tl_data[0], tl_data[1])
    if(nxlo == 'x'):
        axs[0, 0].plot(tl_data[2], tl_data[3])
    axs[0, 0].set_title(label[0])
    
    axs[0, 1].plot(tr_data[0], tr_data[1])
    if(nxlo == 'x'):    
        axs[0, 1].plot(tr_data[2], tr_data[3])
    axs[0, 1].set_title(label[1])
    
    axs[1, 0].plot(bl_data[0], bl_data[1])
    if(nxlo == 'x'):
        axs[1, 0].plot(bl_data[2], bl_data[3])
    axs[1, 0].set_title(label[2])
    
    axs[1, 1].plot(br_data[0], br_data[1])
    if(nxlo == 'x'):
        axs[1, 1].plot(br_data[2], br_data[3])
    axs[1, 1].set_title(label[3])
    
    for ax in axs.flat:
        ax.set(xlabel='kf (1/fm)', ylabel='V (fm)')
        
    plt.tight_layout()
    plt.show()
        
    if(save):
#        print(fig_file(nxlo,fig).split('.')[0])
        fig.savefig(fig_file(nxlo,fig_num).split('.')[0]+'.pdf')
        
        
### MAIN()

# Set-Up

# N2LO Fig. 12 Four-plot set-up
n2f12 = get_file_12(nxlo = 2)
n2f12_data = nxdata_4split(n2f12)
four_plotter(n2f12_data[0], n2f12_data[1], n2f12_data[2], n2f12_data[3], fig_num=12, nxlo=2, save = True)

# N3LO Fig. 12 Four-plot set-up
n3f12 = get_file_12(nxlo = 3)
n3f12_data = nxdata_4split(n3f12)
four_plotter(n3f12_data[0], n3f12_data[1], n3f12_data[2], n3f12_data[3], fig_num=12, nxlo=3, save = True)
                    
# N2LO Fig. 13 Four-plot set-up
n2f13 = get_file_13(nxlo = 2)
n2f13_data = nxdata_4split(n2f13)
four_plotter(n2f13_data[0], n2f13_data[1], n2f13_data[2], n2f13_data[3], fig_num=13, nxlo=2, save = True)

# N3LO Fig. 13 Four-plot set-up
n3f13 = get_file_13(nxlo = 3)
n3f13_data = nxdata_4split(n3f13)
four_plotter(n3f13_data[0], n3f13_data[1], n3f13_data[2], n3f13_data[3], fig_num=13, nxlo=3, save = True)




# NXLO Fig. 12 Four-plot set-up
#n2f12 = get_file_12(nxlo = 2)
#n3f12 = get_file_12(nxlo = 3)
nf12_data = nxdata_16split(n2f12,n3f12)
four_plotter(nf12_data[0], nf12_data[1], nf12_data[2], nf12_data[3], fig_num=12, save = True)

# NXLO Fig. 13 Four-plot set-up
#n2f13 = get_file_13(nxlo = 2)
#n3f13 = get_file_13(nxlo = 3)
nf13_data = nxdata_16split(n2f13,n3f13)
four_plotter(nf13_data[0], nf13_data[1], nf13_data[2], nf13_data[3], fig_num=13, save = True)
                    