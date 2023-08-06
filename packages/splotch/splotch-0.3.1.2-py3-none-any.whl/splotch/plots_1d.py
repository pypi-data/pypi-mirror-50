#### Definition of all wrappers for 1D plotting

# Generalized lines
def axline(x=None,y=None,m=None,c=None,plabel=None,lab_loc=0,ax=None,plot_kw={},**kwargs):
	
	"""Generalised axis lines.
	
	This function aims to generalise the usage of axis lines calls (axvline/axhline) together and to allow
	lines to be specified by a slope/intercept.
	
	Parameters
	----------
	x : int or list, optional 
		x position(s) in data coordinates for a vertical line(s).
	y : int or list, optional
		y position(s) in data coordinates for a horizontal line(s).
	m : int or list, optional
		Slope(s) of diagonal axis line(s), defaults to 1 if not specified when c is given.
	c : int or list, optional
		Intercept points(s) of diagonal axis line(s), defaults to 0 if not specified when m is given.
	plabel : str, optional
		Sets label(s) for line(s) and plots legend.
	lab_loc : int, optional
		Defines the position of the legend. Defaults as lab_loc=0.
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	plot_kw : dict, optional
		Passes the given dictionary as a kwarg to the plotting function. Valid kwargs are Line2D properties.
	**kwargs: Line2D properties, optional
		kwargs are used to specify matplotlib specific properties such as linecolor, linewidth, antialiasing, etc.
		A list of available `Line2D` properties can be found here: 
		https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D

	Returns
	-------
	None
	"""
	   
	from matplotlib.pyplot import plot, legend, gca
	from .base_func import axes_handler,plot_finalizer,dict_splicer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	else:
		ax=gca()
		old_axes=ax        
	
	if (not any([x,y,m,c])): # If nothing has been specified
		raise TypeError("axline() missing one of optional arguments: 'x', 'y', 'm' or 'c'")
	    
	for i, val in enumerate([x,y,m,c]):
		if (val is not None):
			try: # Test whether the parameter is iterable
				temp=(k for k in val)
			except TypeError: # If not, convert to a list
				if   (i == 0): x = [x]
				elif (i == 1): y = [y]
				elif (i == 2): m = [m]
				elif (i == 3): c = [c]
	
	if (x is not None and y is not None): # Check whether both x and y were specified
		raise ValueError("'x' and 'y' cannot be both specified")
	
	if (x is not None): # Check conditions if x specified
		if (any([m,c])): # Should not specify m or c, if x given.
			raise ValueError("'{0}' cannot be specified if x specified".format('m' if m else 'c'))
		L = len(x)
	    
	if (y is not None): # Check conditions if y specified
		if (any([m,c])): # Should not specify m or c, if y given.
			raise ValueError("'{0}' cannot be specified if y specified".format('m' if m else 'c'))
		L = len(y)
	
	if (m is not None):
		if (c is None): # If no intercept specified
			c = [0]*len(m) # set c to 0 for all m
		else:
			if (len(c) == 1):
				c = [c[0]]*len(m)
			elif (len(c) != len(m)):
				if (len(m) == 1):
					m = [m[0]]*len(c)
				else:
					raise ValueError("Length of c ({0}) and length of m ({1}) must be equal or otherwise 1".format(len(c),len(m)))
		L = len(m)
	elif (c is not None):
		if (m is None): # If no slope specified
			m = [1]*len(c) # set m to 1 for all c
		L = len(c)
	
	if type(plabel) is not list:
		plabel=[plabel]*L
	elif (len(plabel) != L):
		raise ValueError("Length of plabel list ({0}) must match the number of lines given ({1}).".format(len(plabel),L))
	
	# Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
	#plot_par = {**plot_kw, **kwargs} # For Python > 3.5
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)

	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	plot_par = dict_splicer(plot_par,L,[1]*L)

	if (x is not None):
		for ii, xx in enumerate(x):
			ax.axvline(x=xx,**plot_par[ii],label=plabel[ii])
	if (y is not None):
		for ii, yy in enumerate(y):
			ax.axhline(y=yy,**plot_par[ii],label=plabel[ii])
	if (m is not None):
		for ii, pars in enumerate(zip(m,c)):
			mm = pars[0]; cc = pars[1]
			
			xLims = ax.get_xlim()
			yLims = ax.get_ylim()
			
			plot([xLims[0],xLims[1]],[mm*xLims[0]+cc,mm*xLims[1]+cc],label=plabel[ii],**plot_par[ii])
			
			ax.set_xlim(xLims)
			ax.set_ylim(yLims)
			
	if any(plabel):
		legend(loc=lab_loc)
	if ax is not None:
		old_axes=axes_handler(old_axes)

