# https://www.jianshu.com/p/88238e34c689
# https://littleround.cn/2019/01/04/Python%E5%88%B6%E4%BD%9C%E5%8A%A8%E6%80%81%E5%9B%BE-matplotlib.animation/

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

'''
log tuple:
    
    (CPU, Addr, Size, OP_TYPE, BIG)
           ↑
        Order by
        
    @ CPU: CPU id
    @ Addr: MALLOC start addr
    @ Size: MALLOC size
    @ OP_TYPE: MALLOC / FREE / MALLOC_PAGE / FREE_PAGE / MALLOC_BIGMEM / FREE_BIGMEM
    @ BIG: bool, if true, means a PAGE / BIGMEM op

'''

# c type enum def
MALLOC = 0
FREE = 1
MALLOC_PAGE = 2
FREE_PAGE = 3
MALLOC_BIGMEM = 4
FREE_BIGMEM = 5

mem_usage_list = []
# TODO: find a data structure

mem_start = 0
mem_end = 0x10000000
ncpu = 4

# now constuct the AxesSubplot objects (in a line)
fig, axs = plt.subplots(ncpu + 1, 1)

def log_parse():
    # read from pipe
    # (CPU, Addr, Size, OP_TYPE, BIG)
    # TODO: parse ...
    mem_usage_list.append([0, 0, 0x1000000, 0, True])

# # clear the scene
def plot_init():
    for i in range(ncpu + 1):
        axs[i].clear()
        axs[i].set_xlim([mem_start, mem_end])
        axs[i].set_ylim([0, 1])
        axs[i].yaxis.set_ticks([])
        axs[i].xaxis.set_ticks([])
        # axs[i].xaxis.set_ticks([mem_start, mem_end])
        # axs[i].xaxis.set_major_formatter(ticker.FormatStrFormatter("0x%x"))
    fig.suptitle('Memory Usage Graph')
    


# read the pre-constructed numpy data
def update(n):
    # clear graph before draw
    for i in range(ncpu + 1):
        axs[i].clear()
        axs[i].set_xlim([mem_start, mem_end])
        axs[i].set_ylim([0, 1])
        axs[i].yaxis.set_ticks([])
        axs[i].xaxis.set_ticks([])
    # for i in range(ncpu+1):
    #     axs[i].clear()
    for [CPU, Addr, Size, OP_TYPE, isBIG] in mem_usage_list:
        assert(mem_start <= Addr <= mem_end)
        assert(mem_start <= Addr + Size <= mem_end)
        rect = patches.Rectangle((Addr, 0), Size, 1, facecolor='orange')
        axs[CPU+1].add_patch(rect)
        if isBIG == True:
            rect = patches.Rectangle((Addr, 0), Size, 1, facecolor='orange')
            axs[0].add_patch(rect)
    # # dynamic draw test.
    # if n==2:
    #     mem_usage_list.append([0, 0x3000000, 0x1000000, 0, True])
    # if n==3:
    #     mem_usage_list.pop(0)
    


if __name__ == '__main__':
    plot_init()
    log_parse()
    ani = FuncAnimation(fig, update, interval=10, save_count=100)

    # live show
    plt.show()

