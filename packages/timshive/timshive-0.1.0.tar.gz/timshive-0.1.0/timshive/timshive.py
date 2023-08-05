import matplotlib as mp
mp.use('pdf')
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import math
import numpy as np

"""
INFO
----------------------------------------------------------------------------------------------
Module for creating simple hive plots from multidimensional arrays using matplotlib and numpy.
Made By TimC July 2019
----------------------------------------------------------------------------------------------

INPUTS
----------------------------------------------------------------------------------------------
 points: a two dimensional list where the first dimension represents each axis you wish to
 draw and the second represents the points on each axes. eg. to plot a hive with three axes
 each containing points 2 and 3, you would use [[2,3],[2,3],[2,3]] as the input value for
 points

 colors: one dimensional list of all colors that corresponds to the first, second third, point
 in each list. Using the last example, if ['green','red'] was entered in the color field given
 teh same points input, all of the twos would show up as greeb and the threes as red. If the
 length of any axiss exceeds the length of colors, all points will be filled in as black

 **range: this gives the value to which the axes should be drawn. Assumed to round up to the
 nearset 10 unless another value is given

 **labels: used to give the text associated with each color if a key is desired. Entering
 labels = ['Set 1','Set 2'] for the previous example would produce a key in which green is
 labeled as 'Set 1' and red is labeled as 'Set 2'

 **axlab: the label given to each axis. If string, will be applied in order as string 1 , string
 etc. if it is a list, each item in the list will be used in order. if not enough conditions are
 given, axes will be unlabeled
 ----------------------------------------------------------------------------------------------
"""


class hive(object):
    def __init__(self,points,colors,range = None,labels = None,axlab = 'Condition'):
        self.points = points #raw inputs for the points in terms of their value
        self.slew = [] #all points unordered
        for each in self.points:
            for every in each:
                self.slew.append(every)
        self.axlab = axlab

        self.axes = len(points)#numebr of axes in the plot
        self.colors = colors#list of colors
        self.labels = labels#list of labels

        self.theta = 2*math.pi/self.axes#angle of each axis about each otehr

        if range == None:
            self.range = max(self.slew) -(max(self.slew) % 10) + 10
        else:
            self.range = range #length of each axis
        self.get_axlab()
        self.colfill()
#####functions called throughout#####
    def radplot(self,num,pos):
        return [num*math.cos(math.radians(90)-self.theta*pos),num*math.sin(math.radians(90)-self.theta*pos)] #given a value and axis it is on, return the x,y coordinate in list form

    def contplot(self,numsin,bounds,n):
        out = [[],[]]
        ils = np.linspace(self.theta*bounds[0],self.theta*bounds[1],n)
        nums = np.linspace(numsin[0],numsin[1],n)
        for i in range(len(ils)):
            out[0].append(nums[i]*math.cos(math.radians(90)-ils[i]))
            out[1].append(nums[i]*math.sin(math.radians(90)-ils[i]))
        return out #given a range of value inputs and range of positions, output an x and y array for n points in between. The points will "create" a line from one value,position to the other.

    def minlen(self,list):
        lens = []
        for each in list:
            lens.append(len(each))
        return min(lens) #calculate the minimum length from a list
##########################################

#####Functions called in self.show()#####
    def get_axlab(self):
        if isinstance(self.axlab,str):
            ph_axlab = []
            for i in range(self.axes):
                ph_axlab.append(str(self.axlab)+' '+str(i+1))
            self.axlab = ph_axlab #convert single key to numbered list of axis labels
        else:
            n = self.axes-len(self.axlab)
            for i in range(n):
                self.axlab.append('')#add blanks for axes not filled by list of labels

    def colfill(self):
        lens = []
        for each in self.points:
            lens.append(len(each))
        n = max(lens)-len(self.colors) #find how many open color slots there are
        if n > 0:
            for i in range(n):
                self.colors.append('black')#this fills all slots of color with black if they are unfilled to avoid index errors

    def ax_config(self):
        self.axls = []
        for i in range(self.axes):
            self.axls.append(self.radplot(self.range,i)) #use radplot to find all of the points for making the axes

    def pt_config(self):
        self.oldpoints = self.points
        self.points = []
        for i in range(self.axes):
            ax = []
            for each in self.oldpoints[i]:
                ax.append(self.radplot(each,i))
            self.points.append(ax) #use radplot to find all of the points that each piece of data should go at

    def lab_config(self):
        if self.labels == None:
            self.label_on = False
        else:
            self.label_on = True
            self.lab_handles = []
            for i in range(self.minlen([self.labels,self.colors])):
                self.lab_handles.append(pat.Patch(color = self.colors[i],label = self.labels[i])) # make the handler list for the key that we craete later

    def make_fig(self,title):
        self.fig,self.ax = plt.subplots() #create the matplotlib figure and add in the title
        self.fig.suptitle(title)

    def show_ax(self):
        i = 0
        for each in self.axls:
            self.ax.plot([0,each[0]],[0,each[1]],color = 'black')
            self.ax.text(each[0]*1.01,each[1]*1.05,self.axlab[i],horizontalalignment='center', verticalalignment='center',fontsize = 8)
            i+=1#plot the lines for each axes and add their labels to matplotlib Axes

    def show_pt(self):
        for i in range(self.axes):
            for j in range(len(self.points[i])):
                each = self.points[i][j]
                self.ax.plot([each[0]],[each[1]],color = self.colors[j],marker = '.', lw = 0) #show all of the points in the matplotlib Axes

    def show_hives(self):
        for j in range(self.minlen(self.points)):
            for i in range(self.axes):
                next = i+1
                val2 = next
                if i == self.axes-1:
                    next = 0
                out = self.contplot([self.oldpoints[i][j],self.oldpoints[next][j]],[i,val2],500)
                self.ax.plot(out[0],out[1],color = self.colors[j], lw = 0.5) #OOOOOOO fun one. this uses that continous ploting function to make the lines inbetween each point n = 500

    def show_lab(self):
        self.fig.legend(handles=self.lab_handles, loc = 1) #add legend to matplotlib Figure

    def show(self,title,name):
        '''
        HERE WE GO! This is the only function you should ever have to call with the hive. This
        is basically just the final execution for all of those nice functions we made earlier
        As inputs give it the string of the title of the graph and then the name of the file
        you want to put your output into.
        '''

        self.ax_config()
        self.pt_config()
        self.lab_config()
        self.make_fig(title)
        self.show_ax()
        self.show_pt()
        self.show_hives()
        if self.label_on == True:
            self.show_lab()

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)
        self.ax.axis('scaled')
        self.fig.savefig(name+'.pdf')
