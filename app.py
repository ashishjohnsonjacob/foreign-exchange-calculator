import datetime             #date related functions
import trip                 #getting details using trip's methods
import currency             #converting the currency

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

#setting the widhth and height
Config.set('graphics', 'width', 350)
Config.set('graphics', 'height', 700)

#class definition starts here
class Foreign_Exchange_Calculator(App):
    current_place = StringProperty()            #current place according to the date
    name_country = ListProperty()               #list of countries from currency_details.txt

    def __init__(self):                         #initializing the class's object
        super().__init__()
        self.locations = trip.Details()             #getting details from trip module's details()
        self.get_home_country()                     #calling function to get the home country from config.txt
        self.get_full_country_list()                #getting full list of country for spinner
        self.today_date = datetime.datetime.now()   #getting current date and time
        self.current_date = self.today_date.strftime('%Y/%m/%d')    #current date only
        self.current_time = self.today_date.strftime('%H:%M:%S')    #current time only

    def build(self):
        self.title = "Foreign Exchange Calculator"          #giving title to the app
        self.root = Builder.load_file("gui.kv")             #loads the .kv file
        self.name_country = self.full_country_name_list     #list for spinner
        self.root.ids.date.text = "{}{}".format('TODAY IS: \n', self.current_date)      #date for date label
        self.current_country = self.current_location(self.current_date)     #getting country name according to the current date
        self.root.ids.current_location.text = "{}{}".format('CURRENT TRIP LOCATION: \n', self.current_country)  #for current trip location label
        return self.root

    def get_home_country(self): #getting home country
        try:
            with open('config.txt', encoding='utf8') as list_countries: #opens the txt file
                for line in list_countries:     #gets each line in the txt file
                    if ',' not in line:         #checks for ',' in the line
                        self.home_country = line.strip()    #getting the home country name (strip() for removing '\n'
            self.home_country_details = currency.get_details(self.home_country)     #getting full details of the home country
            self.status_bar_text = str("TRIP DETAILS ACCEPTED")     #status bar update
        except:
                self.status_bar_text = str("TRIP DETAILS INVALID")  #status bar update

    def set_selected_country(self):     #called after on_text at spinner to set the selected country
        self.selected_country_details = currency.get_details(self.root.ids.spinner_selection.text)  #getting full details of the selected country
        self.convert()  #calls convert()

    def get_current_country_details(self):      #getting full details of the current country
        self.current_country_details = currency.get_details(self.current_country.strip())   #getting full details (according to the current date)

    def get_full_country_list(self):    #gets full list of the country name
        self.full_country_name_list = []    #creating a list for country names
        with open("currency_details.txt", encoding='utf8') as currency_info:    #opens the txt file
                for line in currency_info:          #checks each line
                    self.splitted_line = line.split(",")    #split each line by ',' and putting in a list
                    self.full_country_name_list.append(self.splitted_line[0])   #getting all the country names into the list

    def get_country_details(self, country_name):        #used to get country details of a particular country
        self.country_name = country_name                #local variable
        self.country_details = currency.get_details(self.country_name)      #using the get_details method from currency module
        return self.country_details         #returns the country details

    def convert(self):          #conversion upon getting a selected country name from spinner
            self.converted_amount = currency.convert(1, self.home_country_details[1],self.selected_country_details[1]) #a. converts the amount using convert() from currency module
            self.root.ids.input_selected.text = str(("{:.3f}".format(self.converted_amount)))  #b. allowing only 3 significant decimal digits as per the requirement
            self.root.ids.input_home.text = str(1)      #default conversation rate of home country (= 1)
            self.root.ids.status_bar.text = str("{} ({}) to {} ({})".format(self.home_country_details[1], self.home_country_details[2], self.selected_country_details[1], self.selected_country_details[2])) #c. updates the status bar

    def convert_selected_to_home(self): #conversion upon getting an amount at selected country textinput
        try:
            self.converted_amount_st = currency.convert(self.root.ids.input_selected.text, self.selected_country_details[1], self.home_country_details[1]) #a.
            self.root.ids.input_home.text = str(("{:.3f}".format(self.converted_amount_st))) #b.
            self.root.ids.status_bar.text = str("{} ({}) to {} ({})".format(self.selected_country_details[1], self.selected_country_details[2], self.home_country_details[1], self.home_country_details[2])) #c.
        except:
            print("ERROR IN CONVERSION.") #prints error in the program but continues as it's in try and except

    def convert_home_to_selected(self):     #conversion upon getting an amount at home country textinput
        try:
            self.converted_amount_ts = currency.convert(self.root.ids.input_home.text, self.home_country_details[1],self.selected_country_details[1]) #a.
            self.root.ids.input_selected.text = str(("{:.3f}".format(self.converted_amount_ts))) #b.
            self.root.ids.status_bar.text = str("{} ({}) to {} ({})".format(self.home_country_details[1], self.home_country_details[2], self.selected_country_details[1], self.selected_country_details[2])) #c.
        except:     #if no selection on spinner then current country according to the current date is taken
            self.get_current_country_details()  #gettings the current country details
            self.root.ids.spinner_selection.text = self.current_country #assigning the current country name to spinner text
            self.converted_amount_ts = currency.convert(self.root.ids.input_home.text, self.home_country_details[1], self.current_country_details[1]) #a.
            self.root.ids.input_selected.text = str(("{:.3f}".format(self.converted_amount_ts)))    #b.
            self.root.ids.status_bar.text = str("{} ({}) to {} ({})".format(self.home_country_details[1], self.home_country_details[2], self.selected_country_details[1], self.selected_country_details[2])) #c.

    def current_location(self, str_date):           #getting the current country according to current date
        datetime.datetime.strptime(str_date, '%Y/%m/%d')    #formatting the current date for check
        date_list = []      #creating list for the dates
        with open('config.txt', encoding='utf8') as config:     #opening txt file
            for line in config:         #checks each time
                date_list.append(line.strip().split(','))       #apppends to the date list
        for x in date_list[1:]:             #for loop to check the date list
            if x[2] > str_date > x[1]:      #checks if the current date is between any dates in the date list
                return x[0]                 #returns the current country name

    def updated(self):          #function for the update button
        self.convert_home_to_selected()         #on click the conversation rate is updated with the given values itself as changing home country amount would be inconvenient
        self.root.ids.status_bar.text = str("{}{}".format("UPDATED AT ", self.current_time )) #update status bar

    def status_bar_clear(self):             #to clear status bar on text at the textinputs as per the requirement
        self.status_bar_text = str(" ")     #clears the status bar

if __name__ == '__main__':          #checks if this module is running as main
    Foreign_Exchange_Calculator().run()     #calls an instance of the class Foreign_Exchange_Calculator.. this is where the fun begins ;) ;)