import os
import datetime
import pandas as pd

RESULT_DIR = 'results'
MISSING_DATA_DIR = 'missing_data'

if not os.path.exists(RESULT_DIR):
	os.mkdir(RESULT_DIR)
if not os.path.exists(MISSING_DATA_DIR):
	os.mkdir(MISSING_DATA_DIR)

'''
#   S3 bucket name is required for pulling csv file from.

#   Assumpsions:
        The S3 bucket is public and requested file is accessible anytime.
        The file is being uploaded in S3 bucket everyday at some specified time.

# The bucket name can always be parameterised by any kind of workaround.
S3_BUCKET_NAME = <bucket-name>

# extract sytem date to get today's date and use this to pull today's file from S3 bucket
today = datetime.datetime.today()
str_date = today.strftime('%Y-%m-%d')

try:
    csv_file = 'https://' + S3_BUCKET_NAME + '.s3.amazonaws.com/' + str_date + '_patient_data.csv'

except Exception as e:
    pass
'''

file_date = datetime.datetime(2020, 10, 28)
str_file_date = file_date.strftime('%Y-%m-%d')

# Read csv file and clean the glucose data to replace n/a and null values to NaN
try:
    df = pd.read_csv(f'{str_file_date}_patient_data.csv', 
                    delimiter=',', 
                    encoding='ISO-8859-1', 
                    na_values={
                        'glucose_mg/dl_t1': ['n/a', 'null'],
                        'glucose_mg/dl_t2': ['n/a', 'null'],
                        'glucose_mg/dl_t3': ['n/a', 'null']     
                    },
                    header=0,
                    names=['patient_id', 'first_name', 'last_name', 'email', 'address', 'glucose_test_1', 'glucose_test_2', 'glucose_test_3', 'cancer_present', 'atrophy_present']
                    )
except Exception as e:
    pass