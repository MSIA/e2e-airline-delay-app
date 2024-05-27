import pandas as pd
import pytest
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import src.evaluate_performance as ep

def test_evaluate_performance_happy_path():
    # Create a sample DataFrame with valid data
    data = {
        "test": pd.Series([3, -0.5, 2, 7]),
        "pred": pd.Series([2.5, 0.0, 2, 8])
    }
    scores = pd.DataFrame(data)
    
    # Calculate expected metrics
    y_test = scores["test"]
    y_pred = scores["pred"]
    expected_mae = mean_absolute_error(y_test, y_pred)
    expected_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    expected_r2 = r2_score(y_test, y_pred)
    
    # Call the function
    result = ep.evaluate_performance(scores)
    
    # Assert the results
    assert result["mae"] == expected_mae
    assert result["rmse"] == expected_rmse
    assert result["r2"] == expected_r2


def test_evaluate_performance_nan_values():
    # Create a DataFrame with NaN values
    data = {
        "test": pd.Series([3, np.nan, 2, 7]),
        "pred": pd.Series([2.5, 0.0, 2, 8])
    }
    scores = pd.DataFrame(data)
    
    # Expect ValueError due to NaN values
    with pytest.raises(ValueError, match="Input scores contain NaN values"):
        ep.evaluate_performance(scores)
  