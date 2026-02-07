import pandas as pd
import os

print("Reading the large file... please wait ")

try:
  
    df = pd.read_csv('Saudi_Supply_Chain.csv', encoding='utf-8')
except UnicodeDecodeError:
 
    df = pd.read_csv('Saudi_Supply_Chain.csv', encoding='ISO-8859-1')


required_columns = [
    'Shipping Mode', 
    'Order City', 
    'Category Name', 
    'Customer Segment', 
    'Order Item Quantity', 
    'Delivery Status'
]

output_filename = 'Saudi_Supply_Chain_Lite.csv'
df_lite = df[required_columns]
df_lite.to_csv(output_filename, index=False)

file_size_mb = os.path.getsize(output_filename) / (1024 * 1024)
print(f"✅ Done! New file created: {output_filename}")
print(f"📉 New Size: {file_size_mb:.2f} MB")
print("👉 Action required: Upload this file to GitHub but RENAME it to 'Saudi_Supply_Chain.csv'.")