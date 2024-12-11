function enviarDatos(){
    const danceability = parseFloat(document.getElementById("danceability").value) || 0;
    const loudness = parseFloat(document.getElementById("loudness").value) || 0;
    const acousticness = parseFloat(document.getElementById("acousticness").value) || 0;
    const releaseDecade = parseInt(document.getElementById("release_decade").value) || 0;

    const genres = ["blues", "country", "hiphop", "jazz", "pop", "reggae", "rock"];
    const themes = ["feelings", "music", "night/time", "obscene", "sadness", "violence", "world/life"];

    // Mapeo de valores de géneros: 1 si está seleccionado, 0 si no
    const genreValues = genres.map(genre => document.querySelector(`input[value="${genre}"]`).checked ? 1 : 0);

    // Mapeo de valores de temas: 1 si está seleccionado, 0 si no
    const themeValues = themes.map(theme => document.querySelector(`input[value="${theme}"]`).checked ? 1 : 0);

     // Construir el vector característico
     const vectorCaracteristico = [
        danceability,
        loudness,
        acousticness,
        releaseDecade,
        ...genreValues,
        ...themeValues
      ];
  
      console.log("Vector Característico:", vectorCaracteristico);

      // Hacer la solicitud a la API
      fetch('http://127.0.0.1:5600/buscar_cancion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vectorCaracteristico })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta de la API:', data);
        // Guarda los datos en localStorage
        localStorage.setItem('recommendations', JSON.stringify(data));

        // Redirige a recomendaciones.html
        window.location.href = "recomendaciones.html";
    })
    .catch(error => console.error("Error obteniendo las recomendaciones:", error));
}