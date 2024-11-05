num_1 = '42'
num_2 = '45.12'
num_3 = '1.00'
num_4 = '1.0'


def last_discharge(number):
    if '.' in number:
        number = number.split('.')
        if len(number[-1]) == 2:
            number[-1] = int(number[-1]) - 1
            if number[-1] == -1:
                number[0] = int(number[0]) - 1
                number[-1] = 99
        else:
            number[-1] = int(number[-1]) - 1
            if number[-1] == -1:
                number[0] = int(number[0]) - 1
                number[-1] = 9
        return f'{str(number[0])}.{str(number[1])}'
    else:
        return str(int(number) - 1)


print(last_discharge("42"))    # Вывод: "41"
print(last_discharge("45.12"))  # Вывод: "45.11"
print(last_discharge("1.00"))  # Вывод: "0.99"
print(last_discharge("1.0"))    # Вывод: "0.9"
