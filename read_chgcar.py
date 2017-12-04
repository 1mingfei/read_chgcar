#!/usr/bin/python
import numpy as np
import operator 


def read_chgcar(filename):
    with open(filename,'r') as fin:
        lines=fin.readlines()
    cell = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            cell[i][j]=lines[2+i].split()[j]

    vol      = np.dot(np.cross(cell[0,:],cell[1,:]),cell[2,:])
    lst_a    = [int(s) for s in lines[6].split()]
    tot_num  = int(sum(lst_a))
    line_num = 7+tot_num+1+1

    nx = int(lines[line_num].split()[0])
    ny = int(lines[line_num].split()[1])
    nz = int(lines[line_num].split()[2])
    line_num += 1
    
    tot_num    = nx*ny*nz
    line_count = tot_num/int(5)
    tmp        = np.zeros(tot_num)
    for i in range(line_count):
        for j in range(5):
            ap=lines[line_num+i].split()[j]
            tmp[5*i+j] = (float(ap)/float(vol))
    nxyz=[nx,ny,nz]
    return tmp,nxyz,cell

def get_xyz(nxyz,delta_chg,z):
    nx,ny,nz = nxyz[0],nxyz[1],nxyz[2]
    chg = np.zeros((nx,ny,nz))
    for iz in range(nz):
        for iy in range(ny):
            for ix in range(nx):
                chg[ix][iy][iz] = delta_chg[ix+iy*nx+iz*ny*nx]
    tmp3,tmp5=0.0,0.0
    for iz in range(nz):
        tmp2=0.0
        for iy in range(ny):
            for ix in range(nx):
                tmp2 += chg[ix][iy][iz]

        tmp1=iz/float(nz)
        tmp3 +=tmp2
        tmp4=tmp1*tmp2
        tmp5 += tmp4
        c=tmp5/float(tmp3)

    tmp3,tmp5=0.0,0.0
    for iy in range(ny):
        tmp2=0.0
        for iz in range(nz):
            for ix in range(nx):
                tmp2 += chg[ix][iy][iz]

        tmp1=iy/float(ny)
        tmp3 +=tmp2
        tmp4=tmp1*tmp2
        tmp5 += tmp4
        b=tmp5/float(tmp3)

    tmp3,tmp5=0.0,0.0
    for ix in range(nx):
        tmp2=0.0
        for iz in range(nz):
            for iy in range(ny):
                tmp2 += chg[ix][iy][iz]

        tmp1=ix/float(nx)
        tmp3 +=tmp2
        tmp4=tmp1*tmp2
        tmp5 += tmp4
        a=tmp5/float(tmp3)


    return a,b,c


def get_z(nxyz,delta_chg,z):
    nx,ny,nz = nxyz[0],nxyz[1],nxyz[2]
    chg = np.zeros((nx,ny,nz))
    for iz in range(nz):
        for iy in range(ny):
            for ix in range(nx):
                chg[ix][iy][iz] = delta_chg[ix+iy*nx+iz*ny*nx]
    tmp3,tmp5=0.0,0.0
    for iz in range(nz):
        tmp2=0.0
        for iy in range(ny):
            for ix in range(nx):
                tmp2 += chg[ix][iy][iz]

        tmp1=iz/float(nz)
        tmp3 +=tmp2
        tmp4=tmp1*tmp2
        tmp5 += tmp4
        c=tmp5/float(tmp3)
        print tmp1*z, tmp2
    return 

# test Pt charge density for ref
Pt   = read_chgcar('CHGCAR')
chg  = Pt[0]
nxyz = Pt[1]
z    = Pt[2][2][2]

#a = get_xyz(nxyz,chg,z)
#print  a[0],a[1],a[2]
get_z(nxyz,chg,z)

'''
a    = read_chgcar('Pt-Si.CHGCAR')
PtSi = a[0]
nxyz = a[1]
z    = a[2][2][2]
Pt   = read_chgcar('Pt.CHGCAR')[0]
Si   = read_chgcar('Si.CHGCAR')[0]
delta_chg = map(operator.sub, PtSi     , Pt)
delta_chg = map(operator.sub, delta_chg, Si)
get_z(nxyz,delta_chg,z)
'''
