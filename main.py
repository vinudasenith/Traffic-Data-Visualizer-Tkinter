# Author:H.A.V Senith
# Date:25/11/2024

#Task A: Input Validation

def validate_data_input():

    '''
    Prompts the user for a date,format in DD MM YYYY,
    check the day,month,year are valid and within the specified range
    '''

    while True:
        #validate date
        try:
            day=int(input("Please enter the day of the survey in the format DD:"))
            #checking the date is in between valid range(1-31)
            if not (1<=day<=31):
                print("Out of range-value must be in the range 1 and 31")
                continue
            break # exit loop if day is valid
        except ValueError:
            print("Integer required")#error message if input is not an integer

    #validate month
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM:"))
            # checking the month is in between valid range(1-12)
            if not (1 <= month <= 12):
                print("Out of range-value must be in the range 1 and 12")
                continue
            break # exit loop if month is valid
        except ValueError:
            print("Integer required") #error message if input is not an integer

   #validate year
    while True:
        try:
            year=int(input("Please enter the year of the survey in the format YYYY:"))
            # checking the year is in between valid range(2000-2024)
            if not (2000<=year<=2024):
                print("Out of range-value must be in the range 2000 and 2024")
                continue
            break # exit loop if year is valid
        except ValueError:
            print("Integer required") #error message if input is not an integer

    return day,month,year

def vaildate_continue_input():
    '''
    Prompts the user asking to load another dataset:
    'Y' for yes and 'N' for no
    '''

    while True:
        #asking from user if they want to load another data set
        choice=input("Do you want to load another data set,'Y' to yes or'N'to no?(Y/N):").strip().upper()
        #checking input is 'Y' or 'N'
        if choice in['Y','N']:
            return choice #return user choice
        print("Invalid input.Please enter 'Y' to continue or 'N' to quit.")

