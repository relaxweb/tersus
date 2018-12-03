from flask import Flask, render_template, redirect
from dash import Dash
import dash_table as datatable
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from werkzeug.wsgi import DispatcherMiddleware

server = Flask(__name__)

materialize_css = "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
bootstrap_css = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
mdl_css = [
    "https://code.getmdl.io/1.3.0/material.indigo-deep_purple.min.css",
    "https://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en",
    "https://fonts.googleapis.com/icon?family=Material+Icons",
    "https://cdn.datatables.net/1.10.19/css/dataTables.material.min.css"
    ]

js_scripts = [
    "https://code.getmdl.io/1.3.0/material.min.js",
    "https://code.jquery.com/jquery-3.3.1.js",
    "https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js",
    "https://cdn.datatables.net/1.10.19/js/dataTables.material.min.js"
]

# users = Dash(__name__, server=server, url_base_pathname='/users/', external_stylesheets=[materialize_css])
# products = Dash(__name__, server=server, url_base_pathname='/products/', external_stylesheets=[materialize_css])

top_nav_bar = html.Nav(
    html.Div(className="nav-wrapper", children=[
        html.A('Tersus', className="brand-logo", href='/'),
        html.Ul(className='right hide-on-med-and-down', id='nav-mobile', children=[
            html.Li(dcc.Link('Dashboard', href="/dashboard")),
            html.Li(dcc.Link('Catalog', href="/catalog")),
            html.Li(dcc.Link('Orders', href="/orders")),
            html.Li(dcc.Link('Products', href="/products")),
            html.Li(dcc.Link('Customers', href="/customers")),
            html.Li(dcc.Link('Reports', href="/reports")),
            html.Li(dcc.Link('Users', href="/users")),
            html.Li(dcc.Link('Current User', href="/logged_in_user"), className='dropdown-trigger'),
        ]),
    ]),
)

