import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📦 E-Commerce Dashboard")

# pipreqs proyek_kelas\analisis_data\dataset\submission\notebook.ipynb


@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    
    df['order_purchase_timestamp'] = pd.to_datetime(
        df['order_purchase_timestamp'],
        errors='coerce'
    )
    
    df = df.dropna(subset=['order_purchase_timestamp'])
    
    return df

df = load_data()


st.subheader("📅 Filter Berdasarkan Tanggal")

min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

default_start_date = datetime.date(2018, 1, 1)

actual_default_start = max(min_date, default_start_date)

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Tanggal Mulai",
        value=actual_default_start,
        min_value=min_date,
        max_value=max_date
    )

with col2:
    end_date = st.date_input(
        "Tanggal Akhir",
        value=max_date,
        min_value=start_date,   
        max_value=max_date
    )
    
df_filtered = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
].copy()


col1, col2, col3 = st.columns(3)

total_orders = df_filtered['order_id'].nunique()
total_revenue = df_filtered['payment_value'].sum()
avg_delivery = df_filtered['delivery_time'].mean()

col1.metric("📦 Total Orders", total_orders)
col2.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col3.metric("🚚 Avg Delivery Time (days)", f"{avg_delivery:.2f}")


st.subheader("📈 Orders per Month")

df_filtered.loc[:, 'month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M').astype(str)

orders_per_month = df_filtered.groupby('month')['order_id'].nunique().reset_index()

fig_orders = px.line(
    orders_per_month,
    x='month',
    y='order_id',
    title='Orders per Month'
)

st.plotly_chart(fig_orders, width= "stretch")


st.subheader("💰 Revenue per Month")

revenue_per_month = df_filtered.groupby('month')['price'].sum().reset_index()

fig_revenue = px.bar(
    revenue_per_month,
    x='month',
    y='price',
    title='Revenue per Month'
)

st.plotly_chart(fig_revenue, width= "stretch")


st.subheader("💳 Payment Type Distribution")

payment_dist = df_filtered['payment_type'].value_counts().reset_index()
payment_dist.columns = ['payment_type', 'count']

fig_payment = px.pie(
    payment_dist,
    names='payment_type',
    values='count',
    title='Payment Type'
)

st.plotly_chart(fig_payment, width= "stretch")

st.subheader("🏆 Analisis Kategori Produk")

category_sales = (
    df_filtered.groupby('product_category_name')['order_id']
    .count()
    .sort_values(ascending=False)
)

top_5 = category_sales.head(5).reset_index()
bottom_5 = category_sales.tail(5).reset_index()

bottom_5 = bottom_5.sort_values(by='order_id', ascending=False)

# nilai negatif untuk chart terbalik
bottom_5['order_id_neg'] = -bottom_5['order_id']


col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔥 Top 5 Kategori Terlaris")
    
    fig_top = px.bar(
        top_5.sort_values(by='order_id'),
        x='order_id',
        y='product_category_name',
        orientation='h',
        color_discrete_sequence=['#4C78A8'],
        labels={"order_id": "orders", "product_category_name": "category"}

    )

    fig_top.update_layout(showlegend=False)

    fig_top.update_traces(
        text=top_5.sort_values(by='order_id')['order_id'],
        textposition='outside'
    )

    st.plotly_chart(fig_top, width= "stretch")

with col2:
    st.markdown("### ❄️ 5 Kategori Paling Sedikit Terjual")
    
    fig_bottom = px.bar(
        bottom_5,
        x='order_id_neg',
        y='product_category_name',
        orientation='h',
        color_discrete_sequence=['#9ecae1'],
        labels={"order_id_neg": "orders", "product_category_name": "category"}

    )

    fig_bottom.update_layout(showlegend=False)

    fig_bottom.update_traces(
        text=bottom_5['order_id'],
        textposition='outside'
    )

    fig_bottom.update_xaxes(
        tickvals=bottom_5['order_id_neg'],
        ticktext=bottom_5['order_id']
    )

    st.plotly_chart(fig_bottom, width= "stretch")

st.subheader("👤 Top Customers berdasarkan RFM")

rfm_df = df_filtered.groupby(by="customer_unique_id_int", as_index=False).agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
})

rfm_df.columns = ["customer_unique_id_int", "max_order_timestamp", "frequency", "monetary"]

recent_date = df_filtered["order_purchase_timestamp"].max()
rfm_df["recency"] = (recent_date - rfm_df["max_order_timestamp"]).dt.days

recency_top = rfm_df.sort_values(by="recency", ascending=True).head(5)
freq_top = rfm_df.sort_values(by="frequency", ascending=False).head(5)
monetary_top = rfm_df.sort_values(by="monetary", ascending=False).head(5)

col1, col2, col3 = st.columns(3)

# Recency
with col1:
    st.markdown("### ⏱️ Recency (Days)")
    fig_r = px.bar(
        recency_top,
        x="recency",
        y="customer_unique_id_int",
        orientation='h',
        color_discrete_sequence=['#72BCD4'],
        labels={"recency": "Days", "customer_unique_id_int": "ID Customer"}
    )

    fig_r.update_yaxes(type='category', categoryorder='total descending')
    st.plotly_chart(fig_r, width='stretch')

# Frequency
with col2:
    st.markdown("### 🔁 Frequency")
    fig_f = px.bar(
        freq_top,
        x="frequency",
        y="customer_unique_id_int",
        orientation='h',
        color_discrete_sequence=['#72BCD4'],
        labels={"frequency": "Orders", "customer_unique_id_int": "ID Customer"}
    )

    fig_f.update_yaxes(type='category', categoryorder='total ascending')
    st.plotly_chart(fig_f, width='stretch')

# Monetary
with col3:
    st.markdown("### 💰 Monetary")
    fig_m = px.bar(
        monetary_top,
        x="monetary",
        y="customer_unique_id_int",
        orientation='h',
        color_discrete_sequence=['#72BCD4'],
        labels={"monetary": "Revenue", "customer_unique_id_int": "ID Customer"}
    )

    fig_m.update_yaxes(type='category', categoryorder='total ascending')
    st.plotly_chart(fig_m, width='stretch')