#Histogram
def hist(data,bin_type=None,bins=None,dens=True,scale=None,smooth=None,v=None,vstat=None,count_style={},xlim=None,ylim=None,
			xinvert=False,yinvert=False,xlog=False,ylog=None,title=None,xlabel=None,ylabel=None,plabel=None,lab_loc=0,
			ax=None,grid=None,plot_kw={},output=None):
	
	"""1D histogram function.
	
	The plotting is done with pyplot.plot(), so histograms are shown with interpolated curves instead of the
	more common stepwise curve. For this reason splotch.histstep is a better choice for small datasets. 
	
	Parameters
	----------
	data : array-like or list
		If list it is assumed that each elemement is array-like.
	bin_type : {'number','width','edges','equal'}, optional
		Defines how is understood the value given in bins: 'number' for givinf the desired number of bins, 'width' for
		the width of the bins, 'edges' for the edges of bins, and 'equal' for making bins with equal number of elements
		(or as close as possible). If not given it is inferred from the data type of bins: 'number' if int, 'width' if
		float and 'edges' if ndarray.
	bins : int, float, array-like or list, optional
		Gives the values for the bins, according to bin_type.
	dens :  bool or list, optional
		If false the histogram returns raw counts.
	scale : float or list, optional
		Scaling the counts.
	smooth : boolean, optional.
		If True the histogram is plotted with a line that connects between the value of each bin, positioned at the
		centre of the bins. Defaults to False, plotting with a stepped line, each step spanning the bin width.
	v : array-like or list, optional
		If a valid argument is given in cstat, defines the value used for the binned statistics.
	vstat : str, function  or list, optional
		Must be or contain one of the valid str arguments for the statistics variable in scipy.stats.binned_statistic
		('mean’, 'median’, 'count’, 'sum’, 'min’ or 'max’) or function(s) that takes a 1D array and outputs an integer
		 or float.
	count_style : dict, optional
		Defines a change of line style if number of counts in bins get under and/or over a given range. The key
		'low'/'high' is for setting the upper/lower limit of for the change of style. The key 'low_style'/'high_style'
		is used for setting the line style. If the style key is not given defaults to 'dotted' for 'low_style' and
		'dashed' for 'high_style', setting the intermidiate values to a 'solid' line style.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
	xinvert : bool or list, optional
		If true inverts the x-axis.
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_par : dict, optional
		Passes the given dictionary as a kwarg to the plotting function.
	output : boolean, optional
		If True, returns the edges and values of the histogram.
	
	Returns
	-------
	n : list
		List containing the arrays with the values for each histogram drawn. Only provided if output is True.
	bins_edges : list
		List containing the arrays with the bin edges for each of the histograms drawn. Only provided if output is True.
	"""
	
	from numpy import where, nan, inf, array, ones, sum, histogram
	from scipy.stats import binned_statistic
	from matplotlib.pyplot import plot, step, legend

	from .base_func import axes_handler,binned_axis,dict_splicer,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if type(data) is not list:
		data=[data]
	L=len(data)
	if type(bin_type) is not list:
		bin_type=[bin_type]*L
	if type(bins) is not list:
		if bins is not None:
			bins=[bins]*L
		else:
			bins=[int((len(d))**0.4) for d in data]
	if type(dens) is not list:
		dens=[dens]*L
	if type(scale) is not list:
		scale=[scale]*L
	if type(v) is not list:
		v=[v]*L
	if type(vstat) is not list:
		vstat=[vstat]*L
	if type(plabel) is not list:
		plabel=[plabel]*L
	if None in [ylog,smooth,output]:
		from .defaults import Params
		if ylog is None:
			ylog=Params.hist1D_yaxis_log
		if smooth is None:
			smooth=Params.hist1D_smooth
		if output is None:
			output=Params.hist1D_output
	if type(smooth) is not list:
		smooth=[smooth]*L
	plot_smooth={True:plot,False:step}
	plot_par=dict_splicer(plot_kw,L,[len(x) for x in data])
	bin_edges=[]
	n_return=[]
	for i in range(L):
		temp_data,bins_hist,bins_plot=binned_axis(data[i],bin_type[i],bins[i],log=xlog,plot_centre=smooth[i])
		if vstat[i]:
			temp_y=binned_statistic(temp_data,v[i],statistic=vstat[i],bins=bins_hist)[0]
		else:
			temp_y=histogram(temp_data,bins=bins_hist,density=dens[i])[0]
		if dens[i]:
			if scale[i]:
				temp_y*=1.0*len(data[i])/scale[i]
		if ylog:
			temp_y=where(temp_y==0,nan,temp_y)
		y=temp_y
		if not smooth[i]:
			y=array([y[0]]+[j for j in y])
		if count_style:
			if dens[i]:
				raw_counts=histogram(temp_data,bins=bins_hist,density=False)[0]
				raw_counts=array([raw_counts[0]]+[j for j in raw_counts])
			else:
				raw_counts=y
			if 'low' not in count_style.keys():
				count_style['low']=-inf
			if 'high' not in count_style.keys():
				count_style['high']=inf
			sel_low=raw_counts<count_style['low']
			sel_high=raw_counts>count_style['high']
			sel_mid=ones(len(raw_counts)).astype('bool')&~sel_low&~sel_high
			for j in range(len(raw_counts)-1):
				if not sel_low[j] and sel_low[j+1]:
					sel_low[j]=True
				if not sel_high[j] and sel_high[j+1]:
					sel_high[j]=True
			for j in range(1,len(raw_counts))[::-1]:
				if not sel_low[j] and sel_low[j-1]:
					sel_low[j]=True
				if not sel_high[j] and sel_high[j-1]:
					sel_high[j]=True
			if 'low_style' not in count_style.keys() and 'high_style' not in count_style.keys():
				plot_par[i]['linestyle']='solid'
			if 'low_style' not in count_style.keys():
				count_style['low_style']='dotted'
			if 'high_style' not in count_style.keys():
				count_style['high_style']='dashed'
			low_plot_par={k:plot_par[i][k] for k in plot_par[i].keys()}
			low_plot_par['linestyle']=count_style['low_style']
			high_plot_par={k:plot_par[i][k] for k in plot_par[i].keys()}
			high_plot_par['linestyle']=count_style['high_style']
			col=None
			if sum(sel_low)>0:
				low_plabel='n<'+str(count_style['low'])
				if plabel[i] is not None:
					low_plabel=plabel[i]+', '+low_plabel
				p=plot_smooth[smooth[i]](bins_plot,where(sel_low,y,nan),label=low_plabel,**low_plot_par)
				col=p[0].get_color()
			if sum(sel_high)>0:
				high_plabel='n>'+str(count_style['high'])
				if plabel[i] is not None:
					high_plabel=plabel[i]+', '+high_plabel
				if col is None:
					p=plot_smooth[smooth[i]](bins_plot,where(sel_high,y,nan),label=high_plabel,**high_plot_par)
					col=p[0].get_color()
				else:
					high_plot_par['color']=col
					plot_smooth[smooth[i]](bins_plot,where(sel_high,y,nan),label=high_plabel,**high_plot_par)
			if sum(sel_mid)>0:
				if col is not None:
					plot_par[i]['color']=col
				plot_smooth[smooth[i]](bins_plot,where(sel_mid,y,nan),label=plabel[i],**plot_par[i])
		else:
			plot_smooth[smooth[i]](bins_plot,y,label=plabel[i],**plot_par[i])
		bin_edges.append(bins_plot)
		n_return.append(temp_y)
	if any(plabel):
		legend(loc=lab_loc)
	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	if ax is not None:
		old_axes=axes_handler(old_axes)
	if output:
		return(n_return,bin_edges)

