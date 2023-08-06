from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

def readmap(mapname_list):
    if mapname_list[0].lower().endswith(('.mrc', '.mrcs', '.map')):
        hf_list = []
        for j in range(len(mapname_list)):
            uc,hf11,origin = read_mrc(mapname_list[j])
            hf_list.append(hf11)
    if mapname_list[0].lower().endswith('.mtz'):
        hf_list = []
        for i in range(len(mapname_list)):
            uc,data = read_mtz(mapname_list[i])
            hf_list.append(data)
        # Dummy variable
        origin = [0.0, 0.0, 0.0]
    return uc,origin,hf_list

def mrc2map(mapname11):
    import mrcfile as mrc
    file11 = mrc.open(mapname11)
    cell1 = np.array(file11.header.cella)
    a1 = cell1['x']; b1 = cell1['y']; c1 = cell1['z']
    uc = np.asarray([a1 * 1.0, b1 * 1.0, c1 * 1.0, 90.0, 90.0, 90.0])
    origin = [  1 * file11.header.nxstart,
                1 * file11.header.nystart,
                1 * file11.header.nzstart   ]
    ar11 = np.asarray(file11.data,dtype='float')
    file11.close()
    print(mapname11,ar11.shape,uc[:3])
    return uc,ar11,origin

def read_mrc(mapname11):
    import mrcfile as mrc
    file11 = mrc.open(mapname11)
    cell1 = np.array(file11.header.cella)
    a1 = cell1['x']; b1 = cell1['y']; c1 = cell1['z']
    uc = np.asarray([a1 * 1.0, b1 * 1.0, c1 * 1.0, 90.0, 90.0, 90.0])
    origin = [  1 * file11.header.nxstart,
                1 * file11.header.nystart,
                1 * file11.header.nzstart   ]
    ar11 = np.asarray(file11.data,dtype='float')
    ar11_centered = np.fft.fftshift(ar11) # CENTERED IMAGE
    nx,ny,nz = ar11_centered.shape
    nnx = nx; nny = ny; nnz = nz
    if nx%2 != 0: nnx = nx + 1
    if ny%2 != 0: nny = ny + 1
    if nz%2 != 0: nnz = nz + 1    
    dx = nnx-nx; dy=nny-ny; dz=nnz-nz
    print(mapname11,nx,ny,nz,dx,dy,dz,uc[:3])
    data_arr11 = np.zeros(shape=(nx+dx,ny+dy,nz+dz),dtype='float')
    data_arr11[0:nx,0:ny,0:nz] = ar11_centered
    file11.close()
    hf11 = np.fft.fftshift(np.fft.fftn(ar11_centered)) # CENTERED FFT OF CENTERED IMAGE
    return uc,hf11,origin

def read_mrc2(mapname11):
    # No rotation of SF
    import mrcfile as mrc
    file11 = mrc.open(mapname11)
    cell1 = np.array(file11.header.cella)
    a1 = cell1['x']; b1 = cell1['y']; c1 = cell1['z']
    uc = np.asarray([a1 * 1.0, b1 * 1.0, c1 * 1.0, 90.0, 90.0, 90.0])
    origin = [  1 * file11.header.nxstart,
              1 * file11.header.nystart,
              1 * file11.header.nzstart   ]
    ar11 = np.asarray(file11.data,dtype='float')
    '''nx,ny,nz = ar11.shape
    nnx = nx; nny = ny; nnz = nz
    if nx%2 != 0: nnx = nx + 1
    if ny%2 != 0: nny = ny + 1
    if nz%2 != 0: nnz = nz + 1
    dx = nnx-nx; dy=nny-ny; dz=nnz-nz
    print(mapname11,nx,ny,nz,dx,dy,dz,uc[:3])
    data_arr11 = np.zeros(shape=(nnx,nny,nnz),dtype='float')
    data_arr11[0:nx,0:ny,0:nz] = ar11'''
    file11.close()
    hf11 = np.fft.fftshift(np.fft.fftn(ar11))
    return uc,hf11,origin

