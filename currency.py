from io import open


def convert(amount, home_currency, target_currency):
    from web_utility import load_page

    def remove_text_before(position_string, all_text):
        remove_start = all_text.find(position_string)
        if remove_start == -1:
            return ''
        remove_start += len(position_string)
        return all_text[remove_start:]

    def remove_span(all_text):
        remove_start = all_text.find('<')
        remove_end = all_text.find('>') + 1
        return all_text[:remove_start] + all_text[remove_end:]

    format_string = 'https://www.google.com/finance/converter?a={}&from={}&to={}'
    url_string = format_string.format(amount, home_currency, target_currency)

    html_string = load_page(url_string)
    if not html_string:
        return -1

    data_string = remove_text_before('converter_result>', html_string)
    if not data_string:
        return -1

    data_string = remove_span(data_string)
    converted_amount_string = remove_text_before(" = ", data_string)
    if not converted_amount_string:
        return -1

    end_amount = converted_amount_string.find(' ')
    return float(converted_amount_string[:end_amount])


def get_details(country_name):
    file = open('currency_details.txt', encoding='utf-8')
    for line in file:
        words = [word for word in line.strip().split(',')]
        if words[0] == country_name:
            file.close()
            return tuple(words)
    file.close()
    return ()


if __name__ == '__main__':
    def conversion_test(amount, source, target):
        converted_amount = convert(amount, source, target)
        test_info = "{}->{}".format(source, target)
        print_conversion_test('valid conversion', amount, test_info, converted_amount)

        original_amount = convert(converted_amount, target, source)
        test_info = "{}->{}".format(target, source)
        print_conversion_test('valid conversion reverse', converted_amount, test_info, original_amount)


    def print_conversion_test(test_type, test_amount, test_info, test_result):
        text = "{:>30} {:>10.2f} {:^20} {:<10.2f}".format(test_type, test_amount, test_info, test_result)
        print(text)


    print_conversion_test('invalid conversion', 1, 'AUD->AUD', convert(1, 'AUD', 'AUD'))
    print_conversion_test('invalid conversion', 1, 'JPY->ABC', convert(1, 'JPY', 'ABC'))
    print_conversion_test('invalid conversion', 1, 'ABC->USD', convert(1, 'ABC', 'USD'))

    conversion_test(10.95, "AUD", "JPY")
    conversion_test(10.95, "AUD", "BGN")
    conversion_test(200.15, "BGN", "JPY")
    conversion_test(100, "JPY", "USD")
    conversion_test(19.99, "USD", "BGN")
    conversion_test(19.99, "USD", "AUD")
    print()


    def print_details_test(test_type, test_info, test_result):
        text = "{:>20} {:<10} {}".format(test_type, test_info, test_result)
        print(text)


    print_details_test('invalid details', 'ABC land', get_details("ABC land"))
    print_details_test('invalid details', 'Japanese', get_details("Japanese"))
    print_details_test('invalid details', '', get_details(""))

    print_details_test('valid details', 'Australia', get_details("Australia"))
    print_details_test('valid details', 'Japan', get_details("Japan"))
    print_details_test('valid details', 'Hong Kong', get_details("Hong Kong"))