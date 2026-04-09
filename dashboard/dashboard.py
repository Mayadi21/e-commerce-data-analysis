import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📦 E-Commerce Business Dashboard")

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

st.divider()
m_col1, m_col2, m_col3 = st.columns(3)

total_orders = df_filtered['order_id'].nunique()
total_revenue = df_filtered['payment_value'].sum()
avg_delivery = df_filtered['delivery_time'].mean()

m_col1.metric("📦 Total Orders", f"{total_orders:,}")
m_col2.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
m_col3.metric("🚚 Avg Delivery Time", f"{avg_delivery:.2f} Days")


st.write("---")
st.subheader("📈 Monthly Trends")

df_filtered['month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M').astype(str)
orders_month = df_filtered.groupby('month')['order_id'].nunique()
rev_month = df_filtered.groupby('month')['price'].sum()

t_col1, t_col2 = st.columns(2)

with t_col1:
    st.write("**Trend Pesanan**")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(orders_month.index, orders_month.values, marker='o', color='#1f77b4', linewidth=2)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with t_col2:
    st.write("**Trend Pendapatan ($)**")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(rev_month.index, rev_month.values, marker='o', color='#1f77b4', linewidth=2)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.write("---")
st.subheader("🏆 Analisis Kategori Produk (Best vs Worst)")

category_sales = (
    df_filtered.groupby('product_category_name')['order_id']
    .count()
    .sort_values(ascending=False)
)
top_5 = category_sales.head(5).reset_index()

bottom_5 = category_sales.tail(5).sort_values(ascending=True).reset_index() 

cat_col1, cat_col2 = st.columns(2)

with cat_col1:
    st.markdown("<h3>🔥Top 5 Kategori Terlaris </h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_5, x='order_id', y='product_category_name', palette="Greens_r", ax=ax)
    
    ax.set_xlabel("Orders")
    ax.set_ylabel(None)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    st.pyplot(fig)

with cat_col2:
    st.markdown("<h3 style='text-align: left;'>⚠️ 5 Kategori Paling Sedikit Terjual</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(data=bottom_5, x='order_id', y='product_category_name', palette="Reds_r", ax=ax)
    
    ax.set_xlabel("Orders")
    ax.set_ylabel(None)
    
    ax.invert_xaxis()
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    st.pyplot(fig)


st.write("---")
st.subheader("👑 Top Customers Analytics (RFM)")

recent_date = df_filtered["order_purchase_timestamp"].max()
rfm_df = df_filtered.groupby(by="customer_unique_id_int", as_index=False).agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "max_timestamp", "frequency", "monetary"]
rfm_df["recency"] = (recent_date - rfm_df["max_timestamp"]).dt.days

r_col, f_col, m_col = st.columns(3)

def draw_rfm_chart(data, x_col, title, palette, column):
    with column:
        st.write(f"**{title}**")
        fig, ax = plt.subplots(figsize=(6, 4))
        data['label_id'] = data['customer_id'].astype(str).str[-8:]
        sns.barplot(data=data, x=x_col, y='label_id', palette=palette, ax=ax)
        ax.set_ylabel("Customer ID")
        st.pyplot(fig)

draw_rfm_chart(rfm_df.sort_values("recency", ascending=True).head(5), "recency", "Top 5 Recency (Days)", "Oranges", r_col)
draw_rfm_chart(rfm_df.sort_values("frequency", ascending=False).head(5), "frequency", "Top 5 Frequency", "Blues_r", f_col)
draw_rfm_chart(rfm_df.sort_values("monetary", ascending=False).head(5), "monetary", "Top 5 Monetary", "Greens_r", m_col)

