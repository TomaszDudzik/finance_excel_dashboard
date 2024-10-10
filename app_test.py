import openai
from openai import OpenAI
import pandas as pd

from etl.bank_etl.ing_csv import ing_csv

ing_csv_path = r'C:/Users/dudzi/OneDrive/Python/excel_python/Lista_transakcji_nr_0197050513_061024.csv'


# Define a function to use OpenAI to categorize transactions
def categorize_transaction(row):
    
    # Set your OpenAI API key
    client = OpenAI(
        api_key="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",
    )

    prompt = f"Categorize the following bank transaction: Title: {row['title']} Details: {row['details']} Value: {row['value']}. Choose from the following categories: Income, Transportation, Groceries, Dining & Entertainment, Healthcare, Debt Payments, Savings & Investments, Insurance, Miscellaneous. If value is positive, it is an Income."
    
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # or "gpt-4" if available
      messages=[
        {"role": "system", "content": "You are a helpful assistant that categorizes bank transactions."},
        {"role": "user", "content": prompt}
      ],
      max_tokens=10
    )
    
    # Extract the model's response
    category = response.choices[0].message.content.strip()
    return category

def app():
    df = ing_csv(ing_csv_path)

    # Apply the categorization function to the DataFrame
    #df['Category'] = df.apply(categorize_transaction, axis=1)

    # Display the updated DataFrame with the 'Category' column
    print(df)

    # Convert DataFrame to CSV
    output_csv_path = r'C:/Users/dudzi/OneDrive/Python/excel_python/ing_etl.csv'
    csv_data = df.to_csv(output_csv_path, sep='~', encoding='utf-8')

    # Convert DataFrame to Excel
    output_excel_path = r'C:/Users/dudzi/OneDrive/Python/excel_python/ing_etl.xlsx'
    df.to_excel(output_excel_path, index=False)

    return csv_data

if __name__ == '__main__':
    app()