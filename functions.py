import os
import pandas as pd


def load_data(file_path):
    """Load the data in the memory"""

    if not os.path.exists(file_path):
        return None

    return pd.read_csv(file_path)
