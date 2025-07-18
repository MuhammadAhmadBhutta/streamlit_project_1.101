#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
df_reshaped = pd.read_csv('datasets/us-population-2010-2019-reshaped.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')
    
    year_list = list(df_reshaped.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# # Choropleth map
# def make_choropleth(input_df, input_id, input_column, input_color_theme):
#     choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
#                                color_continuous_scale=input_color_theme,
#                                range_color=(0, max(df_selected_year.population)),
#                                scope="usa",
#                                labels={'population':'Population'}
#                               )
#     choropleth.update_layout(
#         template='plotly_dark',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(l=0, r=0, t=0, b=0),
#         height=350
#     )
#     return choropleth

# 3D Globe Choropleth (bubble map)
import plotly.graph_objects as go

import numpy as np
# Remove territories and tiny regions

import numpy as np
import plotly.graph_objects as go

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    # State centroids (shortened example — add all states)
    state_centroids = {
    'AL': (32.806671, -86.791130),
    'AK': (61.370716, -152.404419),
    'AZ': (33.729759, -111.431221),
    'AR': (34.969704, -92.373123),
    'CA': (36.116203, -119.681564),
    'CO': (39.059811, -105.311104),
    'CT': (41.597782, -72.755371),
    'DE': (39.318523, -75.507141),
    'FL': (27.766279, -81.686783),
    'GA': (33.040619, -83.643074),
    'HI': (21.094318, -157.498337),
    'ID': (44.240459, -114.478828),
    'IL': (40.349457, -88.986137),
    'IN': (39.849426, -86.258278),
    'IA': (42.011539, -93.210526),
    'KS': (38.526600, -96.726486),
    'KY': (37.668140, -84.670067),
    'LA': (31.169546, -91.867805),
    'ME': (44.693947, -69.381927),
    'MD': (39.063946, -76.802101),
    'MA': (42.230171, -71.530106),
    'MI': (43.326618, -84.536095),
    'MN': (45.694454, -93.900192),
    'MS': (32.741646, -89.678696),
    'MO': (38.456085, -92.288368),
    'MT': (46.921925, -110.454353),
    'NE': (41.125370, -98.268082),
    'NV': (38.313515, -117.055374),
    'NH': (43.452492, -71.563896),
    'NJ': (40.298904, -74.521011),
    'NM': (34.840515, -106.248482),
    'NY': (42.165726, -74.948051),
    'NC': (35.630066, -79.806419),
    'ND': (47.528912, -99.784012),
    'OH': (40.388783, -82.764915),
    'OK': (35.565342, -96.928917),
    'OR': (44.572021, -122.070938),
    'PA': (40.590752, -77.209755),
    'RI': (41.680893, -71.511780),
    'SC': (33.856892, -80.945007),
    'SD': (44.299782, -99.438828),
    'TN': (35.747845, -86.692345),
    'TX': (31.054487, -97.563461),
    'UT': (40.150032, -111.862434),
    'VT': (44.045876, -72.710686),
    'VA': (37.769337, -78.169968),
    'WA': (47.400902, -121.490494),
    'WV': (38.491226, -80.954456),
    'WI': (44.268543, -89.616508),
    'WY': (42.755966, -107.302490)
}

    # ✅ Filter out Puerto Rico and DC if you don’t want them
    input_df = input_df[~input_df[input_id].isin(['PR', 'DC'])]

    # Add lat/lon columns using centroids
    input_df['lat'] = input_df[input_id].map(lambda x: state_centroids.get(x, (0, 0))[0])
    input_df['lon'] = input_df[input_id].map(lambda x: state_centroids.get(x, (0, 0))[1])

    # Bubble size: square root scale for better visuals
    max_pop = input_df[input_column].max()
    input_df['bubble_size'] = np.sqrt(input_df[input_column] / max_pop) * 50
    input_df['bubble_size'] = input_df['bubble_size'].clip(lower=5)  # minimum size so tiny states show

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            lon = input_df['lon'],
            lat = input_df['lat'],
            text = input_df['states'] + '<br>Population: ' + input_df[input_column].astype(str),
            marker = dict(
                size = input_df['bubble_size'],
                color = input_df[input_column],
                colorscale = input_color_theme,
                colorbar_title = "Population",
                line_color = 'white',
                line_width = 0.5,
                opacity = 0.85
            ),
            hoverinfo='text'
        )
    )

    fig.update_layout(
        title_text = 'US Population Globe View',
        geo = dict(
            projection_type = 'albers usa',  
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            showocean = True,
            oceancolor = 'rgb(0, 0, 80)',
            showlakes = True,
            lakecolor = 'rgb(0, 0, 80)',
            countrycolor = 'rgb(204, 204, 204)',
            coastlinecolor = 'rgb(204, 204, 204)',
            showcoastlines = True,
            center = dict(lat=35, lon=-97),  # Adjust lon for Alaska/Hawaii if needed
        ),
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        autosize = False,
        width = 600,
        height = 600,
        margin = dict(l=0, r=0, t=0, b=0),
        template = 'plotly_dark'
    )

    return fig


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)


