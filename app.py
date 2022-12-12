import dash #Biblioteca principal para criar as aplicações
from dash import dcc #Componentes do Dash
from dash import html #Utilizar as tags html
import dash_bootstrap_components as dbc #Componentes do dbc
from dash.dependencies import Input, Output #Utilizar os inputs e outputs
from dash_bootstrap_templates import load_figure_template #deixar os gráficos no mesmo tema 
import plotly.express as px #Criação dos gráficos 
import pandas as pd #Manipulação de dados 
load_figure_template('cyborg')

# 1-Obtenção dos dados
# ===================================================================================================
df = pd.read_csv("vgsales.csv")

df_games = df[['Name', 'Global_Sales']][:10].sort_values(by='Global_Sales', ascending=False)
df_platforms = df.groupby('Platform', as_index=False)['Global_Sales'].sum().sort_values(by='Global_Sales')
df_genres = df.groupby('Genre', as_index=False)['Global_Sales'].sum().sort_values(by='Global_Sales')

# 2-Criação dos Gráficos
# ==================================================================================================='
fig_games = px.bar(df_games, x='Name', y='Global_Sales', labels={'Name':'Jogos', 'Global_Sales':'Vendas (Milhões de dólares)'}, title='10 Jogos mais vendidos')
fig_platforms = px.scatter(df_platforms, x='Global_Sales', y='Platform', title='Vendas por console')
fig_platforms.update_layout(xaxis_title="Vendas (Milhões de dólares)", yaxis_title="Console")
fig_genres = px.pie(df_genres, values='Global_Sales', title='Vendas por gênero (Milhões de dólares)', names='Genre')

# 3-Instanciar a classe app
# ===================================================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# 4-Criar o Layout
# ===================================================================================================
app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.P("Dashboard de Vendas de Jogos", className="fs-4 text-center mb-0"),
                html.Hr(),
                html.Label("Vendas no(a):", className="mb-0"),
                dbc.RadioItems(
                    options=[
                        {"label": "Mundo", "value": 'Global_Sales'},
                        {"label": "Japão", "value": 'JP_Sales'},
                        {"label": "América do Norte", "value": 'NA_Sales'},
                        {"label": "Europa", "value": 'EU_Sales'},
                        {"label": "Resto do Mundo", "value": 'Other_Sales'},
                    ],
                    value='Global_Sales',
                    id="region",
                ),
            ], className="p-3 h-100")
        ], sm=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig_platforms, id='platforms_fig')
                ], sm=6, className="me-0 pe-0"),
                dbc.Col([
                    dcc.Graph(figure=fig_genres, id='genres_fig')
                ], sm=6, className="ms-0 ps-0 me-0 pe-0"),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(figure=fig_games, id='games_fig')
                    ], className="me-0 pe-0"),
                ])
            ])
        ], sm=9, className="p-2")
    ])
])

# 5-Criar os callbacks
# ===================================================================================================
@app.callback([
    Output('platforms_fig', 'figure'),
    Output('genres_fig', 'figure'),
    Output('games_fig', 'figure')
], [
    Input("region", "value")
])

def update_figs(region):
    df_games = df[['Name', region]][:10].sort_values(by=region, ascending=False)
    df_platforms = df.groupby('Platform', as_index=False)[region].sum().sort_values(by=region)
    df_genres = df.groupby('Genre', as_index=False)[region].sum().sort_values(by=region)

    fig_games = px.bar(df_games, x='Name', y=region, labels={'Name':'Jogos', region:'Vendas (Milhões de dólares)'}, title='10 Jogos mais vendidos')
    fig_platforms = px.scatter(df_platforms, x=region, y='Platform', labels={'Platform':'Console', region:'Vendas (Milhões de dólares)'}, title='Vendas por console')
    fig_genres = px.pie(df_genres, values=region, title='Vendas por gênero (Milhões de dólares)', names='Genre')

    return fig_platforms, fig_genres, fig_games

# 6-Executar a classe
# =========================================================================================
if __name__ == "__main__":
    app.run_server(debug=True)
