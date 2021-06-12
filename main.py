import os
import datetime
import pandas as pd

RESULT_DIR = 'results'
MISSING_DATA_DIR = 'missing_data'

if not os.path.exists(RESULT_DIR):
	os.mkdir(RESULT_DIR)
if not os.path.exists(MISSING_DATA_DIR):
	os.mkdir(MISSING_DATA_DIR)

def getSugarLevel(row):
	if row['avg_glucose'] <= 140:
		return 'normal'
	elif row['avg_glucose'] > 140 and row['avg_glucose'] < 199:
		return 'prediabetes'
	return 'diabetes'

def main():
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

    #Try to read previous day data if exists
    try:
        previous_date = file_date - datetime.timedelta(days=1)
        str_prevous_date = previous_date.strftime('%Y-%m-%d')

        previous_day_df = pd.read_csv(f'{MISSING_DATA_DIR}/{str_prevous_date}_missing_data.csv',
                                delimiter=',',
                                encoding='ISO-8859-1'
                        )
        
        if previous_day_df is not None:
            previous_day_df.set_index('patient_id')
            df.update(previous_day_df)
    except:
        pass

    # Calculate glucose averages, where values is missing NaN will be result in answer
    df['avg_glucose'] = df[['glucose_test_1', 'glucose_test_2', 'glucose_test_3']].mean(axis=1, skipna=False)

    # Remove any rows with NaN values in glucose average value.
    # Create new DataFrame of removed rows and store it into csv file 
    # for processing it next day.
    missing_data_df = df[df['avg_glucose'].isnull()]
    missing_data_df.reset_index(drop=True, inplace=True)

    # Drop PHI Informations including name, email & address
    df.drop(['first_name', 'last_name', 'email', 'address'], axis=1, inplace=True)

    # Drop the NaN average glucose values
    df.dropna(subset = ['avg_glucose'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Get the sugar level and add new column to DataFrame
    df['sugar_level'] = df.apply(getSugarLevel, axis=1)

    # Create new file for missing data to process next day
    missing_data_df.to_csv(f'{MISSING_DATA_DIR}/{str_file_date}_missing_data.csv',
                sep=',',
                index=False
    )

    # Create result file containing the actual output of ETL pipeline
    df.to_csv(f'{RESULT_DIR}/{str_file_date}_result.csv',
                sep=',',
                index=False
    )

if __name__ == '__main__':
    main()