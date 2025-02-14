import json
import pandas as pd
import networkx as nx
import nltk

# This is a basic dash app that runs on the Data in the data folder and allows
# the user to view the existing data. 

from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto

# Load extra layouts
cyto.load_extra_layouts()

# Download required NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# Load JSON data
with open('./data/datasets.json') as f:
    datasets = json.load(f)
with open('./data/publications.json') as f:
    publications = json.load(f)
with open('./data/tools.json') as f:
    tools = json.load(f)

# Load linkage data as pandas DataFrames
dataset_to_dataset = pd.read_json("./data/linkages_dataset_to_dataset.json").set_index('source_dataset_id')
dataset_to_publication = pd.read_json("./data/linkages_dataset_to_publication.json").set_index('source_dataset_id')
dataset_to_tool = pd.read_json("./data/linkages_dataset_to_tool.json").set_index('source_dataset_id')
tool_to_publication = pd.read_json("./data/linkages_tool_to_publication.json").set_index('source_tool_id')

# Construct the NetworkX graph
G = nx.Graph()

# Add dataset nodes (group 1)
for entry in datasets:
    node_id = f"dataset_{entry['id']}"
    short_title = entry.get('metadata', {}).get('summary', {}).get('shortTitle', f"Dataset {node_id}")
    G.add_node(node_id, title=short_title, label=short_title, group=1)

# Add tool nodes (group 3)
for entry in tools:
    node_id = f"tool_{entry['id']}"
    if (name := entry.get('name', None)):
        G.add_node(node_id, title=name, label=name, group=3)

# Add publication nodes (group 2)
for entry in publications:
    node_id = f"publication_{entry['id']}"
    if (doi := entry.get('paper_doi', None)):
        doi = doi.replace("https://doi.org/", "")
        G.add_node(node_id, title=doi, label=doi, group=2)

# Add edges for dataset-to-dataset linkages (group 1)
for _, row in dataset_to_dataset.iterrows():
    source = f"dataset_{row.name}"
    target = f"dataset_{row['target_dataset_id']}"
    G.add_edge(source, target, group=1)

# Add edges for dataset-to-publication linkages (group 2)
for _, row in dataset_to_publication.iterrows():
    source = f"dataset_{row.name}"
    target = f"publication_{row['target_publication_id']}"
    G.add_edge(source, target, group=2)

# Add edges for dataset-to-tool linkages (group 3)
for _, row in dataset_to_tool.iterrows():
    source = f"dataset_{row.name}"
    target = f"tool_{row['target_tool_id']}"
    G.add_edge(source, target, group=3)

# Add edges for tool-to-publication linkages (group 3)
for _, row in tool_to_publication.iterrows():
    source = f"tool_{row.name}"
    target = f"publication_{row['target_publication_id']}"
    G.add_edge(source, target, group=3)

# Remove isolated nodes
isolated_nodes = list(nx.isolates(G))
G.remove_nodes_from(isolated_nodes)

# Function to convert a NetworkX graph (or subgraph) to Cytoscape elements
def generate_elements(subgraph):
    elements = []
    for node, data in subgraph.nodes(data=True):
        elements.append({
            'data': {'id': node, 'label': data.get('label', node)},
            'classes': f"group-{data.get('group', 0)}"
        })
    for source, target, _ in subgraph.edges(data=True):
        elements.append({
            'data': {'source': source, 'target': target}
        })
    return elements

# Generate full graph elements
full_elements = generate_elements(G)

# Define a basic stylesheet with correct property names
stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '10px'
        }
    },
    {'selector': '.group-1', 'style': {'background-color': 'blue'}},
    {'selector': '.group-2', 'style': {'background-color': 'green'}},
    {'selector': '.group-3', 'style': {'background-color': 'red'}},
    {
        'selector': 'edge',
        'style': {
            'line-color': '#bbb',
            'target-arrow-color': '#bbb',
            'target-arrow-shape': 'triangle'
        }
    }
]

# Valid layout options
valid_layouts = [
    {'label': 'Random', 'value': 'random'},
    {'label': 'Preset', 'value': 'preset'},
    {'label': 'Circle', 'value': 'circle'},
    {'label': 'Concentric', 'value': 'concentric'},
    {'label': 'Grid', 'value': 'grid'},
    {'label': 'Breadthfirst', 'value': 'breadthfirst'},
    {'label': 'Cose', 'value': 'cose'},
    {'label': 'Cola', 'value': 'cola'},
    {'label': 'Euler', 'value': 'euler'},
    {'label': 'Spread', 'value': 'spread'},
    {'label': 'Dagre', 'value': 'dagre'},
    {'label': 'Klay', 'value': 'klay'}
]

# Initialise the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='node-type-dropdown',
            options=[
                {'label': 'Dataset', 'value': 'dataset'},
                {'label': 'Publication', 'value': 'publication'},
                {'label': 'Tool', 'value': 'tool'}
            ],
            placeholder="Select node type",
            style={'width': '200px', 'display': 'inline-block', 'margin-right': '10px'}
        ),
        dcc.Dropdown(
            id='node-id-dropdown',
            placeholder="Select node ID",
            style={'width': '200px', 'display': 'inline-block', 'margin-right': '10px'}
        ),
        dcc.Dropdown(
            id='layout-dropdown',
            options=valid_layouts,
            placeholder="Select layout",
            style={'width': '200px', 'display': 'inline-block'}
        )
    ], style={'padding': '10px'}),
    cyto.Cytoscape(
        id='cytoscape-graph',
        elements=full_elements,
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=stylesheet
    )
])

# Callback to update the node ID dropdown based on the selected node type.
@app.callback(
    Output('node-id-dropdown', 'options'),
    Input('node-type-dropdown', 'value')
)
def update_node_id_options(selected_type):
    if not selected_type:
        return []
    options = []
    for node, data in G.nodes(data=True):
        if node.startswith(f"{selected_type}_"):
            options.append({'label': data.get('label', node), 'value': node})
    return sorted(options, key=lambda x: x['label'])

# Callback to update the graph elements. When a node is selected, the subgraph containing that node
# and its immediate neighbours is returned. If no node is selected, the full graph is displayed.
@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('node-id-dropdown', 'value')
)
def update_graph(selected_node):
    if not selected_node:
        return full_elements
    # Obtain immediate neighbours (one degree of separation)
    neighbours = list(G.neighbors(selected_node))
    nodes_to_include = set(neighbours + [selected_node])
    subG = G.subgraph(nodes_to_include)
    return generate_elements(subG)

# Callback to update the layout of the Cytoscape graph.
@app.callback(
    Output('cytoscape-graph', 'layout'),
    Input('layout-dropdown', 'value')
)
def update_layout(selected_layout):
    if not selected_layout:
        selected_layout = 'circle'
    return {'name': selected_layout}

if __name__ == '__main__':
    app.run_server(debug=True)