#Task B: Processed Outcomes
def process_csv_data(file_path):
    '''
    Read and process the csv file which containing traffic data
    '''

    import csv
    from datetime import datetime

    try:
        # open the file
        with open(file_path,'r') as file:
            #read the file using csv.DictReader
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        print(f"Error:The file'{file_path}' does not exist.Please check the date input or file path.")
        return None


    #initialize variables
    total_vehicles=0
    total_trucks=0
    total_electric_vehicles=0
    two_wheeled_vehicles=0
    busses_north=0
    vehicles_straight=0
    total_bicycles=0
    over_speed_limit=0
    vehicles_elm_avenue=0
    vehicles_hanley_highway=0
    scooters_elm=0
    hour_dict = {}
    rain_hours = set()

    #Process each row in dataset
    for row in data:
        #count total vehicles
        total_vehicles+=1

    for row in data:
        #count trucks
        if row['VehicleType']=='Truck':
            total_trucks+=1

    for row in data:
        #Count electric vehicles
        if row['elctricHybrid'] == 'True':
            total_electric_vehicles += 1

    for row in data:
        #count two-wheeled vehicles(Bicycle,Motorcycle,Scooter)
        if row['VehicleType'] == 'Bicycle':
            two_wheeled_vehicles += 1
        if row['VehicleType'] == 'Motorcycle':
            two_wheeled_vehicles += 1
        if row['VehicleType'] == 'Scooter':
            two_wheeled_vehicles += 1

    for row in data:
        #count busses leaving Elm Avenue/Rabbit Road junction heading north
        if row['JunctionName']== 'Elm Avenue/Rabbit Road' and row['travel_Direction_out']=='N'and row['VehicleType']=='Buss':
            busses_north+=1

    for row in data:
        #Vehicles moving straight
        if (
                (row['travel_Direction_in']=='N' and row['travel_Direction_out']=='N')or
                (row['travel_Direction_in'] == 'S' and row['travel_Direction_out'] == 'S') or
                (row['travel_Direction_in'] == 'W' and row['travel_Direction_out'] == 'W') or
                (row['travel_Direction_in'] == 'E' and row['travel_Direction_out'] == 'E') or
                (row['travel_Direction_in'] == 'NE' and row['travel_Direction_out'] == 'NE') or
                (row['travel_Direction_in'] == 'NW' and row['travel_Direction_out'] == 'NW') or
                (row['travel_Direction_in'] == 'SE' and row['travel_Direction_out'] == 'SE') or
                (row['travel_Direction_in'] == 'SW' and row['travel_Direction_out'] == 'SW')

        ):
            vehicles_straight+=1

    for row in data:
        #count bicycles
        if row['VehicleType'] =='Bicycle':
            total_bicycles+=1

    for row in data:
        #count vehicles over the speed limit
        if float(row['VehicleSpeed'])> float(row['JunctionSpeedLimit']):
            over_speed_limit+=1

    for row in data:
        #count  vehicles passing through only Elm Avenue/Rabbit Road
        if row['JunctionName']=='Elm Avenue/Rabbit Road':
            vehicles_elm_avenue+=1

    for row in data:
        #count  vehicles passing through only Hanley Highway/Westway
        if row['JunctionName']=='Hanley Highway/Westway':
            vehicles_hanley_highway+=1

    for row in data:
        #count scooters passing through Elm Avenue/Rabbit Road
        if row['JunctionName']=='Elm Avenue/Rabbit Road':
            if row['VehicleType']=='Scooter':
                scooters_elm+=1

    for row in data:
        #count peak traffic hours
        junction_name = row['JunctionName']
        time_of_day=row['timeOfDay']

        if junction_name =='Hanley Highway/Westway':
            hour = int(time_of_day.split(':')[0])

            if hour<9:
                key=f"{hour}:00 -{hour+1}:00"
            elif hour==9:
                key =f"{hour}:00 - {hour+1}:00"
            else:
                key = f"{hour}:00 - {hour+1}:00"

            hour_dict[key]=hour_dict.get(key,0)+1

    #making new dictionaries for the use of vehicle count
    elm_avenue_data = {hour: 0 for hour in range(24)}
    hanley_highway_data = {hour: 0 for hour in range(24)}

    for row in data:
        #extract the hour from the 'timeOfday' by splitting the string
        hour = int(row['timeOfDay'].split(':')[0])
        #extract the junction name from the current row
        junction = row['JunctionName']
        #checking if the junction name is 'Elm Avenue/Rabbit road'
        if junction == 'Elm Avenue/Rabbit Road':
            elm_avenue_data[hour] += 1
        #checking the junction name is 'Hanley Highway/Westway'
        elif junction == 'Hanley Highway/Westway':
            hanley_highway_data[hour] += 1

    # create traffic data as a dictionary
    traffic_data = {
        'Elm Avenue/Rabbit Road': elm_avenue_data,
        'Hanley Highway/Westway': hanley_highway_data
    }


    #Calculate the peak hour(s)
    max_value=max(hour_dict.values(),default=0)
    max_keys=[key for key,value in hour_dict.items() if value==max_value]

    if len(max_keys)>1:
        #if there are multiple peak hours, join all
        peak_hour_string=",".join(max_keys[:-1])+"and" +max_keys[-1]
    else:
        # if only one peak hour,assign it in to the peak_hour_string
        peak_hour_string=max_keys[0]

    for row in data:
        #count rain hours
        #checking the weather condition indicate rain
        if row['Weather_Conditions'].lower() in ['heavy rain','light rain']:
            time = row ['timeOfDay']
            #convert the time string to a datetime and extract the hour
            hour = datetime.strptime(time, '%H:%M:%S').hour
            #add the hour to the set of rain hours
            rain_hours.add(hour)

    #calculate rain hours
    total_rain_hours = len(rain_hours)

    if total_vehicles >0:
        #calculate percentage of trucks
        percentage_of_trucks=round((total_trucks/total_vehicles)*100)
    else:
        percentage_of_trucks=0

    #calculate average bicycle per hour
    average_bicycle_per_hour=round((total_bicycles/24)) if total_bicycles>0 else 0

    #calculate percentage of scooters passing through Elm avenue
    if vehicles_elm_avenue>0:
        percentage_of_scooters_elm=round((scooters_elm/vehicles_elm_avenue)*100)
    else:
        percentage_of_scooters_elm=0

    #make results into a dictionary
    results = {
        'Data file selected is':file_path.split('/')[-1],
        'The total number of vehicles recorded for this date is':total_vehicles,
        'The total number of trucks recorded for this date is':total_trucks,
        'The total number of electric vehicles recorded for this date is ':total_electric_vehicles,
        'The total number of two-wheeled vehicles recorded for this date is':two_wheeled_vehicles,
        'The total number of Busses leaving Elm Avenue/Rabbit Road heading North is':busses_north,
        'The total number of vehicles through both junctions not turning left or right is': vehicles_straight,
        'The percentage total number of vehicles recorded that are trucks for this date is': str(percentage_of_trucks)+'%',
        'The average number of Bicycle per hour  for this date is':average_bicycle_per_hour,
        'The total number of vehicles recorded as over speed limit for this date is':over_speed_limit,
        'The total number of vehicles recorded through Elm Avenue/Rabbit Road Junction is':vehicles_elm_avenue,
        'The total number of vehicles recorded through Hanley Highway/Westway junction is':vehicles_hanley_highway,
        'The percentage of vehicles through Elm Avenue/Rabbit Road that are Scooters ':str(percentage_of_scooters_elm)+'%',
        'The number of vehicles recorded in the peak (busiest) hour on Hanley Highway/Westway':max_value,
        'The time or times of the peak (busiest) traffic hour (or hours) on Hanley Highway/Westway':peak_hour_string,
        'The total number of hours of rain':total_rain_hours
    }
    return results,traffic_data


