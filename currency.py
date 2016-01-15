import web_utility


def convert(amount, home_currency_code, location_currency_code):            #converts the home currency to foreign currency and returns it
    url_string = "https://www.google.com/finance/converter?a={}&from={}&to={}".format(amount, home_currency_code,
                                                                                          location_currency_code)
    result = web_utility.load_page(url_string)
    if home_currency_code == location_currency_code:
        return -1
    if not home_currency_code + " = <span class=bld>" in result:
        return -1
    else:
        output_google = result[result.index('ld>'):result.index('</span>')]
        money = float(''.join(ele for ele in output_google if ele.isdigit() or ele == '.'))
        return money


def get_details(country_name):                                              #returns the details of a given country
    global splitted_line
    empty = ()
    with open("currency_details.txt", encoding='utf8') as currency_info:
        for line in currency_info:
            splitted_line = line.split(",")
            if splitted_line[0] == country_name:
                details = (splitted_line[0], splitted_line[1], splitted_line[2].strip())
                return details
        if splitted_line[0] != country_name:
                return empty

if __name__ == "__main__": #executed or imported

    def convert_testing(amount, home_currency_code, location_currency_code):
        convert_amount = convert(amount, home_currency_code, location_currency_code)
        if convert_amount < 0:
            return "{} {} {}->{} {}"\
                .format("invalid conversion", amount, home_currency_code, location_currency_code, convert_amount)
        else:
            return "{0} {1} {2}->{3} {4} \n {5} {4} {3}->{2} {1}"\
                .format("valid conversion", amount, home_currency_code, location_currency_code, convert_amount,
                        "valid conversion reverse")


    def details(country_name):
        details_tuple = get_details(country_name)
        if details_tuple:
            valid_or_not = "valid details"
        else:
            valid_or_not = "invalid details"
        return "{} {} {}".format(valid_or_not, country_name, str(details_tuple))

    print(convert_testing(1.00, "AUD", "AUD"))
    print(convert_testing(1.00, "JPY", "ABC"))
    print(convert_testing(1.00, "ABC", "USD"))
    print(convert_testing(10.95, "AUD", "JPY"))
    print(convert_testing(10.95, "AUD", "BGN"))
    print(convert_testing(200.15, "BGN", "JPY"))
    print(convert_testing(100, "JPY", "USD"))
    print(convert_testing(19.99, "USD", "BGN"))
    print(convert_testing(19.99, "USD", "AUD"))
    print("")
    print(details("Unknown"))
    print(details("Japanese"))
    print(details(""))
    print(details("Australia"))
    print(details("Japan"))
    print(details("Hong Kong"))
