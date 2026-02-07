import streamlit as st
import joblib
import pandas as pd

# ==========================================
# 1. إعدادات الصفحة (Design Setup) 🎨
# ==========================================
st.set_page_config(
    page_title="Amazon SC Command Center",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. تحميل البيانات والمودل 📥
# ==========================================
@st.cache_resource
def load_data_and_model():
    # تحميل المودل
    try:
        model = joblib.load('my_model.pkl')
        encoders = {
            'shipping': joblib.load('le_shipping.pkl'),
            'city': joblib.load('le_city.pkl'),
            'category': joblib.load('le_category.pkl'),
            'segment': joblib.load('le_segment.pkl')
        }
    except:
        model, encoders = None, None

    # تحميل البيانات الأصلية (عشان لوحة المعلومات)
    try:
        df = pd.read_csv('Saudi_Supply_Chain.csv')
    except:
        df = pd.DataFrame() # لو الملف مو موجود يسوي جدول فاضي
        
    return df, model, encoders

df, model, encoders = load_data_and_model()

# ==========================================
# 3. القائمة الجانبية (Sidebar Navigation) 🧭
# ==========================================
# شعار أمازون (رابط صورة)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=150)
st.sidebar.title("Supply Chain OPS")
st.sidebar.write("---")

page = st.sidebar.radio(
    "Go to:",
    ["📊 Dashboard (نظرة عامة)", "🤖 AI Predictor (المودل الذكي)", "📂 Data Catalog (سجل الطلبات)"]
)

st.sidebar.write("---")
st.sidebar.info("System Version: v2.0 Lite")

# ==========================================
# 4. الصفحة 1: لوحة المعلومات (Dashboard) 📊
# ==========================================
if page == "📊 Dashboard (نظرة عامة)":
    st.title("📊 Operations Dashboard")
    st.markdown("## Live Supply Chain Metrics")
    
    # حسابات سريعة (KPIs)
    if not df.empty:
        total_orders = len(df)
        late_orders = df[df['Delivery Status'] == 'Late Delivery'].shape[0]
        late_percentage = (late_orders / total_orders) * 100
        
        # عرض الأرقام الكبيرة في الأعلى
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Orders", f"{total_orders:,}", "📦")
        kpi2.metric("Late Risk Rate", f"{late_percentage:.1f}%", "-2.5%" if late_percentage > 50 else "1.2%")
        kpi3.metric("System Status", "Online", "🟢")
        
        st.write("---")
        
        # رسوم بيانية بسيطة (بدون plotly)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📦 Orders by Shipping Mode")
            # نستخدم Bar Chart العادي
            shipping_counts = df['Shipping Mode'].value_counts()
            st.bar_chart(shipping_counts)
            
        with col2:
            st.subheader("🚚 Late vs On-Time")
            status_counts = df['Delivery Status'].value_counts()
            st.bar_chart(status_counts, color="#ff4b4b") # لون أحمر

    else:
        st.warning("⚠️ Data file (csv) not found. Please ensure 'Saudi_Supply_Chain.csv' is in the folder.")

# ==========================================
# 5. الصفحة 2: المودل الذكي (AI Predictor) 🤖
# ==========================================
elif page == "🤖 AI Predictor (المودل الذكي)":
    st.title("🤖 AI Risk Predictor")
    st.markdown("### أدخل تفاصيل الطلب الجديد:")
    
    if model is not None:
        # تصميم الفورم
        with st.form("prediction_form"):
            c1, c2 = st.columns(2)
            
            with c1:
                shipping_mode = st.selectbox("Shipping Mode", encoders['shipping'].classes_)
                order_city = st.selectbox("Destination City", encoders['city'].classes_)
                order_quantity = st.number_input("Quantity", 1, 100, 1)
                
            with c2:
                category_name = st.selectbox("Product Category", encoders['category'].classes_)
                customer_segment = st.selectbox("Customer Type", encoders['segment'].classes_)
                
            submit_btn = st.form_submit_button("🔮 Predict Risk Now")
            
        if submit_btn:
            # تجهيز البيانات
            input_data = pd.DataFrame({
                'Shipping Mode': [shipping_mode],
                'Order City': [order_city],
                'Category Name': [category_name],
                'Customer Segment': [customer_segment],
                'Order Item Quantity': [order_quantity]
            })
            
            # التشفير
            input_data['Shipping Mode'] = encoders['shipping'].transform(input_data['Shipping Mode'])
            input_data['Order City'] = encoders['city'].transform(input_data['Order City'])
            input_data['Category Name'] = encoders['category'].transform(input_data['Category Name'])
            input_data['Customer Segment'] = encoders['segment'].transform(input_data['Customer Segment'])
            
            # التوقع
            pred = model.predict(input_data)[0]
            prob = model.predict_proba(input_data)[0][1]
            
            st.write("---")
            if pred == 1:
                st.error(f"🚨 **High Risk Detected!** (Confidence: {prob*100:.1f}%)")
                st.progress(prob)
            else:
                st.success(f"✅ **Safe Order** (Confidence: {(1-prob)*100:.1f}%)")
                st.progress(1-prob)

    else:
        st.error("Model files missing. Run model.py first.")

# ==========================================
# 6. الصفحة 3: تصفح البيانات (Data Catalog) 📂
# ==========================================
elif page == "📂 Data Catalog (سجل الطلبات)":
    st.title("📂 Data Catalog")
    st.markdown("استعرض البيانات الخام:")
    
    if not df.empty:
        filter_city = st.multiselect("Filter by City:", df['Order City'].unique())
        
        if filter_city:
            st.dataframe(df[df['Order City'].isin(filter_city)], use_container_width=True)
        else:
            st.dataframe(df.head(100), use_container_width=True)
            
        st.caption(f"Showing {len(df)} records.")
    else:
        st.warning("CSV file not found.")

