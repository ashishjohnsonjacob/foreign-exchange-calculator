import datetime
import trip
import currency

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

Config.set('graphics', 'width', 350)
Config.set('graphics', 'height', 700)


class Foreign_Exchange_Calculator(App):
    current_place = StringProperty()
    name_country = ListProperty()

    def __init__(self):
        super().__init__()
        self.locations = trip.Details()
        self.get_home_country()
        self.get_full_country_list()
        self.today_date = datetime.datetime.now()
        self.current_date = self.today_date.strftime('%Y/%m/%d')

    def build(self):
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file("gui.kv")
        self.name_country = self.full_country_name_list
        self.root.ids.date.text = "{}{}".format('TODAY IS: \n', self.current_date)
        self.current_country = self.current_location(self.current_date)
        self.root.ids.current_location.text = "{}{}".format('CURRENT TRIP LOCATION: \n', self.current_country)
        return self.root

    def get_home_country(self):
        with open('config.txt', encoding='utf8') as list_countries:
            for line in list_countries:
                if ',' not in line:
                    self.home_country = line.strip()
        self.home_country_details = currency.get_details(self.home_country)

    def set_selected_country(self):
        self.selected_country_details = currency.get_details(self.root.ids.spinner_selection.text)
        self.convert()

    def get_current_country_details(self):
        self.current_country_details = currency.get_details(self.current_country.strip())

    def get_full_country_list(self):
        self.full_country_name_list = []
        with open("currency_details.txt", encoding='utf8') as currency_info:
                for line in currency_info:
                    self.splitted_line = line.split(",")
                    self.full_country_name_list.append(self.splitted_line[0])

    def get_country_details(self, country_name):
        self.country_name = country_name
        self.country_details = currency.get_details(self.country_name)
        return self.country_details

    def convert(self):
        self.root.ids.input_selected.text = str(currency.convert(1, self.home_country_details[1],self.selected_country_details[1]))
        self.root.ids.input_home.text = str(1)

    def convert_selected_to_home(self):
        try:
            self.root.ids.input_home.text = str(currency.convert(self.root.ids.input_selected.text, self.selected_country_details[1], self.home_country_details[1]))
        except:
            print("ERROR")

    def convert_home_to_selected(self):
        try:
            self.root.ids.input_selected.text = str(currency.convert(self.root.ids.input_home.text, self.home_country_details[1],self.selected_country_details[1]))
        except:
            self.get_current_country_details()
            self.root.ids.input_selected.text = str(currency.convert(self.root.ids.input_home.text, self.home_country_details[1], self.current_country_details[1]))

    def current_location(self, str_date):
        datetime.datetime.strptime(str_date, '%Y/%m/%d')
        date_list = []
        with open('config.txt', encoding='utf8') as config:
            for line in config:
                date_list.append(line.strip().split(','))
        for x in date_list[1:]:
            if x[2] > str_date > x[1]:
                return x[0]

if __name__ == '__main__':
    Foreign_Exchange_Calculator().run()