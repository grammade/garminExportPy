import xmltodict
import argparse
import os
from datetime import datetime

format_string = "%Y-%m-%dT%H:%M:%S.%fZ"
parser = argparse.ArgumentParser(description='Parse TCX XML file(s).')
parser.add_argument('dir', type=str, help='Directory of TCX file(s)')

args = parser.parse_args()
hr_list = []
speed_list = []
cad_list = []
distance_list = []
pace_list = []

print(args.dir)
for filename in (f for f in os.listdir(args.dir) if f.endswith(".tcx")):
    path = os.path.join(args.dir, filename)
    basename = os.path.splitext(filename)[0]
    
    actTime = basename.split("_")[1]
    print(basename)




def parseSession(file):
    tcx = xmltodict.parse(open(file, "r", encoding="utf-8").read())
    activity = tcx['TrainingCenterDatabase']['Activities']['Activity']
    for lap in activity['Lap']:
        track = lap['Track']
        for trackpoint in track['Trackpoint']:
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

            print(f"{time.strftime('%H:%M:%S')}, {hr} BPM, {kmh} km/h, {cad} spm, {distance} m, {pace} min/km")
    
    print(f"Avg HR: {round(sum(hr_list)/len(hr_list), 2)} BPM")
    print(f"Avg Speed: {round(sum(speed_list)/len(speed_list), 2)} km/h")
    print(f"Avg Cadence: {round(sum(int(c) for c in cad_list)/len(cad_list), 2)} spm")
    print(f"Total Distance: {round(distance_list[-1], 2)} m")