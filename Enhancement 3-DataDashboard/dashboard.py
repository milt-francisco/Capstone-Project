# Configure the necessary Python module imports for dashboard components
import os
import dash_leaflet as dl
from dash import Dash, dcc, html, dash_table, Input, Output
import dash_leaflet as dl
import plotly.express as px
import base64
import pandas as pd

# Import CRUD module
from crud_module import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# Connection Variables
username = "aacuser"
password = "SNHU1234!"


# Connect to database via CRUD Module
db = AnimalShelter(username, password)

# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# Drop unnecessary MongoDB id column
df.drop(columns=['_id'],inplace=True)

desired_order = ['animal_type', 'animal_id', 'age_upon_outcome', 'breed', 'color', 'date_of_birth', 
                 'name', 'outcome_type', 'outcome_subtype', 'sex_upon_outcome', 'rec_num', 
                 'datetime', 'monthyear', 'location_lat', 'location_long', 'age_upon_outcome_in_weeks']
df = df[desired_order]

#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)

#Add in Grazioso Salvare’s logo
image_filename = 'Grazioso_Salvare_Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Title
app.layout = html.Div([
    html.Div(className='row',
            style={'display': 'flex', 'margin': '10px'},
             children=[
                 html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'height':'5%','width':'5%'}),
                 html.Center(html.B(html.H1('Austin Animal Shelter - Data Dashboard')))
             ]),

    html.Hr(),
    html.Div(

# Interactive filtering options with radio buttons.
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': ' All Animals ', 'value': 'Reset'},
            {'label': ' Cats ', 'value': 'Cats'},
            {'label': ' Dogs ', 'value': 'Dogs'},
            {'label': ' Water Rescue ', 'value': 'Water'},
            {'label': ' Mountain and Wilderness Rescue ', 'value': 'Mountain'},
            {'label': ' Disaster and Individual Tracking ', 'value': 'Disaster'},
            {'label': ' Service Animals ', 'value': 'Service'}    
        ],
        value='Reset',
        inline=True
    )
    ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True} for i in df.columns],
                         hidden_columns=['rec_num', 'datetime', 'monthyear', 'location_lat', 'location_long', 
                                         'age_upon_outcome_in_weeks'],
                         data=df.to_dict('records'),
                        # Features for the interactive data table to make it user-friendly for the client
                         editable=False,
                         filter_action = "native",
                         sort_action = "native",
                         sort_mode = "multi",
                         column_selectable = False,
                         row_selectable = "single",
                         row_deletable = False,
                         selected_columns = [],
                         selected_rows = [0],
                         page_action = "native",
                         page_current = 0,
                         page_size = 10,
                        ),
    html.Br(),
    html.Hr(),

    # Display Pie Chart and Map side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6'
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################    
@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    if filter_type is None:
        return

    data_frame = None

    # Query data based on the selected filter type
    if filter_type == 'Water':
        data_frame = pd.DataFrame.from_records(db.read(
            { "$and": [
                {"$or": [
                    {"breed": {"$regex": "Labrador Retriever Mix"}},
                    {'breed': {'$regex': 'Chesapeake Bay Retriever'}},
                    {'breed': {'$regex': 'Newfoundland'}}
                ]},
                {'sex_upon_outcome': 'Intact Female'},
                {'$and': [
                    {'age_upon_outcome_in_weeks': {'$gt': 26}},
                    {'age_upon_outcome_in_weeks': {'$lt': 156}}
                ]}
            ]}
        ))
    elif filter_type == 'Mountain':
        data_frame = pd.DataFrame.from_records(db.read(
            { "$and": [
                {"$or": [
                    {"breed": {"$regex": 'German Shepherd'}},
                    {'breed': {'$regex': 'Alaskan Malamute'}},
                    {'breed': {'$regex': 'Old English Sheepdog'}},
                    {'breed': {'$regex': 'Siberian Husky'}},
                    {'breed': {'$regex': 'Rottweiler'}}
                ]},
                {'sex_upon_outcome': 'Intact Male'},
                {'$and': [
                    {'age_upon_outcome_in_weeks': {'$gt': 26}},
                    {'age_upon_outcome_in_weeks': {'$lt': 156}}
                ]}
            ]}
        ))
    elif filter_type == 'Disaster':
        data_frame = pd.DataFrame.from_records(db.read(
            { "$and": [
                {"$or": [
                    {"breed": {"$regex": 'Doberman Pinscher'}},
                    {'breed': {'$regex': 'German Shepherd'}},
                    {'breed': {'$regex': 'Golden Retriever'}},
                    {'breed': {'$regex': 'Bloodhound'}},
                    {'breed': {'$regex': 'Rottweiler'}}
                ]},
                {'sex_upon_outcome': 'Intact Male'},
                {'$and': [
                    {'age_upon_outcome_in_weeks': {'$gt': 20}},
                    {'age_upon_outcome_in_weeks': {'$lt': 300}}
                ]}
            ]}
        ))
    elif filter_type == 'Service':
        data_frame = pd.DataFrame.from_records(db.read(
            { "$and": [
                {"$or": [
                    {"breed": {"$regex": "Labrador Retriever"}},
                    {"breed": {"$regex": "Golden Retriever"}},
                    {"breed": {"$regex": "German Shepherd"}},
                ]},
                {"$and": [
                    {"age_upon_outcome_in_weeks": {"$gt": 52}},
                    {"age_upon_outcome_in_weeks": {"$lt": 520}} 
                ]}
            ]}
        ))
    elif filter_type == 'Cats':
        data_frame = pd.DataFrame.from_records(db.read({'animal_type': 'Cat'}))
    elif filter_type == 'Dogs':
        data_frame = pd.DataFrame.from_records(db.read({'animal_type': 'Dog'}))
    else:
        data_frame = pd.DataFrame.from_records(db.read({}))

    data_frame.drop(columns=['_id'], inplace=True)
    return data_frame.to_dict('records')

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):
    if viewData is None:
        return

    df = pd.DataFrame.from_records(viewData)
    animal_count = len(df)

    title = f'Found Animals - {animal_count} Total'

    # Add a Pie Chart
    fig = px.pie(df, names='breed', title=title)
    fig.update_traces(textposition='inside', 
                      hovertemplate='Breed: %{label} <br>Count: %{value}')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    return [
        dcc.Graph(            
            figure = fig
        )    
    ]

#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")]
)
def update_map(viewData, index):  
    if viewData is None:
        return
    elif index is None:
        return

    dff = pd.DataFrame.from_dict(viewData)
    
    # Default map to Austin, TX area if columns are not present
    if 'location_lat' not in dff.columns or 'location_long' not in dff.columns:
        return [dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[dl.TileLayer(id="base-layer-id")])]

    # Because we only allow single row selection, the list can be converted to a row index here
    row = index[0]

    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[dff['location_lat'].iloc[row],dff['location_long'].iloc[row]], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),

            # Marker with tool tip and popup
            dl.Marker(position=[dff['location_lat'].iloc[row],dff['location_long'].iloc[row]], 
                children=[
                    dl.Tooltip(dff['breed'].iloc[row]),
                    dl.Popup([
                    html.H3("Animal Name"),
                    html.P(dff['name'].iloc[row])
                ])
            ])
        ])
    ]
    
if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8050))
    
    print(f"\nTHIS is the correct URL: http://localhost:{port}\n")

    app.run(host=host, port=port, debug=True)
    
