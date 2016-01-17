import datetime


class Error(Exception):                                                 #Error class
    def __init__(self, error_log):
        super().__init__(error_log)


class Country(object):                                                  #Country class
    def __init__(self, country_name, currency_code, currency_symbol):
        self.country_name = country_name
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol

    def format_currency(self, amount):                                  #adds symbol infront of amount
        amount_symbol = self.currency_symbol + str("{0:.2f}".format(round(amount, 2)))
        return amount_symbol

    def __str__(self):
        return "{} {} {}".format(self.country_name, self.currency_code, self.currency_symbol)


class Details(object):

    def __init__(self):
        self.location = []

    def add(self, country_name, start_date, end_date):                  #checks and adds into location list
        start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").date().strftime("%Y/%m/%d")
        end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").date().strftime("%Y/%m/%d")
        try:
            if start_date > end_date:
                raise Error("END DATE IS AFTER START DATE!")
            for x in range(len(self.location)):
                if start_date in self.location[x][0]:
                    raise Error("START DATE IS ALREADY USED!")
        except Error as Er:
            print(Er)
        else:
            self.location.append([start_date, end_date, country_name])

    def current_country(self, date_str):                                #checks and returns the country according to the date given
        date_format = datetime.datetime.strptime(date_str, "%d/%m/%Y").date().strftime("%Y/%m/%d")
        try:
            for x in range(len(self.location)):
                if self.location[x][0] <= date_format <= self.location[x][1]:
                    return self.location[x][2]
                elif x + 1 == len(self.location):
                    raise Error("THERE IS NO COUNTRY WITH THAT DATE")
        except Error as e:
            print(e)

    def is_empty(self):
        if not self.location:
            print("THIS LOCATION LIST IS EMPTY")

if __name__ == "__main__": #executed or imported

#code testing

    import currency                                                     #importing from currency
    testing_country = Country(*currency.get_details("Singapore"))
    print(testing_country)
    print(testing_country.format_currency(10.10), "\n\n")


    testing_date = Details()
    testing_date.is_empty()
    print(testing_date.location, "\n\n")


    Details.add(testing_date, "India", "10/12/2010", "25/12/2010")
    print(testing_date.location)
    Details.add(testing_date, "Saudi Arabia", "11/10/2011", "22/12/2011")
    print(testing_date.location, "\n\n")


    print(Details.current_country(testing_date, "20/12/2010"))
    print(Details.current_country(testing_date, "12/10/2003"))
    testing_date.is_empty()