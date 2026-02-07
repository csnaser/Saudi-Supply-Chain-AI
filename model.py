import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

print("Loading data...")
try:
    df = pd.read_csv('Saudi_Supply_Chain.csv', encoding='utf-8')
except:
    df = pd.read_csv('Saudi_Supply_Chain.csv', encoding='ISO-8859-1')


df = df[['Shipping Mode', 'Order City', 'Category Name', 'Customer Segment', 'Order Item Quantity', 'Delivery Status']]
df.dropna(inplace=True)

le_shipping = LabelEncoder()
le_city = LabelEncoder()
le_category = LabelEncoder()
le_segment = LabelEncoder()

df['Shipping Mode'] = le_shipping.fit_transform(df['Shipping Mode'])
df['Order City'] = le_city.fit_transform(df['Order City'])
df['Category Name'] = le_category.fit_transform(df['Category Name'])
df['Customer Segment'] = le_segment.fit_transform(df['Customer Segment'])

df['Target'] = df['Delivery Status'].apply(lambda x: 1 if x == 'Late Delivery' else 0)


X = df.drop(['Delivery Status', 'Target'], axis=1)
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print("Training Lite Model...")

model = RandomForestClassifier(
    n_estimators=30, 
    max_depth=10, 
    n_jobs=-1, 
    random_state=42
)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

print("Saving compressed files...")

joblib.dump(model, 'my_model.pkl', compress=3) 
joblib.dump(le_shipping, 'le_shipping.pkl', compress=3)
joblib.dump(le_city, 'le_city.pkl', compress=3)
joblib.dump(le_category, 'le_category.pkl', compress=3)
joblib.dump(le_segment, 'le_segment.pkl', compress=3)

size_mb = os.path.getsize('my_model.pkl') / (1024 * 1024)
print(f"Done. Model size is now: {size_mb:.2f} MB")