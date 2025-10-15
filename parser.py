import xmltodict
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


def ensure_list(x):
    return x if isinstance(x, list) else [x]

def parseSession(file, verbose=False, graph=False):
    format_string = "%Y-%m-%dT%H:%M:%S.%fZ"

    hr_list = []
    speed_list = []
    cad_list = []
    distance_list = []
    pace_list = []

    tcx = xmltodict.parse(open(file, "r", encoding="utf-8").read())
    activity = tcx['TrainingCenterDatabase']['Activities']['Activity']
    for lap in ensure_list(activity['Lap']):
        track = lap['Track']
        for trackpoint in ensure_list(track['Trackpoint']):
            time = datetime.strptime(trackpoint['Time'], format_string)
            hr = trackpoint['HeartRateBpm']['Value']
            speed = trackpoint['Extensions']['ns3:TPX']['ns3:Speed']
            cad = trackpoint['Extensions']['ns3:TPX']['ns3:RunCadence']

            kmh = round(float(speed) * 3.6, 2)
            pace = round(60 / kmh, 2) if kmh != 0 else 0
            distance = round(float(trackpoint.get('DistanceMeters', 0)), 2)

            hr_list.append(int(hr))
            speed_list.append(kmh)
            cad_list.append(int(cad))
            distance_list.append(distance)
            pace_list.append(pace)

            if verbose:
                print(f"{time.strftime('%H:%M:%S')}, {hr} BPM, {kmh} km/h, {cad} spm, {distance} m, {pace} min/km")

    avg_hr = round(sum(hr_list)/len(hr_list), 2)
    avg_speed = round(sum(speed_list)/len(speed_list), 2)
    avg_pace = round(sum(pace_list)/len(pace_list), 2)
    avg_cad = round(sum(int(c) for c in cad_list)/len(cad_list), 2)
    total_distance = round(distance_list[-1], 2)

    if(graph):
        fig = px.line(x=list(range(len(hr_list))), y=[hr_list, speed_list, cad_list],
                      labels={'x': 'Data Point', 'value': 'Value', 'variable': 'Metric'},
                      title='Heart Rate, Speed, and Cadence Over Time')
        fig.update_traces(mode='lines')
        fig.show()

    return {
        "avg_hr": avg_hr,
        "avg_speed": avg_speed,
        "avg_pace": avg_pace,
        "avg_cad": avg_cad,
        "total_distance": total_distance
    }