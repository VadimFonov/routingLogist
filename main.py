from typing import List, Any
import fdb
import folium

con = fdb.connect(dsn='server-psa:ApelFbGps', user='STORE', password='store')
cur = con.cursor()


textQuery = """
    SELECT TRACKER_NAME,TRPOINT_TRACKER,TRPOINT_DT,TRPOINT_LAT,TRPOINT_LNG,TRPOINT_SPEED,TRPOINT_SATCOUNT,
     TRPOINT_HDOP,TRPOINT_T1 FROM TRACKER
     LEFT OUTER JOIN TRPOINT ON TRPOINT.TRPOINT_TRACKER = TRACKER.TRACKER_ID
     WHERE TRACKER.TRACKER_NAME = 'С 186 КК 34 RUS' AND TRPOINT.TRPOINT_DT BETWEEN '30.11.2022.07:00' AND '01.12.2022.06:00' AND TRPOINT.TRPOINT_SPEED > 2
     AND TRPOINT_LAT > 10 AND TRPOINT_LNG > 10 ORDER BY TRPOINT_DT """


cur.execute(textQuery)
Result: list[Any] = cur.fetchall()
pathCar = ((float(Result[0][3]), float(Result[0][4])),)

for strRoute in Result:
 lastCord = (float(strRoute[3]), float(strRoute[4]))
 pathCar = pathCar + (lastCord,)

m = folium.Map(location=(float(Result[0][4]), float(Result[0][3])), zoom_start=7)

folium.PolyLine(pathCar).add_to(m)

m.save("map.html")



