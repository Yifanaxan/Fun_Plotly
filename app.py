#flask --app app run --debug
#flask --app app run --debug --port 5024

#(cmd) .\venv\Scripts\activate.bat
#(bash) source ./venv/Scripts/activate

from flask import Flask,render_template
import plotly.express as px
import plotly
import json
import plotly.graph_objects as go
import random
import pandas as pd
from plotly.subplots import make_subplots

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import datasets

app = Flask(__name__)


#07a311#07a311#07a311#07a311#07a311
@app.route("/")
def earthquake():
    # Import data from USGS
    data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

    # Drop rows with missing or invalid values in the 'mag' column
    data = data.dropna(subset=['mag'])
    data = data[data.mag >= 0]
    
    # Create scatter map
    fig = px.scatter_geo(data, lat='latitude', lon='longitude', color='mag', hover_name='place', size='mag', size_max=10,
                        title='Earthquakes Around the World in the last 30 days', hover_data={'time': '|%B %d, %Y %H:%M:%S.%f'})

    # Convert the figure to JSON for rendering in the template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('earthquake.jinja.html', graphJSON=graphJSON)
#07a311#07a311#07a311#07a311#07a311


#f22222#f22222#f22222#f22222#f22222
@app.route("/heatmap")
def heatmap():
    # Load the CSV data
    df = pd.read_csv("2.5std_T+1_T+20_Hearmap.csv", encoding="utf-8")

    # Drop the date column from the dataframe
    df = df.drop('date', axis=1)

    # Create a heatmap
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(df.corr(), annot=True, cmap="coolwarm", annot_kws={"fontsize": 10}, fmt=".2f")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.title("TX vs Top 3 stocks Correlation Heatmap")
    plt.tight_layout()

    # Save the heatmap as an image
    heatmap_path = "static/heatmap.png"
    plt.savefig(heatmap_path)

    # Return the heatmap page with the image path
    return render_template("heatmap.jinja.html", heatmap_path=heatmap_path)
#f22222#f22222#f22222#f22222#f22222


#fc466b#fc466b#fc466b#fc466b#fc466b
@app.route("/heatmapinteract")
def heatmapInteract():
    # Load the Iris dataset
    iris = datasets.load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    # Create the heatmap figure
    fig = go.Figure(data=go.Heatmap(z=correlation_matrix.values,
                                   x=correlation_matrix.columns,
                                   y=correlation_matrix.index,
                                   colorscale='Viridis'))

    # Add annotations to the heatmap cells
    annotations = []
    for i, row in enumerate(correlation_matrix.values):
        for j, value in enumerate(row):
            annotations.append(dict(
                x=correlation_matrix.columns[j],
                y=correlation_matrix.index[i],
                text=f'{value:.2f}',
                showarrow=False,
                font=dict(color='red' if value > 0.5 else 'blue')
            ))
    fig.update_layout(annotations=annotations)

    # Customize the heatmap layout
    fig.update_layout(
        title="Correlation Heatmap - Iris Dataset",
        xaxis_title="Features",
        yaxis_title="Features",
        font=dict(
            family="Arial, sans-serif",
            size=16,
            color="#333"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor= '#ffffff',
        height=600  # Set the height of the figure (in pixels)
    )

    # Generate the HTML div for the heatmap
    plot_div = fig.to_html(full_html=False)

    return render_template('heatmapInteract.jinja.html', plot_div=plot_div)
#fc466b#fc466b#fc466b#fc466b#fc466b


#22c1c3#22c1c3#22c1c3#22c1c3#22c1c3
@app.route("/worldmap")
def worldmap():
    return render_template('worldmap.jinja.html')
#22c1c3#22c1c3#22c1c3#22c1c3#22c1c3


#953ffb#953ffb#953ffb#953ffb#953ffb
@app.route("/iris")
def iris():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                size='petal_length', hover_data=['petal_width'], height=600, width=1200)  
    fig.update_layout(
        title=dict(
            text="Iris Dataset",
            font=dict(size=20)  # Set the title font size to 20
        ),
        xaxis=dict(
            title="Sepal Width",
            tickfont=dict(size=16)  # Set the x-axis tick font size to 16
        ),
        yaxis=dict(
            title="Sepal Length",
            tickfont=dict(size=16)  # Set the y-axis tick font size to 16
        ),
        font=dict(size=20)  # Set the font size for other text elements to 14
    )
    graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('iris.jinja.html',graphJSON=graphJSON)
