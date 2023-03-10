
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Create dash app instance
app = Dash(external_stylesheets=[dbc.themes.FLATLY])

# Dashboard Title
app.title = 'Dashboard Employee'


## 1. NAVBAR
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    ],
    brand="Employee Dashboard",
    brand_href="#",
    color="#618685",
    dark=True,
)

## 2. Load Data Set

Employee = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

## 3. Card Content
#### Card Content 1
information_card = [
    dbc.CardHeader('Information'),
    dbc.CardBody([
        html.P('This is the information of employeed in our Start-Up'),
    ])
]


#### Card Content 2
employee_card = [
    dbc.CardHeader('Total Employee'),
    dbc.CardBody([
        html.H1(Employee.shape[0])
    ]),
]


'''
#### Card Content 3
promotion_card = [
    dbc.CardHeader('Number of employees promoted'),
    dbc.CardBody([
        html.H1(promotion[promotion['is_promoted']=='Yes'].shape[0], style={'color':'red'})
    ]),
]

'''
'''
promotion_card = [
    dbc.CardHeader('Total Employee'),
    dbc.CardBody([
        html.H1(Employee.shape[0])
    ]),
]
'''

### Barplot1
'''
attr_age= Employee.groupby(['Age','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Count')
attr_age.head()
bar_plot1 = px.area(data_frame=attr_age,x='Age', y='Count',color='Attrition'
).update_layout(showlegend=False)
'''
'''
### Lineplot2
data_2020 = promotion[promotion['join_date'] >= '2020-01-01']
data_2020 = data_2020.groupby(['join_date']).count()['employee_id'].reset_index().tail(30)
line_plot2 = px.line(
    data_2020,
    x='join_date',
    y='employee_id',
    markers=True,
    color_discrete_sequence = ['#618685'],
    template = 'ggplot2',
    labels={
        'join_date':'Join date',
        'employee_id':'Number of employee'
    },
    title = 'Number of new hires in the last 30 days',
    height=700,
)
'''

# User Interface
app.layout = html.Div([
    navbar,
    html.Br(),

    #### ----ROW1----
    dbc.Row([

        ## Row 1 Col 1
        dbc.Col(dbc.Card(information_card, color='#fefbd8'), width=6),

        
        ## Row 1 Col 2
        dbc.Col(dbc.Card(employee_card, color='#80ced6'), width=6),
        
        

    ]),

    html.Br(),

    ### ----ROW2----
    dbc.Row([
        
        ## Row 2 Col 1

        ## Row 2 Col 2
        dbc.Col([
            dcc.Dropdown(
                id='choose_dept',
                options=Employee['Department'].unique(),
                value='Sales',
            ),
            dcc.Graph(id='plot3'),
        ]),

    ]),
])

@app.callback(
    Output(component_id='plot3', component_property='figure'),
    Input(component_id='choose_dept', component_property='value')
)

def update_plot(dept_name):
    data_agg = Employee[Employee['Department'] == dept_name]
    hist_plot3 = px.histogram(
        data_agg,
        x = 'TotalWorkingYears',
        nbins = 20,
        color_discrete_sequence = ['#618685','#80ced6'],
        title = f'Length of Working Years in {dept_name} Department',
        template = 'ggplot2',
        labels={
            'TotalWorkingYears': 'Length of Working Years',
        },
        height=700,
    )
    return hist_plot3

# Run app at local
if __name__ == '__main__':
    app.run_server(debug=True)