menu_side = html.Div(className='mdl-layout__container', children=[
    html.Div(className='demo-layout mdl-layout mdl-js-layout mdl-layout--fixed-drawer mdl-layout--fixed-header has-drawer is-upgraded is-small-screen', **{'data-upgraded': ',MaterialLayout'},
             children=[
                 html.Header(className='demo-header mdl-layout__header mdl-color--grey-100 mdl-color-text--grey-600 is-casting-shadow', children=[
                     html.Div(role="button", **{'aria-expanded': 'true'}, tabIndex='0', className='mdl-layout__drawer-button', children=[
                         html.I(className='material-icons')
                     ]),
                     html.Div(className='mdl-layout__header-row')
                 ]),
                 html.Div(className='demo-drawer mdl-layout__drawer mdl-color--blue-grey-900 mdl-color-text--blue-grey-50', **{'aria-hidden': 'false'}, children=[
                     html.Header(className='demo-drawer-header', children=[
                         html.Img(src='/assets/avatar-7.png', className='demo-avatar clickable'),
                         html.Div(className='demo-avatar-dropdown', children=[
                             html.Span('Roman'),
                             html.Div(className='mdl-layout-spacer'),
                             html.Button(id='accbtn', className='mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon', **{'data-upgraded': ',MaterialButton,MaterialRipple'}, children=[
                                 html.I('arrow_drop_down', className='material-icons', role='presentation'),
                                 html.Span('Accounts', className='visuallyhidden'),
                                 html.Span(className='mdl-button__ripple-container', children=[
                                     html.Span(className='mdl-ripple is-animating')
                                 ])
                             ]),
                             html.Div(className='mdl-menu__container is-upgraded', children=[
                                 html.Div(className='mdl-menu__outline mdl-menu--bottom-right'),
                                 html.Ul(className='mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events', **{'data-upgraded': ',MaterialMenu,MaterialRipple'}, children=[
                                     html.Li(className='mdl-menu__item mdl-js-ripple-effect', **{'data-upgraded': ',MaterialRipple'}, children=[
                                        html.I('My Profile', className='material-icons'),
                                        html.Span(className='mdl-menu__item-ripple-container', children=[
                                            html.Span(className='mdl-ripple')
                                        ])
                                     ])
                                 ])
                             ])
                         ])
                     ]),
                     html.Nav(className='demo-navigation mdl-navigation mdl-color--blue-grey-800', children=[
                         dcc.Link(href='/dashboard', className='mdl-navigation__link', children=[
                             html.I('dashboard', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                             'Dashboard'
                         ])
                     ])
                 ])
             ])
])
#     html.Nav(className='demo-navigation mdl-navigation mdl-color--blue-grey-800', children=[
#         html.A(className='mdl-navigation__link', href='/dashboard', children=[html.I('board', className='mdl-color-text--blue-grey-400 material-icons', role='presentation')]),
#         html.A('Catalog', className='mdl-navigation__link', href='/catalog'), # children=[html.I('list', className='mdl-color-text--blue-grey-400 material-icons', role='presentation')]),
#         html.A('Orders', className='mdl-navigation__link', href='/orders') #children=[html.I('note', className='mdl-color-text--blue-grey-400 material-icons', role='presentation')]),
#     ])
# ])


def mainmenu_block_func(title):
    return html.Header(className="demo-header mdl-layout__header mdl-color--grey-100 mdl-color-text--grey-600", children=[
        html.Div(className="mdl-layout__header-row", children=[
            html.Span(title, className="mdl-layout__header-row"),
            html.Div(className="mdl-layout-spacer"),
            html.Button(id="hdrbtn", className="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon", children=[
                html.I('more_vert', className="material-icons")
            ]),
            html.Ul(className="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right", children=[
                html.Li('My profile', className="mdl-menu__item"),
                html.Li('Logout', className="mdl-menu__item"),
            ])
        ])
    ])


def sidemenu_block_func(image_name, first_name, last_name):
    return html.Div(className="demo-drawer mdl-layout__drawer mdl-color--blue-grey-900 mdl-color-text--blue-grey-50", children=[
        html.Header(className="demo-drawer-header", children=[
            html.Img(src="/assets/images/default/" + image_name, className="demo-avatar clickable"),
            html.Div(className="demo-avatar-dropdown", children=[
                html.Span(first_name + " " + last_name),
                html.Div(className="mdl-layout-spacer"),
                html.Button(id="accbtn1", className="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon", children=[
                    html.I('arrow_drop_down', className="material-icons", role="presentation"),
                    html.Span('Accounts', className="visuallyhidden")
                ]),
                html.Ul(className="mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect", children=[
                    html.Li(className="mdl-menu__item", children=[
                        html.I('person', className="material-icons"),
                        '&nbsp;&nbsp;My profile'
                    ]),
                    html.Li(className="mdl-menu__item", children=[
                        html.I('exit_to_app', className="material-icons"),
                        '&nbsp;&nbsp;Log out'
                    ])
                ])
            ])
        ]),
        html.Nav(className='demo-navigation mdl-navigation mdl-color--blue-grey-800', children=[
            dcc.Link(href='/dashboard', className='mdl-navigation__link', children=[
                html.I('dashboard', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Dashboard'
            ]),
            dcc.Link(href='/catalog', className='mdl-navigation__link', children=[
                html.I('list', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Catalog'
            ]),
            dcc.Link(href='/orders', className='mdl-navigation__link', children=[
                html.I('note', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Orders'
            ]),
            dcc.Link(href='/products', className='mdl-navigation__link', children=[
                html.I('shopping_cart', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Products'
            ]),
            dcc.Link(href='/customers', className='mdl-navigation__link', children=[
                html.I('people', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Customers'
            ]),
            dcc.Link(href='/reports', className='mdl-navigation__link', children=[
                html.I('bar_chart', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Reports'
            ]),
            dcc.Link(href='/users', className='mdl-navigation__link', children=[
                html.I('supervisor_account', className='mdl-color-text--blue-grey-400 material-icons', role='presentation'),
                'Users'
            ]),
            html.Div(className="mdl-layout-spacer")
        ])
    ])


def main_layout_func(title, image_name, first_name, last_name):
    return html.Div(className="demo-layout mdl-layout mdl-js-layout mdl-layout--fixed-drawer mdl-layout--fixed-header", children=[
        mainmenu_block_func(title),
        sidemenu_block_func(image_name, first_name, last_name),
        html.Main(className="mdl-layout__content mdl-color--white-100")
    ])


def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        # top_nav_bar,
        main_layout_func('Main', 'avatar-7.png', 'John', 'Smith'),
        html.Div(id='page-content')
    ])


app = Dash(__name__, server=server, url_base_pathname='/dash/', external_stylesheets=mdl_css, external_scripts=js_scripts)
app.layout = serve_layout
app.config.supress_callback_exceptions = True

side_menu = html.Div(children=[
    html.Nav(className = "nav nav-pills", children=[
        html.A('Users', className="nav-item nav-link btn", href='/users'),
        html.A('Products', className="nav-item nav-link active btn", href='/products')
    ])
])


drop_down_user=html.Ul(id='dropdown1', className='dropdown-content', children=[
    html.Li(dcc.Link('Profile', href='/profile')),
    html.Li(dcc.Link('Log out', href='/log_out'))
])

users_layout = html.Div([
    # top_nav_bar,
    datatable.DataTable(
        id='users',
        columns=[{'name': 'id', 'id': 'id'}, {'name': 'First Name', 'id': 'first_name'}, {'name': 'Last Name', 'id': 'last_name'}],
        data = [{'id': 1, 'first_name': 'John', 'last_name': 'Smith'}],
        style_cell = {'textAlign': 'center'},
        style_as_list_view = True,
    )
])

products_layout = html.Div([
    # top_nav_bar,
    datatable.DataTable(
        id='users',
        columns=[{'name': 'id', 'id': 'id'}, {'name': 'Name', 'id': 'name'}, {'name': 'Type', 'id': 'type'}],
        data = [{'id': 1, 'name': 'somename', 'type': 't_shirt'}],
        style_cell = {'textAlign': 'center'},
        style_as_list_view = True,
    )
])

dashboard_layout = html.Div(children=[
    # main_layout_func('Dashboard', 'avatar-7.png', 'John', 'Smith'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/users':
        return users_layout
    elif pathname == '/products':
        return products_layout
    elif pathname == '/dashboard':
        return dashboard_layout
    else:
        return html.Div([
            html.H3(' unknown')
        ])


@server.route('/')
def login():
    return render_template('login.html')


@server.route('/dashboard')
@login_required
def render_users():
    return redirect('/dash_app_dashboard')

# @server.route('/products')
# @login_required
# def render_products():
#     return Flask.redirect('/dash2')
#
#
# app = DispatcherMiddleware(server, {
#     '/dash1': users.server,
#     '/dash2': products.server,
# })


if __name__ == "__main__":
    server.run('0.0.0.0', 8081, use_reloader=True)
    # app.run_server(host='0.0.0.0', port=8081)
