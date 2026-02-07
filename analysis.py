import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
"""
# 1. تحميل البيانات
print(">>> ⏳ Loading Data...")
df = pd.read_csv('Saudi_Supply_Chain.csv')

# ضبط الستايل
sns.set_style("whitegrid")

# ==========================================
# 🛑 خطوة التصفية (Filtering)
# هنا نقول له: "يا كمبيوتر، تجاهل Other City وركز على مدننا الحبيبة"
# ==========================================
df_saudi = df[df['Order City'] != 'Other City']

# ==========================================
# الرسمة 1: مبيعات المدن السعودية (الصافية) 📊
# ==========================================
print("\n>>> 📊 Generating Chart 1 (Saudi Cities Only)...")

# نستخدم المتغير الجديد df_saudi
city_sales = df_saudi.groupby('Order City')['Sales per customer'].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=city_sales.index, y=city_sales.values, palette='viridis')

plt.title('Total Sales by Saudi City (Excluding Others)', fontsize=15)
plt.xlabel('City', fontsize=12)
plt.ylabel('Total Sales (SAR)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================
# الرسمة 2: توزيع حالات الطلب 🍕
# ==========================================
print(">>> 🍕 Generating Chart 2...")

# هنا نرجع نستخدم df الأصلية عشان نشوف الوضع العام (أو تقدر تستخدم df_saudi لو تبي بس للسعودية)
status_counts = df['Order Status'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Order Status Distribution (Global)', fontsize=15)
plt.show()

# ==========================================
# طباعة اسم المدينة الفائزة 🏆
# ==========================================
print("\n" + "="*50)
print(f"🏆 Top Performing City in Saudi Arabia: {city_sales.index[0]}")
print("="*50)
"""


"""
df = pd.read_csv('Saudi_Supply_Chain.csv')
print(">>>  Type of deliver")    # عشان نعرف سبب من اسباب التاخير اشوف خيارات التوصيل
print(df['Shipping Mode'].unique())
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. تحميل البيانات
print(">>> ⏳ Loading Data...")
df = pd.read_csv('Saudi_Supply_Chain.csv')

# نركز فقط على المدن السعودية
df_saudi = df[df['Order City'] != 'Other City']

# ==========================================
# التحقيق: من هي طريقة الشحن التي تتأخر؟ 🚛🔍
# ==========================================
print("\n>>> 🕵️‍♂️ Investigating Shipping Modes...")

# نحسب نسبة التأخير لكل نوع شحن
# نجمع (المتأخرين) ونقسمهم على (العدد الكلي) لكل نوع
shipping_delay = df_saudi.groupby('Shipping Mode')['Late_delivery_risk'].mean() * 100
shipping_delay = shipping_delay.sort_values(ascending=False)

# الطباعة بالأرقام
print("\n📊 نسبة التأخير لكل نوع شحن:")
print(shipping_delay)

# الرسم البياني
plt.figure(figsize=(10, 6))
# نرسم الأعمدة
sns.barplot(x=shipping_delay.index, y=shipping_delay.values, hue=shipping_delay.index, legend=False, palette='Reds_r')

plt.title('Delay Percentage by Shipping Mode ⚠️\n(من هي طريقة الشحن الأسوأ؟)', fontsize=15)
plt.xlabel('Shipping Mode (طريقة الشحن)', fontsize=12)
plt.ylabel('Delay Percentage (%)', fontsize=12)
plt.ylim(0, 100) # نخلي الرسمة من 0 إلى 100%

# نضيف الخط الأحمر عند 50% عشان نعرف الخطر
plt.axhline(y=50, color='red', linestyle='--', label='Danger Zone (50%)')
plt.legend()

plt.tight_layout()
plt.show()
