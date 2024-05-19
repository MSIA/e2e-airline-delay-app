import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger('delay')

def generate_features(data: pd.DataFrame) -> pd.DataFrame:
    '''
    Generate features from data

    Args:
        data (pd.DataFrame): The input DataFrame containing the data.

    Returns:
        pd.DataFrame: The DataFrame with generated features.
    '''
    data = data[data['Cancelled'] == False]
    dep_time = []
    for i in data['DepTimeBlk']:
        dep_time.append(int(i[0:2]))
    data['dep_time'] = dep_time
    for col in ['Airline', 'dept-type', 'arr-type']:
        ohe = pd.get_dummies(data[col])
        data = pd.concat([data, ohe], axis=1)
    return data

def save_features(data: pd.DataFrame, location: Path) -> None:
    '''
    Save data as csv

    Args:
        data (pd.DataFrame): The DataFrame to be saved.
        location (Path): The path to save the CSV file.
    '''
    try:
        data.to_csv(location)
        logger.info('Data with features saved to %s', location)
    except FileNotFoundError as e:
        logger.error('File not found error occurred while saving features: %s', e)