#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Gains/Losses')

    df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

    if selected_year > 2010:
        first_state_name = df_population_difference_sorted.states.iloc[0]
        first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
        first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
    else:
        first_state_name = '-'
        first_state_population = '-'
        first_state_delta = ''
    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    if selected_year > 2010:
        last_state_name = df_population_difference_sorted.states.iloc[-1]
        last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
        last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
    else:
        last_state_name = '-'
        last_state_population = '-'
        last_state_delta = ''
    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    
    st.markdown('#### States Migration')

    if selected_year > 2010:
        # Filter states with population difference > 50000
        # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
        df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference > 50000]
        df_less_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference < -50000]
        
        # % of States with population difference > 50000
        states_migration_greater = round((len(df_greater_50000)/df_population_difference_sorted.states.nunique())*100)
        states_migration_less = round((len(df_less_50000)/df_population_difference_sorted.states.nunique())*100)
        donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
        donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')
    else:
        states_migration_greater = 0
        states_migration_less = 0
        donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
        donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')

    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Inbound')
        st.altair_chart(donut_chart_greater)
        st.write('Outbound')
        st.altair_chart(donut_chart_less)

# with col[1]:
#     st.markdown('#### Total Population')
    
#     choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
#     # choropleth = make_choropleth_3d(df_selected_year, 'states_code', 'population', selected_color_theme)

#     st.plotly_chart(choropleth, use_container_width=True)
    
#     heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
#     st.altair_chart(heatmap, use_container_width=True)
with col[1]:
    st.markdown('#### Total Population')

    choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)

    heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)

    st.markdown('#### 3D Scatter: Year vs Population vs Migration')
    
    # Add population_difference to df_reshaped if missing
    # Make sure you added the population_difference to df_reshaped first!
    df_reshaped = df_reshaped.sort_values(['states', 'year'])
    df_reshaped['population_difference'] = df_reshaped.groupby('states')['population'].diff().fillna(0)

    fig = px.scatter_3d(
        df_reshaped,
        x='year',
        y='population',
        z='population_difference',
        color='states',
        title='Animated 3D Scatter: Population and Migration Over Years'
)
    st.plotly_chart(fig, use_container_width=True)

    # st.plotly_chart(fig, use_container_width=True)

# import plotly.express as px

# fig = px.scatter_3d(
#     df_reshaped,
#     x='population',
#     y='population_difference',
#     z='year',
#     color='states',
#     animation_frame='year',
#     title='Animated 3D Scatter: Population and Migration Over Years'
# )


with col[2]:
    st.markdown('#### Top States')

    st.dataframe(df_selected_year_sorted,
                 column_order=("states", "population"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "states": st.column_config.TextColumn(
                        "States",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.population),
                     )}
                 )
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')
