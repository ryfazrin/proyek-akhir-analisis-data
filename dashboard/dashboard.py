import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_customer_city_df(df):
    customer_city_df = df.groupby("customer_city").customer_unique_id.nunique().sort_values(ascending=False).reset_index()
    
    return customer_city_df

def create_sum_order_by_customer_city_df(df):
    sum_order_by_customer_city_df = df.groupby("customer_city").order_id.nunique().sort_values(ascending=False).reset_index()
    
    return sum_order_by_customer_city_df

def create_sum_order_items_df(df):
    sum_order_items_df = all_df.groupby("product_category_name").order_id.nunique().sort_values(ascending=False).reset_index()
    
    return sum_order_items_df

# All DataFrame
all_df = pd.read_csv("dashboard/all_data.csv")


datetime_columns = ["order_purchase_timestamp", "order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu Delivered Carrier',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# All Visualization
daily_orders_df = create_daily_orders_df(main_df)
customer_city_df = create_customer_city_df(main_df)
sum_order_by_customer_city_df = create_sum_order_by_customer_city_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)

# daily_orders_df
st.header('Brazilian E-Commerce :sparkles:')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# customer_city_df
st.subheader("Most customers in a city")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="customer_unique_id", y="customer_city", data=customer_city_df.head(10), palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Most customers in a city", loc="center", fontsize=15)
ax.tick_params(axis ='y', labelsize=12)

st.pyplot(fig)

# sum_order_by_customer_city_df
st.subheader("Most Orders in a city")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_id", y="customer_city", data=sum_order_by_customer_city_df.head(10), palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Most customers in a city", loc="center", fontsize=15)
ax.tick_params(axis ='y', labelsize=12)

st.pyplot(fig)

# sum_order_items_df
st.subheader("Best and Worst Performing Category Product by Number of Sales")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_id", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Category Product", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)
 
sns.barplot(x="order_id", y="product_category_name", data=sum_order_items_df.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Category Product", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)