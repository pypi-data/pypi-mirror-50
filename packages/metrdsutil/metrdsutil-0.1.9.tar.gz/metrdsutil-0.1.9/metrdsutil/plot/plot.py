import matplotlib.pyplot as plt


def line_plot(df, columns="all", x="none", time_series=False, time_col="index"):
    """
	makes a lineplot out of a dataframe

	parameters:
	-----------
	df : pandas Dataframe
		the dataframe from which you want to make a line plot
	columns : list
		the columns you want to plot, defaults to all
	x : str
		which column is the x, not relevant for a time series
	time_series : boolean
		is a time series or not
	time_col : str
		if not the index, which column is the time
	"""
    # cutting down to columns to plot
    if columns == 'all':
        to_plot = df
    else:
        to_plot = df.loc[:,columns]
        
    # making a default x
    if x == "none":
        x = list(range(0,len(df)))
    else:
        x = df.loc[:,x]
    
    # making x time series
    if time_series:
        rotation = 70
    else:
        rotation = 0
        
    # plotting a time series
    if time_series and time_col != "index":
        x = df.loc[:,time_col]
    elif time_series and time_col == "index":
        x = df.index()

    for col in to_plot.columns:
        plt.plot(x, to_plot[col], label=col)
    plt.xticks(rotation=rotation)
    plt.legend()
