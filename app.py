import streamlit as st
import pandas as pd
import folium

# ==================== PAGE CONFIG & BRANDING ====================
st.set_page_config(page_title="Access Properties | QSR Strategy", layout="wide", page_icon="🏠")

st.markdown("""
<style>
    .main-header {font-size: 2.8rem; color: #004225; font-weight: bold;}
    .stButton>button {background-color: #004225; color: white; border-radius: 12px; padding: 12px 24px; font-weight: 600;}
    .section {padding: 20px; border-radius: 16px; background: #f8f9fa;}
</style>
""", unsafe_allow_html=True)

st.title("🏠 Access Properties")
st.markdown("**AI-Powered Real Estate Strategy for QSR & Retail Expansion**")

# Sidebar
st.sidebar.title("Access Properties")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Navigate", [
    "Home",
    "Property Search",
    "QSR Strategy Tool",
    "Market Reports"
])
starting_location = st.sidebar.text_input("Primary Market", "Costa Mesa, CA")

# ==================== HOME ====================
if page == "Home":
    st.header("Welcome to Access Properties")
    st.write("""
    Your partner for **data-driven commercial real estate decisions**, with specialized expertise in  
    **Quick Service Restaurant (QSR)** site selection and expansion strategy.  
    Built by Justin R. Crawford — former strategic real estate leader at Habit Burger & Grill and Panda Restaurant Group.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.success("**QSR Expansion Tools**")
        st.write("• Performance Analysis\n• 7-min Drive Time Trade Areas\n• Site Ranking & Scoring")
    with col2:
        st.success("**Access Properties Features**")
        st.write("• Property Intelligence\n• Demographic Insights\n• Listing Database\n• AI-Powered Reports")

# ==================== PROPERTY SEARCH ====================
elif page == "Property Search":
    st.header("General Property Search")
    st.write("Search commercial listings across Orange County and beyond.")
    search_term = st.text_input("Search by Address, Type, or Zip")
    if st.button("Search Listings"):
        st.info("Simulated results from LoopNet / Access Database:")
        listings = pd.DataFrame([
            {"Address": "3130 Harbor Blvd, Costa Mesa", "Type": "Retail / Drive-Thru", "Size": "8,107 SF", "Price": "Contact"},
            {"Address": "2500 Bristol St, Costa Mesa", "Type": "Restaurant Space", "Size": "4,500 SF", "Price": "$5.25/SF"},
        ])
        st.dataframe(listings, use_container_width=True)

# ==================== QSR STRATEGY TOOL ====================
elif page == "QSR Strategy Tool":
    st.header("🍔 QSR Real Estate Strategy Tool")
    
    # Upload Existing Locations
    st.subheader("1. Upload Your Existing Locations")
    uploaded = st.file_uploader("CSV (Location, Lat, Lon, Annual_Sales_M, ADT, Med_HH_Income, Pop_7min, Avg_Age, SqFt, DriveThru)", type="csv")
    
    if uploaded:
        df_existing = pd.read_csv(uploaded)
    else:
        df_existing = pd.DataFrame({
            'Location': ['CM1', 'IR2', 'HB3'],
            'Lat': [33.6411, 33.6695, 33.6603],
            'Lon': [-117.9187, -117.8265, -117.9984],
            'Annual_Sales_M': [2.8, 3.5, 2.1],
            'ADT': [45000, 52000, 38000],
            'Med_HH_Income': [95000, 120000, 85000],
            'Pop_7min': [12500, 18500, 9800],
            'Avg_Age': [38, 35, 42],
            'SqFt': [2800, 3200, 2500],
            'DriveThru': [True, True, False]
        })
    
    st.dataframe(df_existing, use_container_width=True)
    
    if len(df_existing) > 1:
        st.subheader("Performance Insights")
        corr = df_existing.select_dtypes(include='number').corr()['Annual_Sales_M'].sort_values(ascending=False)
        st.dataframe(corr.round(3), use_container_width=True)
    
    # Criteria
    st.subheader("2. Define Your Success Criteria")
    col1, col2 = st.columns(2)
    with col1:
        min_pop = st.number_input("Min Pop (7-min)", 8000, 30000, 11000)
        target_income = st.number_input("Target Median Income ($)", 60000, 200000, 100000)
        min_sqft = st.number_input("Min Sq Ft", 1500, 8000, 2200)
    with col2:
        target_adt = st.number_input("Target ADT", 20000, 100000, 42000)
        drive_thru = st.checkbox("Require Drive-Thru", True)
    
    # Analysis Button
    if st.button("🚀 Run Full Analysis & Find Sites"):
        # Hardcoded Costa Mesa coordinates (no external API needed)
        lat, lon = 33.6411, -117.9187
        
        # Create map
        m = folium.Map([lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup="Market Center", icon=folium.Icon(color="red")).add_to(m)
        
        for _, row in df_existing.iterrows():
            folium.Circle([row['Lat'], row['Lon']], 3500, color="green", fill=True, opacity=0.25, popup="7-min Trade Area").add_to(m)
        
        st.subheader("Trade Areas & Recommended Sites")
        st.components.v1.html(m._repr_html_(), height=550)
        
        # Ranked Sites
        sites = pd.DataFrame([
            {"Address": "3130 Harbor Blvd, Costa Mesa", "SqFt": 8107, "Est_Income": 98000, "Est_Pop": 14200, "ADT": 48000, "Type": "Drive-Thru Pad"},
            {"Address": "330 E 17th St, Costa Mesa", "SqFt": 6744, "Est_Income": 105000, "Est_Pop": 11800, "ADT": 42000, "Type": "2nd Gen QSR"},
            {"Address": "1800 Newport Blvd, Costa Mesa", "SqFt": 5200, "Est_Income": 125000, "Est_Pop": 16500, "ADT": 55000, "Type": "Corner Site"},
        ])
        
        def score(row):
            s = 0
            if row["Est_Pop"] >= min_pop: s += 3
            if row["Est_Income"] >= target_income * 0.9: s += 3
            if min_sqft <= row["SqFt"] <= 4500: s += 2
            if row["ADT"] >= target_adt * 0.85: s += 2
            return min(10, s + 2)
        
        sites["Score"] = sites.apply(score, axis=1)
        st.dataframe(sites.sort_values("Score", ascending=False), use_container_width=True)

# ==================== MARKET REPORTS ====================
elif page == "Market Reports":
    st.header("Market Reports & Downloads")
    st.write("Generate professional PDF reports for clients.")
    st.download_button("Download QSR Strategy Report", "Sample report content...", "qsr_strategy_report.pdf")

st.sidebar.success("Access Properties © 2026 • Justin R. Crawford")