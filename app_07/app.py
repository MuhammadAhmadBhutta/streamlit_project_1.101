# -----------------------------------------------
# 🟢 Full Sales Dashboard with Heatmap, Bubble & Geo Map
# -----------------------------------------------

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# -----------------------------------------------
# 🟢 Page config
# -----------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# -----------------------------------------------
# 🟢 Load data
# -----------------------------------------------
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="./datasets/supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# -----------------------------------------------
# 🟢 Sidebar: Filters + Color Theme
# -----------------------------------------------
st.sidebar.header("Please Filter Here:")

city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

color_theme_list = ['viridis', 'plasma', 'cividis', 'inferno', 'magma', 'blues', 'greens', 'reds', 'turbo', 'rainbow']
selected_color_theme = st.sidebar.selectbox("Select a Color Theme:", color_theme_list)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

# -----------------------------------------------
# 🟢 Main KPIs
# -----------------------------------------------
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# -----------------------------------------------
# 🟢 Sales by Product Line [Bar Chart]
# -----------------------------------------------
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total").reset_index()

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y="Product line",
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color="Total",
    color_continuous_scale=selected_color_theme,
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# -----------------------------------------------
# 🟢 Sales by Hour [Bar Chart]
# -----------------------------------------------
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum().reset_index()

fig_hourly_sales = px.bar(
    sales_by_hour,
    x="hour",
    y="Total",
    title="<b>Sales by Hour</b>",
    color="Total",
    color_continuous_scale=selected_color_theme,
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# -----------------------------------------------
# 🟢 Sunburst Chart
# -----------------------------------------------
fig_sunburst = px.sunburst(
    df_selection,
    path=['City', 'Customer_type', 'Gender'],
    values='Total',
    color='Total',
    color_continuous_scale=selected_color_theme,
    title='<b>Sales Distribution - Sunburst</b>',
    template='plotly_white'
)
fig_sunburst.update_layout(
    margin=dict(t=50, l=25, r=25, b=25)
)

# -----------------------------------------------
# 🟢 Treemap Chart
# -----------------------------------------------
fig_treemap = px.treemap(
    df_selection,
    path=['City', 'Product line'],
    values='Total',
    color='Total',
    color_continuous_scale=selected_color_theme,
    title='<b>Sales Distribution - Treemap</b>',
    template='plotly_white'
)
fig_treemap.update_layout(
    margin=dict(t=50, l=25, r=25, b=25)
)

st.markdown("""---""")
st.subheader("Sunburst & Treemap")

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_sunburst, use_container_width=True)
right_column.plotly_chart(fig_treemap, use_container_width=True)

# -----------------------------------------------
# 🟢 Heatmap (Correlation)
# -----------------------------------------------
corr_matrix = df_selection[["Unit price", "Quantity", "Total", "Rating"]].corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale=selected_color_theme,
    title="<b>Correlation Heatmap</b>",
    template='plotly_white'
)
fig_heatmap.update_layout(
    margin=dict(t=50, l=25, r=25, b=25)
)

st.markdown("""---""")
st.subheader("Correlation Heatmap")
st.plotly_chart(fig_heatmap, use_container_width=True)

# -----------------------------------------------
# 🟢 Bubble Chart (Scatter with Size)
# -----------------------------------------------
fig_bubble = px.scatter(
    df_selection,
    x="Unit price",
    y="Total",
    size="Quantity",
    color="City",
    color_discrete_sequence=px.colors.qualitative.Set1,
    title="<b>Bubble Chart - Unit Price vs Total Sales</b>",
    template='plotly_white'
)
fig_bubble.update_layout(
    margin=dict(t=50, l=25, r=25, b=25)
)

st.markdown("""---""")
st.subheader("Bubble Chart")
st.plotly_chart(fig_bubble, use_container_width=True)

# # -----------------------------------------------
# # 🟢 Geo Map (Scatter Geo)
# # NOTE: You need lat/lon data for this to be meaningful!
# # For demo, we'll map cities to dummy lat/lon:
# city_coords = {
#     'Yangon': {'lat': 16.8409, 'lon': 96.1735},
#     'Mandalay': {'lat': 21.9588, 'lon': 96.0891},
#     'Naypyitaw': {'lat': 19.7633, 'lon': 96.0785}
# }

# df_selection["lat"] = df_selection["City"].map(lambda x: city_coords[x]['lat'])
# df_selection["lon"] = df_selection["City"].map(lambda x: city_coords[x]['lon'])

# fig_geo = px.scatter_geo(
#     df_selection,
#     lat="lat",
#     lon="lon",
#     scope="asia",
#     color="City",
#     size="Total",
#     title="<b>Sales by City - Geo Map</b>",
#     template='plotly_white'
# )
# fig_geo.update_layout(
#     margin=dict(t=50, l=25, r=25, b=25)
# )

# st.markdown("""---""")
# st.subheader("Geo Map")
# st.plotly_chart(fig_geo, use_container_width=True)

# -----------------------------------------------
# 🟢 Hide Streamlit Default Style
# -----------------------------------------------
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
