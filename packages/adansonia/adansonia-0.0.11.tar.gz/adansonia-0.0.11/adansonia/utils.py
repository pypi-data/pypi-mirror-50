#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
from subprocess import Popen
from os.path import abspath



def reduce_mem_usage(df, verbose=False):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
    """
    df = pd.DataFrame(df)

    UINT8 = np.iinfo(np.uint8)
    UINT16=np.iinfo(np.uint16)
    UINT32=np.iinfo(np.uint32)
    UINT64=np.iinfo(np.uint64)

    INT8=np.iinfo(np.int8)
    INT16=np.iinfo(np.int16)
    INT32=np.iinfo(np.int32)
    INT64=np.iinfo(np.int64)

    FLOAT16=np.finfo(np.float16)
    FLOAT32=np.finfo(np.float32)

    if verbose:
        start_mem = df.memory_usage().sum() / 1024**2
        print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))

    for col in list(df.columns):
        col_type = df[col].dtype

        if col_type == 'float64' or col_type == 'int64':
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':

            # Test Unsigned Integer
                if c_min > UINT8.min and c_max < UINT8.max:
                    df[col] = df[col].astype(np.uint8)

                elif c_min > UINT16.min and c_max < UINT16.max:
                    df[col] = df[col].astype(np.uint16)

                elif c_min > UINT32.min and c_max < UINT32.max:
                    df[col] = df[col].astype(np.uint32)

                elif c_min > UINT64.min and c_max < UINT64.max:
                    df[col] = df[col].astype(np.uint64)

            # Test Integer
                elif c_min > INT8.min and c_max < INT8.max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > INT16.min and c_max < INT16.max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > INT32.min and c_max < INT32.max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > INT64.min and c_max < INT64.max:
                    df[col] = df[col].astype(np.int64)

            # Test Float   
            else:
                if c_min > FLOAT16.min and c_max < FLOAT16.max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > FLOAT32.min and c_max < FLOAT32.max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        elif col_type == object:
            df[col] = df[col].astype('category')

    if verbose:
        end_mem = df.memory_usage().sum() / 1024**2
        print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
        print('Decreased by {:.1f}%'.format(100 *
                                        (start_mem - end_mem) / start_mem))
    return df


class scp_AWS(object):
    def __init__(self, servername, key_file, username):
        self.servername = servername
        self.key_file = abspath(key_file)
        self.username = username

    def get(self, distant_file, destination):
        p = Popen([
            'scp',
            '-i',
            self.key_file,
            self.username + '@' + self.servername + ':' + distant_file,
            destination
        ])
        if p.wait() !=0:
            raise Exception('Process failed')

    def set(self, file, destination):
        p = Popen([
            'scp', '-i', self.key_file, file,
            self.username + '@' + self.servername + ':' + destination
        ])
        if p.wait() !=0:
            raise Exception('Process failed')