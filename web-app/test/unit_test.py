import sys
import os
from unittest.mock import patch, MagicMock, mock_open
import warnings
import pandas as pd
import numpy as np
import pytest

# Suppress all warnings
warnings.filterwarnings('ignore')

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import aws_import as ai
import generate_features as gf

# Tests for aws_import.py
@patch('aws_import.boto3.client')
@patch('aws_import.joblib.load')
@patch('builtins.open', new_callable=mock_open)
def test_download_model_from_s3(mock_open, mock_joblib_load, mock_boto_client):
    # Mock S3 client
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    # Mock model loading
    mock_model = MagicMock()
    mock_joblib_load.return_value = mock_model

    bucket_name = 'test-bucket'
    model_key = 'test-model.pkl'
    local_path = 'local-model.pkl'

    # Simulate FileNotFoundError
    mock_open.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError):
        ai.download_model_from_s3(bucket_name, model_key, local_path)

    mock_s3.download_file.assert_called_with(bucket_name, model_key, local_path)

@patch('aws_import.download_model_from_s3')
def test_load_model(mock_download_model_from_s3):
    aws_config = {
        'bucket_name': 'test-bucket',
        'rf_key': 'rf-model.pkl',
        'gb_key': 'gb-model.pkl',
        'rf_path': 'rf-local.pkl',
        'gb_path': 'gb-local.pkl'
    }

    mock_model_rf = MagicMock()
    mock_model_gb = MagicMock()
    mock_download_model_from_s3.side_effect = [mock_model_rf, mock_model_gb]

    result_rf = ai.load_model(aws_config, 'Random Forest')
    result_gb = ai.load_model(aws_config, 'Gradient Boosting')

    assert result_rf == mock_model_rf
    assert result_gb == mock_model_gb

def test_make_prediction():
    model = MagicMock()
    input_data = pd.DataFrame(np.random.rand(10, 5))
    model.predict_proba.return_value = np.random.rand(10, 2)
    model.predict.return_value = np.random.randint(2, size=10)

    proba, prediction = ai.make_prediction(model, input_data)

    model.predict_proba.assert_called_with(input_data)
    model.predict.assert_called_with(input_data)
    assert proba.shape == (10, 2)
    assert prediction.shape == (10,)

# Tests for generate_features.py
def test_generate_features():
    data = pd.DataFrame({
        'min_col': [1, 2, 3],
        'max_col': [4, 5, 6],
        'mean_col': [2, 3, 4],
        'value': [10, 20, 30]
    })

    config = {
        'calculate_norm_range': {
            'norm_range': {'min_col': 'min_col', 'max_col': 'max_col', 'mean_col': 'mean_col'}
        },
        'log_transform': {
            'log_value': 'value'
        },
        'multiply': {
            'value_product': {'col_a': 'value', 'col_b': 'min_col'}
        }
    }

    expected_data = data.copy()
    expected_data['norm_range'] = (data['max_col'] - data['min_col']) / data['mean_col']
    expected_data['log_value'] = np.log(data['value'] + 1)
    expected_data['value_product'] = data['value'] * data['min_col']

    result_data = gf.generate_features(data, config)

    pd.testing.assert_frame_equal(result_data, expected_data)

if __name__ == '__main__':
    pytest.main()