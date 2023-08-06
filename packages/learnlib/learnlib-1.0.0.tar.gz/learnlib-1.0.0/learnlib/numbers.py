def add(numbers):
    total = 0
    for number in numbers:
        total += number
    return total


def subtract(numbers):
    highest = max(numbers)
    for number in numbers:
        if number != highest:
            highest -= number
    return highest


def multiply(numbers):
    product = 1
    for number in numbers:
        product *= number
    return product


def divide(dividend, divisor):
    return dividend/divisor


def count_up(num):
    for i in range(num):
        print(i)


def count_down(num):
    for i in range(num, 0, -1):
        print(i)
