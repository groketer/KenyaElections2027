import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Kenya Elections Analysis 2002-2027",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
    }
    .prediction-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 20px 0;
    }
    .swing-county {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .stronghold {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# County name mapping (data name -> GeoJSON name)
COUNTY_NAME_MAP = {
    "Elgeyo Marakwet": "Keiyo-Marakwet",
    "Tharaka Nithi": "Tharaka"
}

# Reverse mapping (GeoJSON name -> data name)
GEOJSON_TO_DATA_MAP = {v: k for k, v in COUNTY_NAME_MAP.items()}

def get_geojson_name(data_name):
    """Convert data county name to GeoJSON county name"""
    return COUNTY_NAME_MAP.get(data_name, data_name)

def get_data_name(geojson_name):
    """Convert GeoJSON county name to data county name"""
    return GEOJSON_TO_DATA_MAP.get(geojson_name, geojson_name)

# Load data
@st.cache_data
def load_election_data():
    with open('election_data.json', 'r') as f:
        return json.load(f)

@st.cache_data
def load_county_data():
    with open('county_data.json', 'r') as f:
        return json.load(f)

@st.cache_data
def load_geojson():
    try:
        with open('kenya_counties.geojson', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading GeoJSON: {e}")
        return None

data = load_election_data()
county_data = load_county_data()
kenya_geojson = load_geojson()

# Sidebar navigation
st.sidebar.title("🗳️ Navigation")
page = st.sidebar.radio(
    "Select Analysis",
    ["Overview", "Interactive Map", "Historical Results", "Turnout Trends", "Regional Patterns", 
     "County Analysis", "County Predictions 2027", "2027 National Predictions"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard analyzes Kenya's presidential elections from 2002-2022 "
    "and provides county-level insights and predictions for the 2027 elections "
    "based on demographic trends and historical patterns."
)

# Main title
st.title("🇰🇪 Kenya Presidential Elections Analysis (2002-2027)")

# OVERVIEW PAGE
if page == "Overview":
    st.header("Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Elections Analyzed", "5", "2002-2022")
    with col2:
        st.metric("2022 Turnout", "64.77%", "-14.74%")
    with col3:
        st.metric("Counties Tracked", "47", "Complete coverage")
    with col4:
        st.metric("Projected 2027 Voters", "27.8M", "+5.7M")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Findings")
        st.markdown("""
        - **Highest Turnout**: 2013 with 85.91%
        - **Lowest Turnout**: 2017 re-run with 38.84%
        - **Closest Race**: 2022 (Ruto 50.49% vs Odinga 48.85%)
        - **Voter Growth**: 111% increase from 2002 to 2022
        - **2027 Game Changer**: 5.7M new youth voters (65% of electorate)
        - **All 47 Counties**: Complete nationwide coverage with predictions
        - **Key Battlegrounds**: Nairobi, Machakos, Bungoma, Kakamega, Narok, Kajiado
        """)
    
    with col2:
        st.subheader("Election Timeline")
        years = [2002, 2007, 2013, 2017, 2022]
        turnouts = [57.18, 69.23, 85.91, 79.51, 64.77]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years,
            y=turnouts,
            mode='lines+markers',
            name='Turnout %',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title="Voter Turnout Trend (2002-2022)",
            xaxis_title="Election Year",
            yaxis_title="Turnout (%)",
            height=300,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Regional overview map
    st.subheader("2027 Swing Potential by Region")
    regions_df = pd.DataFrame([
        {"Region": "Nairobi", "Swing Potential": "Very High", "Youth %": 72},
        {"Region": "Western", "Swing Potential": "Very High", "Youth %": 64},
        {"Region": "Eastern", "Swing Potential": "High", "Youth %": 67},
        {"Region": "Coast", "Swing Potential": "Medium", "Youth %": 69},
        {"Region": "Mt Kenya", "Swing Potential": "Medium", "Youth %": 68},
        {"Region": "Rift Valley", "Swing Potential": "Low", "Youth %": 65},
        {"Region": "Nyanza", "Swing Potential": "Low", "Youth %": 65}
    ])
    
    fig = px.bar(regions_df, x="Region", y="Youth %", color="Swing Potential",
                 color_discrete_map={"Very High": "#e74c3c", "High": "#f39c12", 
                                    "Medium": "#f1c40f", "Low": "#95a5a6"},
                 title="Youth Population and Swing Potential by Region")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 Navigate to 'Interactive Map' to explore county-by-county visualizations!")

# INTERACTIVE MAP PAGE
elif page == "Interactive Map":
    st.header("Interactive County Map of Kenya")
    
    if kenya_geojson is None:
        st.error("GeoJSON file not found. Map visualization is unavailable.")
        st.info("The map requires kenya_counties.geojson file to display county boundaries.")
    else:
        # Map visualization options
        st.subheader("Select Map View")
        map_view = st.radio(
            "Choose what to visualize:",
            ["2027 Swing Potential", "2022 Election Results (Ruto %)", "2022 Election Results (Odinga %)", 
             "2027 Projected Voters", "Youth Percentage", "2022 Turnout"],
            horizontal=True
        )
        
        # Prepare data for map - use GeoJSON county names
        counties = county_data['counties']
        map_data = []
        
        for county_name, county_info in counties.items():
            geojson_name = get_geojson_name(county_name)
            county_dict = {
                'County': geojson_name,  # Use GeoJSON name for mapping
                'Display_Name': county_name,  # Keep original for display
                'Swing_Potential': county_info['prediction_2027']['swing_potential'],
                'Ruto_2022': county_info['results_2022']['Ruto'],
                'Odinga_2022': county_info['results_2022']['Odinga'],
                'Projected_Voters_2027': county_info['prediction_2027']['projected_voters'],
                'Youth_Percentage': county_info['youth_percentage'],
                'Turnout_2022': county_info['results_2022']['turnout'],
                'Trend_2027': county_info['prediction_2027']['trend']
            }
            map_data.append(county_dict)
        
        map_df = pd.DataFrame(map_data)
        
        # Create choropleth map based on selection
        if map_view == "2027 Swing Potential":
            # Convert swing potential to numeric for coloring
            swing_map = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4, "Very High": 5}
            map_df['Swing_Numeric'] = map_df['Swing_Potential'].map(swing_map)
            
            fig = px.choropleth(
                map_df,
                geojson=kenya_geojson,
                locations='County',
                featureidkey="properties.COUNTY",
                color='Swing_Numeric',
                color_continuous_scale=["#95a5a6", "#f1c40f", "#f39c12", "#e74c3c", "#c0392b"],
                range_color=(1, 5),
                hover_name='Display_Name',
                hover_data={
                    'Swing_Potential': True,
                    'Swing_Numeric': False,
                    'County': False,
                    'Trend_2027': True,
                    'Youth_Percentage': True
                },
                labels={'Swing_Numeric': 'Swing Level'},
                title="Kenya Counties: 2027 Swing Potential"
            )
            
        elif map_view == "2022 Election Results (Ruto %)":
            fig = px.choropleth(
                map_df,
                geojson=kenya_geojson,
                locations='County',
                featureidkey="properties.COUNTY",
                color='Ruto_2022',
                color_continuous_scale="Reds",
                range_color=(0, 100),
                hover_name='Display_Name',
                hover_data={
                    'Ruto_2022': ':.1f',
                    'Odinga_2022': ':.1f',
                    'Turnout_2022': ':.1f',
                    'County': False
                },
                labels={'Ruto_2022': 'Ruto %'},
                title="2022 Election: William Ruto Vote Share by County"
            )
            
        elif map_view == "2022 Election Results (Odinga %)":
            fig = px.choropleth(
                map_df,
                geojson=kenya_geojson,
                locations='County',
                featureidkey="properties.COUNTY",
                color='Odinga_2022',
                color_continuous_scale="Greens",
                range_color=(0, 100),
                hover_name='Display_Name',
                hover_data={
                    'Odinga_2022': ':.1f',
                    'Ruto_2022': ':.1f',
                    'Turnout_2022': ':.1f',
                    'County': False
                },
                labels={'Odinga_2022': 'Odinga %'},
                title="2022 Election: Raila Odinga Vote Share by County"
            )
            
        elif map_view == "2027 Projected Voters":
            fig = px.choropleth(
                map_df,
                geojson=kenya_geojson,
                locations='County',
                featureidkey="properties.COUNTY",
                color='Projected_Voters_2027',
                color_continuous_scale="Blues",
                hover_name='Display_Name',
                hover_data={
                    'Projected_Voters_2027': ':,',
                    'Youth_Percentage': True,
                    'Swing_Potential': True,
                    'County': False
                },
                labels={'Projected_Voters_2027': 'Projected Voters'},
                title="2027 Projected Registered Voters by County"
            )
            
        elif map_view == "Youth Percentage":
            fig = px.choropleth(
                map_df,
                geojson=kenya_geojson,
                locations='County',
                featureidkey="properties.COUNTY",
                color='Youth_Percentage',
                color_continuous_scale="Purples",
                range_color=(60, 75),
                hover_name='Display_Name',
                hover_data={
                    'Youth_Percentage': True,
                    'Projected_Voters_2027': ':,',
                    'Swing_Potential': True,
                    'County': False
                },
                labels={'Youth_Percentage': 'Youth %'},
                title="Youth Population Percentage (Ages 20-34) by County"
            )
            
        else:  # 2022 Turnout
            fig = px.choropleth(
                map_df,
                geojson=kenya_geojson,
                locations='County',
                featureidkey="properties.COUNTY",
                color='Turnout_2022',
                color_continuous_scale="Viridis",
                range_color=(35, 85),
                hover_name='Display_Name',
                hover_data={
                    'Turnout_2022': ':.1f',
                    'Ruto_2022': ':.1f',
                    'Odinga_2022': ':.1f',
                    'County': False
                },
                labels={'Turnout_2022': 'Turnout %'},
                title="2022 Election: Voter Turnout by County"
            )
        
        # Update map layout
        fig.update_geos(
            fitbounds="locations",
            visible=False
        )
        
        fig.update_layout(
            margin={"r":0,"t":50,"l":0,"b":0},
            height=700
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Map insights
        st.markdown("---")
        st.subheader("Map Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if map_view == "2027 Swing Potential":
                very_high = len(map_df[map_df['Swing_Potential'] == 'Very High'])
                high = len(map_df[map_df['Swing_Potential'] == 'High'])
                st.metric("Very High Swing Counties", very_high)
                st.metric("High Swing Counties", high)
            elif "2022 Election Results" in map_view:
                if "Ruto" in map_view:
                    avg_ruto = map_df['Ruto_2022'].mean()
                    st.metric("Average Ruto %", f"{avg_ruto:.1f}%")
                    max_county = map_df.loc[map_df['Ruto_2022'].idxmax()]
                    st.metric("Highest", f"{max_county['Display_Name']}", f"{max_county['Ruto_2022']:.1f}%")
                else:
                    avg_odinga = map_df['Odinga_2022'].mean()
                    st.metric("Average Odinga %", f"{avg_odinga:.1f}%")
                    max_county = map_df.loc[map_df['Odinga_2022'].idxmax()]
                    st.metric("Highest", f"{max_county['Display_Name']}", f"{max_county['Odinga_2022']:.1f}%")
        
        with col2:
            if map_view == "2027 Projected Voters":
                total_projected = map_df['Projected_Voters_2027'].sum()
                st.metric("Total Projected Voters", f"{total_projected/1000000:.1f}M")
                largest = map_df.loc[map_df['Projected_Voters_2027'].idxmax()]
                st.metric("Largest County", largest['Display_Name'], f"{largest['Projected_Voters_2027']:,}")
            elif map_view == "Youth Percentage":
                avg_youth = map_df['Youth_Percentage'].mean()
                st.metric("Average Youth %", f"{avg_youth:.1f}%")
                highest_youth = map_df.loc[map_df['Youth_Percentage'].idxmax()]
                st.metric("Highest Youth %", highest_youth['Display_Name'], f"{highest_youth['Youth_Percentage']}%")
            elif map_view == "2022 Turnout":
                avg_turnout = map_df['Turnout_2022'].mean()
                st.metric("Average Turnout", f"{avg_turnout:.1f}%")
                highest_turnout = map_df.loc[map_df['Turnout_2022'].idxmax()]
                st.metric("Highest Turnout", highest_turnout['Display_Name'], f"{highest_turnout['Turnout_2022']:.1f}%")
        
        with col3:
            st.markdown("**Quick Facts:**")
            if map_view == "2027 Swing Potential":
                competitive = len(map_df[map_df['Swing_Potential'].isin(['Very High', 'High'])])
                st.markdown(f"- {competitive} competitive counties")
                st.markdown(f"- {47 - competitive} relatively stable counties")
            elif "2022 Election Results" in map_view:
                if "Ruto" in map_view:
                    ruto_majority = len(map_df[map_df['Ruto_2022'] > 50])
                    st.markdown(f"- Ruto won {ruto_majority} counties")
                else:
                    odinga_majority = len(map_df[map_df['Odinga_2022'] > 50])
                    st.markdown(f"- Odinga won {odinga_majority} counties")
        
        # Legend explanation
        st.markdown("---")
        st.subheader("Legend")
        if map_view == "2027 Swing Potential":
            st.markdown("""
            | Level | Description |
            |-------|-------------|
            | **Very High** (Dark Red) | Highly competitive, could go either way |
            | **High** (Orange) | Competitive with recent shifts |
            | **Medium** (Yellow) | Some competition, but leaning |
            | **Low** (Light Gray) | Relatively stable, minor shifts |
            | **Very Low** (Gray) | Stronghold, unlikely to change |
            """)

# HISTORICAL RESULTS PAGE
elif page == "Historical Results":
    st.header("Historical Election Results (2002-2022)")
    
    selected_year = st.selectbox(
        "Select Election Year",
        options=[2002, 2007, 2013, 2017, 2022]
    )
    
    election = data['elections'][str(selected_year)]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Registered Voters", f"{election['registered_voters']:,}")
    with col2:
        st.metric("Votes Cast", f"{election['votes_cast']:,}")
    with col3:
        st.metric("Turnout", f"{election['turnout']}%")
    
    st.markdown("---")
    
    st.subheader(f"{selected_year} Presidential Results")
    
    candidates_df = pd.DataFrame(election['candidates'])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = px.bar(
            candidates_df,
            x='name',
            y='percentage',
            color='party',
            text='percentage',
            title=f"{selected_year} Vote Share by Candidate"
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(xaxis_title="Candidate", yaxis_title="Vote Share (%)", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            candidates_df,
            values='votes',
            names='name',
            title=f"{selected_year} Vote Distribution"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Detailed Results")
    display_df = candidates_df[['name', 'party', 'votes', 'percentage']].copy()
    display_df['votes'] = display_df['votes'].apply(lambda x: f"{x:,}")
    display_df['percentage'] = display_df['percentage'].apply(lambda x: f"{x}%")
    display_df.columns = ['Candidate', 'Party', 'Votes', 'Percentage']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# TURNOUT TRENDS PAGE
elif page == "Turnout Trends":
    st.header("Voter Turnout Analysis")
    
    years = []
    turnouts = []
    registered = []
    votes_cast = []
    
    for year in [2002, 2007, 2013, 2017, 2022]:
        election = data['elections'][str(year)]
        years.append(year)
        turnouts.append(election['turnout'])
        registered.append(election['registered_voters'])
        votes_cast.append(election['votes_cast'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years,
            y=turnouts,
            mode='lines+markers',
            name='Turnout %',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=12),
            fill='tozeroy'
        ))
        fig.update_layout(
            title="Voter Turnout Trend",
            xaxis_title="Election Year",
            yaxis_title="Turnout (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=years,
            y=registered,
            name='Registered Voters',
            marker_color='#3498db',
            text=[f"{v/1000000:.1f}M" for v in registered],
            textposition='outside'
        ))
        fig.update_layout(
            title="Registered Voters Growth",
            xaxis_title="Election Year",
            yaxis_title="Registered Voters",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Turnout Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Turnout", f"{sum(turnouts)/len(turnouts):.2f}%")
    with col2:
        st.metric("Highest Turnout", f"{max(turnouts)}%", "2013")
    with col3:
        st.metric("Lowest Turnout", f"{min(turnouts)}%", "2002")
    with col4:
        st.metric("2022 vs 2017", f"{turnouts[-1] - turnouts[-2]:.2f}%", "Decrease")
    
    st.subheader("Detailed Turnout Data")
    turnout_df = pd.DataFrame({
        'Year': years,
        'Registered Voters': [f"{v:,}" for v in registered],
        'Votes Cast': [f"{v:,}" for v in votes_cast],
        'Turnout (%)': [f"{t:.2f}%" for t in turnouts]
    })
    st.dataframe(turnout_df, use_container_width=True, hide_index=True)

# REGIONAL PATTERNS PAGE
elif page == "Regional Patterns":
    st.header("Regional Voting Patterns")
    
    st.info("Detailed regional data is available for the 2002 election. This analysis shows voting patterns across Kenya's provinces.")
    
    election_2002 = data['elections']['2002']
    regional_data = election_2002['regional']
    
    regions = list(regional_data.keys())
    kibaki_votes = [regional_data[r]['Kibaki'] for r in regions]
    kenyatta_votes = [regional_data[r]['Kenyatta'] for r in regions]
    nyachae_votes = [regional_data[r]['Nyachae'] for r in regions]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Mwai Kibaki (NARC)', x=regions, y=kibaki_votes, marker_color='#2ecc71'))
    fig.add_trace(go.Bar(name='Uhuru Kenyatta (KANU)', x=regions, y=kenyatta_votes, marker_color='#e74c3c'))
    fig.add_trace(go.Bar(name='Simeon Nyachae (FORD)', x=regions, y=nyachae_votes, marker_color='#f39c12'))
    
    fig.update_layout(
        title="2002 Election Results by Province",
        xaxis_title="Province",
        yaxis_title="Vote Share (%)",
        barmode='stack',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Regional Strongholds (2002)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Kibaki's Strongest Regions:**")
        kibaki_regions = sorted([(r, regional_data[r]['Kibaki']) for r in regions], key=lambda x: x[1], reverse=True)[:4]
        for region, percentage in kibaki_regions:
            st.markdown(f"- **{region}**: {percentage}%")
    
    with col2:
        st.markdown("**Kenyatta's Strongest Regions:**")
        kenyatta_regions = sorted([(r, regional_data[r]['Kenyatta']) for r in regions], key=lambda x: x[1], reverse=True)[:4]
        for region, percentage in kenyatta_regions:
            st.markdown(f"- **{region}**: {percentage}%")
    
    st.subheader("Detailed Regional Results (2002)")
    regional_df = pd.DataFrame({
        'Province': regions,
        'Kibaki (%)': kibaki_votes,
        'Kenyatta (%)': kenyatta_votes,
        'Nyachae (%)': nyachae_votes
    })
    st.dataframe(regional_df, use_container_width=True, hide_index=True)

# COUNTY ANALYSIS PAGE
elif page == "County Analysis":
    st.header("County-Level Electoral Analysis")
    
    st.markdown("""
    This section provides detailed analysis of voting patterns in all 47 counties across Kenya, 
    comparing 2017 and 2022 election results.
    """)
    
    # County selector
    counties = sorted(list(county_data['counties'].keys()))
    selected_county = st.selectbox("Select County", counties)
    
    county_info = county_data['counties'][selected_county]
    
    # County metrics - with safe access
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Population", f"{county_info.get('population', 0):,}")
    with col2:
        st.metric("Registered Voters (2022)", f"{county_info.get('registered_voters_2022', 0):,}")
    with col3:
        st.metric("Youth Percentage", f"{county_info.get('youth_percentage', 0)}%")
    with col4:
        turnout_2022 = county_info.get('results_2022', {}).get('turnout', 0)
        turnout_2017 = county_info.get('results_2017', {}).get('turnout', 0)
        turnout_change = turnout_2022 - turnout_2017
        st.metric("Turnout Change", f"{turnout_change:+.1f}%", "2017 to 2022")
    
    st.markdown("---")
    
    # Comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2017 vs 2022 Results Comparison")
        
        results_2017 = county_info.get('results_2017', {})
        results_2022 = county_info.get('results_2022', {})
        
        comparison_df = pd.DataFrame({
            'Year': ['2017', '2017', '2022', '2022'],
            'Candidate': ['Kenyatta/Ruto', 'Odinga', 'Ruto', 'Odinga'],
            'Percentage': [
                results_2017.get('Kenyatta', 0),
                results_2017.get('Odinga', 0),
                results_2022.get('Ruto', 0),
                results_2022.get('Odinga', 0)
            ]
        })
        
        fig = px.bar(comparison_df, x='Year', y='Percentage', color='Candidate',
                     barmode='group', text='Percentage',
                     color_discrete_map={'Kenyatta/Ruto': '#3498db', 'Ruto': '#3498db', 
                                        'Odinga': '#e74c3c'})
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Turnout Trend")
        
        turnout_df = pd.DataFrame({
            'Year': ['2017', '2022'],
            'Turnout': [turnout_2017, turnout_2022]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=turnout_df['Year'],
            y=turnout_df['Turnout'],
            mode='lines+markers+text',
            text=turnout_df['Turnout'].apply(lambda x: f"{x:.1f}%"),
            textposition='top center',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=15)
        ))
        fig.update_layout(
            yaxis_title="Turnout (%)",
            height=400,
            yaxis_range=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis
    st.subheader(f"{selected_county} County Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**2017 Results:**")
        st.markdown(f"- Uhuru Kenyatta: **{results_2017.get('Kenyatta', 0)}%**")
        st.markdown(f"- Raila Odinga: **{results_2017.get('Odinga', 0)}%**")
        st.markdown(f"- Turnout: **{turnout_2017}%**")
    
    with col2:
        st.markdown("**2022 Results:**")
        st.markdown(f"- William Ruto: **{results_2022.get('Ruto', 0)}%**")
        st.markdown(f"- Raila Odinga: **{results_2022.get('Odinga', 0)}%**")
        st.markdown(f"- Turnout: **{turnout_2022}%**")
    
    # Vote shift analysis
    st.markdown("---")
    st.subheader("Vote Shift Analysis (2017 → 2022)")
    
    gov_shift = results_2022.get('Ruto', 0) - results_2017.get('Kenyatta', 0)
    opp_shift = results_2022.get('Odinga', 0) - results_2017.get('Odinga', 0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Government Coalition Shift", f"{gov_shift:+.1f}%", 
                 "Kenyatta 2017 → Ruto 2022")
    with col2:
        st.metric("Opposition Shift", f"{opp_shift:+.1f}%",
                 "Odinga 2017 → Odinga 2022")

# COUNTY PREDICTIONS 2027 PAGE
elif page == "County Predictions 2027":
    st.header("County-Level Predictions for 2027")
    
    st.markdown("""
    Based on demographic trends, historical voting patterns, and youth population growth, 
    here are the predictions for all 47 counties in the 2027 elections.
    """)
    
    # Overview metrics - with safe access
    total_new_youth = 0
    for c in county_data['counties']:
        pred = county_data['counties'][c].get('prediction_2027', {})
        total_new_youth += pred.get('new_youth_voters', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total New Youth Voters", f"{total_new_youth/1000000:.1f}M", "All 47 counties")
    with col2:
        swing_counties = sum([1 for c in county_data['counties'] 
                             if county_data['counties'][c].get('prediction_2027', {}).get('swing_potential', '') in ['High', 'Very High']])
        st.metric("Swing Counties", swing_counties, "High/Very High potential")
    with col3:
        avg_youth = sum([county_data['counties'][c].get('youth_percentage', 0) 
                        for c in county_data['counties']]) / len(county_data['counties'])
        st.metric("Avg Youth %", f"{avg_youth:.1f}%", "All counties")
    
    st.markdown("---")
    
    # Swing potential visualization
    st.subheader("2027 Swing Potential by County")
    
    county_pred_data = []
    for county_name, county_info in county_data['counties'].items():
        pred = county_info.get('prediction_2027', {})
        county_pred_data.append({
            'County': county_name,
            'Projected Voters': pred.get('projected_voters', 0),
            'New Youth Voters': pred.get('new_youth_voters', 0),
            'Likely Turnout': pred.get('likely_turnout', 0),
            'Trend': pred.get('trend', 'Unknown'),
            'Swing Potential': pred.get('swing_potential', 'Unknown')
        })
    
    pred_df = pd.DataFrame(county_pred_data)
    
    # Swing potential visualization
    fig = px.scatter(pred_df, 
                     x='New Youth Voters', 
                     y='Likely Turnout',
                     size='Projected Voters',
                     color='Swing Potential',
                     hover_data=['County', 'Trend'],
                     color_discrete_map={'Very High': '#e74c3c', 'High': '#f39c12', 
                                        'Medium': '#f1c40f', 'Low': '#95a5a6', 'Very Low': '#bdc3c7'},
                     title="County Swing Potential vs Youth Voters and Turnout")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # County-by-county predictions
    st.subheader("Detailed County Predictions")
    
    # Group by swing potential
    swing_groups = {
        'Very High': [],
        'High': [],
        'Medium': [],
        'Low': [],
        'Very Low': []
    }
    
    for county_name, county_info in county_data['counties'].items():
        swing_potential = county_info.get('prediction_2027', {}).get('swing_potential', 'Unknown')
        if swing_potential in swing_groups:
            swing_groups[swing_potential].append(county_name)
    
    # Display by swing potential
    for swing_level in ['Very High', 'High', 'Medium', 'Low', 'Very Low']:
        if swing_groups[swing_level]:
            with st.expander(f"🎯 {swing_level} Swing Potential Counties ({len(swing_groups[swing_level])})"):
                for county_name in swing_groups[swing_level]:
                    county_info = county_data['counties'][county_name]
                    pred = county_info.get('prediction_2027', {})
                    
                    st.markdown(f"### {county_name} County")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Projected Voters", f"{pred.get('projected_voters', 0):,}")
                    with col2:
                        st.metric("New Youth Voters", f"{pred.get('new_youth_voters', 0):,}")
                    with col3:
                        st.metric("Likely Turnout", f"{pred.get('likely_turnout', 0)}%")
                    with col4:
                        st.metric("Youth %", f"{county_info.get('youth_percentage', 0)}%")
                    
                    st.markdown(f"**Trend:** {pred.get('trend', 'Unknown')}")
                    st.markdown("---")
    
    # Key battleground counties
    st.markdown("---")
    st.subheader("🔥 Key Battleground Counties for 2027")
    
    battleground = [c for c in county_data['counties'] 
                   if county_data['counties'][c].get('prediction_2027', {}).get('swing_potential', '') in ['Very High', 'High']]
    
    st.markdown(f"""
    <div class="swing-county">
    <h4>Critical Counties to Watch</h4>
    <p>These {len(battleground)} counties have high swing potential and could determine the 2027 election outcome:</p>
    </div>
    """, unsafe_allow_html=True)
    
    for county_name in battleground:
        county_info = county_data['counties'][county_name]
        pred = county_info.get('prediction_2027', {})
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**{county_name}**")
            st.markdown(f"- Trend: {pred.get('trend', 'Unknown')}")
            st.markdown(f"- New youth voters: {pred.get('new_youth_voters', 0):,}")
        with col2:
            st.metric("Swing Potential", pred.get('swing_potential', 'Unknown'))
    
    # Regional trends summary
    st.markdown("---")
    st.subheader("Regional Trends for 2027")
    
    regional_trends = county_data.get('regional_trends', {})
    for region_name, region_info in regional_trends.items():
        with st.expander(f"📍 {region_name.replace('_', ' ')} Region"):
            st.markdown(f"**Counties:** {', '.join(region_info.get('counties', []))}")
            st.markdown(f"**Trend:** {region_info.get('trend', 'Unknown')}")
            st.markdown(f"**Key Factor:** {region_info.get('key_factor', 'Unknown')}")

# 2027 NATIONAL PREDICTIONS PAGE
elif page == "2027 National Predictions":
    st.header("2027 National Election Predictions & Analysis")
    
    predictions = data['predictions_2027']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Projected Voters", f"{predictions['total_projected_voters']/1000000:.1f}M")
    with col2:
        st.metric("New Voters", f"{predictions['new_voters']/1000000:.1f}M", "+25.8%")
    with col3:
        st.metric("Youth Voters", f"{predictions['youth_percentage']}%", "Ages 20-34")
    with col4:
        st.metric("Critical Year", "2026", "Coalition Formation")
    
    st.markdown("---")
    
    st.subheader("🎯 The Youth Factor: Game Changer for 2027")
    
    st.markdown("""
    <div class="prediction-box">
    <h3>Critical Insight</h3>
    <p>An estimated <strong>5.7 million new voters</strong> will be registered for 2027, with youth (ages 20-34) 
    comprising approximately <strong>65% of the voting bloc</strong>. This represents the largest demographic shift 
    in Kenya's electoral history and could fundamentally disrupt traditional voting patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=['Youth Voters (20-34)', 'Other Age Groups'],
            values=[predictions['youth_percentage'], 100 - predictions['youth_percentage']],
            hole=.4,
            marker_colors=['#e74c3c', '#95a5a6']
        )])
        fig.update_layout(
            title="Projected 2027 Voter Composition",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Turnout Scenarios")
        scenarios_df = pd.DataFrame(predictions['scenarios'])
        
        fig = px.bar(
            scenarios_df,
            x='name',
            y='turnout',
            text='turnout',
            color='name',
            title="Projected Turnout Scenarios"
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(xaxis_title="Scenario", yaxis_title="Turnout (%)", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Key Factors Influencing 2027 Elections")
    
    for i, factor in enumerate(predictions['factors'], 1):
        st.markdown(f"{i}. {factor}")
    
    st.markdown("---")
    
    st.subheader("Scenario Analysis")
    
    for scenario in predictions['scenarios']:
        with st.expander(f"📊 {scenario['name']} ({scenario['turnout']}% turnout)"):
            st.markdown(f"**Description:** {scenario['description']}")
            
            projected_votes = int(predictions['total_projected_voters'] * scenario['turnout'] / 100)
            st.markdown(f"**Projected Votes Cast:** {projected_votes:,}")
            
            if scenario['name'] == 'High Youth Turnout':
                st.success("This scenario would represent unprecedented youth political engagement in Kenya.")
            elif scenario['name'] == 'Moderate Turnout':
                st.info("This scenario assumes similar patterns to 2022, with modest youth mobilization.")
            else:
                st.warning("This scenario reflects historical youth voter apathy and could favor established candidates.")
    
    st.markdown("---")
    st.subheader("⚠️ Why 2026 is More Important Than 2027")
    
    st.markdown("""
    Political analysts emphasize that **2026 will be the decisive year** for the 2027 elections:
    
    - **Coalition Formation**: Political alliances must be solidified
    - **Voter Registration**: Mass registration drive begins September 2025
    - **Economic Reforms**: Policy decisions that will influence voter sentiment
    - **Youth Engagement**: Campaigns must start connecting with young voters early
    - **Opposition Unity**: Opposition parties must settle on unified candidates
    
    The massive youth voting bloc creates significant uncertainty, as they could potentially rally 
    behind any candidate who resonates with their values and communication style, making traditional 
    political calculations less reliable.
    """)
    
    st.markdown("---")
    st.subheader("Historical Context: How 2027 Compares")
    
    years = [2002, 2007, 2013, 2017, 2022, 2027]
    voters = [10.45, 14.30, 14.35, 19.61, 22.12, 27.82]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=voters,
        mode='lines+markers',
        name='Registered Voters (Millions)',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10)
    ))
    fig.add_annotation(
        x=2027,
        y=27.82,
        text="Projected<br>+5.7M new voters",
        showarrow=True,
        arrowhead=2,
        arrowcolor='#e74c3c',
        font=dict(color='#e74c3c', size=12)
    )
    fig.update_layout(
        title="Registered Voter Growth (2002-2027)",
        xaxis_title="Election Year",
        yaxis_title="Registered Voters (Millions)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>Data sources: Kenya Electoral Commission, Political Analysis Reports, County Demographics</p>
    <p>Dashboard created for educational and analytical purposes</p>
    <p><strong>Note:</strong> County-level data represents estimates based on available information and historical trends</p>
    </div>
""", unsafe_allow_html=True)