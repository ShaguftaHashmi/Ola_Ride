import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚖",
    layout="wide"
)
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
load_css()

st.sidebar.image("C:\\Users\\shaguftha\\Documents\\Ola_ride\\ola_pic.png", width=180)
# ---------- Database Connection ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   # Replace with your MySQL password
    database="ola"
)
page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Home",
        "🔍 Filter Criteria",
        "📊 SQL Queries",
        "🙏 Thank You"
    ]
)
query = "SELECT * FROM ola_data"

df = pd.read_sql(query, conn)

conn.close()

st.title("🚖 OLA Ride Insights Dashboard")

st.markdown("### Business Intelligence Dashboard")

st.sidebar.header("🔍 Filters")

vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    options=sorted(df["Vehicle_Type"].dropna().unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["Payment_Method"].dropna().unique())
)


status = st.sidebar.multiselect(
    "Booking Status",
    options=sorted(df["Booking_Status"].dropna().unique())
)

filtered_df = df.copy()

if vehicle:
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"].isin(vehicle)
    ]

if payment:
    filtered_df = filtered_df[
        filtered_df["Payment_Method"].isin(payment)
    ]

if status:
    filtered_df = filtered_df[
        filtered_df["Booking_Status"].isin(status)
    ]
if page == "🏠 Home":    
    #KPIs    
    total_bookings = len(filtered_df)

    total_revenue = filtered_df["Booking_Value"].sum()

    successful = filtered_df[
        filtered_df["Booking_Status"] == "Success"
    ].shape[0]

    cancelled = filtered_df[
        filtered_df["Booking_Status"] != "Success"
    ].shape[0]

    avg_customer = round(
        filtered_df["Customer_Rating"].mean(), 2
    )

    #to display KPIs
    avg_driver = round(
        filtered_df["Driver_Ratings"].mean(), 2)    
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📌 Bookings", total_bookings)

    c2.metric("💰 Revenue", f"₹{total_revenue:,.0f}")

    c3.metric("✅ Successful", successful)

    c4.metric("❌ Cancelled", cancelled)

    c5.metric("⭐ Rating", avg_customer)

