import glob, os, json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class CSVRow:
    def __init__(self):
        self.items = []
        self.csvChar = ';'
    
    def add(self, item : str):
        self.items.append(item)
        return self
    
    def generate(self, columnCount : int):
        return self.csvChar.join((self.items + [""] * columnCount)[0:columnCount])

class SteamDBParser:
    def __init__(self, path : str):
        self.items = []

        with open(path, "r") as fp:
            lines = fp.readlines()
            for x in lines[1:]:
                self.items.append([
                    datetime.strptime(x.split(";")[0][1:-1], "%Y-%m-%d %H:%M:%S"),
                    float(x.split(";")[1].strip().replace(",", "."))
                ])

    def getPriceForDate(self, date : datetime):
        prev = self.items[0]
        for x in self.items[1:]:
            if (prev[0] < date and x[0] > date):
                return prev[1]
            
            prev = x
        
        #raise Exception("Price not found?")
        print("Price not found?")
        return self.items[-1][1]

class G2AGame:
    def __init__(self, filename : str, path : str = "."):
        self.records = []
        self.filename = filename
        allFiles = os.listdir(path)
        dirs = allFiles #[x for x in allFiles if os.path.isdir(x)]
        #print(dirs)
        for x in dirs:
            date = datetime.strptime(os.path.basename(x), "%Y-%m-%d_%H-%M-%S")
            filepath = f"{path}/{x}/{filename}"
            #print(filepath)
            if (not os.path.exists(filepath)):
                print("Failed to read "+ filename)
                #if (len(self.records) > 0):
                #    self.records.append([date, self.records[-1][1]])
                #else:
                self.records.append([date, float(0)])
                continue

            b = json.load(open(filepath))
            prices = []
            for y in b["data"]["offers"]:
                prices.append(float(y["prices"]["normal"]["price"]))
                
            if (len(prices) < 1):
                #if (len(self.records) > 0):
                #    self.records.append([date, self.records[-1][1]])
                #else:
                self.records.append([date, float(0)])
                continue

            self.records.append([date, min(prices)])
        
    def generateCSV(self, steam : SteamDBParser):
        csv = []
        csv.append(CSVRow().add(self.filename))
        
        for x in self.records:
            csv.append(CSVRow()
                .add("")
                .add(x[0].strftime("%Y-%m-%d %H:%M:%S"))
                .add(str(x[1]))
                .add(str(steam.getPriceForDate(x[0])))
            )
        
        return csv

    def generatePlot(self, steam : SteamDBParser):
        xAxis = [x[0] for x in self.records]
        yAxis1 = [x[1] for x in self.records]
        yAxis2 = [steam.getPriceForDate(x[0]) for x in self.records]

        #plt.clf()
        #plt.title(self.filename)
        #plt.gca().xaxis

        dataframe = pd.DataFrame({"G2A Prijzen": yAxis1, "Steam Prijzen": yAxis2}, index=xAxis)
        dataframe.plot(x_compat=True, rot=90)
        plt.title(self.filename)
        plt.savefig(f"Images/{self.filename}.png")
        #plt.show()
        #input("Press any key")
        

steamDB = []

def findSteamDB(game : str):
    for x in steamDB:
        if (game.startswith(x[0])):
            return x[1]
    
    raise Exception(f"{game} not found!")

for fil in glob.glob("SteamDB_Sales/*.csv"):
    steamDB.append([os.path.basename(fil[:-4]), SteamDBParser(fil)])
    print(fil)

games = json.load(open("games.json"))
g2aGames = []
for x in games:
    g2aGames.append(G2AGame(f"{x}.json", "./Data"))

csvs = [CSVRow().add("GameName").add("Date").add("G2A Price").add("Steam Price")]
for x in g2aGames:
    parser = findSteamDB(x.filename)
    csvs += x.generateCSV(parser)
    csvs.append(CSVRow())
    x.generatePlot(parser)

with open("output.csv", "w") as fp:
    fp.write("\n".join([x.generate(4) for x in csvs]))