#953ffb#953ffb#953ffb#953ffb#953ffb


#f27000#f27000#f27000#f27000#f27000
@app.route("/capitalcities")
def capitalcities():

    capital_cities = {
'AF': {'city': 'Kabul', 'lat': 34.5553, 'lon': 69.2075},
'AL': {'city': 'Tirana', 'lat': 41.3275, 'lon': 19.8187},
'DZ': {'city': 'Algiers', 'lat': 36.7538, 'lon': 3.0588},
'AD': {'city': 'Andorra la Vella', 'lat': 42.5061, 'lon': 1.5218},
'AO': {'city': 'Luanda', 'lat': -8.8115, 'lon': 13.242},
'AG': {'city': "Saint John's", 'lat': 17.1171, 'lon': -61.845},
'AR': {'city': 'Buenos Aires', 'lat': -34.6037, 'lon': -58.3816},
'AM': {'city': 'Yerevan', 'lat': 40.1872, 'lon': 44.5152},
'AU': {'city': 'Canberra', 'lat': -35.3075, 'lon': 149.1244},
'AT': {'city': 'Vienna', 'lat': 48.2092, 'lon': 16.3728},
'AZ': {'city': 'Baku', 'lat': 40.3834, 'lon': 49.8932},
'BS': {'city': 'Nassau', 'lat': 25.0389, 'lon': -77.343},
'BH': {'city': 'Manama', 'lat': 26.2285, 'lon': 50.586},
'BD': {'city': 'Dhaka', 'lat': 23.8103, 'lon': 90.4125},
'BB': {'city': 'Bridgetown', 'lat': 13.0975, 'lon': -59.6165},
'BY': {'city': 'Minsk', 'lat': 53.9045, 'lon': 27.5615},
'BE': {'city': 'Brussels', 'lat': 50.8503, 'lon': 4.3517},
'BZ': {'city': 'Belmopan', 'lat': 17.2534, 'lon': -88.7713},
'BJ': {'city': 'Porto-Novo', 'lat': 6.4779, 'lon': 2.6323},
'BT': {'city': 'Thimphu', 'lat': 27.4728, 'lon': 89.639},
'BO': {'city': 'La Paz', 'lat': -16.5004, 'lon': -68.1504},
'BA': {'city': 'Sarajevo', 'lat': 43.8563, 'lon': 18.4131},
'BW': {'city': 'Gaborone', 'lat': -24.657, 'lon': 25.9089},
'BR': {'city': 'Brasília', 'lat': -15.7801, 'lon': -47.9292},
'BN': {'city': 'Bandar Seri Begawan', 'lat': 4.9031, 'lon': 114.939},
'BG': {'city': 'Sofia', 'lat': 42.6977, 'lon': 23.3219},
'BF': {'city': 'Ouagadougou', 'lat': 12.3714, 'lon': -1.5197},
'BI': {'city': 'Bujumbura', 'lat': -3.3818, 'lon': 29.3622},
'KH': {'city': 'Phnom Penh', 'lat': 11.5564, 'lon': 104.9282},
'CM': {'city': 'Yaoundé', 'lat': 3.848, 'lon': 11.5021},
'CA': {'city': 'Ottawa', 'lat': 45.4215, 'lon': -75.6982},
'CV': {'city': 'Praia', 'lat': 14.922, 'lon': -23.5142},
'CF': {'city': 'Bangui', 'lat': 4.3947, 'lon': 18.5582},
'TD': {'city': "N'Djamena", 'lat': 12.1347, 'lon': 15.0557},
'CL': {'city': 'Santiago', 'lat': -33.4489, 'lon': -70.6693},
'CN': {'city': 'Beijing', 'lat': 39.9042, 'lon': 116.4074},
'CO': {'city': 'Bogotá', 'lat': 4.6097, 'lon': -74.0817},
'KM': {'city': 'Moroni', 'lat': -11.7022, 'lon': 43.2551},
'CG': {'city': 'Brazzaville', 'lat': -4.2634, 'lon': 15.2429},
'CD': {'city': 'Kinshasa', 'lat': -4.4419, 'lon': 15.2663},
'CR': {'city': 'San José', 'lat': 9.9281, 'lon': -84.0907},
'HR': {'city': 'Zagreb', 'lat': 45.815, 'lon': 15.9819},
'CU': {'city': 'Havana', 'lat': 23.1136, 'lon': -82.3666},
'CY': {'city': 'Nicosia', 'lat': 35.1856, 'lon': 33.3823},
'CZ': {'city': 'Prague', 'lat': 50.0755, 'lon': 14.4378},
'DK': {'city': 'Copenhagen', 'lat': 55.6761, 'lon': 12.5683},
'DJ': {'city': 'Djibouti', 'lat': 11.589, 'lon': 43.1416},
'DM': {'city': 'Roseau', 'lat': 15.301, 'lon': -61.387},
'DO': {'city': 'Santo Domingo', 'lat': 18.4861, 'lon': -69.9312},
'TL': {'city': 'Dili', 'lat': -8.5569, 'lon': 125.5603},
'EC': {'city': 'Quito', 'lat': -0.2295, 'lon': -78.5249},
'EG': {'city': 'Cairo', 'lat': 30.0444, 'lon': 31.2357},
'SV': {'city': 'San Salvador', 'lat': 13.6929, 'lon': -89.2182},
'GQ': {'city': 'Malabo', 'lat': 3.7523, 'lon': 8.7372},
'ER': {'city': 'Asmara', 'lat': 15.3229, 'lon': 38.925},
'EE': {'city': 'Tallinn', 'lat': 59.437, 'lon': 24.7536},
'ET': {'city': 'Addis Ababa', 'lat': 9.145, 'lon': 38.7319},
'FJ': {'city': 'Suva', 'lat': -18.1248, 'lon': 178.4501},
'FI': {'city': 'Helsinki', 'lat': 60.1699, 'lon': 24.9384},
'FR': {'city': 'Paris', 'lat': 48.8566, 'lon': 2.3522},
'GA': {'city': 'Libreville', 'lat': 0.4162, 'lon': 9.4673},
'GM': {'city': 'Banjul', 'lat': 13.4399, 'lon': -16.6775},
'GE': {'city': 'Tbilisi', 'lat': 41.7151, 'lon': 44.8271},
'DE': {'city': 'Berlin', 'lat': 52.5200, 'lon': 13.4050},
'GH': {'city': 'Accra', 'lat': 5.6037, 'lon': -0.187},
'GR': {'city': 'Athens', 'lat': 37.9838, 'lon': 23.7275},
'GD': {'city': "Saint George's", 'lat': 12.0567, 'lon': -61.7486},
'GT': {'city': 'Guatemala City', 'lat': 14.6349, 'lon': -90.5069},
'GN': {'city': 'Conakry', 'lat': 9.6412, 'lon': -13.5784},
'GW': {'city': 'Bissau', 'lat': 11.863, 'lon': -15.5984},
'GY': {'city': 'Georgetown', 'lat': 6.8013, 'lon': -58.1551},
'HT': {'city': 'Port-au-Prince', 'lat': 18.5944, 'lon': -72.3074},
'HN': {'city': 'Tegucigalpa', 'lat': 14.0723, 'lon': -87.1921},
'HU': {'city': 'Budapest', 'lat': 47.4979, 'lon': 19.0402},
'IS': {'city': 'Reykjavik', 'lat': 64.1466, 'lon': -21.9426},
'IN': {'city': 'New Delhi', 'lat': 28.6139, 'lon': 77.2090},
'ID': {'city': 'Jakarta', 'lat': -6.2088, 'lon': 106.8456},
'IR': {'city': 'Tehran', 'lat': 35.6892, 'lon': 51.3890},
'IQ': {'city': 'Baghdad', 'lat': 33.3152, 'lon': 44.3661},
'IE': {'city': 'Dublin', 'lat': 53.3498, 'lon': -6.2603},
'IL': {'city': 'Jerusalem', 'lat': 31.7683, 'lon': 35.2137},
'IT': {'city': 'Rome', 'lat': 41.9028, 'lon': 12.4964},
'JM': {'city': 'Kingston', 'lat': 17.971, 'lon': -76.792},
'JP': {'city': 'Tokyo', 'lat': 35.6895, 'lon': 139.6917},
'JO': {'city': 'Amman', 'lat': 31.9566, 'lon': 35.9450},
'KZ': {'city': 'Nur-Sultan', 'lat': 51.1694, 'lon': 71.4491},
'KE': {'city': 'Nairobi', 'lat': -1.2864, 'lon': 36.8172},
'KI': {'city': 'South Tarawa', 'lat': -0.8696, 'lon': 169.5369},
'KP': {'city': 'Pyongyang', 'lat': 39.0392, 'lon': 125.7625},
'KR': {'city': 'Seoul', 'lat': 37.5665, 'lon': 126.9780},
'KW': {'city': 'Kuwait City', 'lat': 29.3759, 'lon': 47.9774},
'KG': {'city': 'Bishkek', 'lat': 42.8746, 'lon': 74.5698},
'LA': {'city': 'Vientiane', 'lat': 17.9689, 'lon': 102.6137},
'LV': {'city': 'Riga', 'lat': 56.9496, 'lon': 24.1052},
'LB': {'city': 'Beirut', 'lat': 33.8938, 'lon': 35.5018},
'LS': {'city': 'Maseru', 'lat': -29.3105, 'lon': 27.4842},
'LR': {'city': 'Monrovia', 'lat': 6.2907, 'lon': -10.7605},
'LY': {'city': 'Tripoli', 'lat': 32.8872, 'lon': 13.1913},
'LI': {'city': 'Vaduz', 'lat': 47.1411, 'lon': 9.5215},
'LT': {'city': 'Vilnius', 'lat': 54.6896, 'lon': 25.2799},
'LU': {'city': 'Luxembourg', 'lat': 49.6116, 'lon': 6.1319},
'MG': {'city': 'Antananarivo', 'lat': -18.8792, 'lon': 47.5079},
'MW': {'city': 'Lilongwe', 'lat': -13.9626, 'lon': 33.7741},
'MY': {'city': 'Kuala Lumpur', 'lat': 3.1390, 'lon': 101.6869},
'MV': {'city': 'Malé', 'lat': 4.1755, 'lon': 73.5093},
'ML': {'city': 'Bamako', 'lat': 12.6392, 'lon': -8.0029},
'MT': {'city': 'Valletta', 'lat': 35.8989, 'lon': 14.5146},
'MH': {'city': 'Majuro', 'lat': 7.1164, 'lon': 171.1859},
'MR': {'city': 'Nouakchott', 'lat': 18.0791, 'lon': -15.9785},
'MU': {'city': 'Port Louis', 'lat': -20.1609, 'lon': 57.5012},
'MX': {'city': 'Mexico City', 'lat': 19.4326, 'lon': -99.1332},
'FM': {'city': 'Palikir', 'lat': 6.9248, 'lon': 158.1610},
'MD': {'city': 'Chisinau', 'lat': 47.0104, 'lon': 28.8638},
'MC': {'city': 'Monaco', 'lat': 43.7384, 'lon': 7.4246},
'MN': {'city': 'Ulaanbaatar', 'lat': 47.8864, 'lon': 106.9057},
'ME': {'city': 'Podgorica', 'lat': 42.4304, 'lon': 19.2594},
'MA': {'city': 'Rabat', 'lat': 33.9716, 'lon': -6.8498},
'MZ': {'city': 'Maputo', 'lat': -25.9655, 'lon': 32.5832},
'MM': {'city': 'Naypyidaw', 'lat': 19.7633, 'lon': 96.0785},
'NA': {'city': 'Windhoek', 'lat': -22.5597, 'lon': 17.0832},
'NR': {'city': 'Yaren', 'lat': -0.5477, 'lon': 166.9209},
'NP': {'city': 'Kathmandu', 'lat': 27.7172, 'lon': 85.3240},
'NL': {'city': 'Amsterdam', 'lat': 52.3667, 'lon': 4.8945},
'NZ': {'city': 'Wellington', 'lat': -41.2865, 'lon': 174.7762},
'NI': {'city': 'Managua', 'lat': 12.1149, 'lon': -86.2362},
'NE': {'city': 'Niamey', 'lat': 13.5127, 'lon': 2.1128},
'NG': {'city': 'Abuja', 'lat': 9.0579, 'lon': 7.4951},
'MK': {'city': 'Skopje', 'lat': 41.996, 'lon': 21.4317},
'NO': {'city': 'Oslo', 'lat': 59.9139, 'lon': 10.7522},
'OM': {'city': 'Muscat', 'lat': 23.6105, 'lon': 58.5405},
'PK': {'city': 'Islamabad', 'lat': 33.6844, 'lon': 73.0479},
'PW': {'city': 'Ngerulmud', 'lat': 7.5000, 'lon': 134.6242},
'PS': {'city': 'Ramallah', 'lat': 31.8980, 'lon': 35.2041},
'PA': {'city': 'Panama City', 'lat': 8.9833, 'lon': -79.5167},
'PG': {'city': 'Port Moresby', 'lat': -9.4438, 'lon': 147.1803},
'PY': {'city': 'Asunción', 'lat': -25.2637, 'lon': -57.5759},
'PE': {'city': 'Lima', 'lat': -12.0464, 'lon': -77.0428},
'PH': {'city': 'Manila', 'lat': 14.5995, 'lon': 120.9842},
'PL': {'city': 'Warsaw', 'lat': 52.2297, 'lon': 21.0122},
'PT': {'city': 'Lisbon', 'lat': 38.7223, 'lon': -9.1393},
'QA': {'city': 'Doha', 'lat': 25.2867, 'lon': 51.5333},
'RO': {'city': 'Bucharest', 'lat': 44.4268, 'lon': 26.1025},
'RU': {'city': 'Moscow', 'lat': 55.7558, 'lon': 37.6176},
'RW': {'city': 'Kigali', 'lat': -1.9441, 'lon': 30.0619},
'KN': {'city': 'Basseterre', 'lat': 17.3026, 'lon': -62.7177},
'LC': {'city': 'Castries', 'lat': 14.0101, 'lon': -60.9875},
'VC': {'city': 'Kingstown', 'lat': 13.1552, 'lon': -61.227},
'WS': {'city': 'Apia', 'lat': -13.8339, 'lon': -171.7699},
'SM': {'city': 'San Marino', 'lat': 43.9424, 'lon': 12.4578},
'ST': {'city': 'São Tomé', 'lat': 0.3358, 'lon': 6.7273},
'SA': {'city': 'Riyadh', 'lat': 24.7136, 'lon': 46.6753},
'SN': {'city': 'Dakar', 'lat': 14.7167, 'lon': -17.4677},
'RS': {'city': 'Belgrade', 'lat': 44.7866, 'lon': 20.4489},
'SC': {'city': 'Victoria', 'lat': -4.6191, 'lon': 55.4513},
'SL': {'city': 'Freetown', 'lat': 8.4653, 'lon': -13.2317},
'SG': {'city': 'Singapore', 'lat': 1.3521, 'lon': 103.8198},
'SK': {'city': 'Bratislava', 'lat': 48.1486, 'lon': 17.1077},
'SI': {'city': 'Ljubljana', 'lat': 46.0569, 'lon': 14.5058},
'SB': {'city': 'Honiara', 'lat': -9.4380, 'lon': 159.9498},
'SO': {'city': 'Mogadishu', 'lat': 2.0469, 'lon': 45.3182},
'ZA': {'city': 'Pretoria', 'lat': -25.7461, 'lon': 28.1881},
'SS': {'city': 'Juba', 'lat': 4.8594, 'lon': 31.5713},
'ES': {'city': 'Madrid', 'lat': 40.4168, 'lon': -3.7038},
'LK': {'city': 'Colombo', 'lat': 6.9271, 'lon': 79.8612},
'SD': {'city': 'Khartoum', 'lat': 15.5007, 'lon': 32.5599},
'SR': {'city': 'Paramaribo', 'lat': 5.8520, 'lon': -55.2038},
'SZ': {'city': 'Mbabane', 'lat': -26.3186, 'lon': 31.1410},
'SE': {'city': 'Stockholm', 'lat': 59.3293, 'lon': 18.0686},
'CH': {'city': 'Bern', 'lat': 46.9480, 'lon': 7.4474},
'SY': {'city': 'Damascus', 'lat': 33.5138, 'lon': 36.2765},
'TW': {'city': 'Taipei', 'lat': 25.0330, 'lon': 121.5654},
'TJ': {'city': 'Dushanbe', 'lat': 38.5737, 'lon': 68.7738},
'TZ': {'city': 'Dodoma', 'lat': -6.1730, 'lon': 35.7410},
'TH': {'city': 'Bangkok', 'lat': 13.7563, 'lon': 100.5018},
'TL': {'city': 'Dili', 'lat': -8.5569, 'lon': 125.5603},
'TG': {'city': 'Lomé', 'lat': 6.1750, 'lon': 1.2312},
'TO': {'city': 'Nukuʻalofa', 'lat': -21.1393, 'lon': -175.2049},
'TT': {'city': 'Port of Spain', 'lat': 10.6596, 'lon': -61.4789},
'TN': {'city': 'Tunis', 'lat': 36.8065, 'lon': 10.1815},
'TR': {'city': 'Ankara', 'lat': 39.9334, 'lon': 32.8597},
'TM': {'city': 'Ashgabat', 'lat': 37.9601, 'lon': 58.3254},
'TV': {'city': 'Funafuti', 'lat': -8.5167, 'lon': 179.2167},
'UG': {'city': 'Kampala', 'lat': 0.3476, 'lon': 32.5825},
'UA': {'city': 'Kyiv', 'lat': 50.4501, 'lon': 30.5234},
'AE': {'city': 'Abu Dhabi', 'lat': 24.4539, 'lon': 54.3773},
'GB': {'city': 'London', 'lat': 51.5074, 'lon': -0.1278},
'US': {'city': 'Washington, D.C.', 'lat': 38.9072, 'lon': -77.0369},
'UY': {'city': 'Montevideo', 'lat': -34.9011, 'lon': -56.1645},
'UZ': {'city': 'Tashkent', 'lat': 41.2995, 'lon': 69.2401},
'VU': {'city': 'Port Vila', 'lat': -17.7333, 'lon': 168.3167},
'VA': {'city': 'Vatican City', 'lat': 41.9029, 'lon': 12.4534},
'VE': {'city': 'Caracas', 'lat': 10.5000, 'lon': -66.9167},
'VN': {'city': 'Hanoi', 'lat': 21.0285, 'lon': 105.8542},
'YE': {'city': 'Sanaa', 'lat': 15.3694, 'lon': 44.1910},
'ZM': {'city': 'Lusaka', 'lat': -15.4167, 'lon': 28.2833},
'ZW': {'city': 'Harare', 'lat': -17.8292, 'lon': 31.0522}
}
    
    # Create the map figure
    fig = go.Figure()

    # Iterate over the capital cities
    for code, city_info in capital_cities.items():
        # Get the country's latitude and longitude
        lat = city_info['lat']
        lon = city_info['lon']
        city_name = city_info['city']


        # Define a list of nicer-looking colors
        color_palette = [
            '#FF1744', '#F1FAEE', '#A8DADC', '#039BE5', '#00E5FF',
            '#FF8F00', '#FFFF00', '#00C853', '#E040FB', '#00ACC1'
        ]

        # Generate a random index to select a color from the palette
        random_index = random.randint(0, len(color_palette) - 1)
        color = color_palette[random_index]

        # Generate a random RGB color
        #color = f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'

        # Add a scattermapbox trace for the capital city with the random color
        fig.add_trace(go.Scattermapbox(
            mode='markers',
            lon=[lon],
            lat=[lat],
            marker=dict(
                size=10,
                color=color,  # Use the random color
                opacity=0.7
            ),
            text=city_name,
            name=code
        ))

    # Set the map layout
    fig.update_layout(
        mapbox=dict(
            center=dict(lon=0, lat=0),
            zoom=1,
            style='carto-positron'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )

    # Generate the HTML div for the map
    plot_div = fig.to_html(full_html=False)

    return render_template('capitalcities.jinja.html', plot_div=plot_div)
#f27000#f27000#f27000#f27000#f27000


#FFF9AA#FFF9AA#FFF9AA#FFF9AA#FFF9AA
@app.route("/piechart")
def piechart():
    #df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    #df.to_csv("covid_data.csv", index=False)
    df = pd.read_csv("covid_data.csv")

    df["date"] = pd.to_datetime(df.date)

    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)
    mdf = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    mdf = mdf.reset_index()

    # Filter the DataFrame to include only columns with more than 100,000 missing values
    filtered_mdf = mdf.query("Total > 100000")

    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=filtered_mdf["index"], values=filtered_mdf["Total"])])
    fig.update_layout(showlegend=True)

    # Convert the chart to JSON
    chart_json = fig.to_json()

    return render_template('piechart.jinja.html', chart_json=chart_json)
