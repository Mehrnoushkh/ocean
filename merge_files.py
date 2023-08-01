
# coding: utf-8

# In[1]:


import numpy as np
from netCDF4 import Dataset

ofile = 'merged_fine_200km_4y.nc'

#ifiles =  [ "fine_vel_AVISO_3_{0:02d}_{1:02d}_500km.nc".format() for ii in range(1,12) ]
ifiles = ["filter_{0}_{1}km.nc".format(ii, 200) for ii in range(1, 5)]

with Dataset( ifiles[0], 'r' ) as dset:
    time  = dset['time'][:]
    depth = dset['depth'][:]
    lat   = dset['latitude'][:]
    lon   = dset['longitude'][:]

    Ntime, Ndepth, Nlat, Nlon = dset['u_lon_tor'].shape
    
    fill_value = getattr(dset['u_lon_tor'], "_FillValue")
    

    
    
Ntimes = []
for ifile in ifiles:
    with Dataset( ifile, 'r' ) as dset:
        time  = dset['time'][:]
        Ntimes += [len(time)]
Ntimes = np.array(Ntimes)
Ntime = np.sum(Ntimes)


####
dtype = np.float32
dtype_dim = np.float64

dims = ('time', 'depth', 'latitude', 'longitude')

# Now create a file to run through coarse-graining
with Dataset(ofile, 'w', format='NETCDF4') as fp:

    # time
    dim = 'time'
    t_dim = fp.createDimension(dim, Ntime)
    t_var = fp.createVariable(dim, dtype_dim, (dim,))

    # depth
    dim = 'depth'
    d_dim = fp.createDimension(dim, Ndepth)
    d_var = fp.createVariable(dim, dtype_dim, (dim,))
    d_var[:] = depth

    # lat
    dim = 'latitude'
    lat_dim = fp.createDimension(dim, Nlat)
    lat_var = fp.createVariable(dim, dtype_dim, (dim,))
    lat_var[:] = lat

    # lon
    dim = 'longitude'
    lon_dim = fp.createDimension(dim, Nlon)
    lon_var = fp.createVariable(dim, dtype_dim, (dim,))
    lon_var[:] = lon

    #
    uo_var = fp.createVariable('u_lon', dtype, dims, contiguous=True, fill_value = fill_value)
    uo_var.scale_factor = 1.

    vo_var = fp.createVariable('u_lat', dtype, dims, contiguous=True, fill_value = fill_value)
    vo_var.scale_factor = 1.

    #
    Itime = 0
    for II, ifile in enumerate(ifiles):
        with Dataset( ifile, 'r' ) as dset:
            for Iday in range( Ntimes[II] ):
                t_var[ Itime] = dset['time'][Iday]

                uo_var[Itime,0,:,:] = dset['u_lon_tor'][Iday,0,:,:] +dset['u_lon_pot'][Iday,0,:,:]
                vo_var[Itime,0,:,:] = dset['u_lat_tor'][Iday,0,:,:] +dset['u_lat_pot'][Iday,0,:,:]
                Itime += 1


print('Done')