def display_outcomes(outcomes):

    '''
    Display the calculated outcomes in formatted way
    '''
    #print the title(program results),centering with '='
    print('program Results'.center(60,'='))
    for key,value in outcomes.items():
        #print each key-value pairs
        print(f'{key} {value}')
    #print a line made of '=' to mark the end of the output
    print('='*60)

#Task C: Save results to Text file

def save_results_to_a_file(outcomes,file_name='result.txt'):

   '''
   saves the processed outcomes to a text file and appends
   '''

   try:
       #open file in append mode
      with open(file_name,'a') as file:
          #write a section title for the program results in the file
        file.write('\n===program Results===\n')
        for key,value in outcomes.items():
            #write each key-value pair
            file.write(f'{key} {value}\n')
        #add new line after the resuls to seperate
        file.write('\n')
      #print message to confirm the results
      print(f'Results saved successfully to {file_name}')
   #if an error occurs during the file opeartion,print an error message
   except Exception as e:
       print(f'An error occurred while saving results:{e}')

#Task D: Histogram Display
import tkinter as tk

class HistogramApp:

    def __init__(self, traffic_data, date):
        #Initialize class with the traffic data and date
        self.traffic_data = traffic_data
        self.date = date

        #Getting traffic data for two specific junctions
        elm_traffic=self.traffic_data['Elm Avenue/Rabbit Road']
        hanley_traffic=self.traffic_data['Hanley Highway/Westway']

        #making up the main window for the Tkinter
        self.root = tk.Tk()
        self.root.title('Histogram')

        #create canvas for drawing the histogram
        self.canvas = tk.Canvas(self.root, width=1600, height=900, bg='white')
        self.canvas.pack()

    def setup_window(self):

        #creating a title for the window including date
        title = f'Histogram of Vehicles Frequency per Hour {self.date}'

        #Adding text for the title at the top of the window
        self.canvas.create_text(800, 20, text=title, font=('Arial', 16, 'bold'), fill='black')

    def draw_histogram(self):

        #setting up colors for the junction bars
        colors = ['blue', 'pink']
        #Getting a list of junction names from the traffic data
        junctions = list(self.traffic_data.keys())
        #creating a range from 0 to 23 for the hours of days
        hours = range(24)


        #Find the maximum traffic volume to scale the bars
        max_volume = 0
        for junction in junctions:
            for hour in hours:
                volume = self.traffic_data[junction][hour]
                if volume > max_volume:
                    max_volume = volume

        #scaling y axis
        y_scale = 400 / max_volume

        # width of the bar
        bar_width = 20
        gap_between_hours = 53 #gap between hours

        #Drawing X axis and Y axis seperately
        self.canvas.create_line(100, 500, 1500, 500, width=2)
        self.canvas.create_line(100, 500, 100, 100, width=2)

        #Labeling X axis and Y axis
        self.canvas.create_text(600, 530, text='Hours 00:00 to 24:00', font=('Arial', 12), fill='black')
        self.canvas.create_text(60, 300, text='Traffic Volume', font=('Arial', 12), angle=90, fill='black')


        #draw the bars of histogram for each junction
        color_index = 0
        for junction in junctions:
            for hour in hours:
                volume = self.traffic_data[junction][hour]

                #Calculate x co-orinates for the lest and right sides of the bar
                x1 = 100 + (hour * gap_between_hours) + color_index * bar_width
                x2 = x1 + bar_width

                #Calculate y co-ordinates for the top and bottom of the bar
                y1 = 500 - volume * y_scale
                y2 = 500

                #drawing rectangles for each hour
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[color_index % len(colors)], outline='black')

                #show the  count of the vehicles on top of the bar
                self.canvas.create_text((x1+x2)/2,y1-10,text=str(volume),font=('Arial',8),fill='black')
            #Moving to the next color for the next junction
            color_index += 1

        #labeling the  hours at the bottom of the histogram
        for hour in hours:
            x = 100 + (hour * gap_between_hours) + bar_width
            self.canvas.create_text(x, 510, text=str(hour), font=('Arial', 10), fill='black')

    def add_legend(self):
        #Adding a legend to explain which color represents with each junction
        colors = ['blue', 'pink']
        junctions = list(self.traffic_data.keys())


        #Loop through each junction to create a legend entry
        index = 0
        for junction in junctions:
            #drawing a colored rectangle for each junction in the legend
            self.canvas.create_rectangle(800, 40 + index * 20, 820, 60 + index * 20, fill=colors[index % len(colors)],
                                         outline='black')

            #Adding text next to the colored rectangle to name the junction
            self.canvas.create_text(830, 50 + index * 20, text=junction, font=('Arial', 10), anchor='w', fill='black')
            index += 1

    def run(self):

        #setting upm window and drawing the histogram and legend
        self.setup_window()
        self.draw_histogram()
        self.add_legend()

        #starting Tkinter mainloop to display the window
        self.root.mainloop()


