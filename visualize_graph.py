import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# ------------------------------------------------------------
# 1) CARICAMENTO WAYPOINTS
# ------------------------------------------------------------
wp = pd.read_csv("File_CSV/waypoints.csv")
pos = {}
for _, row in wp.iterrows():
    node_id = row["id"]
    x = row["x"]
    y = row["y"]

    # OFFSET scaffali per i livelli
    if "_X" in node_id and "_L" in node_id:
        level = int(node_id.split("_L")[1])
        x = x + level * 0.30   # 30 cm offset orizzontale

    pos[node_id] = (x, y)


# ------------------------------------------------------------
# 2) CARICAMENTO GRAFO PESATO
# ------------------------------------------------------------
edges_df = pd.read_csv("File_CSV/graph.csv")

G = nx.DiGraph()
for node_id in pos.keys():
    G.add_node(node_id)

for _, row in edges_df.iterrows():
    G.add_edge(row["node_from"], row["node_to"], weight=row["distance"])


# ------------------------------------------------------------
# 3) DEFINIZIONE COLORI NODI
# ------------------------------------------------------------
def node_color(node):
    if node == "MEETING_AREA":
        return "yellow"
    if node == "SHIPPING_AREA":
        return "orange"
    if node.endswith("_F"):
        return "green"
    if node.endswith("_FS"):
        return "red"
    if "_C_X" in node:
        return "royalblue"
    if "_M_X" in node:
        return "purple"
    if "_X" in node and "_L" in node:
        return "gray"
    return "black"


node_colors = [node_color(n) for n in G.nodes()]

# ------------------------------------------------------------
# 4) CREAZIONE ARCHI PER PLOTLY con TRACES SEPARATI PER COLORE
# ------------------------------------------------------------

# Raggruppiamo gli archi per colore
edges_by_color = {}

for u, v in G.edges():

    # Determiniamo colore
    if "_C_X" in u and "_C_X" in v:
        col = "blue"

    elif u.endswith("_F") and v.endswith("_F"):
        col = "yellow"

    elif u.endswith("_FS") and v.endswith("_FS"):
        col = "orange"

    elif (u == "MEETING_AREA" and v.endswith("_F")) or \
         (v == "MEETING_AREA" and u.endswith("_F")):
        col = "yellow"

    elif (u == "SHIPPING_AREA" and v.endswith("_FS")) or \
         (v == "SHIPPING_AREA" and u.endswith("_FS")):
        col = "orange"

    elif ("_X" in u and "_L" in u) or ("_X" in v and "_L" in v):
        col = "gray"

    else:
        col = "black"

    # Aggiungiamo segmento al gruppo colore
    if col not in edges_by_color:
        edges_by_color[col] = {"x": [], "y": []}

    x0, y0 = pos[u]
    x1, y1 = pos[v]

    edges_by_color[col]["x"] += [x0, x1, None]
    edges_by_color[col]["y"] += [y0, y1, None]


# Creiamo un trace Plotly per ogni colore
edge_traces = []

for col, coords in edges_by_color.items():
    edge_traces.append(
        go.Scatter(
            x=coords["x"],
            y=coords["y"],
            mode="lines",
            line=dict(width=2, color=col),
            hoverinfo="none",
            showlegend=False
        )
    )



# ------------------------------------------------------------
# 5) CREAZIONE NODI
# ------------------------------------------------------------
node_x = [pos[n][0] for n in G.nodes()]
node_y = [pos[n][1] for n in G.nodes()]

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    text=[n for n in G.nodes()],  # label visibile con hover
    hoverinfo="text",
    marker=dict(
        size=12,
        color=node_colors
    )
)


# ------------------------------------------------------------
# 6) LEGENDA FISSA SUL LATO DESTRO
# ------------------------------------------------------------
legend_items = [
    ("Meeting Area", "yellow"),
    ("Shipping Area", "orange"),
    ("Front Meeting", "green"),
    ("Front Shipping", "red"),
    ("Corridor Node", "royalblue"),
    ("Corridor Midpoint", "purple"),
    ("Shelf Node", "gray"),
]

legend_traces = []
for name, col in legend_items:
    legend_traces.append(
        go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=12, color=col),
            legendgroup=name,
            showlegend=True,
            name=name
        )
    )


# ------------------------------------------------------------
# 7) GRAFICO INTERATTIVO
# ------------------------------------------------------------
fig = go.Figure(
    data=edge_traces + [node_trace] + legend_traces,
    layout=go.Layout(
        title="Interactive Warehouse Graph Visualization",
        showlegend=True,
        hovermode="closest",
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        width=1300,
        height=900
    )
)

fig.show()
