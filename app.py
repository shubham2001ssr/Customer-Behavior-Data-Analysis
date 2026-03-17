import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Advanced Customer Analytics", page_icon="📈", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .metric-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Add a little breathing room to the top metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📈 Advanced Customer Behavior & Sales Analytics")
st.markdown("An end-to-end interactive dashboard demonstrating key business metrics, demographic segmentation, and sales performance.")

# Load data
@st.cache_data(show_spinner=False)
def load_data():
    try:
        df = pd.read_csv('data/customer_shopping_data.csv')
        df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
        df['Month'] = df['Purchase Date'].dt.to_period('M').astype(str)
        df['Day of Week'] = df['Purchase Date'].dt.day_name()
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("Data file not found. Please ensure 'data/customer_shopping_data.csv' exists.")
else:
    # Sidebar for advanced filtering
    st.sidebar.header("🔍 Dynamic Filters")
    
    # Filter by Location
    locations = st.sidebar.multiselect("📍 Location:", options=sorted(df['Location'].unique()), default=sorted(df['Location'].unique()))
    
    # Filter by Season
    seasons = st.sidebar.multiselect("🌤️ Season:", options=sorted(df['Season'].unique()), default=sorted(df['Season'].unique()))
    
    # Filter by Category
    categories = st.sidebar.multiselect("🛍️ Category:", options=sorted(df['Category'].unique()), default=sorted(df['Category'].unique()))
    
    # Apply filters
    mask = (df['Location'].isin(locations)) & (df['Season'].isin(seasons)) & (df['Category'].isin(categories))
    filtered_df = df[mask]
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- TOP LEVEL METRICS ---
        st.markdown("### 📊 Executive Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(label="Total Revenue", value=f"${filtered_df['Purchase Amount (USD)'].sum():,.0f}")
        with col2:
            st.metric(label="Total Orders", value=f"{len(filtered_df):,}")
        with col3:
            st.metric(label="AOV (Avg Order Value)", value=f"${filtered_df['Purchase Amount (USD)'].mean():,.2f}")
        with col4:
            retention_pct = len(filtered_df[filtered_df['Subscription Status'] == 'Yes']) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
            st.metric(label="Cust. Retention (Subs)", value=f"{retention_pct:.1f}%")
        with col5:
            st.metric(label="Avg Review Rating", value=f"{filtered_df['Review Rating'].mean():.2f} / 5.0")
            
        st.markdown("---")
        
        # --- TABULAR LAYOUT FOR DEEP DIVES ---
        tab1, tab2, tab3 = st.tabs(["💰 Sales Performance", "👥 Customer Demographics", "📦 Product & Operations"])
        
        with tab1:
            st.markdown("#### Revenue Trends & Distribution")
            col_chart1, col_chart2 = st.columns([2, 1])
            
            with col_chart1:
                # Monthly Revenue Trend
                monthly_rev = filtered_df.groupby('Month')['Purchase Amount (USD)'].sum().reset_index().sort_values('Month')
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(x=monthly_rev['Month'], y=monthly_rev['Purchase Amount (USD)'], 
                                               mode='lines+markers', name='Revenue', line=dict(color='#1f77b4', width=3)))
                fig_trend.update_layout(title="Monthly Revenue Growth", template="plotly_white", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_trend, use_container_width=True)
                
            with col_chart2:
                # Revenue by Location context map / bar
                loc_rev = filtered_df.groupby('Location')['Purchase Amount (USD)'].sum().reset_index().sort_values('Purchase Amount (USD)', ascending=True)
                fig_loc = px.bar(loc_rev, x='Purchase Amount (USD)', y='Location', orientation='h',
                                 title="Revenue by Location", color='Purchase Amount (USD)', color_continuous_scale='Blues')
                fig_loc.update_layout(coloraxis_showscale=False, template="plotly_white", margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_loc, use_container_width=True)

        with tab2:
            st.markdown("#### Demographic Breakdown")
            col_chart3, col_chart4, col_chart5 = st.columns(3)
            
            with col_chart3:
                # Age distribution (Histogram)
                fig_age = px.histogram(filtered_df, x='Age', nbins=15, 
                                       title="Age Distribution", 
                                       color_discrete_sequence=['#ff7f0e'], template="plotly_white")
                fig_age.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_age, use_container_width=True)
                
            with col_chart4:
                # Spending by Gender
                rev_by_gender = filtered_df.groupby('Gender')['Purchase Amount (USD)'].sum().reset_index()
                fig_gender = px.pie(rev_by_gender, values='Purchase Amount (USD)', names='Gender', 
                                    title="Revenue by Gender", hole=0.5, template="plotly_white",
                                    color_discrete_sequence=['#2ca02c', '#d62728'])
                fig_gender.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_gender, use_container_width=True)
                
            with col_chart5:
                # Payment Method Preferences
                pay_pref = filtered_df['Payment Method'].value_counts().reset_index()
                pay_pref.columns = ['Payment Method', 'Count']
                fig_pay = px.bar(pay_pref, x='Payment Method', y='Count', 
                                 title="Payment Method Preferences",
                                 color_discrete_sequence=['#9467bd'], template="plotly_white")
                fig_pay.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_pay, use_container_width=True)

        with tab3:
            st.markdown("#### Product Categories & Operational Efficiency")
            col_chart6, col_chart7 = st.columns([1, 1])
            
            with col_chart6:
                # Boxplot of Purchase Amounts by Category to show distribution and outliers
                fig_box = px.box(filtered_df, x='Category', y='Purchase Amount (USD)', 
                                 title="Order Value Distribution by Category", 
                                 color='Category', template="plotly_white")
                fig_box.update_layout(margin=dict(l=0, r=0, t=40, b=0), showlegend=False)
                st.plotly_chart(fig_box, use_container_width=True)
                
            with col_chart7:
                # Relationship between Discount and Promo Code
                discount_impact = filtered_df.groupby('Discount Applied')['Purchase Amount (USD)'].mean().reset_index()
                fig_discount = px.bar(discount_impact, x='Discount Applied', y='Purchase Amount (USD)',
                                      title="Avg Order Value: Discount vs No Discount",
                                      color='Discount Applied', template="plotly_white",
                                      color_discrete_sequence=['#e377c2', '#7f7f7f'])
                fig_discount.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_discount, use_container_width=True)
        
        st.markdown("---")
        with st.expander("🔍 View Raw Analytics Data"):
            st.dataframe(filtered_df.sort_values(by='Purchase Date', ascending=False).head(500), use_container_width=True)
