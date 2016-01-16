class Country:
    def __init__(self, name, code, symbol):
        self.name = name
        self.code = code
        self.symbol = symbol

    def formatted_amount(self, amount):
        return self.symbol + str(round(amount, 2))

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)

    @classmethod
    def make(cls, data_list):
        if not data_list:
            raise Error("can't make country")
        return Country(*data_list)


class Details:
    def __init__(self):
        self.locations = []

    def add(self, country_name, start_date, end_date):
        if start_date > end_date:
            raise Error('invalid trip dates: {} {}'.format(start_date, end_date))
        for location in self.locations:
            if location[0] == start_date:
                raise Error('{}-{} already added'.format(start_date, end_date))
        self.locations.append((start_date, end_date, country_name))

    def current_country(self, date_string):
        for location in self.locations:
            if location[0] <= date_string <= location[1]:
                return location[2]
        raise Error('invalid date')

    def empty(self):
        return len(self.locations) == 0


class Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    from currency import get_details
    import time

    print('test country class')
    country = Country('Australia', 'AUD', '$')
    print(country.formatted_amount(10.95))
    country = Country.make(get_details("Turkey"))
    print(country.formatted_amount(10.95))

    print('test tripdetails class')
    trip = Details()
    trip.add(country, "2015/09/05", "2015/09/20")
    trip.add(country, "2015/09/21", "2016/09/20")
    try:
        print(trip.current_country("2015/09/01"))
    except Error as error:
        print(error.value)

    print(trip.current_country(time.strftime('%Y/%m/%d')))

    try:
        trip.add(country, "2015/09/05", "2015/09/20")
    except Error as error:
        print(error.value)