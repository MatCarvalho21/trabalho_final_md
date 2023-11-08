import math

def cal_dist(lat_inicial:float, lon_inicial:float, lat_final:float, lon_final:float) -> float:
    """
    """
    dif_lat = math.radians(float(lat_final) - float(lat_inicial))
    dif_lon = math.radians(float(lon_final) - float(lon_inicial))

    raio_terra_km = 6370

    #funções de haversine para distância esférica
    hav_lat = math.sin(dif_lat/2)**2
    hav_lon = math.sin(dif_lon/2)**2

    cos_1 = math.cos(float(math.radians(lat_inicial)))
    cos_2 = math.cos(float(math.radians(lat_final)))

    dist_real = 2*raio_terra_km*math.asin(math.sqrt(hav_lat + cos_1 * cos_2 * hav_lon))

    return round(dist_real, 2)


def cal_horas(dist_km:float) -> float:
    """
    """
    velociade_km_h = 850
    tempo_horas = round(float(dist_km)/velociade_km_h, 2)

    return tempo_horas