#FFF9AA#FFF9AA#FFF9AA#FFF9AA#FFF9AA


#FF0
@app.route("/funcircles")
def funcircles():
    return render_template('funcircles.jinja.html')

#FF0


#af161e#af161e#af161e#af161e#af161e
@app.route('/sunburstdiagram')
def sunburstdiagram():
    # Read the CSV data
    df = pd.read_csv('data.csv')

    # Create the sunburst figure
    fig2 = px.sunburst(df, path=['Parent', 'Item and Group'], values='Weight', color='Parent'
    )

    fig2.update_layout(font_size=20, width=1200,  # Set the width of the diagram
        height=800,  # Set the height of the diagram
    )

    # Convert the figure to HTML
    plot_html = fig2.to_html(full_html=False, include_plotlyjs='cdn')

    # Render the HTML template with the plot
    return render_template('sunburst.jinja.html', plot_html=plot_html)
#af161e#af161e#af161e#af161e#af161e


#166daf#166daf#166daf#166daf#166daf
@app.route('/gdpbycountry')
def gdpbycountry():
    
    # Import data from GitHub
    data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv')

    # Filter data for the latest year (2007) 資料只有1952-2007
    data = data[data['year'] == 2007]

    # Create basic choropleth map with hover data
    fig = px.choropleth(data, locations='iso_alpha', color='gdpPercap', hover_name='country',
                        hover_data=['year', 'gdpPercap'], projection='natural earth',
                        title='GDP per Capita by Country')

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    return render_template('gdpbycountry.jinja.html', plot_html=plot_html)
#166daf#166daf#166daf#166daf#166daf

