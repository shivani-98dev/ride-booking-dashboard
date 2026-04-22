import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Ride Booking Dashboard",
    layout="wide"
)

df = pd.read_csv('cleaned_data.csv')
df['date'] = pd.to_datetime(df['date'])


st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>
Ride Booking Analysis Dashboard
</h1>
""", unsafe_allow_html=True)

#st.write("This dashboard provides insights into ride booking data in the NCR region")

st.sidebar.markdown("## Filters")
st.sidebar.markdown("---")
vehicle = st.sidebar.selectbox(
    "Select Vehicle Type",
    df['vehicle_type'].unique()
)

start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

filtered_df = df[
    (df['vehicle_type'] == vehicle) &
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
]

st.markdown("## Key Metrics")

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="card">
<h4>Total Rides</h4>
<h2>{len(filtered_df)}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
<h4>Total Revenue</h4>
<h2>₹ {filtered_df['booking_value'].sum():,.0f}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
<h4>Avg Distance</h4>
<h2>{filtered_df['ride_distance'].mean():.2f} km</h2>
</div>
""", unsafe_allow_html=True)


st.markdown("## Ratings")

col4, col5 = st.columns(2)
col4.metric("Driver Rating", f"{filtered_df['driver_ratings'].mean():.2f}")
col5.metric("Customer Rating", f"{filtered_df['customer_rating'].mean():.2f}")

st.markdown("---")

col6, col7 = st.columns(2)
with col6:
    st.subheader("Booking Status Distribution")
    data = filtered_df['booking_status'].value_counts().reset_index()
    data.columns = ['Status', 'Count']

    fig1 = px.bar(data, x='Status', y='Count', color='Status')
    st.plotly_chart(fig1, use_container_width=True)

with col7:
    st.subheader("Payment Method Distribution")
    data = filtered_df['payment_method'].value_counts().reset_index()
    data.columns = ['Method', 'Count']
    fig2 = px.pie(data, names='Method', values='Count')
    st.plotly_chart(fig2, use_container_width=True)
col8, col9 = st.columns(2)

with col8:
    st.subheader("Top Pickup Locations")
    data = filtered_df['pickup_location'].value_counts().head(10).reset_index()
    data.columns = ['Location', 'Count']
    fig3 = px.bar(data, x='Location', y='Count', color='Location')
    st.plotly_chart(fig3, use_container_width=True)

with col9:
    st.subheader("Top Drop Locations")
    data = filtered_df['drop_location'].value_counts().head(10).reset_index()
    data.columns = ['Location', 'Count']

    fig4 = px.bar(data, x='Location', y='Count', color='Location')
    st.plotly_chart(fig4, use_container_width=True)

if 'month' in df.columns:
    st.subheader("Monthly Ride Trend")
    monthly = df.groupby('month').size().reset_index(name='rides')
    fig5 = px.line(monthly, x='month', y='rides', markers=True)
    st.plotly_chart(fig5, use_container_width=True)
col10, col11 = st.columns(2)

with col10:
    st.subheader("Customer Cancellation")
    data = filtered_df['reason_for_cancelling_by_customer'].value_counts().reset_index()
    data.columns = ['Reason', 'Count']
    fig6 = px.pie(data, names='Reason', values='Count')
    st.plotly_chart(fig6, use_container_width=True)

with col11:
    st.subheader("Driver Cancellation")
    data = filtered_df['driver_cancellation_reason'].value_counts().reset_index()
    data.columns = ['Reason', 'Count']

    fig7 = px.pie(data, names='Reason', values='Count')
    st.plotly_chart(fig7, use_container_width=True)

st.subheader(" Ride Distance Distribution")

fig8 = px.histogram(filtered_df, x='ride_distance', nbins=50)
st.plotly_chart(fig8, use_container_width=True)


