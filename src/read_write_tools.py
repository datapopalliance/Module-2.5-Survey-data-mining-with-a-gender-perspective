import os
import json
import pandas as pd
import pyreadstat

from os import listdir
from os.path import isfile, join


def read_files_in_folder(dir_path, file_type='csv', skip_rows={},low_memory=True, py_read_stat=False):
    """
    reads all the files of an specified 'file_type' into a pandas dataframe

    :param dir_path: location of a directory with multiple files
    :param file_type: type of files that are going to be read
    :param skip_rows: a dictionary where the key is the file name and the value is for how many rows you want to skip
    :return:
    """
    if os.path.exists(dir_path):
        # generating input logs
        print('Reading csv file(s) from', dir_path)
        all_files = listdir(dir_path)
        print('Total of', len(all_files), 'file(s)')
        csv_files = [file for file in all_files if file.endswith(file_type)]
        print('Total of', len(csv_files), f'{file_type} file(s)')

        # reading
        print('\nReading ...')
        dfs_with_names = {}

        for file in csv_files:
            print(file)
            # TODO: skip_rows only works with csv files, if you want to include more cases, add relevant code
            if file_type == "csv":
                if low_memory:
                    df = pd.read_csv(join(dir_path, file), skiprows=skip_rows.get(file))
                else: 
                    df = pd.read_csv(join(dir_path, file), skiprows=skip_rows.get(file),low_memory=False)
            elif file_type == "sav":
                if py_read_stat:
                    df, meta = pyreadstat.read_sav(join(dir_path, file),encoding="LATIN1")
                else:
                    df = pd.read_spss(join(dir_path, file))
            else:
                raise Exception('Oops!  That was no valid file type.  Try again...')

            dfs_with_names[file] = df

        return dfs_with_names
    else:
        print('This directory', dir_path, 'does not exists')
        return None


def read_xlsx_files_in_folder(dir_path, read_inputs={}):
    """
    reads all the xlsx files on a dir_path into pandas dataframes

    :param dir_path: location of a directory with multiple files
    :param read_inputs: a dictionary whith the following schema
                        {
                        file_name_1:
                                  {
                                  sheet_name_1:
                                               {
                                               usecols: str
                                               skiprows: int
                                               }
                                  sheet_name_2:
                                                ...
                                  },
                        file_name_2:
                                    ...
                        }
    :return:
    """
    if os.path.exists(dir_path):
        # generating input logs
        print('Reading csv file(s) from', dir_path)
        all_files = listdir(dir_path)
        print('Total of', len(all_files), 'file(s)')
        csv_files = [file for file in all_files if file.endswith("xlsx")]
        print('Total of', len(csv_files), f'{"xlsx"} file(s)')

        # reading
        print('\nReading ...')
        dfs_with_names = {}

        for file in csv_files:
            print(file)
            file_inputs = read_inputs.get(file)

            if not file_inputs:
                print(f"  Not input setting were specified for {file}.", "The input settings will be inferred by pandas")
                df = pd.read_excel(join(dir_path, file))

                dfs_with_names[file] = df
            else:
                for sheet_name, sheet_input in file_inputs.items():
                    use_cols = sheet_input.get("usecols")
                    skip_rows = sheet_input.get("skiprows")

                    print(f"  The specified inputs for {file} {sheet_name} were usecols: {use_cols} skiprows: {skip_rows}")
                    df = pd.read_excel(join(dir_path, file), sheet_name=sheet_name, usecols=use_cols, skiprows=skip_rows)

                    dfs_with_names["SHEET_" + str(sheet_name) + "_FILE_" + file] = df

        return dfs_with_names
    else:
        print('This directory', dir_path, 'does not exists')
        return None

#def read_csv_and_xlsx_files_in_folder 

def create_dir(dir_path):
    os.mkdir(dir_path)
    print("Directory", dir_path, "created ")


def write_files_dpa_convention(dfs_with_names, data_code, file_type="csv"):
    """

    :param dfs_with_names:
    :param data_code:
    :param file_type: type of output file
    :return:
    """
    dir_path = f'data/prepared/{data_code}/'

    if file_type not in ["parquet", "csv"]:
        raise Exception('Oops!  That was no valid file type.  Try again...')

    if not os.path.exists(dir_path):
        create_dir(dir_path)
        names_dictionary = {}

        for index, (name, df) in enumerate(dfs_with_names.items()):
            new_name = data_code + '_' + str(index) + '_cleaned'
            names_dictionary[new_name] = name

            print('Writing ', new_name)
            if file_type == "parquet":
                output_path = dir_path + new_name + '.parquet.gzip'
                df.to_parquet(output_path, compression='gzip')
            elif file_type == "csv":
                output_path = dir_path + new_name + '.csv'
                df.to_csv(output_path, index=False)

        print("Writing data_names_dictionary.json")
        with open(os.path.join(dir_path, "data_names_dictionary.json"), 'w') as outfile:
            json.dump(names_dictionary, outfile)
    else:
        print("Directory", dir_path, "already exists. The file is not going to be written as a precaution")
        
        
