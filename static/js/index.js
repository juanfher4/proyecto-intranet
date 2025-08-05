/* Mapa */

window.onload = init_mapa_grande

function init_mapa_grande() {
  // HTML element
  const mapElement = document.getElementById('mapid')

  // Basemaps
  const openStreetMapStandard = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });

  // Leaflet map object
  const mymap = L.map(mapElement, {
    center: [48, 14],
    zoom: 5,
    minZoom: 4,
    zoomSnap: 0.25,
    zoomDelta: 0.25,
    layers: [openStreetMapStandard]
  })
/* 
  // Basemap Object
  const baseLayers = {
    '<b>OpenStreetMapStandard</b>': openStreetMapStandard,
  }

  // Overlays
  const perthBaseMapImage = './Data/Perth_image.png'
  const perthBaseMapBounds = [[-37.66664575662111, 113.64257812500001], [-25.495660029660613, 134.20898437500003]]
  const imagePerthOverlay = L.imageOverlay(perthBaseMapImage, perthBaseMapBounds)

  // Overlay Object
  const overlayerLayers = {
    'Perth Image': imagePerthOverlay
  }

  // Layer control
  const layerControl = L.control.layers(baseLayers, overlayerLayers, {
    collapsed: false
  }).addTo(mymap)

 */  mymap.on('click', function(e) {
    console.log(e.latlng)
  })

  // Casa Abde
  for (let i = 0; i < array.length; i++) {
      
    const perthMarker = L.marker([36.7623718628174, -3.0201635511954676], {
      title: 'Casa Abde',
      opacity: 1
    }).addTo(mymap)

  }

  const perthMarkerPopup = perthMarker.bindPopup('')
  perthMarker.bindTooltip('Casa Abde').openTooltip()

}