#Step histogram
def histstep(data,bin_num=None,dens=True,xlim=None,ylim=None,xinvert=False,yinvert=False,xlog=False,ylog=True,
			title=None,xlabel=None,ylabel=None,plabel=None,lab_loc=0,ax=None,grid=None,plot_kw={}):
	
	"""'Clasic' 1D histogram function.
	
	This function is designed around pyplot.hist(), so it lacks the functionality to use arbitraty y-axis
	normalisation of splotch.hist().
	It is better choice for small datasets, as it plots with stepwise curves, instead of the interpolated
	ones of splotch.hist().
	
	Parameters
	----------
	data : array-like or list
		If list it is assumed that each elemement is array-like.
	bin_num : int or list, optional
		Number of bins.
	dens :  bool or list, optional
		If false the histogram returns raw counts.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	xinvert : bool or list, optional
		If true inverts the x-axis.
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_par : dict, optional
		Passes the given dictionary as a kwarg to the plotting function.
	
	Returns
	-------
	None
	"""
	
	from matplotlib.pyplot import hist, legend
	from .base_func import axes_handler,dict_splicer,plot_finalizer
	
	if ax is not None:
		old_axes=axes_handler(ax)
	if type(data) is not list:
		data=[data]
	L=len(data)
	if bin_num is None:
		bin_num=[int((len(d))**0.4) for d in data]
	if type(bin_num) is not list:
		bin_num=[bin_num+1]*L
	if type(plabel) is not list:
		plabel=[plabel]*L
	plot_par=dict_splicer(plot_kw,L,[len(x) for x in data])
	for i in range(L):
		temp_data,bins,temp=binned_axis(data[i],bin_num[i],log=xlog)
		hist(temp_data,bins=bins,density=dens,label=plabel[i],**plot_par[i])
	if any(plabel):
		legend(loc=lab_loc)
	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	if ax is not None:
		old_axes=axes_handler(old_axes)

