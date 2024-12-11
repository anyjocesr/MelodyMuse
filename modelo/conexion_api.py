import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from annoy import AnnoyIndex


app = Flask(__name__)
CORS(app)

def knn_annoy(vectorCaracteristico, k=10):
    '''
    Halla índices de las canciones más parecidas usando Annoy
    '''

    data3 = pd.read_csv('C:/Users/anaid/OneDrive/Documentos/ANAID/IS/modelo/musica_reducido.csv')
    numeric_columns = data3.columns.tolist()
    
    # Normalizar columnas numéricas
    data_normalized = data3.copy()
    data_normalized[numeric_columns] = (data3[numeric_columns] - data3[numeric_columns].min()) / (data3[numeric_columns].max() - data3[numeric_columns].min())
    
    vectorCaracteristico_normalizado = (vectorCaracteristico - data3.min()) / (data3.max() - data3.min())
    
    # Crear índice Annoy
    n_dim = data_normalized.shape[1]
    annoy_index = AnnoyIndex(n_dim, 'euclidean')
    
    for i in range(len(data_normalized)):
        annoy_index.add_item(i, data_normalized.iloc[i].values)
    
    annoy_index.build(10)
    
    # Buscar k vecinos más cercanos
    indices_vecinos = annoy_index.get_nns_by_vector(vectorCaracteristico_normalizado.values, k, include_distances=False)
    
    # Obtener los vecinos más cercanos
    vecinos_mas_cercanos = data3.iloc[indices_vecinos]
    
    return indices_vecinos, vecinos_mas_cercanos

def buscar_cancion(vectorCaracteristico):
    '''
    Retorna nombre del artista y de la canción
    '''
    canciones = pd.read_csv('C:/Users/anaid/OneDrive/Documentos/ANAID/IS/modelo/info_cancion.csv')
    indices, vc = knn_annoy(vectorCaracteristico)

    resumen = []
    for i in indices:
        registro = canciones.iloc[i]
        
        sublista = []
        sublista.append(registro['artist_name'])
        sublista.append(registro['track_name'])
        resumen.append(sublista)
    
    print(resumen)
    #print(vc) #para ver vector característico de las opciones sjjs
    return resumen

@app.route('/buscar_cancion', methods=['POST'])
def buscar_cancion_api():
    # Obtiene el vectorCaracteristico de la solicitud
    data = request.get_json()
    vectorCaracteristico = data['vectorCaracteristico']
    
    # Llama a la función buscar_cancion
    resultado = buscar_cancion(vectorCaracteristico)
    
    # Devuelve los resultados en formato JSON
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True,port=5600)

