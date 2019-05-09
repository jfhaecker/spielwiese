from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
import numpy as np

dates = [
"21.7.2010",
"15.9.2010",
"17.11.2010",
"20.1.2011",
"28.3.2011",
"3.6.2011",
"12.8.2011",
"24.10.2011",
"5.1.2012",
"22.3.2012",
"1.6.2012",
"13.8.2012",
"25.10.2012",
"27.12.2012",
"1.3.2013",
"10.5.2013",
"11.7.2013",
"9.9.2013",
"11.11.2013",
"8.1.2014",
"6.3.2014",
"07.05.2014",
"08.07.2014",
"07.09.2014",
"6.11.2014",
"7.1.2015",
"9.3.2015",
"11.05.2015",
"10.7.2015",
"10.9.2015",
"13.11.2015",
"18.01.2016",
"21.3.2016",
"20.5.2016",
"28.7.2016",
"4.10.2016",
"12.12.2016",
"20.2.2017",
"28.4.2017",
"10.07.2017",
"19.09.2017",
"24.11.2017",
"2.2.2018",
"13.4.2018",
"19.6.2018",
"27.8.2018",
"30.10.2018",
"03.01.2019",
"07.03.2019",
"09.05.2019"
]

date_format = "%d.%m.%Y"
days_between = 63
last = dates[-1]

last_date = datetime.strptime(last,date_format) 
print("Last:{a}".format(a=datetime.strftime(last_date, date_format )))
nd = last_date + timedelta(days=days_between) 
next_date = datetime.strftime(nd, date_format)
print("Next(+{a}days)=>{b}".format(a=days_between,b=next_date))
 
dates.append(next_date)

k = [
        (datetime.strptime(date, date_format) -
            datetime.strptime(dates[i-1], date_format)).days
        for i, date in enumerate(dates)
        if i> 0
    ]

k.insert(0, int(sum(k) / len(k)))
print(k)


#a = np.arange(0, len(dates))
plt.plot(dates, k, "bo", dates, k, "k")
plt.plot(dates, [k[0]]*len(k), label="AVG", linestyle="--")
#plt.bar(dates, k)
plt.xlabel("Datum")
plt.ylabel("Tage")
plt.xticks(rotation=60)
plt.grid(True)

plt.show()
