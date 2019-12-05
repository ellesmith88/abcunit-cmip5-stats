"""This script takes arguments from the command line and runs the function
run_unit for each of the variables provided as an argument or for
all variables if none were provided."""

import glob
import argparse
import xarray as xr

from lib import defaults

# parse command line and check all arguments are valid
def arg_parse_chunk():
    """Parses arguments given at the command line"""
    parser = argparse.ArgumentParser()
    stat_choices = ['min', 'max', 'mean']
    model_choices = defaults.models
    ensemble_choices = defaults.ensembles
    variable_choices = defaults.variables
    parser.add_argument('-s', '--stat', nargs=1, type=str, choices=stat_choices,
                        required=True, help=f'Type of statistic, must be one of: '
                                            f'{stat_choices}', metavar='')
    parser.add_argument('-m', '--model', nargs=1, type=str, choices=model_choices,
                        required=True, help=f'Institue and model combination to run statistic on, '
                                            f'must be one of: {model_choices}', metavar='')
    parser.add_argument('-e', '--ensemble', nargs=1, type=str, choices=ensemble_choices,
                        required=True, help=f'Ensemble to run statistic on, must be one of: '
                                            f'{ensemble_choices}', metavar='')
    parser.add_argument('-v', '--var', choices=variable_choices, default=variable_choices,
                        help=f'Variable to run statistic on, can be one or many of: '
                             f'{variable_choices}. Default is all variables.', metavar='')
    return parser.parse_args()


def loop_over_variables(args):
    """Runs the function run_unit for each of the variables listed"""
    # iterate over variables
    for i in args.var:
        arg_list = argparse.Namespace(ensemble=[args.ensemble], model=[args.model],
                                      stat=[args.stat], var=[i])
        # run_unit(arg_list)


def define_file_paths(args):
    """Defines output, success and failure file paths"""
    # define paths as absolute paths
    arguments = f"{args.stat}/{args.model}/{args.ensemble}"
    output_file_path = f"{current_directory}/outputs/{arguments}"
    success_file_path = f"{current_directory}/success/{arguments}"
    bad_data_file_path = f"{current_directory}/bad_valid_data/{arguments}"
    bad_num_file_path = f"{current_directory}/bad_num/{arguments}"
    return output_file_path, success_file_path, bad_data_file_path, bad_num_file_path


def find_files(args):
    """Finds files that correspond to the given arguments"""
    pattern = '/badc/cmip5/data/cmip5/output1/{model}/historical/mon/land' \
              '/Lmon/{ensemble}/latest/{var_id}/*.nc'
    try:
        glob_pattern = pattern.format(model=args.model,
                                      ensemble=args.ensemble, var=args.var)
        nc_files = glob.glob(glob_pattern)
        print(f'[INFO] found files: {nc_files}')
        return nc_files

    except Exception as err:
        print('[ERROR] No valid data')
        return False


def is_valid_range(nc_files, start='1900-01-01', end='2000-01-01'):
    """Checks the time range is valid for the given NetCDF files"""
    try:
        ds = xr.open_mfdataset(nc_files)
        times_in_range = ds.time.loc[start:end]

        n_req_times = 100 * 12 # yrs * months
        assert(len(times_in_range) == n_req_times)

        print('[INFO] Range is valid')
        return True

    except Exception as err:
        print('[ERROR] Range is invalid')
        return False


def calculate_statistic(nc_files, args):
    """Calculates the required statistic for each variable for each ensemble
    and model requested."""
    # args.var is a string so convert to variable name
    var_id = args.var
    dataset = xr.open_mfdataset(nc_files)
    if args.stat == 'mean':
        mean = dataset[var_id].mean(dim='time')
        return mean
    elif args.stat == 'max':
        maximum = dataset[var_id].max(dim='time')
        return maximum
    elif args.stat == 'min':
        minimum = dataset[var_id].max(dim='time')
        return minimum

def run_unit(args):
    """Keeps track of whether the job was successful or not and writes the
    result of the statistic to an output file."""
    # keep track of failures. MAny failures expected for this example so
    # limit is set to -1.
    # good practice to include this
    failure_count = 0
    # call other functions - add to failure count if needed & create failure files, write to output file
    # if fails - add to failure count
    # if succeeds - write success file

# exit if too many failures
# check for success file
# delete previous failure files
# files aree named after their variables

def main():
    """Runs script if called on command line"""
    args = arg_parse_chunk()
    loop_over_variables(args)



if __name__ == '__main__':
    main()
