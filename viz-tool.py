import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import json
import sys
import random

def parse():
    f = open('test_cases/n=3_t=5_output.json')
    data = json.load(f)
    f.close()

    return data["solution"]

def get_robot_names(robots):
    names = []
    for i in robots:
        names.append(i["name"])
    return names

def extract_task_times(tasks):
    d = {} # {id : (start, duration)}
    for t in tasks:
        d[t["id"]] = (t["start_timepoint"], t["finish_timepoint"]-t["start_timepoint"])
    return d

def graph(sol):
    robots = sol["robots"]
    task_dict = extract_task_times(sol["tasks"])
    print('tasd:', task_dict)

    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    
    # Setting Y-axis limits
    y_max = 60
    gnt.set_ylim(0, y_max)
    
    # Setting X-axis limits
    x_max = sol["makespan"]
    gnt.set_xlim(0, x_max)
    
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('time')
    gnt.set_ylabel('agent')

    # Setting ticks on y-axis
    yticks = range(y_max//(1+len(robots)), y_max, y_max//(1+len(robots)))[:len(robots)]
    print('yt:', list(yticks))
    gnt.set_yticks(yticks)
    # Labelling tickes of y-axis
    robot_names = list(reversed(get_robot_names(robots)))
    # gnt.set_yticklabels(robot_names)
    
    # Setting graph attribute
    gnt.grid(True)

    # draw bars
    bar_height = 9
    colors = ['#E64646', '#E64646', 'tab:red']
    number_of_colors = 8
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    print(colors)
    for i, r in enumerate(robots):
        schedule = []

        r_tasks = r["individual_plan"]
        print('rt:', r_tasks)
        for t in r_tasks:
            schedule.append(task_dict[t])
        
        print('sch:', schedule)

        gnt.broken_barh(schedule, (yticks[i]-bar_height//2, bar_height), facecolors=(colors[i]))

    # Legend
    l_dict = {}
    for i in range(len(robot_names)):
        l_dict[robot_names[i]] = colors[i]
    legend_elements = [Patch(facecolor=l_dict[i], label=i) for i in l_dict]
    plt.legend(handles=legend_elements)
    
    # Declaring a bar in schedule
    # gnt.broken_barh([(40, 50)], (30, bar_height), facecolors =('tab:orange'))
    
    # # Declaring multiple bars in at same level and same width
    # gnt.broken_barh([(110, 10), (150, 10)], (10, bar_height),
    #                         facecolors ='tab:blue')
    
    # gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, bar_height),
    #                                 facecolors =('tab:red'))
    
    plt.show()

def __main__():
    task_dict = {}
    sol = parse()
    graph(sol)

__main__()