elif page == "🔍 Filter Criteria":
    st.header("📊 Visualizations")
    col1, col2 = st.columns(2)

    with col1:

        ride = filtered_df.groupby("Date").size().reset_index(name="Bookings")

        fig1 = px.line(
            ride,
            x="Date",
            y="Bookings",
            markers=True,
            title="📈 Ride Volume Over Time"
        )

        st.plotly_chart(fig1, use_container_width=True, key="ride_volume")

    with col2:

        status = filtered_df["Booking_Status"].value_counts().reset_index()

        status.columns = ["Status", "Count"]

        fig2 = px.pie(
            status,
            values="Count",
            names="Status",
            hole=0.55,
            title="Booking Status"
        )

        st.plotly_chart(fig2, use_container_width=True, key="booking_status")
        
    col3, col4 = st.columns(2)

    with col3:

        payment = filtered_df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()

        fig3 = px.bar(
            payment,
            x="Payment_Method",
            y="Booking_Value",
            text_auto=True,
            title="💰 Revenue by Payment Method"
        )

        st.plotly_chart(fig3, use_container_width=True, key="payment_method")
        

    #top vehicles types

    with col4:

        vehicle = filtered_df.groupby("Vehicle_Type")["Ride_Distance"].sum().reset_index()

        vehicle = vehicle.sort_values(
            by="Ride_Distance",
            ascending=False
        )

        fig4 = px.bar(
            vehicle,
            x="Vehicle_Type",
            y="Ride_Distance",
            color="Ride_Distance",
            title="🚗 Ride Distance by Vehicle Type"
        )

        st.plotly_chart(fig4, use_container_width=True, key="vehicle_type")
        
    #customer ratings
    col5, col6 = st.columns(2)

    with col5:

        fig5 = px.histogram(
            filtered_df,
            x="Customer_Rating",
            nbins=20,
            title="⭐ Customer Rating Distribution"
        )

        st.plotly_chart(fig5, use_container_width=True,key="customer_rating")

    with col6:

        fig6 = px.histogram(
            filtered_df,
            x="Driver_Ratings",
            nbins=20,
            title="👨 Driver Rating Distribution"
        )

        st.plotly_chart(fig6, use_container_width=True,key="driver_rating")
    #ride distance distribution  
            
    fig7 = px.histogram(
        filtered_df,
        x="Ride_Distance",
        nbins=30,
        title="📍 Ride Distance Distribution"
    )

    st.plotly_chart(fig7, use_container_width=True,key="ride_distance")

    #top 10 customers

    top = filtered_df.groupby("Customer_ID")["Booking_Value"].sum().reset_index()

    top = top.sort_values(
        by="Booking_Value",
        ascending=False
    ).head(10)

    fig8 = px.bar(
        top,
        x="Customer_ID",
        y="Booking_Value",
        color="Booking_Value",
        text_auto=True,
        title="🏆 Top 10 Customers"
    )

    st.plotly_chart(fig8, use_container_width=True, key="top_customers")

    #date side filter
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
    min_date = filtered_df["Date"].min()
    max_date = filtered_df["Date"].max()

    #date filter
    date_range = st.sidebar.date_input(
        "📅 Select Date Range",
        [min_date, max_date]
    )
    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered_df = filtered_df[
            (filtered_df["Date"] >= pd.to_datetime(start_date)) &
            (filtered_df["Date"] <= pd.to_datetime(end_date))
        ]
    #download filter data    
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="ola_filtered_data.csv",
        mime="text/csv"
    ) 
    #pickup location distribution   
    pickup = (
        filtered_df["Pickup_Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pickup.columns = ["Location", "Bookings"]

    fig9 = px.bar(
        pickup,
        x="Location",
        y="Bookings",
        color="Bookings",
        title="📍 Top 10 Pickup Locations"
    )

    st.plotly_chart(fig9, use_container_width=True, key="pickup_location")
    #Drop Location Analysis
    drop = (
        filtered_df["Drop_Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    drop.columns = ["Location", "Bookings"]

    fig10 = px.bar(
        drop,
        x="Location",
        y="Bookings",
        color="Bookings",
        title="📍 Top 10 Drop Locations"
    )

    st.plotly_chart(fig10, use_container_width=True, key="drop_location")
    #cancelled bookings analysis
    customer_cancel = (
        filtered_df["Canceled_Rides_by_Customer"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    customer_cancel.columns = ["Reason", "Count"]

    fig = px.pie(
        customer_cancel,
        names="Reason",
        values="Count",
        title="❌ Customer Cancellation Reasons"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="customer_cancel_chart"
    )

    #driver_cancel
    driver_cancel = (
        filtered_df["Canceled_Rides_by_Driver"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    driver_cancel.columns = ["Reason", "Count"]

    fig = px.pie(
        driver_cancel,
        names="Reason",
        values="Count",
        title="🚗 Driver Cancellation Reasons"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="driver_cancel_chart"
    )

    #pick hour analysis
    filtered_df["Time"] = pd.to_datetime(
        filtered_df["Time"],
        format="%H:%M:%S",
        errors="coerce"
    )
    filtered_df["Hour"] = filtered_df["Time"].dt.hour

    hour = (
        filtered_df.groupby("Hour")
        .size()
        .reset_index(name="Bookings")
    )

    fig13 = px.line(
        hour,
        x="Hour",
        y="Bookings",
        markers=True,
        title="⏰ Peak Booking Hours"
    )

    st.plotly_chart(fig13, use_container_width=True,key="peak_booking_hours")
elif page == "📊 SQL Queries":
    st.title("🗄 SQL Query Viewer")


    queries = {

        "1. Successful Bookings":
        """
        SELECT * FROM ola_data
        WHERE Booking_Status='Success';
        """,

        "2. Cancelled Bookings":
        """
        SELECT * FROM ola_data
        WHERE Booking_Status LIKE 'Canceled%';
        """,

        "3. Total Revenue":
        """
        SELECT SUM(Booking_Value) AS Total_Revenue
        FROM ola_data;
        """,

        "4. Revenue by Payment Method":
        """
        SELECT Payment_Method,
            SUM(Booking_Value) AS Revenue
        FROM ola_data
        GROUP BY Payment_Method;
        """,

        "5. Average Booking Value":
        """
        SELECT AVG(Booking_Value) AS Average_Booking_Value
        FROM ola_data;
        """,

        "6. Top 10 Customers":
        """
        SELECT Customer_ID,
            COUNT(*) AS Total_Rides
        FROM ola_data
        GROUP BY Customer_ID
        ORDER BY Total_Rides DESC
        LIMIT 10;
        """,

        "7. Vehicle Type Usage":
        """
        SELECT Vehicle_Type,
            COUNT(*) AS Total_Bookings
        FROM ola_data
        GROUP BY Vehicle_Type
        ORDER BY Total_Bookings DESC;
        """,

        "8. Average Ride Distance":
        """
        SELECT AVG(Ride_Distance) AS Avg_Ride_Distance
        FROM ola_data;
        """,

        "9. Highest Booking Value":
        """
        SELECT *
        FROM ola_data
        ORDER BY Booking_Value DESC
        LIMIT 10;
        """,

        "10. Driver Rating Analysis":
        """
        SELECT Vehicle_Type,
            ROUND(AVG(Driver_Ratings),2) AS Avg_Driver_Rating
        FROM ola_data
        GROUP BY Vehicle_Type;
        """,

        "11. Customer Rating Analysis":
        """
        SELECT Vehicle_Type,
            ROUND(AVG(Customer_Rating),2) AS Avg_Customer_Rating
        FROM ola_data
        GROUP BY Vehicle_Type;
        """,

        "12. Pickup Location Analysis":
        """
        SELECT Pickup_Location,
            COUNT(*) AS Total_Rides
        FROM ola_data
        GROUP BY Pickup_Location
        ORDER BY Total_Rides DESC
        LIMIT 10;
        """,

        "13. Drop Location Analysis":
        """
        SELECT Drop_Location,
            COUNT(*) AS Total_Rides
        FROM ola_data
        GROUP BY Drop_Location
        ORDER BY Total_Rides DESC
        LIMIT 10;
        """,

        "14. Customer Cancellation Reasons":
        """
        SELECT Canceled_Rides_by_Customer,
            COUNT(*) AS Total
        FROM ola_data
        WHERE Canceled_Rides_by_Customer IS NOT NULL
        GROUP BY Canceled_Rides_by_Customer;
        """,

        "15. Driver Cancellation Reasons":
        """
        SELECT Canceled_Rides_by_Driver,
            COUNT(*) AS Total
        FROM ola_data
        WHERE Canceled_Rides_by_Driver IS NOT NULL
        GROUP BY Canceled_Rides_by_Driver;
        """,

        "16. Incomplete Ride Reasons":
        """
        SELECT Incomplete_Rides_Reason,
            COUNT(*) AS Total
        FROM ola_data
        WHERE Incomplete_Rides_Reason IS NOT NULL
        GROUP BY Incomplete_Rides_Reason;
        """,

        "17. Average Vehicle TAT":
        """
        SELECT ROUND(AVG(V_TAT),2) AS Avg_Vehicle_TAT
        FROM ola_data;
        """,

        "18. Average Customer TAT":
        """
        SELECT ROUND(AVG(C_TAT),2) AS Avg_Customer_TAT
        FROM ola_data;
        """,

        "19. Booking Status Summary":
        """
        SELECT Booking_Status,
            COUNT(*) AS Total
        FROM ola_data
        GROUP BY Booking_Status;
        """,

        "20. Daily Revenue":
        """
        SELECT Date,
            SUM(Booking_Value) AS Revenue
        FROM ola_data
        GROUP BY Date
        ORDER BY Date;
        """
    }

    selected = st.selectbox(
        "Select SQL Query",
        list(queries.keys())
    )


    # Create a NEW connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ola"
    )

    df_sql = pd.read_sql(queries[selected], conn)

    conn.close()

    st.dataframe(df_sql)
elif page == "🙏 Thank You":

    st.balloons()
    st.snow()
    st.markdown(
        """
        <div style="
            text-align:center;
            background-color:#f8f9fa;
            padding:50px;
            border-radius:15px;
            box-shadow:2px 2px 10px lightgray;
        ">

        <h1 style="color:#00A651;">
        🚖 OLA Ride Insights Dashboard
        </h1>

        <h2>🙏 Thank You!</h2>

        <br>

        <h3>Thank you for exploring this dashboard.</h3>

        <p style="font-size:20px;">
        This project demonstrates the use of
        <b>Python</b>, <b>MySQL</b>, <b>Pandas</b>,
        <b>Plotly</b>, and <b>Streamlit</b>
        to analyze OLA ride booking data and generate
        meaningful business insights.
        </p>

        <br>

        <h3>✨ Features</h3>

        <p style="font-size:18px;">
        📊 Interactive Dashboard <br>
        📈 Business Analytics <br>
        🗄 SQL Query Explorer <br>
        🚖 Ride Performance Analysis <br>
        📍 Pickup & Drop Insights <br>
        ⭐ Ratings Analysis <br>
        💰 Revenue Insights
        </p>

        <br>

        <h2 style="color:#00A651;">
        Thank You for Visiting! ❤️
        </h2>

        <p style="font-size:18px;">
        Have a Wonderful Day! 😊
        </p>

        <hr>

        <p style="color:gray;">
        Developed by <b>Shagufta Hashmi</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("Project Completed Successfully 🎉")   