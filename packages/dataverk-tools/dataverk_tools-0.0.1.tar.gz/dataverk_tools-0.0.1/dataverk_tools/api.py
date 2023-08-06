import requests
import pandas as pd


def mask_names(url: str, df: pd.DataFrame, columns: list):
    for column in columns:
        df[column] = [_mask_cell(url, cell) for cell in df[column]]


def _mask_cell(url, cell):
    return requests.post(url, data={"message": cell}).text
