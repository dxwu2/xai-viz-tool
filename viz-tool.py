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

def random_colors(n):
    colors = []
    for i in range(n):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        # Set alpha value to 50% (0x80 in hex)
        alpha = 0x80

        # Combine RGB and alpha values into a single integer
        color = (alpha << 24) + (red << 16) + (green << 8) + blue

        # Convert integer to hex format and remove the leading '0x'
        hex_color = hex(color)[2:]

        # Pad with zeros if necessary to ensure a six-digit hex code
        hex_color = hex_color.zfill(6)

        s = '#' + hex_color
        colors.append(s)
    return colors

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
    robot_names = get_robot_names(robots)
    # gnt.set_yticklabels(robot_names)
    
    # Setting graph attribute
    gnt.grid(True)

    # draw bars
    bar_height = 9
    # number_of_colors = len(robots)
    # colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            #  for i in range(number_of_colors)]
    colors = random_colors(len(robots))
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
    
    plt.show()

def __main__():
    task_dict = {}
    sol = parse()
    graph(sol)

__main__()