import pandas as pd
import numpy as np

# 1. Load Data
print(">>> ⏳ Loading Raw Data...")
df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='latin-1')

# ---------------------------------------------------------
# STEP 1: CURRENCY CONVERSION (USD -> SAR) 💵
# ---------------------------------------------------------
print(">>> 🔄 Converting Currency to Saudi Riyals (SAR)...")
# سعر الصرف 3.75
df['Sales per customer'] = round(df['Sales per customer'] * 3.75, 2)
df['Benefit per order'] = round(df['Benefit per order'] * 3.75, 2)

# ---------------------------------------------------------
# STEP 2: LOCATION MAPPING (Cities -> Saudi Cities) 🇸🇦
# ---------------------------------------------------------
print(">>> 🗺️ Mapping Cities to Saudi Arabia...")

# نغير اسم الدولة للجميع
df['Order Country'] = 'Saudi Arabia'

# خريطة التحويل (بناءً على المدن الأكثر تكراراً اللي طلعت لك)
city_map = {
    'Santo Domingo': 'Riyadh',        # العاصمة (الأكثر تكراراً)
    'New York City': 'Jeddah',        # العاصمة التجارية
    'Los Angeles': 'Dammam',          # المنطقة الشرقية
    'Tegucigalpa': 'Mecca',           # مكة المكرمة
    'Managua': 'Medina',              # المدينة المنورة
    'Mexico City': 'Khobar',          # الخبر
    'Manila': 'Abha',                 # أبها
    'Philadelphia': 'Tabuk',          # تبوك
    'San Francisco': 'Buraidah',      # بريدة
    'London': 'Jizan'                 # جازان
}

# تطبيق التحويل: أي مدينة غير موجودة فوق بنسميها 'Other City'
df['Order City'] = df['Order City'].map(city_map).fillna('Other City')

# نغير المنطقة (Region) بناءً على المدينة الجديدة
def get_saudi_region(city):
    if city in ['Riyadh', 'Buraidah']: return 'Central Region'
    if city in ['Jeddah', 'Mecca', 'Medina', 'Jizan', 'Tabuk']: return 'Western Region'
    if city in ['Dammam', 'Khobar']: return 'Eastern Region'
    if city == 'Abha': return 'Southern Region'
    return 'Other Region'

df['Order Region'] = df['Order City'].apply(get_saudi_region)

# ---------------------------------------------------------
# STEP 3: SAVE NEW FILE 💾
# ---------------------------------------------------------
print(">>> 💾 Saving new Saudi dataset...")
df.to_csv('Saudi_Supply_Chain.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*50)
print("✅ SUCCESS! SAUDIZATION COMPLETE.")
print("="*50)
print("New File Created: 'Saudi_Supply_Chain.csv'")
print("\n👀 SAMPLE OF NEW DATA:")
print(df[['Order Country', 'Order Region', 'Order City', 'Sales per customer']].head(10))