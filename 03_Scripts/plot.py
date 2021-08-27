# plot.py

# --------------- #
# Import Packages #
# --------------- #
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Set seaborn as default plot config
sns.set()
sns.set_style("whitegrid")
from itertools import cycle

# ---------------------------------- #
# Define Subdirectories & Info Files #
# ---------------------------------- #
data_dir = '../01_Data/'
info_dir = '../02_Info/'
plot_dir = '../04_Charts/'
# Create plot dir if necessary
if not os.path.exists(plot_dir): os.makedirs(plot_dir)

# Read in channel list & create list of sensor groups
full_channel_list = pd.read_csv(f'{info_dir}channel_list.csv', index_col='Channel_Name')

# ------------------- #
# Set Plot Parameters #
# ------------------- #
label_size = 18
tick_size = 16
line_width = 2
event_font = 12
font_rotation = 60
legend_font = 12
fig_width = 10
fig_height = 8

# ---------------------- #
# User-Defined Functions #
# ---------------------- #
def timestamp_to_seconds(timestamp):
    timestamp = timestamp[11:]
    hh, mm, ss = timestamp.split(':')
    return(3600 * int(hh) + 60 * int(mm) + int(ss))

def convert_timestamps(timestamps, start_time):
    raw_seconds = map(timestamp_to_seconds, timestamps)
    return([s - start_time for s in list(raw_seconds)])

def create_1plot_fig():
    # Define figure for the plot
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    # Set line colors & markers; reset axis lims
    current_palette_8 = sns.color_palette('deep', 8)
    sns.set_palette(current_palette_8)

    plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v', '8', 'D', '*', '<', '>', 'H'])
    x_max, y_min, y_max = 0, 0, 0

    return(fig, ax1, plot_markers, x_max, y_min, y_max)

def format_and_save_plot(y_lims, x_lims, secondary_axis_label, file_loc):
    # Set tick parameters
    ax1.tick_params(labelsize=tick_size, length=0, width=0)

    # Scale axes limits & labels
    ax1.grid(True)
    ax1.set_ylim(bottom=y_lims[0], top=y_lims[1])
    ax1.set_xlim(x_lims[0] - x_lims[1] / 500, x_lims[1])
    ax1.set_xlabel('Time (s)', fontsize=label_size)

    # Secondary y-axis parameters
    if secondary_axis_label != 'None':
        ax2 = ax1.twinx()
        ax2.tick_params(labelsize=tick_size, length=0, width=0)
        ax2.set_ylabel(secondary_axis_label, fontsize=label_size)
        if secondary_axis_label == 'Temperature ($^\circ$F)':
            ax2.set_ylim([y_lims[0] * 1.8 + 32., y_lims[1] * 1.8 + 32.])
        else:
            ax2.set_ylim([secondary_axis_scale * y_lims[0], secondary_axis_scale * y_lims[1]])
        ax2.yaxis.grid(b=None)

    # Add vertical lines and labels for timing information (if available)
    ax3 = ax1.twiny()
    ax3.set_xlim(x_lims[0] - x_lims[1] / 500, x_lims[1])
    ax3.set_xticks([_x for _x in Events.index.values if _x >= x_lims[0] and _x <= x_lims[1]])
    ax3.tick_params(axis='x', width=1, labelrotation=font_rotation, labelsize=event_font)
    ax3.set_xticklabels([Events['Event'][_x] for _x in Events.index.values if _x >= x_lims[0] and _x <= x_lims[1]], fontsize=event_font, ha='left')
    ax3.xaxis.grid(b=None)

    # Add legend, clean up whitespace padding, save chart as pdf, & close fig
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(handles1, labels1, loc='best', fontsize=legend_font, handlelength=3, frameon=True, framealpha=0.75)

    fig.tight_layout()
    plt.savefig(file_loc)
    plt.close()

