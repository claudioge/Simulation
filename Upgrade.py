import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

Population = 1000
inf_chance = 5
Death_Prob = 1
Grid_Size = 20


def GetRandList(low, high, size):

    Rand = []

    while (len(Rand) < size):

        r = np.random.randint(low, high)
        if r not in Rand: Rand.append(r)

    return Rand


class Person():

    def __init__(self):

        self.status = 0
        self.opinion = 0
        self.immunity = 60
        self.recovery_time = 10

    def CheckHealth(self):

        chance_Death = np.random.randint(0,1000)
        
        if self.status == 1 and chance_Death < Death_Prob: 
            self.status = 3
        elif self.status == 1 and self.recovery_time > 0:
            self.recovery_time -= 1
        elif self.status == 1 and self.recovery_time == 0:
            self.status = 2
            self.recovery_time = 10

        elif self.status == 2 and self.immunity > 0: self.immunity -= 1
        elif self.status == 2 and self.immunity <= 0:
            self.status = 0
            self.immunity = 60


class Town():

    def __init__(self):

        self.grid = np.zeros((Grid_Size, Grid_Size))
        self.inhabitants = []
        self.location = []
        self.Status = []

        for i in range(0, Population):
            P = Person()
            self.inhabitants.append(P)
            self.location.append(
                (np.random.randint(0, Grid_Size), np.random.randint(0, Grid_Size)))
            self.Status.append(P.status)

        Dict = {'Person': self.inhabitants,
            'Location': self.location, 'Status': self.Status}
        self.DF = pd.DataFrame(data=Dict)

    def Infect(self):

        Infections = GetRandList(0, Population, 10)

        for Infection in Infections:
            self.DF.at[Infection, "Status"] = 1
            self.DF.at[Infection, "Person"].status = 1

    def Infected(self):
        tracker = 0
        for person in self.inhabitants:
            if person.status == 1: tracker += 1
        return tracker

    def Immune(self):
        tracker = 0
        for person in self.inhabitants:
            if person.status == 2: tracker += 1
        return tracker

    def Death(self):
        tracker = 0
        for person in self.inhabitants:
            if person.status == 3: tracker += 1
        return tracker

    def Spread(self):

        for i in range(0, Grid_Size):
            for j in range(0, Grid_Size):
                Occupants = self.DF[self.DF["Location"] == (i, j)]

                if Occupants.size > 3 and 1 in Occupants.values:

                    for ind in Occupants.index:
                        chance = np.random.randint(0, 100)
                        if self.DF.iloc[ind]["Person"].status == 0 and chance < inf_chance:
                            self.DF.at[ind, "Person"].status = 1

    def Move(self):
       newLoc = [(np.random.randint(0, Grid_Size), np.random.randint(
           0, Grid_Size)) for i in range(Population)]
       self.DF.Location = newLoc

       for i in range(0, Population):

           self.inhabitants[i].CheckHealth()
           self.DF.at[i,"Status"] = self.inhabitants[i].status


start = time.time()
inf_tracker = []
imm_tracker = []
death_tracker = []
T = Town()
T.Infect()
inf_tracker.append(T.Infected())
imm_tracker.append(T.Immune())
death_tracker.append(T.Death())
for i in range(0, 500):

    T.Spread()
    T.Move()
    inf_tracker.append(T.Infected())
    imm_tracker.append(T.Immune())
    death_tracker.append(T.Death())

plt.plot(np.arange(0, 501), inf_tracker, color='r')
plt.plot(np.arange(0, 501), imm_tracker, color='b')
plt.plot(np.arange(0, 501), death_tracker, color = 'y')
end = time.time()

print(end - start)
