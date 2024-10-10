import pandas as pd

def ing_csv(csv_file):
    """
    Extracts data from an ING CSV file and performs basic data cleaning.

    Args:
        csv_file (str): The path to the ING CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the cleaned data.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file,
                     encoding='ISO-8859-2',
                     #error_bad_lines=False, 
                     sep='~~', 
                     header=None)

    # Extract the first four characters of each row as a string.
    # This is to find the first row contains the date, everhitng before is not needed.
    first_four = df[0].apply(lambda x: str(x)[:4])

    # Check if the first four characters are digits
    mask = first_four.str.isdigit()

    # Select only the rows where the first four characters are digits
    df = df[mask]

    # Split the values in the DataFrame by ';'
    df = df[0].str.split(';', expand=True)

    # Select only needed columns
    df = df[[0, 2, 3, 8, 9, 15, 16]]

    # Replace empty strings with NaN values
    df.replace("", None, inplace=True)

    # Remove rows with missing values
    df.dropna(axis=0, inplace=True)

    # Rename columns
    df = df.rename(columns={0:  'date',
                            2:  'title',
                            3:  'details',
                            8:  'value',
                            9:  'value_currency',
                            15: 'saldo',
                            16: 'saldo_currency'
                            })

    # Replace ',' with '.' and change type of columns
    df['value'] = df['value'].str.replace(',', '.').astype(float)
    df['saldo'] = df['saldo'].str.replace(',', '.').astype(float)
    df['date'] = df['date'].astype('datetime64[ns]')
    df.reset_index(drop=True, inplace=True)

    return df