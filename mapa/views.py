from django.shortcuts import render
from productos.models import Ubicacion

def mapa(request):

  # Fetch all locations from the database
  ubicaciones = Ubicacion.objects.all()
  latitudes = [ubicacion.latitud for ubicacion in ubicaciones if ubicacion.latitud is not None]
  longitudes = [ubicacion.longitud for ubicacion in ubicaciones if ubicacion.longitud is not None]
  print(f"Latitudes: {latitudes}")
  print(f"Longitudes: {longitudes}")

  return render(request, 'mapa/mapa.html')