def read_mtz(filename):
    import numpy as np
    ''' Primitive MTZ parser by Takanori Nakane, 2018. GPLv3.
        modified by Rangana Warshamanage for Python3
        Reference: http://www.ccp4.ac.uk/html/mtzformat.html '''
    f = open(filename, "rb")
    magic = np.fromfile(f, dtype='S1', count=4).tostring().decode() # byte
    assert magic == 'MTZ '
    header_offset = (np.fromfile(f, dtype='u4', count=1)[0] - 1) * 4 # 1indexed
    f.seek(header_offset, 0) # from origin
    columns = []
    space_group = None
    unit_cell = None
    while True:
        header_record = np.fromfile(f, dtype='S1', count=0x50).tostring().decode()
        if header_record.startswith("END"):
            break
        elif header_record.startswith("COLUMN"):
            columns.append(header_record[7:38].strip())
        # TODO: you might want to parse the column type
        elif header_record.startswith("CELL"):
            unit_cell = np.array(header_record.split()[1:7], dtype=np.float)
        elif header_record.startswith("SYMINF"):
            space_group = int(header_record.split()[4])
    start_offset = (21 - 1) * 4
    f.seek(start_offset, 0)
    n_elems = (header_offset - start_offset) // 4
    data = np.fromfile(f, dtype=np.float32, count=n_elems).reshape(-1,len(columns))
    f.close()
    return unit_cell,data

def read_mtz_gemmi(mtzfile):
    import gemmi
    import numpy as np
    mtz = gemmi.read_mtz_file(mtzfile)
    uc = np.zeros(6, dtype='float')
    uc[0] = mtz.dataset(0).cell.a
    uc[1] = mtz.dataset(0).cell.b
    uc[2] = mtz.dataset(0).cell.c
    uc[3:] = 90.0
    # h - slowest; l - fastest
    '''l = np.array(mtz.column_with_label('H'), copy=False)
    k = np.array(mtz.column_with_label('K'), copy=False)
    h = np.array(mtz.column_with_label('L'), copy=False)
    ampl = np.array(mtz.column_with_label('Fout0'), copy=False)
    phas = np.array(mtz.column_with_label('Pout0'), copy=False)'''
    import pandas
    all_data = np.array(mtz, copy=False)
    df = pandas.DataFrame(data=all_data, columns=mtz.column_labels())
    # Index df by column_labels e.g. df['Fout0']
    return uc,df

def run_f2mtz(cell,filename):
    # Creating the f2mtz.inp with custom parameters
    f2mtz_inp = open("f2mtz.inp","w+")
    f2mtz_inp.write("TITLE USER to MTZ\n")
    f2mtz_inp.write("NAME PROJECT TEST CRYSTAL NATIVE DATASET NATIVE\n")
    f2mtz_inp.write("CELL %s\n"% cell)
    f2mtz_inp.write("LABOUT H  K  L  FP  PHIB\n")
    f2mtz_inp.write("CTYPE  H  H  H  F    P\n")
    f2mtz_inp.write("FORMAT '(3I4,2F10.2)'\n")
    f2mtz_inp.write("SYMM 1")
    f2mtz_inp.close()
    # Read in f2mtz_inp
    import os
    import os.path
    import subprocess
    fmtz = filename[:-4]+".mtz"
    cmd = ["f2mtz","HKLIN",filename,"HKLOUT",fmtz]
    PATH='f2mtz.inp'
    logf = open("mtz.log", "w+")
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print("f2mtz.inp exists and is readable")
        inp = open("f2mtz.inp","r")
        # Run the command with parameters from file f2mtz.inp
        subprocess.call(cmd,stdin=inp,stdout=logf)
    else:
        print("Either the file is missing or not readable")
    logf.close()
    inp.close()

def write_mrc(mapdata,filename,unit_cell,map_origin=[0.0,0.0,0.0]):
    import mrcfile as mrc
    import numpy as np
    #data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(mapdata))))
    file = mrc.new(name=filename, data=np.float32(mapdata), compression=None, overwrite=True)
    file.header.cella.x = unit_cell[0]
    file.header.cella.y = unit_cell[1]
    file.header.cella.z = unit_cell[2]
    file.header.nxstart = map_origin[0]
    file.header.nystart = map_origin[1]
    file.header.nzstart = map_origin[2]
    file.close()

'''def write_mtz2mrc(mapdata,filename,unit_cell,map_origin):
    import mrcfile as mrc
    import numpy as np
    print(map_origin)
    #data2write = np.real((np.fft.ifftn(np.fft.ifftshift(mapdata))))
    file = mrc.new(name=filename, data=np.float32(data2write), compression=None, overwrite=True)
    file.header.cella.x = unit_cell[0]
    file.header.cella.y = unit_cell[1]
    file.header.cella.z = unit_cell[2]
    file.header.nxstart = 0 # Note that map origin is always @ 0,0,0 of the cell box
    file.header.nystart = 0
    file.header.nzstart = 0
    file.close()'''

