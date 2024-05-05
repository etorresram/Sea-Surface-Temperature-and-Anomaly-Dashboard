app = dash.Dash(__name__)

path = 'data'
files = glob(os.path.join(path, '*.txt'))

data_frames = []
for file in files:
    df = pd.read_csv(file, sep='\s+', encoding='ISO-8859-1', skiprows=10, names=['year', 'month', 'day', 'sst', 'ssta'])
    # Limpiar datos
    df['year'] = df['year'].astype(str).str.strip()
    df['month'] = df['month'].astype(str).str.strip().str.zfill(2)
    df['day'] = df['day'].astype(str).str.strip().str.zfill(2)
    # Asegurar que los datos de fecha sean válidos
    df = df[~df['year'].str.contains('yyyy')]
    df = df[df['year'].apply(lambda x: x.isnumeric())]
    df = df[df['month'].apply(lambda x: x.isnumeric())]
    df = df[df['day'].apply(lambda x: x.isnumeric())]
    # Convertir a fecha
    df['date'] = pd.to_datetime(df['year'] + '-' + df['month'] + '-' + df['day'], format='%Y-%m-%d')
    df['city'] = os.path.basename(file).split('.')[0]  # city names
    data_frames.append(df)

combined_df = pd.concat(data_frames, ignore_index=True)

# Dropdown
@app.callback(
    Output('graph', 'figure'),
    [Input('variable-selector', 'value')]
)
def update_graph(selected_variable):
    fig = px.line(combined_df, x='date', y=selected_variable, color='city', 
                  title=f'{selected_variable.upper()} by City')
    return fig

# Layout 
app.layout = html.Div([
    html.H1('Dashboard Sea Surface Temperature (SST) of Peru'),
    dcc.Dropdown(
        id='variable-selector',
        options=[
            {'label': 'Sea Surface Temperature (SST)', 'value': 'sst'},
            {'label': 'Sea Surface Temperature Anomaly (SSTA)', 'value': 'ssta'}
        ],
        value='sst',  # default value
        clearable=False
    ),
    dcc.Graph(
        id='graph'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
