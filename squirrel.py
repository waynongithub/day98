import pandas

nc = "\033[0;97m"
red = "\033[0;91m"
green = "\033[0;92m"
blue = "\033[0;96m"
yellow = "\033[0;93m"
lilac = "\033[0;95m"


def read_weather1():
    arr = []
    with open("weather_data.csv") as f:
        for line in f.readlines():
            arr.append(line)
    print(arr)


def read_weather2():
    with open("weather_data.csv") as f:
        data = csv.reader(f)
        print(data)
        temps = []
        for idx, v in enumerate(data):
            if idx > 0:
                temps.append(int(v[1]))
        print(temps)


def read_weather_pd():
    data = pandas.read_csv("weather_data.csv")
    print(data)
    print(data['temp'])
    datadict = data.to_dict()
    print(datadict)
    templist = data['temp'].to_list()
    print(templist)
    print(sum(templist) / len(templist))
    print(data['temp'].mean())
    print(data['temp'].max())
    print(data.temp.min())
    print(data[data.day == "Monday"])
    print( data[ data.temp == data.temp.max()])
    print(data[data.day == "Monday"]["condition"])
    print(f"=={data[data.day == 'Monday'].condition}")
    monday = data[data.day == 'Monday']
    print(f"monday wass {monday.temp * 23}")
    print(f"monday wass {monday.temp[1] * 23}")



df = pandas.read_csv("2018_Squirrel_Data.csv")
print(df.columns)
colors = df[['Date', 'Primary Fur Color']]
print(f"{green}{colors}{nc}")
print(df[df['Primary Fur Color'] == 'Gray'])
print(df.groupby('Primary Fur Color').count())
print(f"{blue}{colors.groupby('Primary Fur Color').count()}{nc}")



dfw = pandas.read_csv("weather_data.csv")
# print(dfw)
# print(dfw[dfw.day == 'Sunday'])
# print(f"sunny -------")
# print(dfw[dfw.condition == 'Sunny'].count())
# print(f"rain -------")
# print(dfw[dfw.condition == 'Rain'].count())
# print(f"cloudy -------")
# print(dfw[dfw.condition == 'Cloudy'].count())
# print(dfw.groupby(dfw.condition).count())
#
# weather = {
#     "condition": ['cloudy', 'rain', 'sunny'],
#     "count": [1, 2, 4]
# }
#
# mydf = pandas.DataFrame.from_dict(weather)
# print(mydf)

# read_weather1()
# read_weather2()
read_weather_pd()
