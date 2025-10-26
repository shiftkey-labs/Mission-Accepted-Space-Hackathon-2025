import pandas as pd


df = pd.read_csv('groundTemp.csv')

temp_list = df['MOD11A1_061_LST_Day_1km'].values.tolist()
latList = df['Latitude'].values.tolist()
longList = df['Longitude'].values.tolist()

sum = 0 
i = 0
count = 0
noFrostList = set()
lastLat= latList[0]
currentLat = latList[0]
lastLong= latList[1]
currentLong = latList[1]

for element in temp_list:
    if((currentLat != lastLat) | (currentLong != lastLong)):
            if(count != 0):
                print("Lat", latList[i], " Long", longList[i], " AvgTempK: ", sum / count)
                count = 0
                sum = 0
            
    
    if(element != 0):
        if(element > 273):
            noFrostList.add((df['Latitude'].at[i], df['Longitude'].at[i]))
            
        
        
        sum += element
        count += 1
       
    i+=1
    if(i < 17325):
        lastLat = currentLat
        currentLat = latList[i]

for coord in noFrostList:
    print("No Frost at Lat: ", coord[0], " Long: ", coord[1])