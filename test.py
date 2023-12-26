import folium
from pyproj import Geod


def compute_orthodrome_points(point1, point2, num_points=100):
    # Вычисление координат промежуточных точек на ортодромии
    geod = Geod(ellps='WGS84')
    line = geod.npts(point1[1], point1[0], point2[1], point2[0], num_points + 2)

    points = [(lat, lon) for lon, lat in line]

    return points


def draw_orthodrome_on_map(points):
    # Создание интерактивной карты с использованием folium
    m = folium.Map(location=[(points[0][0] + points[-1][0]) / 2, (points[0][1] + points[-1][1]) / 2], zoom_start=4)

    # Добавление маркера для начальной точки
    folium.Marker([points[0][0], points[0][1]], popup='Start', icon=folium.Icon(color='green')).add_to(m)

    # Добавление маркера для конечной точки
    folium.Marker([points[-1][0], points[-1][1]], popup='End', icon=folium.Icon(color='red')).add_to(m)

    # Добавление линии ортодромии на карту
    folium.PolyLine(locations=points, color='blue').add_to(m)

    # Отображение карты
    return m


# Пример использования
point1 = (43.842349, -84.000442) # Координаты Праги
point2 = (-6.295347, -70.629833)  # Координаты Штат Техас

orthodrome_points = compute_orthodrome_points(point1, point2)

# Отображение точек на карте
map_with_orthodrome = draw_orthodrome_on_map(orthodrome_points)

# Сохранение карты в HTML-файл
map_with_orthodrome.save("templates/orthodrome_map.html")