def write_3d2mtz(uc,arr,outfile='output.mtz'):
    import numpy.fft as fft
    print(arr.shape)
    nx, ny, nz = arr.shape
    import gemmi
    mtz = gemmi.Mtz()
    mtz.spacegroup = gemmi.find_spacegroup_by_name('P 1')
    mtz.cell.set(uc[0], uc[1], uc[2], 90, 90, 90)
    mtz.add_dataset('HKL_base')
    for label in ['H', 'K', 'L']: mtz.add_column(label, 'H')
    mtz.add_column('Fout0','F')
    mtz.add_column('Pout0','P')
    # Add more columns if you need
    x = fft.fftshift(fft.fftfreq(arr.shape[0])*nx)
    y = fft.fftshift(fft.fftfreq(arr.shape[1])*ny)
    z = fft.fftshift(fft.fftfreq(arr.shape[2])*nz)
    xv, yv, zv = np.meshgrid(x,y,z)
    xvf = xv.flatten(order='F')
    yvf = yv.flatten(order='F')
    zvf = zv.flatten(order='F')
    
    arr_real = np.real(arr)
    arr_imag = np.imag(arr)
    ampli = np.sqrt(np.power(arr_real,2) + np.power(arr_imag,2))
    phase = np.arctan2(arr_imag, arr_real) * 180 / np.pi
    
    ampli_1d = ampli.flatten(order='F')
    phase_1d = phase.flatten(order='F')
    
    nrows = len(xvf)
    ncols = 5 # Change this according to what columns to write
    data = np.ndarray(shape=(nrows,ncols), dtype=object)
    '''data[:,0] = -1 * zvf.astype(int)
    data[:,1] = -1 * xvf.astype(int)
    data[:,2] = -1 * yvf.astype(int)'''
    data[:,0] = zvf.astype(int)
    data[:,1] = xvf.astype(int)
    data[:,2] = yvf.astype(int)
    data[:,3] = ampli_1d.astype(np.float32)
    data[:,4] = phase_1d.astype(np.float32)
    print(data.shape)
    mtz.set_data(data)
    mtz.write_to_file(outfile)

def write_3d2mtz_fortran(uc,arr,outfile='output.mtz'):
    import numpy.fft as fft
    print(arr.shape)
    nx, ny, nz = arr.shape
    import gemmi
    mtz = gemmi.Mtz()
    mtz.spacegroup = gemmi.find_spacegroup_by_name('P 1')
    mtz.cell.set(uc[0], uc[1], uc[2], 90, 90, 90)
    mtz.add_dataset('HKL_base')
    for label in ['H', 'K', 'L']: mtz.add_column(label, 'H')
    mtz.add_column('Fout0','F')
    mtz.add_column('Pout0','P')
    # calling fortran function
    import fcodes
    h,k,l,ampli,phase = fcodes.prepare_hkl(arr,1,nx,ny,nz)
    nrows = len(h)
    ncols = 5 # Change this according to what columns to write
    data = np.ndarray(shape=(nrows,ncols), dtype=object)
    data[:,0] = -l.astype(int)
    data[:,1] = -k.astype(int)
    data[:,2] = -h.astype(int)
    data[:,3] = ampli.astype(np.float32)
    data[:,4] = phase.astype(np.float32)
    print(data.shape)
    mtz.set_data(data)
    mtz.write_to_file(outfile)

def write_3d2mtz_fortran_refmac(uc,arr1,arr2,outfile='output.mtz'):
    # One time function for REFMAC 3D refinement data
    import numpy.fft as fft
    print(arr1.shape)
    assert arr1.shape == arr2.shape
    nx, ny, nz = arr1.shape
    import gemmi
    mtz = gemmi.Mtz()
    mtz.spacegroup = gemmi.find_spacegroup_by_name('P 1')
    mtz.cell.set(uc[0], uc[1], uc[2], 90, 90, 90)
    mtz.add_dataset('HKL_base')
    for label in ['H', 'K', 'L']: mtz.add_column(label, 'H')
    mtz.add_column('Fout0','F')
    mtz.add_column('Pout0','P')
    mtz.add_column('SIGF','Q')
    # calling fortran function
    import fcodes
    h,k,l,ampli,phase = fcodes.prepare_hkl(arr1,1,nx,ny,nz) # map
    _,_,_,ampli_noise,_ = fcodes.prepare_hkl(arr2,1,nx,ny,nz) # map
    assert len(ampli) == len(ampli_noise)
    nrows = len(h)
    ncols = 6 # Change this according to what columns to write
    data = np.ndarray(shape=(nrows,ncols), dtype=object)
    data[:,0] = -l.astype(int)
    data[:,1] = -k.astype(int)
    data[:,2] = -h.astype(int)
    data[:,3] = ampli.astype(np.float32)
    data[:,4] = phase.astype(np.float32)
    data[:,5] = ampli_noise.astype(np.float32)
    print(data.shape)
    mtz.set_data(data)
    mtz.write_to_file(outfile)

