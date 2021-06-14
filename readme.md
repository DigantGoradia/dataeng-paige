# Paige Data Engineer Test
An ETL script to transform the data per requirement and store it for the future process. This script is developed using python3.9 scripting language.
## Assumptions
1. The S3 bucket name needs to be defined and the files inside the bucket are accessible publicly(or by the company domain).
2. The source file is being uploaded daily before 9 AM.
3. The file which is used in this ETL script is static(provided with the problem statement) and the code is provided if one want to use the S3 bucket for pulling the file.
4. The results are satored in csv format in the local system which will be used to start the ETL pipeline. (This result data can be uploaded to any kind of target environment including mysql, mongodb, AWS service etc.)
5. The logs of the ETL pipeline will be stored in `logs.log` file, so user can see the logs anytime regardless of monitoring it.
## Prerequisites
To install dependecies, please run the following command in the terminal
```pip install -r requirements.txt```
## Usage
To start the ETL script, run the following command
```python main.py```

## Testing
`pytest` is used to test the developed functions in the script. This unit-testing script tests the basic user-defined functions developed in the script. To start the testing, please run the following command in the terminal. This will automatically target the test script and executes it.
```pytest```