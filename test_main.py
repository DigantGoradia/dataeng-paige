import main
import pandas as pd
from pandas.testing import assert_frame_equal

test_data = {
    'patient_name': ['patient_1', 'patient_2', 'patient_3', 'patient_4', 'patient_5'],
    'avg_glucose': [139.0, 155.0, 199.05, 240.10, 100]
}

result_data = {
    'patient_name': ['patient_1', 'patient_2', 'patient_3', 'patient_4', 'patient_5'],
    'avg_glucose': [139.0, 155.0, 199.05, 240.10, 100],
    'sugar_level': ['normal', 'prediabetes', 'diabetes', 'diabetes', 'normal']
}

def test_getSugarLevel():
    test_df = pd.DataFrame(test_data)
    result_df = pd.DataFrame(result_data)

    test_df['sugar_level'] = test_df.apply(main.getSugarLevel, axis=1)

    assert_frame_equal(result_df, test_df)