def write_mtz2_3d(h,k,l,f,nx,ny,nz):
    import numpy as np
    arr = np.zeros((nx*ny*nx), dtype=np.complex)
    xv, yv, zv = np.meshgrid(h,k,l)
    xvf = xv.flatten(order='F')
    lb = (len(arr)-len(xvf))//2
    ub = lb + len(xvf)
    print(lb,ub)
    arr[lb:ub] = f
    f3d = arr.reshape(nx,ny,nz)
    mapdata = np.fft.ifftn(np.fft.fftshift(f3d))
    return mapdata

def write_mtz2_3d_gemmi(mtzfile,map_size):
    import gemmi
    mtz = gemmi.read_mtz_file(mtzfile)
    ccp4 = gemmi.Ccp4Map()
    ccp4.grid = mtz.transform_f_phi_to_map('Fout0', 'Pout0', map_size)
    ccp4.update_ccp4_header(2, True)
    ccp4.write_ccp4_map('5wkd.ccp4')
    return

def resample2staticmap(target_pix_size,target_dim,uc2,arr2):
    tnx,tny,tnz = target_dim
    assert uc2[0] == uc2[1] == uc2[2]
    nx, ny, nz = arr2.shape
    tnx, tny, tnz = target_dim
    assert tnx == tny == tnz
    assert nx == ny == nz
    current_pix_size = round(uc2[0]/nx,3)
    target_pix_size = round(target_pix_size,3)
    print('pixel size [current, target]: ', current_pix_size,target_pix_size)
    if current_pix_size == target_pix_size:
        if tnx == nx: 
            print('No change of dims')
            new_arr = arr2
        elif nx < tnx:
            # pad with zeros
            print('Padded with zeros')
            dx = (tnx - nx)//2
            new_arr = np.zeros((tnx,tny,tnz),dtype='float')
            new_arr[dx:nx+dx, dx:nx+dx, dx:nx+dx] = arr2
        elif tnx < nx:
            # strip out edge rows
            print('Cropped image')
            dx = (nx - tnx)//2
            new_arr = np.zeros((target_dim),dtype='float')
            new_arr = arr2[dx:dx+tnx,dx:dx+tnx,dx:dx+tnx]
    elif current_pix_size != target_pix_size:
        print('Resizing in Fourier space and transforming back')
        new_arr = np.real(np.fft.ifftn(np.fft.fftn(arr2,s=target_dim)))
    return new_arr

def cut_resolution(f,bin_idx,res_arr,smax):
    import fcodes
    # Making data for map fitting
    nx,ny,nz = f.shape
    dist = np.sqrt((res_arr - smax)**2)
    cbin = np.argmin(dist) + 1 # adding 1 because fResArr starts with zero
    print('cnbin=', cbin)
    # fcodes.cutmap cuts f according to resolution defined by smax and output same size
    # map as f but padded with zeros outside smax
    fout = fcodes.cutmap(f,bin_idx,cbin,0,len(res_arr),nx,ny,nz)
    # cutmapresize.cutmap_resize imposes smax on f and resizes mapsize
    #import cutmapresize
    #fout = cutmapresize.cutmap_resize(f,bin_idx,cbin,0,len(res_arr),nx,ny,nz)
    return fout

