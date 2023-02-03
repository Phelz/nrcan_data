
from dataclasses import dataclass, field

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from classes import DataFile
from utils import load_object

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch


@dataclass
class DataOrganizer:
    
    year: int
    
    frequencies: list[float] = field( default_factory= lambda: [ 5.382, 6.9285, 8.0995, 10.422, 11.107, 14.3644 ])
    colors: tuple = ("#F8EDD8", "#EEC069")
    
    
    def __post_init__(self):
        
        self.data_dic = {}
        
        for freq in self.frequencies:
            q, r = divmod(freq, 1)
            self.data_dic[freq] = load_object("data\\%4d\\%4d_%dp%.4d.dat" % ( self.year, self.year, q, np.round(r,5)*1e4))
            
        
        self.time_keeper = {}
        
    def sort_data_availability(self, freq):
        
        data_files = self.data_dic[freq]
        
        time_list = [data_file.date_time for data_file in data_files]
        fill_time_list = pd.date_range(time_list[0], time_list[-1]).to_pydatetime()

        time_keeper = [time_list[0]]
        odd_days = []
        for indx, time, in enumerate(time_list):
            
            time_ahead = time_list[indx + 1] if indx < len(time_list) -1 else time
            time_before = time_list[indx - 1] if indx > 0 else time
            
            ahead = time_ahead - time >= timedelta(days=2)
            before = time - time_before >= timedelta(days=2)
            
            if ahead and before:
                odd_days.append(time)
            
            elif ahead or before:
                time_keeper.append(time)

        else: time_keeper.append(time_list[-1])

        time_diff_there = np.subtract( time_keeper[1::2], time_keeper[::2] )
        time_diff_notthere = np.subtract( time_keeper[::2][1:], time_keeper[1::2][:-1] )

        self.time_keeper[freq] = time_keeper, odd_days, time_diff_there.sum() + timedelta(days=len(odd_days))

        return time_list, time_keeper, time_diff_there, time_diff_notthere, odd_days

    def plot_data_availability(self, freq, time_list, time_keeper, time_diff_there, time_diff_notthere, odd_days, ax, legend=False):
        

        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=np.arange(1, 13, 1)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=[0, 7, 14, 21, 28]))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d"))

        ax.xaxis.set_tick_params(which="minor", labelsize="20", length=7, labelcolor="gray", rotation=0, top=False, direction='out' )
        ax.xaxis.set_tick_params(which="major", labelsize="20", length=7, labelcolor="k", rotation=30 , pad=20, top=False, direction='out')

        for time in time_keeper:
            ax.annotate( time.day, (time - timedelta(hours=12), 1.05), fontsize=15, color = "gray",  xycoords='data', xytext=(1, 1), textcoords="offset points", annotation_clip=False, zorder=13, transform=ax.transData)

        for odd_time in odd_days:
            ax.annotate( odd_time.day, (odd_time - timedelta(hours=6), 1.05), fontsize=13, color = "gray", textcoords='data',  annotation_clip=False, zorder=13)


        ax.broken_barh([ (start, diff) for start, diff in zip(time_keeper[::2], time_diff_there) ], (0, 1), facecolors=self.colors[-1], zorder=9)
        ax.broken_barh([ (start, timedelta(days=1)) for start in odd_days ], (0, 1), facecolors=self.colors[-1], zorder=9)
        
        ax.broken_barh([ (start, diff) for start, diff in zip(time_keeper[1::2], time_diff_notthere) ], (0, 1), facecolors=self.colors[0], alpha=0.5, zorder=9)

        ax.plot(time_keeper, np.zeros_like(time_keeper), marker="D", color="k", markerfacecolor="w", markersize=5, zorder=13)  
        ax.vlines(time_keeper, 0, 1, color="k",zorder=12)

        ax.set_xlim(time_list[0], time_list[-1])

        ax.spines[["left", "top", "right"]].set_visible(False)

        ax.set_yticks([])
        ax.set_ylabel(  "%.4f MHz" % (freq), fontsize=15 )
        ax.margins(y=0)
        
        ax.grid(False, which='both')
        
        if legend:
            legend_elements = [ Patch(facecolor=color, edgecolor='k', label=label) for color, label in zip(self.colors, ["Not Available", "Available"]) ]
            ax.legend(handles=legend_elements,  prop={'size': 12},  bbox_to_anchor=(1, 2.1 ), fancybox=True, shadow=True)
        
    
    def show_data_availability(self):
        fig, axs = plt.subplots(len(self.frequencies), 1, figsize=(15, len(self.frequencies)*1.5), constrained_layout=True, sharex=True)
        
        for i, (freq, ax) in enumerate( zip(self.frequencies, axs) ):
            
            
            time_list, time_keeper, time_diff_there, time_diff_notthere, odd_days = self.sort_data_availability( freq )
            self.plot_data_availability(freq, time_list, time_keeper, time_diff_there, time_diff_notthere, odd_days, ax, legend=True if i==0 else False )

        fig.suptitle("Data Availability %s" % (self.year), va="top", x=0.5, y=1)
        
        return fig, axs
    
    def find_freq_max_days(self):
        
        if self.time_keeper == {}:
            self.show_data_availability()
        
        return  max(self.time_keeper, key=lambda k:self.time_keeper[k][-1])
        