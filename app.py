from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
import folium
from pyproj import Geod
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

class CoordinateForm(FlaskForm):
    lat1 = FloatField('Latitude for Point 1')
    lon1 = FloatField('Longitude for Point 1')
    lat2 = FloatField('Latitude for Point 2')
    lon2 = FloatField('Longitude for Point 2')
    submit = SubmitField('Generate Map')

def compute_orthodrome_points(point1, point2, num_points=100):
    geod = Geod(ellps='WGS84')
    line = geod.npts(point1[1], point1[0], point2[1], point2[0], num_points + 2)
    points = [(lat, lon) for lon, lat in line]
    return points

def draw_orthodrome_on_map(points):
    m = folium.Map(location=[(points[0][0] + points[-1][0]) / 2, (points[0][1] + points[-1][1]) / 2], zoom_start=4)
    folium.Marker([points[0][0], points[0][1]], popup='Start', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([points[-1][0], points[-1][1]], popup='End', icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(locations=points, color='blue').add_to(m)
    return m

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CoordinateForm()

    if form.validate_on_submit():
        point1 = (form.lat1.data, form.lon1.data)
        point2 = (form.lat2.data, form.lon2.data)
        orthodrome_points = compute_orthodrome_points(point1, point2)
        map_with_orthodrome = draw_orthodrome_on_map(orthodrome_points)
        map_file_path = "static/orthodrome_map.html"
        map_with_orthodrome.save(map_file_path)
        return render_template('index.html', form=form, map_created=True, map_file_path=map_file_path)

    return render_template('index.html', form=form, map_created=False)

if __name__ == '__main__':
    app.run(debug=True)
