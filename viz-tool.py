import matplotlib.pyplot as plt
import json
import sys

def parse():
    f = open('n=3_t=5_output.json')
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
    y_max = 50
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
    gnt.set_yticklabels(list(reversed(get_robot_names(robots))))
    
    # Setting graph attribute
    gnt.grid(True)

    # draw bars
    bar_height = 9
    colors = ['tab:orange', 'tab:blue', 'tab:red']
    for i, r in enumerate(robots):
        schedule = []

        r_tasks = r["individual_plan"]
        print('rt:', r_tasks)
        for t in r_tasks:
            schedule.append(task_dict[t])
        
        print('sch:', schedule)

        gnt.broken_barh(schedule, (yticks[i]-bar_height//2, bar_height), facecolors=(colors[i]))


    
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