#多張圖放一起
#rgba(154, 14, 118, 1)rgba(154, 14, 118, 1)
@app.route('/2sunburst')
def a():
        return render_template('a.jinja.html')

@app.route('/data')
def chart_data():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/sales_success.csv')

    levels = ['salesperson', 'county', 'region'] # levels used for the hierarchical chart
    color_columns = ['sales', 'calls']
    value_column = 'calls'

    def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
        """
        Build a hierarchy of levels for Sunburst or Treemap charts.

        Levels are given starting from the bottom to the top of the hierarchy,
        ie the last level corresponds to the root.
        """
        df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        for i, level in enumerate(levels):
            df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
            dfg = df.groupby(levels[i:]).sum()
            dfg = dfg.reset_index()
            df_tree['id'] = dfg[level].copy()
            if i < len(levels) - 1:
                df_tree['parent'] = dfg[levels[i+1]].copy()
            else:
                df_tree['parent'] = 'total'
            df_tree['value'] = dfg[value_column]
            df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]

            df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
        total = pd.Series(dict(id='total', parent='',
                                value=df[value_column].sum(),
                                color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
        df_all_trees = pd.concat([df_all_trees, pd.DataFrame(total).T], ignore_index=True)
        return df_all_trees

    df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)
    average_score = df['sales'].sum() / df['calls'].sum()

    fig = make_subplots(1, 2, specs=[[{"type": "domain"}, {"type": "domain"}]],)

    fig.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        branchvalues='total',
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='RdBu',
            cmid=average_score),
        hovertemplate='<b>%{label} </b> <br> Sales: %{value}<br> Success rate: %{color:.2f}',
        name=''
        ), 1, 1)

    fig.add_trace(go.Sunburst(
        labels=df_all_trees['id'],
        parents=df_all_trees['parent'],
        values=df_all_trees['value'],
        marker=dict(
            colors=df_all_trees['color'],
            colorscale='RdBu'),
        hovertemplate='<b>%{label} </b> <br></br> Allocated: %{value}',
        name=''
    ), 1, 2)

    fig.update_layout(
            grid=dict(columns=2, rows=1),
            margin=dict(t=0, l=0, r=0, b=0),
            width=1200,  # Set the width of the chart to 1200px
            height= 800
    )

    chart_data_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return chart_data_json
