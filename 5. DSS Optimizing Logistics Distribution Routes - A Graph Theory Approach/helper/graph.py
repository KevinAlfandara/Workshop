import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import osmnx as ox
import folium

# get total
# G = graf
# source = nama node source
# target = nama node tujuan
# cutoff = Maksimal node yang dilewati (tidak termasuk node awal)
def get_total(G, source, target, cutoff=2):
    route, total = [], []
    # Mencari semua path
    path = nx.all_simple_paths(G, source=source, target=target, cutoff=cutoff)
    # Iterasi setiap path yang ditemukan
    for p in path:
        # mencari total weight masing-masing path
        le = nx.path_weight(G, p, weight="weight")
        # Menambahkan di list path dan total weight (untuk dataframe)
        route.append(p)
        total.append(le)
    
    # Membentuk dataframe
    df = pd.DataFrame({'route': route, 'total': total})
    # Return dan mengembalikan dalam keadaan terurut
    return df.sort_values(by = 'total')

# Visualize Graf
# Graf = Objek graf
# Position = Layout visualisasi
def visualize_graph(Graf, position = 'shell'):

    # Pilihan layout
    if position == 'spring':
        pos = nx.spring_layout(Graf)
    elif position == 'spectral':
        pos = nx.spectral_layout(Graf)
    elif position == 'circular':
        pos = nx.circular_layout(Graf)
    elif position == 'planar':
        pos = nx.planar_layout(Graf)
    else:
        pos = nx.shell_layout(Graf)
    
    # Menggambar setiap node dari objek graf
    nx.draw_networkx_nodes(Graf, pos,node_size=600)
    # Menggambar setiap edges dari objek graf
    nx.draw_networkx_edges(Graf, pos, width=1)
    # Memberi label masing-masing node
    nx.draw_networkx_labels(Graf, pos, font_size=8, font_family='sans-serif')
    # Mendapatkan weight dari tiap edges
    edge_labels = nx.get_edge_attributes(Graf, 'weight')
    # Memberi label weight pada masing-masing edges
    nx.draw_networkx_edge_labels(Graf, pos, edge_labels)

    # Custom matplotlib
    ax = plt.gca()
    ax.margins(0.01)
    plt.tight_layout()
    plt.show()

# Membuat map objek
# place = Query tempat objek peta, semakin besar petanya, semakin lama
def create_map_object(place = 'Jakarta, Indonesia'):
    # Mendapatkan objek peta dari OSMnx
    graph = ox.graph_from_place(place, network_type = 'drive')
    # Mengembalikan objek peta
    return graph

# Visualisasi rute menggunakan folium dan OSMnx
# graph = objek peta dari create_map_object
# df = dataframe yang akan divisualisasikan
# optimizer = Pemilihan rute yang divisualisasikan apakah berdasarkan jarak "distance" atau waktu "time"
# lokasi = (tuple) Nama kolom lokasi awal dan tujuan
# coord_start = (tuple) Nama kolom longitude dan latitude lokasi awal secara berurutan
# coord_end = (tuple) Nama kolom longitude dan latitude lokasi akhir secara berurutan
def visualize_route(graph,
                    df,
                    optimizer = 'time',
                    lokasi = ('lokasi_start', 'lokasi_end'),
                    coord_start = ('longitude_start', 'latitude_start'),
                    coord_end = ('longitude_end', 'latitude_end')):
    
    optimizer = optimizer
    # cuman pilihan warna
    colors = [
        'blue',
        'red',
        'gray',
        'darkred',
        'orange',
        'beige',
        'green',
        'darkgreen',
        'darkblue',
        'purple',
        'darkpurple',
        'pink',
        'cadetblue',
        'lightgray',
        'black'
    ]
    
    # Iterasi jalur di setiap harinya
    for day in df['day'].unique():
        # Mendapatkan dataframe jalur di hari tertentu (yang diiterasi)
        per_day = df[df.day == day].reset_index()

        # Iterasi dataframe/pengiriman di hari tertentu
        for index, row in per_day.iterrows():
            # Inisiasi node lokasi awal
            start_node = ox.distance.nearest_nodes(graph, 
                                                  row[coord_start[0]],
                                                  row[coord_start[1]])
            # Inisiasi node lokasi tujuan
            end_node = ox.distance.nearest_nodes(graph,
                                                  row[coord_end[0]],
                                                  row[coord_end[1]])
            # Mendapatkan koordinat rute dari lokasi awal - lokasi tujuan
            route = nx.shortest_path(graph,
                                     start_node,
                                     end_node,
                                     weight = optimizer)
            
            # Jika lokasi paling pertama (lokasi berangkat)
            if index == 0:
                # Membuat visualisasi rute lokasi pertama ke lokasi kedua
                route_map = ox.plot_route_folium(G = graph, 
                                                 route = route)
                # Menambahkan marker dan label nama lokasi pertama
                folium.Marker([row[coord_start[1]], row[coord_start[0]]],
                              popup = row[lokasi[0]]).add_to(route_map)
                
                # Menambahkan marker dan label nama lokasi kedua
                folium.Marker([row[coord_end[1]], row[coord_end[0]]], 
                            popup=row[lokasi[1]],
                            icon = folium.Icon(icon='1', color='blue', prefix = 'fa')).add_to(route_map)
                continue
            
            # Membuat visualisasi rute lokasi kedua dan seterusnya
            route_map = ox.plot_route_folium(G = graph,
                                             route = route,
                                             route_map = route_map,
                                             color = colors[index])
            
            angka = str(index + 1)
            # # Menambahkan marker dan label nama lokasi kedua
            # folium.Marker([row[coord_start[1]], row[coord_start[0]]],
            #             popup=row[lokasi[0]],
            #             icon = folium.Icon(icon='1', color='blue', prefix = 'fa')).add_to(route_map)
            # Menambahkan marker dan label nama lokasi ketiga dan seterusnya
            folium.Marker([row[coord_end[1]], row[coord_end[0]]], 
                            popup=row[lokasi[1]],
                            icon = folium.Icon(icon=angka, color=colors[index], prefix = 'fa')).add_to(route_map)
        
        # Memberikan title untuk setiap harinya
        title_html = '''
                <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                '''.format(day)
        # Menambahkan title di map
        route_map.get_root().html.add_child(folium.Element(title_html))

        # Menampilkan rute untuk setiap harinya
        display(route_map)