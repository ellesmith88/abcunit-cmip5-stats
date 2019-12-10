import xarray as xr
import subprocess
import glob


def test_output_shape():
    cmd = 'python run_chunk.py -s min -m MOHC/HadGEM2-ES -e r1i1p1 -v rh'
    subprocess.call(cmd, shell=True)
    
    fpath = 'ALL_OUTPUTS/outputs/min/MOHC/HadGEM2-ES/r1i1p1/rh.nc'
    ds = xr.open_dataset(fpath)
    assert ds.rh.shape == (145, 192)

    cmd_delete = 'rm -r ALL_OUTPUTS'
    subprocess.call(cmd_delete, shell=True)


def test_is_valid_range():
    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land/Lmon' \
              '/{ensemble}/latest/{var_id}/*.nc'
    model = 'MOHC/HadGEM2-ES'
    ensemble = 'r1i1p1'
    var_id = 'rh'
    glob_pattern = pattern.format(model=model, ensemble=ensemble, var_id=var_id)
    nc_files = glob.glob(glob_pattern)

    ds = xr.open_mfdataset(nc_files)
    times_in_range = ds.time.loc['1900-01-01':'2000-01-01']

    n_req_times = 100 * 12  # yrs * months
    assert len(times_in_range) == n_req_times