#rgba(154, 14, 118, 1)rgba(154, 14, 118, 1)


#rgba(34, 150, 221, 1)rgba(34, 150, 221, 1)
@app.route('/4sunburst')
def b():

    fig1 = go.Figure(go.Sunburst(
        labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
        values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
    ))

    fig2 = go.Figure(go.Sunburst(
        ids=["North America", "Europe", "Australia", "North America - Football", "Soccer",
             "North America - Rugby", "Europe - Football", "Rugby",
             "Europe - American Football","Australia - Football", "Association",
             "Australian Rules", "Autstralia - American Football", "Australia - Rugby",
             "Rugby League", "Rugby Union"],
        labels=["North<br>America", "Europe", "Australia", "Football", "Soccer", "Rugby",
                "Football", "Rugby", "American<br>Football", "Football", "Association",
                "Australian<br>Rules", "American<br>Football", "Rugby", "Rugby<br>League",
                "Rugby<br>Union"],
        parents=["", "", "", "North America", "North America", "North America", "Europe",
                 "Europe", "Europe","Australia", "Australia - Football", "Australia - Football",
                 "Australia - Football", "Australia - Football", "Australia - Rugby",
                 "Australia - Rugby"],
    ))

    l1 = ["produce", "produce", "produce", "produce", "pantry", "pantry", "pantry", "pantry", "pantry", "ice"]
    l2 = ["fruit", "fruit", "vegetable", "vegetable", "canned goods","bread", "canned goods", "baking goods", "baking goods", None]
    l3 = ["apple", "banana", "tomato", "potato", "soup",None, "Beans", "flour", "active yeast", None]
    l4 = ["Fuji", None, None, "idaho", "tomato",None, "black", "bleached white", None, None]
    sales = [1, 3, 2, 4, 1, 2, 2, 1, 4, 1]
    df = pd.DataFrame(dict(l1=l1, l2=l2, l3=l3, l4=l4, sales=sales))

    fig3 = px.sunburst(df, path=['l1', 'l2', 'l3','l4'], values='sales')

    vendors = ["A", "B", "C", "D", None, "E", "F", "G", "H", None]
    sectors = ["Tech", "Tech", "Finance", "Finance", "Other",
               "Tech", "Tech", "Finance", "Finance", "Other"]
    regions = ["North", "North", "North", "North", "North",
               "South", "South", "South", "South", "South"]
    sales = [1, 3, 2, 4, 1, 2, 2, 1, 4, 1]
    df = pd.DataFrame(dict(vendors=vendors, sectors=sectors, regions=regions, sales=sales))

    fig4 = px.sunburst(df, path=['regions', 'sectors', 'vendors'], values='sales')

    return render_template('b.jinja.html', fig1=fig1.to_json(), fig2=fig2.to_json(),
                           fig3=fig3.to_json(), fig4=fig4.to_json())
#rgba(34, 150, 221, 1)rgba(34, 150, 221, 1)   
    
    