# Task E :  Code loops to handle Multiple

class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and process its data
        """
        try:
            #open the file and read
            with open(file_path,'r'):
                results, traffic_data = process_csv_data(file_path)
                return results, traffic_data
        except FileNotFoundError:

            #handle the case when there is no any file
            print(f"Error:The file '{file_path}' does not exist.")
            return None,None # return processed results and data

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):

        """
        Handles user input for processing multiple files
        """
        while True:
            # get the valid inputs from the user
            day, month, year = validate_data_input()

            #process the file path based on given inputs
            file_path = f'excel_files/traffic_data{day:02}{month:02}{year}.csv'

            #load and process the csv file using the processed file path
            results, traffic_data = self.load_csv_file(file_path)

            if results:
                #if results are successfully processed then display outcomes
                display_outcomes(results)
                save_results_to_a_file(results)#save results to a file
                self.current_data = traffic_data

                #launch Histogram app with the processed traffic data and the date
                app = HistogramApp(traffic_data, date=f'{day:02}/{month:02}/{year}')
                app.run()
            else:
                print("Please try again  or type 'N' to quit")

            #ask the user for loading another data set
            choice = vaildate_continue_input()
            #if user chooses 'N', the loop will get exit and program will get end
            if choice == 'N':
                print('The End!.')
                break

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction()

#starting processing file using MultiCSVProcessor
processor = MultiCSVProcessor()
processor.process_files()