# ----------------- #
# Main Body of Code #
# ----------------- #
# Loop through test data files & create plots
for f in os.listdir(data_dir):
    # Skip if f is not a exp data file
    if any([not f.endswith('.csv'), f.startswith('.'), f.startswith('exp_'), f.endswith('_Events.csv')]):
        continue

    # Get test name from file & load data & event files for given experiment
    test_name = f[:-4]
    data_df = pd.read_csv(f'{data_dir}{f}', index_col='Time')
    Events = pd.read_csv(f'{data_dir}{test_name}_Events.csv')
    print (f'--- Loaded data for {test_name} ---')

    # Create index column of time relative to ignition in events file
    Events = pd.read_csv(f'{data_dir}{f[:-4]}_Events.csv')
    Events.rename(columns={'Time':'Timestamp'}, inplace=True)
    start_timestamp = Events.loc[0, 'Timestamp'][11:]
    hh,mm,ss = start_timestamp.split(':')
    start_time = 3600 * int(hh) + 60 * int(mm) + int(ss)
    Events['Time'] = convert_timestamps(Events['Timestamp'], start_time)
    Events = Events.set_index('Time')

    # Define channel list as full list & drop unused channels for given experiment
    channel_list = full_channel_list[[i in data_df.columns for i in full_channel_list.index]]

    # Loop through channel groups to plot data from all channels in each group
    for group in channel_list.groupby('Group').groups:
        # Create figure for plot
        print (f"  Plotting {group.replace('_',' ')}")
        fig, ax1, plot_markers, x_max, y_min, y_max = create_1plot_fig()

        # Loop through each channel in given group
        for channel in channel_list.groupby('Group').get_group(group).index.values:
            # Set secondary axis default to None, get data type from channel list
            secondary_axis_label = 'None'
            data_type = channel_list.loc[channel, 'Type']

            # Set plot parameters based on data type
            if data_type == 'Temperature':
                # Set y-axis labels & y_min
                ax1.set_ylabel('Temperature ($^\circ$C)', fontsize=label_size)
                secondary_axis_label = 'Temperature ($^\circ$F)'
                y_min = 0

            elif data_type == 'Velocity':
                # Set y-axis labels, secondary scale
                ax1.set_ylabel('Velocity (m/s)', fontsize=label_size)
                secondary_axis_label = 'Velocity (mph)'
                secondary_axis_scale = 2.23694

            elif data_type == 'Pressure':
                # Set y-axis label, secondary scale
                ax1.set_ylabel('Pressure (Pa)', fontsize=label_size)
                # secondary_axis_label = 'Pressure (psi)'
                # secondary_axis_scale = 0.000145038

            elif data_type == 'Oxygen':
                # Set y-axis label
                ax1.set_ylabel('O$_2$ Concentration (%)', fontsize=label_size)

            elif data_type.endswith('Heat Flux'):
                # Set y-axis label
                ax1.set_ylabel('Heat Flux (kW/m$^2$)', fontsize=label_size)

            # Determine x max bound for current data & update max of chart if necessary
            x_end = data_df[channel].index[-1]
            if x_end > x_max:
                x_max = x_end

            # Plot channel data
            ax1.plot(data_df.index, data_df[channel], lw=line_width,
                marker=next(plot_markers), markevery=30, mew=3, mec='none', ms=7, 
                label=channel_list.loc[channel, 'Label'])

            # Check if y min/max need to be updated
            if data_df[channel].min() - abs(data_df[channel].min() * .1) < y_min:
                y_min = data_df[channel].min() - abs(data_df[channel].min() * .1)

            if data_df[channel].max() * 1.1 > y_max:
                y_max = data_df[channel].max() * 1.1

        # Add vertical lines for event labels; label to y axis
        [ax1.axvline(_x, color='0.25', lw=1.5) for _x in Events.index.values if _x >= 0 and _x <= x_max]

        # Define/create save directory, call function to format & save plot
        save_dir = f'{plot_dir}{test_name}/'
        if not os.path.exists(save_dir): os.makedirs(save_dir)
        format_and_save_plot([y_min, y_max], [0, x_max], secondary_axis_label, f'{save_dir}{group}.pdf')

    print()