# Calculator

def add(x,y):
    return x+y

def sub(x,y):
    return x-y

def multiplication(x,y):
    return x*y

def div(x,y):
    return x//y

def square(x):
    return x**2


print("Select Operations")
print("1. Add")
print("2. Sub")
print("3. Multiplication")
print("4. Div")
print("5. Square")


while True:
    choice = input("Enter your choice (1/2/3/4/5)")\
    
    if choice in ['1', '2', '3', '4','5']:
        try:
            num1 = float(input("Enter the first number"))
            num2 = float(input("Enter the second number"))
        except ValueError:
            print("You entered invalid")
        

        if choice == "1":
            print(f"Results: {add(num1,num2)}")
        elif choice == "2":
            print(f"Result: {sub(num1,num2)}")
        elif choice == "3":
            print(f"Result: {multiplication(num1,num2)}")
        elif choice == "4":
            print(f"Results: {div(num1,num2)}") 
        elif choice == "5":
            num = float(input("Enter the number"))
            print(f"Results: {square(num)}")
    else:
        print("Invalid choice")

    next_cal = input("Do you want to perform other calculation? (yes/no):")
    if next_cal.lower() != 'yes':
        print("Goodbye")
        break