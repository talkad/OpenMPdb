import numpy as np 
import matplotlib.pyplot as plt 

plt.rc('axes', labelsize=16)
plt.rc('xtick', labelsize=16)    
plt.rc('ytick', labelsize=16)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def show_stats():
    # omp_usage = loader.load(is_dry=True)
    # print(omp_usage)

    # omp_usage_mpi = {'1-2012': 3, '3-2012': 4, '4-2012': 0, '5-2012': 0, '6-2012': 2, '7-2012': 1, '8-2012': 3, '9-2012': 2, '10-2012': 4, '11-2012': 1, '12-2012': 1, '1-2013': 2, '2-2013': 3, '3-2013': 4, '4-2013': 4, '5-2013': 1, '6-2013': 3, '7-2013': 3, '8-2013': 3, '9-2013': 10, '10-2013': 7, '11-2013': 5, '12-2013': 4, '1-2014': 3, '2-2014': 8, '3-2014': 6, '4-2014': 6, '5-2014': 4, '6-2014': 9, '7-2014': 9, '8-2014': 12, '9-2014': 4, '10-2014': 10, '11-2014': 5, '12-2014': 8, '1-2015': 14, '2-2015': 11, '3-2015': 12, '4-2015': 6, '5-2015': 9, '6-2015': 3, '7-2015': 8, '8-2015': 7, '9-2015': 11, '10-2015': 15, '11-2015': 11, '12-2015': 11, '1-2016': 11, '2-2016': 15, '3-2016': 16, '4-2016': 14, '5-2016': 10, '6-2016': 9, '7-2016': 8, '8-2016': 3, '9-2016': 15, '10-2016': 15, '11-2016': 23, '12-2016': 15, '1-2017': 21, '2-2017': 24, '3-2017': 36, '4-2017': 22, '5-2017': 19, '6-2017': 18, '7-2017': 12, '8-2017': 13, '9-2017': 8, '10-2017': 15, '11-2017': 26, '12-2017': 15, '1-2018': 24, '2-2018': 29, '3-2018': 22, '4-2018': 21, '5-2018': 17, '6-2018': 19, '7-2018': 13, '8-2018': 17, '9-2018': 28, '10-2018': 29, '11-2018': 28, '12-2018': 22, '1-2019': 30, '2-2019': 40, '3-2019': 26, '4-2019': 27, '5-2019': 22, '6-2019': 20, '7-2019': 21, '8-2019': 24, '9-2019': 17, '10-2019': 26, '11-2019': 29, '12-2019': 24, '1-2020': 16, '2-2020': 32, '3-2020': 23, '4-2020': 27, '5-2020': 41, '6-2020': 18, '7-2020': 20, '8-2020': 18, '9-2020': 31, '10-2020': 26, '11-2020': 27, '12-2020': 20, '1-2021': 24, '2-2021': 28, '3-2021': 25, '4-2021': 19, '5-2021': 28, '6-2021': 22, '7-2021': 24, '8-2021': 23, '9-2021': 26, '10-2021': 26, '11-2021': 29, '12-2021': 29, '1-2022': 33, '2-2022': 22, '3-2022': 26, '4-2022': 32, '5-2022': 39, '6-2022': 25, '7-2022': 13, '8-2022': 13, '9-2022': 17, '10-2022': 23, '11-2022': 25, '12-2022': 6}
    # omp_usage {'1-2012': 9, '3-2012': 9, '4-2012': 4, '5-2012': 4, '6-2012': 6, '7-2012': 5, '8-2012': 11, '9-2012': 12, '10-2012': 14, '11-2012': 8, '12-2012': 5, '1-2013': 11, '2-2013': 14, '3-2013': 18, '4-2013': 11, '5-2013': 7, '6-2013': 16, '7-2013': 9, '8-2013': 13, '9-2013': 19, '10-2013': 21, '11-2013': 23, '12-2013': 25, '1-2014': 20, '2-2014': 28, '3-2014': 30, '4-2014': 22, '5-2014': 22, '6-2014': 22, '7-2014': 16, '8-2014': 24, '9-2014': 20, '10-2014': 35, '11-2014': 30, '12-2014': 32, '1-2015': 34, '2-2015': 36, '3-2015': 41, '4-2015': 38, '5-2015': 44, '6-2015': 21, '7-2015': 28, '8-2015': 40, '9-2015': 45, '10-2015': 60, '11-2015': 54, '12-2015': 36, '1-2016': 38, '2-2016': 56, '3-2016': 64, '4-2016': 49, '5-2016': 56, '6-2016': 41, '7-2016': 30, '8-2016': 28, '9-2016': 54, '10-2016': 81, '11-2016': 79, '12-2016': 58, '1-2017': 59, '2-2017': 78, '3-2017': 122, '4-2017': 92, '5-2017': 80, '6-2017': 63, '7-2017': 71, '8-2017': 56, '9-2017': 70, '10-2017': 96, '11-2017': 95, '12-2017': 56, '1-2018': 104, '2-2018': 114, '3-2018': 109, '4-2018': 109, '5-2018': 84, '6-2018': 65, '7-2018': 71, '8-2018': 78, '9-2018': 105, '10-2018': 103, '11-2018': 97, '12-2018': 94, '1-2019': 106, '2-2019': 142, '3-2019': 130, '4-2019': 118, '5-2019': 104, '6-2019': 81, '7-2019': 65, '8-2019': 84, '9-2019': 114, '10-2019': 136, '11-2019': 116, '12-2019': 98, '1-2020': 86, '2-2020': 110, '3-2020': 110, '4-2020': 151, '5-2020': 136, '6-2020': 88, '7-2020': 86, '8-2020': 85, '9-2020': 114, '10-2020': 145, '11-2020': 127, '12-2020': 107, '1-2021': 97, '2-2021': 108, '3-2021': 111, '4-2021': 112, '5-2021': 119, '6-2021': 72, '7-2021': 83, '8-2021': 92, '9-2021': 88, '10-2021': 113, '11-2021': 136, '12-2021': 99, '1-2022': 95, '2-2022': 92, '3-2022': 113, '4-2022': 136, '5-2022': 154, '6-2022': 94, '7-2022': 83, '8-2022': 89, '9-2022': 117, '10-2022': 98, '11-2022': 80}
    
    # cumulative
    omp_usage = {'1-2012': 9, '3-2012': 18, '4-2012': 22, '5-2012': 26, '6-2012': 32, '7-2012': 37, '8-2012': 48, '9-2012': 60, '10-2012': 74, '11-2012': 82, '12-2012': 87, '1-2013': 98, '2-2013': 112, '3-2013': 130, '4-2013': 141, '5-2013': 148, '6-2013': 164, '7-2013': 173, '8-2013': 186, '9-2013': 205, '10-2013': 226, '11-2013': 249, '12-2013': 274, '1-2014': 294, '2-2014': 322, '3-2014': 352, '4-2014': 374, '5-2014': 396, '6-2014': 418, '7-2014': 434, '8-2014': 458, '9-2014': 478, '10-2014': 513, '11-2014': 543, '12-2014': 575, '1-2015': 609, '2-2015': 645, '3-2015': 686, '4-2015': 724, '5-2015': 768, '6-2015': 789, '7-2015': 817, '8-2015': 857, '9-2015': 902, '10-2015': 962, '11-2015': 1016, '12-2015': 1052, '1-2016': 1090, '2-2016': 1146, '3-2016': 1210, '4-2016': 1259, '5-2016': 1315, '6-2016': 1356, '7-2016': 1386, '8-2016': 1414, '9-2016': 1468, '10-2016': 1549, '11-2016': 1628, '12-2016': 1686, '1-2017': 1745, '2-2017': 1823, '3-2017': 1945, '4-2017': 2037, '5-2017': 2117, '6-2017': 2180, '7-2017': 2251, '8-2017': 2307, '9-2017': 2377, '10-2017': 2473, '11-2017': 2568, '12-2017': 2624, '1-2018': 2728, '2-2018': 2842, '3-2018': 2951, '4-2018': 3060, '5-2018': 3144, '6-2018': 3209, '7-2018': 3280, '8-2018': 3358, '9-2018': 3463, '10-2018': 3566, '11-2018': 3663, '12-2018': 3757, '1-2019': 3863, '2-2019': 4005, '3-2019': 4135, '4-2019': 4253, '5-2019': 4357, '6-2019': 4438, '7-2019': 4503, '8-2019': 4587, '9-2019': 4701, '10-2019': 4837, '11-2019': 4953, '12-2019': 5051, '1-2020': 5137, '2-2020': 5247, '3-2020': 5357, '4-2020': 5508, '5-2020': 5644, '6-2020': 5732, '7-2020': 5818, '8-2020': 5903, '9-2020': 6017, '10-2020': 6162, '11-2020': 6289, '12-2020': 6396, '1-2021': 6493, '2-2021': 6601, '3-2021': 6712, '4-2021': 6824, '5-2021': 6943, '6-2021': 7015, '7-2021': 7098, '8-2021': 7190, '9-2021': 7278, '10-2021': 7391, '11-2021': 7527, '12-2021': 7626, '1-2022': 7721, '2-2022': 7813, '3-2022': 7926, '4-2022': 8062, '5-2022': 8216, '6-2022': 8310, '7-2022': 8393, '8-2022': 8482, '9-2022': 8599, '10-2022': 8697, '11-2022': 8777}

    labels = []
    cur = ''

    for label in list(omp_usage.keys()):
        year = label.split('-')[1]

        if cur != year:
            labels.append(year)
            cur = year
        else:
            labels.append('')

    fig, ax = plt.subplots(figsize=(16, 8))

    ax.bar(list(omp_usage.keys()), omp_usage.values())

    # ax.plot(list(range(len(labels))), list(omp_usage.values()))
    # ax.fill_between(list(range(len(labels))), list(omp_usage.values()))

    # ax.set_xticklabels(labels)
    ax.set_xticklabels(list(map(lambda val: val if len(val) > 0 and int(val)%2==0 else '', labels)))

    ax.set_title('Cumulative OpenMP Repositories Per Month', fontsize=20)
    ax.set_ylabel('Cumulative Amount of repositories')
    ax.set_xlabel('Month')

    # plt.savefig('repo_gathering.png', dpi=400)
    plt.show()    

show_stats()