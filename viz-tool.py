import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import json
import sys
import random

def parse():
    configs = []
    sols = []
    for i in range(1, len(sys.argv)):
        f = open(sys.argv[1])
        configs.append(json.load(f))
        f.close()

        f_sol = open(sys.argv[1][:-5] + '_output.json')
        sols.append(json.load(f_sol)["solution"])
        f_sol.close()

    return configs, sols

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
        while True:
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            # prevent white
            if red+green+blue > 40:
                break

        # Set alpha value to 50% (0x80 in hex)
        alpha = 0xe0

        # Combine RGB and alpha values into a single integer
        color = (alpha << 24) + (red << 16) + (green << 8) + blue

        # Convert integer to hex format and remove the leading '0x'
        hex_color = hex(color)[2:]

        # Pad with zeros if necessary to ensure a six-digit hex code
        hex_color = hex_color.zfill(6)

        s = '#' + hex_color
        colors.append(s)
    return colors

def generate_explanation(i):
    if i == 0:
        return "Robot closest to starting location of task"
    elif i == 1:
        return "Only robot that is available for this task"
    elif i == 2:
        return "Only robot that is available for this task"
    elif i == 3:
        return "Only robot with the required traits for this task"
    elif i == 4: 
        return "Only robot that is available for this task"

def graph(sol):
    for s_i, s in enumerate(sol):
        robots = s["robots"]
        task_dict = extract_task_times(s["tasks"])

        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        annot_boxes = [] # list of [x_lo, x_hi, y_lo, y_hi]
        def get_annot_boxes(schedule, vert_len):
            if len(schedule) > 0:
                for start, dur in schedule:
                    annot_boxes.append([start, start+dur, vert_len[0], sum(vert_len)])

        def create_annots(annot_boxes):
            annots = []
            for i in range(len(annot_boxes)):
                text = generate_explanation(i)
                annots.append(gnt.annotate(text, xy=(0,0), xytext=(20,20),textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"),
                arrowprops=dict(arrowstyle="->")))
                annots[i].set_visible(False)
            return annots # list of annots

        # returns annot if in box, otherwise returns None
        def in_box(x, y):
            for i in range(len(annot_boxes)):
                if x >= annot_boxes[i][0] and x <= annot_boxes[i][1] and y >= annot_boxes[i][2] and y <= annot_boxes[i][3]:
                    return annots[i]
            return None

        '''
        def update_annot(ind):
            pos = sc.get_offsets()[ind["ind"][0]]
            annot.xy = pos
            # text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
            #                     " ".join([names[n] for n in ind["ind"]]))
            text = "ashdhssssf"
            annot.set_text(text)
            annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
            annot.get_bbox_patch().set_alpha(0.4)
        '''

        def hover(event):
            if event.inaxes == gnt:
                x, y = event.xdata, event.ydata
                if in_box(x, y) is not None:
                    in_box(x,y).xy = (x, y)
                    in_box(x,y).set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    for ann in annots:
                        ann.set_visible(False)
        
        # Setting Y-axis limits
        y_max = 60
        gnt.set_ylim(0, y_max)
        
        # Setting X-axis limits
        x_max = s["makespan"]
        gnt.set_xlim(0, x_max)
        
        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('time')
        gnt.set_ylabel('agent')

        # Setting ticks on y-axis
        yticks = range(y_max//(1+len(robots)), y_max, y_max//(1+len(robots)))[:len(robots)]
        gnt.set_yticks(yticks)
        # Labelling tickes of y-axis
        robot_names = get_robot_names(robots)
        
        # Setting graph attribute
        gnt.grid(True)

        # draw bars
        bar_height = 9
        colors = random_colors(len(robots))
        for i, r in enumerate(robots):
            schedule = []

            r_tasks = r["individual_plan"]
            for t in r_tasks:
                schedule.append(task_dict[t])
            vert_len = (yticks[i]-bar_height//2, bar_height)

            gnt.broken_barh(schedule, vert_len, facecolors=(colors[i]))
            get_annot_boxes(schedule, vert_len)

        annots = create_annots(annot_boxes)

        # Legend
        l_dict = {}
        for i in range(len(robot_names)):
            l_dict[robot_names[i]] = colors[i]
        legend_elements = [Patch(facecolor=l_dict[i], label=i) for i in l_dict]
        plt.legend(handles=legend_elements)

        plt.title(sys.argv[s_i+1])
    
    cid = fig.canvas.mpl_connect('motion_notify_event', hover)
    plt.show()

def __main__():
    task_dict = {}
    configs, sol = parse()
    graph(sol)

__main__()