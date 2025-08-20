import pandas as pd

def clean(df):
    df = df.copy()
    df['age'] = df['age'].astype(str).str.replace(r'\D+', '', regex=True)
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    return df