def cut_resolution_for_linefit(f,bin_idx,res_arr,smax):
    import fcodes
    # Making data for map fitting
    nx,ny,nz = f.shape
    dist = np.sqrt((res_arr - smax)**2)
    cbin = np.argmin(dist) + 1 # adding 1 because fResArr starts with zero
    #print('cnbin=', cbin)
    if cbin%2 != 0: cx = cbin + 1
    else: cx = cbin
    #print('cx = ', cx, 'cnbin=', cbin)
    dx = int((nx - 2*cx)/2)
    dy = int((ny - 2*cx)/2)
    dz = int((nz - 2*cx)/2)
    cBIdx = bin_idx[dx:dx+2*cx,dy:dy+2*cx,dz:dz+2*cx]
    # fcodes.cutmap cuts f according to resolution defined by smax and output same size
    # map as f but padded with zeros outside smax
    fout = fcodes.cutmap(f,bin_idx,cbin,0,cbin,nx,ny,nz)[dx:dx+2*cx,dy:dy+2*cx,dz:dz+2*cx]
    # cutmapresize.cutmap_resize imposes smax on f and resizes mapsize
    #import cutmapresize
    #fout = cutmapresize.cutmap_resize(f,bin_idx,cbin,0,len(res_arr),nx,ny,nz)
    return fout

def mask_by_value(array,masking_value=0.0,filling_value=0.0):
    import numpy.ma as ma
    array_ma = ma.masked_less_equal(array, masking_value)
    array_masked_filled = array_ma.filled(filling_value)
    return array_masked_filled

def mask_by_value_greater(array,masking_value=0.0,filling_value=0.0):
    import numpy.ma as ma
    array_ma = ma.masked_greater(array, masking_value)
    array_masked_filled = array_ma.filled(filling_value)
    return array_masked_filled

def read_mmcif(mmcif_file):
    from gemmi import cif
    import numpy as np
    doc = cif.read_file(mmcif_file)
    block = doc.sole_block() # cif file as a single block
    a = block.find_value('_cell.length_a')
    b = block.find_value('_cell.length_b')
    c = block.find_value('_cell.length_c')
    alf = block.find_value('_cell.angle_alpha')
    bet = block.find_value('_cell.angle_beta')
    gam = block.find_value('_cell.angle_gamma')
    cell = np.array([a,b,c,alf,bet,gam],dtype='float')
    # Reading X coordinates in all atoms
    col_x = block.find_values('_atom_site.Cartn_x')
    col_y = block.find_values('_atom_site.Cartn_y')
    col_z = block.find_values('_atom_site.Cartn_z')
    # Reading B_iso values
    col_Biso = block.find_values('_atom_site.B_iso_or_equiv')
    # Casting gemmi.Columns into a numpy array
    #xyz_np = np.zeros((3,len(col_x)), dtype='float')
    #xyz_np = np.zeros((3,len(col_x)), dtype='float')
    #xyz_np = np.zeros((3,len(col_x)), dtype='float')
    #xyz_np[0,:] = np.array(col_x, dtype='float', copy=False)
    #xyz_np[1,:] = np.array(col_y, dtype='float', copy=False)
    #xyz_np[2,:] = np.array(col_z, dtype='float', copy=False)
    x_np = np.array(col_x, dtype='float', copy=False)
    y_np = np.array(col_y, dtype='float', copy=False)
    z_np = np.array(col_z, dtype='float', copy=False)
    Biso_np = np.array(col_Biso, dtype='float', copy=False)
    return cell,x_np,y_np,z_np,Biso_np

def run_refmac_sfcalc(filename,resol,bfac):
    # Creating the sfcalc.inp with custom parameters
    sfcalc_inp = open("sfcalc.inp","w+")
    sfcalc_inp.write("model sfcalc\n")
    sfcalc_inp.write("sfcalc cr2f\n")
    sfcalc_inp.write("resolution %f\n"%resol)
    sfcalc_inp.write("temp set %f\n"%bfac)
    sfcalc_inp.write("source em mb\n")
    sfcalc_inp.write("make hydrogen no\n")
    sfcalc_inp.write("end")
    sfcalc_inp.close()
    # Read in sfcalc_inp
    import os
    import os.path
    import subprocess
    fmtz = filename[:-4]+".mtz"
    #cmd = ["f2mtz","HKLIN",filename,"HKLOUT",fmtz]
    cmd = ["refmac5","XYZIN",filename,"HKLOUT",fmtz]
    PATH='sfcalc.inp'
    logf = open("sfcalc.log", "w+")
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print("sfcalc.inp exists and is readable")
        inp = open("sfcalc.inp","r")
        # Run the command with parameters from file f2mtz.inp
        subprocess.call(cmd,stdin=inp,stdout=logf)
    else:
        print("Either the file is missing or not readable")
    logf.close()
    inp.close()

def pdb2mmcif(filename_pdb):
    import gemmi
    structure = gemmi.read_structure(filename_pdb)
    mmcif = structure.make_mmcif_document()
    mmcif.write_file('out.cif')
