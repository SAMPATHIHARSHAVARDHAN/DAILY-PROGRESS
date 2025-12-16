# Program to check Armstrong number

num = int(input("Enter a number: "))

# Convert number to string to find the number of digits
n = len(str(num))

sum_of_powers = 0
temp = num

while temp > 0:
    digit = temp % 10
    sum_of_powers += digit ** n
    temp //= 10

if num == sum_of_powers:
    print(num, "is an Armstrong number")
else:
    print(num, "is not an Armstrong number")
