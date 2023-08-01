
# coding: utf-8

# In[1]:


from netCDF4 import Dataset
import numpy as np


# In[27]:


fname = 'merged_fine_200km_4y.nc'
fname_o = '../../full_AVISO_timeseries.nc'
ofile = 'filter_small_200km.nc'


# In[25]:


# high pass filtered velocity

with Dataset('merged_fine_200km_4y.nc', 'r') as ds:
    print( ds.variables.keys() )
    lon = np.array(ds.variables['longitude'])
    lat = np.array(ds.variables['latitude'])
    Itime = np.array(ds.variables['time'])
    vel = np.array(ds.variables['u_lon'])
    
    time  = ds['time'][:]
    depth = ds['depth'][:]
    lat   = ds['latitude'][:]
    lon   = ds['longitude'][:]
    Ntime, Ndepth, Nlat, Nlon = ds['u_lon'].shape
    fill_value = getattr(ds['u_lon'], "_FillValue")


# In[9]:


# *************.  total velocity  ********************
with Dataset(fname_o, 'r') as ds2:
    
    print( ds2.variables.keys() )
    vel_1 = np.array(ds2.variables['uo'][0:1460,:,:,:])


# In[15]:


print(vel.shape, time.shape)


# In[ ]:


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
    uo_var = fp.createVariable('uo', dtype, dims, contiguous=True, fill_value = fill_value)
    uo_var.scale_factor = 1.
    
    vo_var = fp.createVariable('vo', dtype, dims, contiguous=True, fill_value = fill_value)
    vo_var.scale_factor = 1.

   
    

    with Dataset(fname, 'r') as ds:
        with Dataset(fname_o, 'r') as ds2:
            Itime = 0
            for Itime in range(0,1460,1):
                t_var[Itime] = ds['time'][Itime]
                uo_var[Itime,0,:,:] = ds2['uo'][Itime,0,:,:] - ds['u_lon'][Itime,0,:,:] 
                vo_var[Itime,0,:,:] = ds2['vo'][Itime,0,:,:] - ds['u_lat'][Itime,0,:,:] 

                Itime += 1
    print('Done')


# In[ ]:


with Dataset('filter_small_200km.nc', 'r') as ds3:
    print( ds3.variables.keys() )
    time1 = np.array(ds3.variables['time'])
    vel2 = np.array(ds3.variables['u'])
    print(time1.shape)
    print(vel2.shape)       
vel2.shape
#print(vel[52,0,336,522])
print(np.nanmin(vel2))
print(np.nanmax(vel2))

