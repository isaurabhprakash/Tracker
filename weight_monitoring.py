import xlrd
import numpy as np
import matplotlib.pyplot as graph

# Location of the file
loc = ("weight_monitoring.xlsx")

# Open the workbook
workbook = xlrd.open_workbook(loc)
current_sheet = workbook.sheet_by_index(0)

## Get the dates on which weight has been recorded in a list
day_list = current_sheet.col_values(0)
day_list = day_list[1:]   ## Remove the top cell value 'Date'

## Get the recorded weights
weight_list = current_sheet.col_values(1)
weight_list = weight_list[1:] ##Remove the top cell value 'Weight'

## Get the value we got for the starting date
    # xlrd returns date after converting them into floats
    # which are difficult to interpret. Also, we are concerned with
    # the number of days rather than the date itself.
first_day = int(day_list[0]) 

convert_to_day = lambda x : int(x) - first_day

## After this, we will have the days.
day_list = list(map(convert_to_day,day_list))

## Now let's start with the graph
graph.xlabel("Days")
graph.ylabel("Weight (in Kg)")
graph.title("Weight Monitoring")
graph.xticks(np.arange(min(day_list), max(day_list)+1, 3.0))


graph.plot(day_list,weight_list, color = 'orange', marker = 'o',
           markerfacecolor = 'red')

graph.show()

