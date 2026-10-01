import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="FORESIGHT",
    page_icon="📦",
    layout="wide"
)

        
        

# Authentication credentials
auth_username = os.getenv("AUTH_USERNAME")
auth_password = os.getenv("AUTH_PASSWORD")

# Local development fallback
if not auth_username or not auth_password:
    try:
        auth_username = st.secrets["auth"]["username"]
        auth_password = st.secrets["auth"]["password"]
    except Exception:
        auth_username = ""
        auth_password = ""







# ---------------- LOGIN SYSTEM ----------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.markdown(
        """
<style>
.login-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.login-subtitle {
    text-align: center;
    font-size: 17px;
    color: #64748B;
    margin-bottom: 35px;
}

div[data-testid="stForm"] {
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 16px;
    padding: 30px;
    background-color: transparent;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

div[data-testid="stForm"] h3 {
    font-size: 24px;
}

div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    border-radius: 8px;
    font-weight: 600;
}
</style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">📦 FORESIGHT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Demand & Inventory Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        with st.form("login_form"):

            st.subheader("🔐 Welcome Back")
            st.caption("Log in to access your dashboard.")

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button("Login")

            if login_button:

                # if (
                #     username == st.secrets["auth"]["username"]
                #     and password == st.secrets["auth"]["password"]
                # ):
                if username == auth_username and password == auth_password:
                    st.session_state.authenticated = True
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

    st.stop()


# ---------------- LOGOUT BUTTON ----------------

if st.session_state.authenticated:

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
        
        
        
        
        
        
        
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-top: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.title("FORESIGHT")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Sales Analytics",
        "Demand Forecast",
        "Inventory Dashboard",
        "Risk Dashboard",
        "Product Details",
        "Executive Summary"
    ]
)

if page == "Home":
    st.markdown(
        '<div class="main-title">📦 FORESIGHT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Demand & Inventory Intelligence Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        **FORESIGHT** combines historical sales analysis, machine-learning
        demand forecasting, inventory monitoring, and risk detection
        into a single decision-support platform.
        """
    )

    st.divider()

    st.subheader("What FORESIGHT Does")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Analyze")
        st.write(
            "Explore historical sales, revenue, promotions, "
            "and product-level performance."
        )

    with col2:
        st.markdown("### 📈 Forecast")
        st.write(
            "Generate 7-day SKU-level demand forecasts "
            "using the trained machine-learning model."
        )

    with col3:
        st.markdown("### ⚠️ Act")
        st.write(
            "Identify inventory risks using demand forecasts, "
            "lead times, safety stock, and reorder points."
        )


    st.divider()

    # st.subheader("🤖 Demand Forecasting Model")

    # col1, col2, col3, col4 = st.columns(4)

    # col1.metric("Model", "HistGradientBoosting")
    # col2.metric("MAE", "2.85")
    # col3.metric("RMSE", "3.69")
    # col4.metric("WAPE", "23.49%")

    # st.caption(
    #     "Evaluated on a chronological holdout period from "
    #     "2025-08-09 to 2025-12-31. The model achieved a 24.70% "
    #     "WAPE improvement over the Seasonal Naive baseline."
    # )

    # st.divider()

    st.subheader("Platform Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **📊 Sales Analytics**
            
            Historical sales trends, revenue analysis,
            promotions, and top-performing SKUs.

            **📈 Demand Forecast**

            ML-powered 7-day demand forecasting at SKU level.

            **📦 Inventory Dashboard**

            Current stock, inventory value, stock coverage,
            and forecasted demand.
            """
        )

    with col2:
        st.markdown(
            """
            **⚠️ Risk Dashboard**

            Detect products requiring inventory attention.

            **🔎 Product Details**

            Investigate demand, forecast, and inventory
            position for individual SKUs.

            **🧭 Executive Summary**

            A consolidated view of business performance,
            forecast demand, inventory, and risk.
            """
        )

    st.divider()

    st.info(
        "Use the sidebar to explore the FORESIGHT platform."
    )

elif page == "Sales Analytics":

    st.title("📊 Sales Analytics")
    st.caption("Historical sales performance and business trends")

    sales = pd.read_csv("data/sales_clean.csv")
    sales["Date"] = pd.to_datetime(sales["Date"])
    
    date_range = st.date_input(
    "Select Date Range",
    value=(sales["Date"].min(), sales["Date"].max()),
    min_value=sales["Date"].min(),
    max_value=sales["Date"].max()
    )

    if len(date_range) == 2:
        start_date, end_date = date_range

        sales = sales[
            (sales["Date"] >= pd.Timestamp(start_date)) &
            (sales["Date"] <= pd.Timestamp(end_date))
        ]

    # KPI calculations
    total_units = sales["Units_Sold"].sum()
    total_revenue = sales["Revenue"].sum()
    avg_daily_units = sales.groupby("Date")["Units_Sold"].sum().mean()
    active_skus = sales["SKU"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Units Sold", f"{total_units:,.0f}")
    col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col3.metric("Avg Daily Units", f"{avg_daily_units:,.1f}")
    col4.metric("Active SKUs", active_skus)

    st.divider()

    # Daily sales trend
    st.subheader("Daily Sales Trend")

    daily_sales = (
        sales.groupby("Date")["Units_Sold"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        daily_sales.set_index("Date")["Units_Sold"]
    )

    st.divider()

    # Top products
    st.subheader("Top 10 Products by Units Sold")

    top_skus = (
        sales.groupby("SKU")["Units_Sold"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_skus)
    
    st.divider()
    st.subheader("Sales by Category")

    analysis_data = pd.read_csv("data/analysis_ready.csv")

    category_sales = (
        analysis_data.groupby("Category")["Units_Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

    st.divider()
    
    
    st.subheader("Revenue by Category")

    category_revenue = (
        analysis_data.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_revenue)

    st.divider()

    #Revenue by Promotion
    st.subheader("Revenue by Promotion")

    promotion_revenue = (
        sales.groupby("Promotion")["Revenue"]
        .sum()
        .rename(index={
            0: "No Promotion",
            1: "Promotion"
        })
    )

    st.bar_chart(promotion_revenue)
    
    
elif page == "Demand Forecast":

    st.title("📈 Demand Forecast")
    st.caption("7-day demand forecast generated by the trained ML model")

    forecast = pd.read_csv("outputs/forecasts.csv")
    forecast["Date"] = pd.to_datetime(forecast["Date"])

    forecast_dates = st.date_input(
        "Select Forecast Date Range",
        value=(forecast["Date"].min(), forecast["Date"].max()),
        min_value=forecast["Date"].min(),
        max_value=forecast["Date"].max()
    )

    if len(forecast_dates) == 2:
        start_date, end_date = forecast_dates

        forecast = forecast[
            (forecast["Date"] >= pd.Timestamp(start_date)) &
            (forecast["Date"] <= pd.Timestamp(end_date))
        ]
    
    total_forecast = forecast["Predicted_Demand"].sum()
    avg_daily_forecast = forecast.groupby("Date")["Predicted_Demand"].sum().mean()
    forecast_skus = forecast["SKU"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "7-Day Forecast Demand",
        f"{total_forecast:,.0f}"
    )

    col2.metric(
        "Avg Daily Forecast",
        f"{avg_daily_forecast:,.0f}"
    )

    col3.metric(
        "Forecasted SKUs",
        forecast_skus
    )

    st.divider()

    st.subheader("Daily Forecast")

    daily_forecast = (
        forecast.groupby("Date")["Predicted_Demand"]
        .sum()
    )

    st.line_chart(daily_forecast)

    st.divider()

    st.subheader("SKU Forecast")

    sku_forecast = (
        forecast.groupby("SKU")["Predicted_Demand"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(sku_forecast.head(10))    
    
    

elif page == "Inventory Dashboard":

    st.title("📦 Inventory Dashboard")
    st.caption("Inventory position based on the latest available inventory snapshot")

    inventory = pd.read_csv("outputs/inventory_analysis.csv")

    total_stock = inventory["Current_Stock"].sum()
    total_on_order = inventory["On_Order"].sum()
    inventory_value = inventory["Inventory_Value"].sum()
    avg_days_cover = inventory["Days_of_Cover"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Current Stock", f"{total_stock:,.0f}")
    col2.metric("On Order", f"{total_on_order:,.0f}")
    col3.metric("Inventory Value", f"₹{inventory_value:,.0f}")
    col4.metric("Avg Days of Cover", f"{avg_days_cover:.1f}")

    st.divider()

    st.subheader("Inventory Overview")

    inventory_display = inventory[
        [
            "SKU",
            "Current_Stock",
            "On_Order",
            "Forecast_7_Day_Demand",
            "Days_of_Cover",
            "Risk_Category"
        ]
    ].copy()

    st.dataframe(
        inventory_display,
        # use_container_width=True,
        width="stretch",
        hide_index=True
    )
elif page == "Risk Dashboard":

    st.title("⚠️ Risk Dashboard")
    st.caption("Inventory risk signals based on forecast demand and stock position")

    risk = pd.read_csv("outputs/inventory_analysis.csv")

    high_risk = (risk["Risk_Category"] == "High Risk").sum()
    medium_risk = (risk["Risk_Category"] == "Medium Risk").sum()
    healthy = (risk["Risk_Category"] == "Healthy").sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("🔴 High Risk", high_risk)
    col2.metric("🟠 Medium Risk", medium_risk)
    col3.metric("🟢 Healthy", healthy)

    st.divider()

    st.subheader("Risk Distribution")

    risk_counts = (
        risk["Risk_Category"]
        .value_counts()
    )

    st.bar_chart(risk_counts)

    st.divider()

    st.subheader("Products Requiring Attention")

    attention = risk[
        risk["Risk_Category"] != "Healthy"
    ][
        [
            "SKU",
            "Current_Stock",
            "On_Order",
            "Forecast_7_Day_Demand",
            "Days_of_Cover",
            "Lead_Time_Days",
            "Risk_Category"
        ]
    ].sort_values(
        "Risk_Category"
    )

    st.dataframe(
        attention,
        # use_container_width=True,
        width="stretch",
        hide_index=True
    )

elif page == "Product Details":

    st.title("🔎 Product Details")
    st.caption("Detailed demand and inventory view for an individual SKU")

    sales = pd.read_csv("data/sales_clean.csv")
    sales["Date"] = pd.to_datetime(sales["Date"])

    forecast = pd.read_csv("outputs/forecasts.csv")
    forecast["Date"] = pd.to_datetime(forecast["Date"])

    inventory = pd.read_csv("outputs/inventory_analysis.csv")

    sku_list = sorted(sales["SKU"].unique())

    selected_sku = st.selectbox(
        "Select SKU",
        sku_list
    )

    sku_sales = sales[sales["SKU"] == selected_sku]
    sku_forecast = forecast[forecast["SKU"] == selected_sku]
    sku_inventory = inventory[inventory["SKU"] == selected_sku].iloc[0]

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Historical Units Sold",
        f"{sku_sales['Units_Sold'].sum():,.0f}"
    )

    col2.metric(
        "7-Day Forecast",
        f"{sku_forecast['Predicted_Demand'].sum():,.1f}"
    )

    col3.metric(
        "Current Stock",
        f"{sku_inventory['Current_Stock']:,.0f}"
    )

    col4.metric(
        "Days of Cover",
        f"{sku_inventory['Days_of_Cover']:.1f}"
    )

    st.divider()

    st.subheader("Historical Demand")

    historical = (
        sku_sales.groupby("Date")["Units_Sold"]
        .sum()
    )

    st.line_chart(historical)

    st.divider()

    st.subheader("7-Day Forecast")

    forecast_chart = (
        sku_forecast.set_index("Date")["Predicted_Demand"]
    )

    st.line_chart(forecast_chart)

    st.divider()

    st.subheader("Inventory Status")

    inventory_details = pd.DataFrame({
        "Metric": [
            "Current Stock",
            "On Order",
            "Safety Stock",
            "Reorder Point",
            "Lead Time (Days)",
            "Risk Category"
        ],
        "Value": [
            sku_inventory["Current_Stock"],
            sku_inventory["On_Order"],
            sku_inventory["Safety_Stock"],
            sku_inventory["Reorder_Point"],
            sku_inventory["Lead_Time_Days"],
            sku_inventory["Risk_Category"]
        ]
    })
    
    inventory_details["Value"] = inventory_details["Value"].astype(str)

    st.dataframe(
        inventory_details,
        # use_container_width=True,
        width="stretch",
        hide_index=True
    )

elif page == "Executive Summary":

    st.title("🧭 Executive Summary")
    st.caption("High-level demand, sales, inventory, and risk overview")

    sales = pd.read_csv("data/sales_clean.csv")
    forecast = pd.read_csv("outputs/forecasts.csv")
    inventory = pd.read_csv("outputs/inventory_analysis.csv")

    # Sales metrics
    total_units = sales["Units_Sold"].sum()
    total_revenue = sales["Revenue"].sum()

    # Forecast metrics
    total_forecast = forecast["Predicted_Demand"].sum()

    # Inventory metrics
    total_stock = inventory["Current_Stock"].sum()
    inventory_value = inventory["Inventory_Value"].sum()

    # Risk metrics
    high_risk = (
        inventory["Risk_Category"] == "High Risk"
    ).sum()

    medium_risk = (
        inventory["Risk_Category"] == "Medium Risk"
    ).sum()

    healthy = (
        inventory["Risk_Category"] == "Healthy"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Historical Units Sold",
        f"{total_units:,.0f}"
    )

    col2.metric(
        "7-Day Forecast",
        f"{total_forecast:,.0f}"
    )

    col3.metric(
        "Current Stock",
        f"{total_stock:,.0f}"
    )

    col4.metric(
        "Inventory Value",
        f"₹{inventory_value:,.0f}"
    )

    st.divider()

    st.subheader("Inventory Risk Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("🔴 High Risk", high_risk)
    col2.metric("🟠 Medium Risk", medium_risk)
    col3.metric("🟢 Healthy", healthy)

    st.divider()

    st.subheader("7-Day Demand Forecast")

    daily_forecast = (
        forecast.groupby("Date")["Predicted_Demand"]
        .sum()
    )

    st.line_chart(daily_forecast)

    st.divider()

    st.subheader("High-Risk Products")

    high_risk_products = inventory[
        inventory["Risk_Category"] == "High Risk"
    ][
        [
            "SKU",
            "Current_Stock",
            "On_Order",
            "Forecast_7_Day_Demand",
            "Days_of_Cover",
            "Lead_Time_Days"
        ]
    ].sort_values("Days_of_Cover")

    st.dataframe(
        high_risk_products,
        # use_container_width=True,
        width="stretch",
        hide_index=True
    )