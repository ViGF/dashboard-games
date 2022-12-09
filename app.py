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

df_games = df[['Name', 'Global_Sales']][:10]
df_platforms = df.groupby('Platform', as_index=False)['Global_Sales'].sum()

# 2-Criação dos Gráficos
# ==================================================================================================='
fig_games = px.bar(df_games, x='Name', y='Global_Sales', labels={'Name':'Jogos', 'Global_Sales':'Vendas (Milhão)'}, title='10 Jogos mais vendidos no mundo')
fig_platforms = px.pie(df_platforms, values='Global_Sales', title='Vendas por Console', names='Platform')

# 3-Instanciar a classe app
# ===================================================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# 4-Criar o Layout
# ===================================================================================================
app.layout = html.Div(children=[
    dcc.Graph(figure=fig_games), 
    dcc.Graph(figure=fig_platforms) 
])

# 5-Criar os callbacks
# ===================================================================================================


# 6-Executar a classe
# =========================================================================================
if __name__ == "__main__":
    app.run_server(debug=True)
