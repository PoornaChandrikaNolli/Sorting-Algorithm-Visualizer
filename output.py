import random
import os
import sys
import re
from matplotlib import pyplot as plt
from matplotlib import animation
from sorting.data import Data
from sorting.quicksort import quick_sort

# Dictionary for sorting type with only Quick Sort
stype_dic = {'quick-sort': 0}
titles = [r'Quick Sort ($O(n \cdot log_2(n))$)']
funs = [quick_sort]

def create_original_data(dtype):
    data = []
    if dtype == 'random':
        data = list(range(1, Data.data_count + 1))
        random.shuffle(data)
    elif dtype == 'reversed':
        data = list(range(Data.data_count, 0, -1))
    elif dtype == 'few-unique':
        d = Data.data_count // 4
        for i in range(0, d):
            data.append(d)
        for i in range(d, d*2):
            data.append(d*2)
        for i in range(d*2, d*3):
            data.append(d*3)
        for i in range(d*3, Data.data_count):
            data.append(Data.data_count)
        random.shuffle(data)
    elif dtype == 'almost-sorted':
        data = list(range(1, Data.data_count + 1))
        a = random.randint(0, Data.data_count - 1)
        b = random.randint(0, Data.data_count - 1)
        while a == b:
            b = random.randint(0, Data.data_count - 1)
        data[a], data[b] = data[b], data[a]
    return data

def draw_chart(stype, original_data, frame_interval):
    # Set up the figure, axis, and plot elements
    fig = plt.figure(1, figsize=(16, 9))
    data_set = [Data(d) for d in original_data]
    axs = fig.add_subplot(111)
    axs.set_xticks([])
    axs.set_yticks([])
    plt.subplots_adjust(left=0.01, bottom=0.02, right=0.99, top=0.95,
                        wspace=0.05, hspace=0.15)
    
    # Get the data of all frames
    frames = funs[stype](data_set)
    print('%s: %d frames.' % (titles[stype], len(frames)))

    # Animation function
    def animate(fi):
        bars = []
        if(len(frames) > fi):
            axs.cla()
            axs.set_title(titles[stype])
            axs.set_xticks([])
            axs.set_yticks([])
            bars += axs.bar(list(range(Data.data_count)),        # X
                            [d.value for d in frames[fi]],       # data
                            1,                                   # width
                            color=[d.color for d in frames[fi]]  # color
                            ).get_children()
        return bars

    # Call the animator
    anim = animation.FuncAnimation(fig, animate, frames=len(frames), interval=frame_interval)
    return plt, anim

def draw_all_charts(original_data, frame_interval):
    # Set up the figure, axis, and plot elements
    axs = []
    frames = []
    fig = plt.figure(1, figsize=(16, 9))
    data_set = [Data(d) for d in original_data]
    axs.append(fig.add_subplot(111))
    axs[-1].set_xticks([])
    axs[-1].set_yticks([])
    plt.subplots_adjust(left=0.01, bottom=0.02, right=0.99, top=0.95,
                        wspace=0.05, hspace=0.15)

    # Get the data of all frames
    frames.append(funs[0](data_set))

    # Output the frame counts
    print('%s: %d frames' % (titles[0], len(frames[0])))

    # Animation function
    def animate(fi):
        bars = []
        if(len(frames[0]) > fi):
            axs[0].cla()
            axs[0].set_title(titles[0])
            axs[0].set_xticks([])
            axs[0].set_yticks([])
            bars += axs[0].bar(list(range(Data.data_count)),           # X
                               [d.value for d in frames[0][fi]],       # data
                               1,                                      # width
                               color=[d.color for d in frames[0][fi]]  # color
                               ).get_children()
        return bars

    # Call the animator
    anim = animation.FuncAnimation(fig, animate, frames=max(len(f) for f in frames), interval=frame_interval)
    return plt, anim

if __name__ == "__main__":
    try:
        Data.data_count = int(input('Please set the number of items to be sorted(32): '))
    except:
        Data.data_count = 32
    if len(sys.argv) > 1:
        # Type of sort algorithm
        stype = -1
        if len(sys.argv) > 2:
            if sys.argv[2] in stype_dic:
                stype = stype_dic[sys.argv[2]]
            else:
                print('Error: Wrong argument!')
                exit()
        stype_str = list(stype_dic.keys())[list(stype_dic.values()).index(stype)]

        # Type of original data
        dtype = 'random'
        if len(sys.argv) > 3:
            dtype = sys.argv[3]
            if dtype not in ('random', 'reversed', 'few-unique', 'almost-sorted'):
                print('Error: Wrong argument!')
                exit()
        od = create_original_data(dtype)

        if sys.argv[1] == 'play':
            try:
                fi = int(input('Please set the frame interval(100): '))
            except:
                fi = 100
            plt, _ = draw_chart(stype, od, fi)
            plt.show()
        elif sys.argv[1] == 'save-mp4':
            default_fn = stype_str + '-' + dtype + '-animation'
            fn = input('Please input a filename(%s): ' % default_fn)
            if fn == '':
                fn = default_fn
            try:
                fps = int(input('Please set the fps(25): '))
            except:
                fps = 25
            _, anim = draw_chart(stype, od, 100)
            print('Please wait...')
            anim.save(fn + '.mp4', writer=animation.FFMpegWriter(fps=fps, extra_args=['-vcodec', 'libx264']))
            print('The file has been successfully saved in %s' % os.path.abspath(fn + '.mp4'))
        elif sys.argv[1] == 'save-html':
            default_fn = stype_str + '-' + dtype + '-animation'
            fn = input('Please input a filename(%s): ' % default_fn)
            if fn == '':
                fn = default_fn
            try:
                fps = int(input('Please set the fps(25): '))
            except:
                fps = 25
            _, anim = draw_chart(stype, od, 100)
            print('Please wait...')
            anim.save(fn + '.html', writer=animation.HTMLWriter(fps=fps))
            print('The file has been successfully saved in %s' % os.path.abspath(fn + '.html'))