#Plots
def plot(x,y=None,xlim=None,ylim=None,xinvert=False,yinvert=False,xlog=False,ylog=False,title=None,xlabel=None,
			ylabel=None,plabel=None,lab_loc=0,ax=None,grid=None,plot_kw={},**kwargs):
	
	"""Base plotting function.
	
	This is a wrapper for pyplot.plot().
	
	Parameters
	----------
	x : array-like or list
		If list it is assumed that each elemement is array-like. If y is not given, the given values pass to y and a
		numpy array is generated with numpy.arange() for the x values.
	y : array-like or list, optional
		If list it is assumed that each elemement is array-like.
	xlim : tuple-like, optional
		Defines the limits of the x-axis, it must contain two elements (lower and higer limits).
	ylim : tuple-like, optional
		Defines the limits of the y-axis, it must contain two elements (lower and higer limits).
	xinvert : bool or list, optional
		If true inverts the x-axis.
	yinvert : bool or list, optional
		If true inverts the y-axis.
	xlog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	ylog : bool or list, optional
		If True the scale of the x-axis is logarithmic.
	title : str, optional
		Sets the title of the plot
	xlabel : str, optional
		Sets the label of the x-axis.
	ylabel : str, optional
		Sets the label of the y-axis.
	plabel : str, optional
		Sets the legend for the plot.
	lab_loc : int, optional
		Defines the position of the legend
	ax : pyplot.Axes, optional
		Use the given axes to make the plot, defaults to the current axes.
	grid : boolean, optional
		If not given defaults to the value defined in splotch.Params.
	plot_kw : dict, optional
		Passes the given dictionary as a kwarg to the plotting function. Valid kwargs are Line2D properties.
	**kwargs: Line2D properties, optional
		kwargs are used to specify matplotlib specific properties such as linecolor, linewidth, antialiasing, etc.
		A list of available `Line2D` properties can be found here: 
		https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D
	
	Returns
	-------
	None
	"""

	from numpy import shape, arange
	from matplotlib.pyplot import plot, legend
	from .base_func import axes_handler,dict_splicer,plot_finalizer
	

	if ax is not None:
		old_axes=axes_handler(ax)
	if type(x) is not list or len(shape(x))==1:
		x=[x]
	L=len(x)
	if y is None:
		y=x
		x=[arange(len(x[i])) for i in range(L)]
	else:
		if type(y) is not list or len(shape(y))==1:
			y=[y]
	if type(plabel) is not list:
		plabel=[plabel]*L
	
	# Combine the `explicit` plot_kw dictionary with the `implicit` **kwargs dictionary
	#plot_par = {**plot_kw, **kwargs} # For Python > 3.5
	plot_par = plot_kw.copy()
	plot_par.update(kwargs)

	# Create 'L' number of plot kwarg dictionaries to parse into each plot call
	plot_par = dict_splicer(plot_par,L,[1]*L)

	for i in range(L):
		plot(x[i],y[i],label=plabel[i],**plot_par[i])
	if any(plabel):
		legend(loc=lab_loc)
	plot_finalizer(xlog,ylog,xlim,ylim,title,xlabel,ylabel,xinvert,yinvert,grid)
	if ax is not None:
		old_axes=axes_handler(old_axes)