def read_files_in_multiple_folders(parent_dir, file_type='csv', skip_rows={},low_memory=True):
    """
    reads all the files in multiple folders of a specific directory into a pandas dataframe, works with csv and sav files.

    :param parent_dir: location of a directory with multiple folders containing multiple files
    :param file_type: type of files that are going to be read
    :param skip_rows: a dictionary where the key is the file name and the value is for how many rows you want to skip
    :return:
    """
    if os.path.exists(parent_dir):
        dfs_with_names = {}
        for folder in os.listdir(parent_dir):
            # generating input logs
            print('Reading csv file(s) from', folder)
            dir_path = join(parent_dir, folder)
            all_files = listdir(dir_path)
            print('Total of', len(all_files), 'file(s)')
            csv_files = [file for file in all_files if file.endswith(file_type)]
            print('Total of', len(csv_files), f'{file_type} file(s)')

            # reading
            print('\nReading from', folder, '...')

            for file in csv_files:
                print(file)
                # TODO: skip_rows only works with csv files, if you want to include more cases, add relevant code
                if file_type == "csv":
                    if low_memory==True:
                        df = pd.read_csv(join(dir_path, file), skiprows=skip_rows.get(file))
                    else: 
                        df = pd.read_csv(join(dir_path, file), skiprows=skip_rows.get(file),low_memory=False)
                elif file_type == "DTA":
                    df = pd.read_stata(join(dir_path, file),convert_categoricals=False)
                else:
                    raise Exception('Oops!  That was no valid file type.  Try again...')

                dfs_with_names[file] = df
       
        return dfs_with_names
    else:
        print('This directory', dir_path, 'does not exists')
        return None        
    
    
def read_files_with_multiple_tables(dir_path, table='Table',file_type='csv',skip_rows={}):
    """
    reads files with multiple tables and separates each table in a new dataframe, only works with csv, if the specified file_type is sav or another the function is the same than read_files_in_folder

    :param dir_path: location of a directory with multiple files
    :param file_type: type of files that are going to be read
    :param skip_rows: a dictionary where the key is the file name and the value is for how many rows you want to skip
    :return:
    """
    if os.path.exists(dir_path):
        # generating input logs
        print('Reading csv file(s) from', dir_path)
        all_files = listdir(dir_path)
        print('Total of', len(all_files), 'file(s)')
        csv_files = [file for file in all_files if file.endswith(file_type)]
        print('Total of', len(csv_files), f'{file_type} file(s)')

        # reading
        print('\nReading ...')
        dfs_with_names = {}

        for file in csv_files:
            print(file)
            # TODO: skip_rows only works with csv files, if you want to include more cases, add relevant code
            if file_type == "csv": 
                    df = pd.read_csv(join(dir_path, file), skiprows=skip_rows.get(file),low_memory=False, header=None)
                    tables = df[0].str.contains(str(table))
                    contain_table = [row for row in df[0].index if tables[row] == True]
                    
                    blanks =  df[0].isnull()
                    blank_rows = [row for row  in blanks.index if blanks[row] == True]
                    blank_rows.append(df[0].index[-1]+1)
                    
                    for begin in contain_table:
                        end = next(blank for blank in blank_rows if blank > begin)
                        df_temp = df.iloc[begin+2:end,:] 
                        df_temp.rename(columns=df.iloc[begin+1,:],inplace=True)
                        df_temp.reset_index(drop=True, inplace=True)
                        dfs_with_names[file + ' ' + df.iloc[begin,0]] = df_temp
    
            elif file_type == "sav":
                if py_read_stat:
                    df, meta = pyreadstat.read_sav(join(dir_path, file),encoding="LATIN1")
                else:
                    df = pd.read_spss(join(dir_path, file))
            else:
                raise Exception('Oops!  That was no valid file type.  Try again...')


        return dfs_with_names
    else:
        print('This directory', dir_path, 'does not exists')
        return None
    
