import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import Ridge
from git_clone import loader

  
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def show_stats():
    # omp_usage = loader.load(is_dry=True)
    # print(omp_usage)

    omp_usage = {'1-2012': 9, '3-2012': 9, '4-2012': 4, '5-2012': 4, '6-2012': 6, '7-2012': 5, '8-2012': 11, '9-2012': 12, '10-2012': 14, '11-2012': 8, '12-2012': 5, '1-2013': 11, '2-2013': 14, '3-2013': 18, '4-2013': 11, '5-2013': 7, '6-2013': 16, '7-2013': 9, '8-2013': 13, '9-2013': 19, '10-2013': 21, '11-2013': 23, '12-2013': 25, '1-2014': 20, '2-2014': 28, '3-2014': 30, '4-2014': 22, '5-2014': 22, '6-2014': 22, '7-2014': 16, '8-2014': 24, '9-2014': 20, '10-2014': 35, '11-2014': 30, '12-2014': 32, '1-2015': 34, '2-2015': 36, '3-2015': 41, '4-2015': 38, '5-2015': 44, '6-2015': 21, '7-2015': 28, '8-2015': 40, '9-2015': 45, '10-2015': 60, '11-2015': 54, '12-2015': 36, '1-2016': 38, '2-2016': 56, '3-2016': 64, '4-2016': 49, '5-2016': 56, '6-2016': 41, '7-2016': 30, '8-2016': 28, '9-2016': 54, '10-2016': 81, '11-2016': 79, '12-2016': 58, '1-2017': 59, '2-2017': 78, '3-2017': 122, '4-2017': 92, '5-2017': 80, '6-2017': 63, '7-2017': 71, '8-2017': 56, '9-2017': 70, '10-2017': 96, '11-2017': 95, '12-2017': 56, '1-2018': 104, '2-2018': 114, '3-2018': 109, '4-2018': 109, '5-2018': 84, '6-2018': 65, '7-2018': 71, '8-2018': 78, '9-2018': 105, '10-2018': 103, '11-2018': 97, '12-2018': 94, '1-2019': 106, '2-2019': 142, '3-2019': 130, '4-2019': 118, '5-2019': 104, '6-2019': 81, '7-2019': 65, '8-2019': 84, '9-2019': 114, '10-2019': 136, '11-2019': 116, '12-2019': 98, '1-2020': 86, '2-2020': 110, '3-2020': 110, '4-2020': 151, '5-2020': 136, '6-2020': 88, '7-2020': 86, '8-2020': 85, '9-2020': 114, '10-2020': 145, '11-2020': 127, '12-2020': 107, '1-2021': 97, '2-2021': 108, '3-2021': 111, '4-2021': 112, '5-2021': 119, '6-2021': 72, '7-2021': 83, '8-2021': 92, '9-2021': 88, '10-2021': 113, '11-2021': 136, '12-2021': 99, '1-2022': 95, '2-2022': 92, '3-2022': 113, '4-2022': 136, '5-2022': 154, '6-2022': 94, '7-2022': 83, '8-2022': 89, '9-2022': 117, '10-2022': 98, '11-2022': 80}

    labels = []
    cur = ''

    for label in list(omp_usage.keys()):
        year = label.split('-')[1]

        if cur != year:
            labels.append(year)
            cur = year
        else:
            labels.append('')

    fig, ax = plt.subplots()

    ax.bar(list(omp_usage.keys()), omp_usage.values())

    # ax.plot(list(range(len(labels))), list(omp_usage.values()))
    # ax.fill_between(list(range(len(labels))), list(omp_usage.values()))

    ax.set_xticklabels(labels)

    ax.set_title('OpenMP Repositories per Month')
    ax.set_ylabel('# repositories')
    ax.set_xlabel('year')

    plt.show()    
