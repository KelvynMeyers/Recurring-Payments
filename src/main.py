from payment import Payment
import datetime
import os


paymentList = []


def main():
    continueApp = True
    while continueApp:
        # Greeting & Commands
        printLine(100)
        printHeader("RECURRING PAYMENTS TERMINAL")
        print("Welcome to recurring payments application terminal.")
        print("\tType 'view all' to show all existing payments")
        print("\tType 'view name' to show an existing payment")
        print("\tType 'new' to create a new payment")
        print("\tType 'edit name' to edit an existing payment")
        print("\tType 'delete name' to delete an existing payment")

        # Request User Input
        userInput = input("\nUser Input: ").lower()
        userInput = userInput.split(" ")
        print()

        # Parse User Input
        # TODO: Move all these parse things into a seperate function maybe, or at least new/edit
        if userInput[0] == "view":
            if len(userInput) <= 1:
                printError("Invalid parameter extensions for view.")
            if userInput[1] == "all":
                printHeader("DISPLAYING ALL PAYMENTS")
                printPayments()
            else:
                printHeader("DISPLAYING SPECIFIC PAYMENT")
                print("Attempting to locate " + userInput[1])

        elif userInput[0] == "new":
            readyToSubmit = False
            while not readyToSubmit:
                # Request Payment Name
                # TODO: Ensure no repeats in names
                printHeader("CREATING A NEW PAYMENT")
                paymentName = input("Enter payment's name: ").lower()
                while len(paymentName) <= 0 or len(paymentName) > 128:
                    printError("Payment's name must contain appropriate number of characters (1-128).")
                    paymentName = input("Enter payment's name: ")

                # Request Payment Value
                # TODO: Ensure if value is flat like 5, it rounds to 5.00 and not 5.0
                try:
                    paymentValue = round(float(input("Enter payment's value: ")), 2)
                except ValueError:
                    paymentValue = 0
                while paymentValue <= 0.00:
                    printError("Payment's value must be a number greater than zero")
                    try:
                        paymentValue = round(float(input("Enter payment's value: ")), 2)
                    except ValueError:
                        paymentValue = 0

                # Request Payment Date
                paymentDate = validateDate(input("Enter payment's last or upcoming date in MM/DD/YYYY format: "))
                while paymentDate is None:
                    printError("Payment date must be in the MM/DD/YYYY format.")
                    paymentDate = validateDate(input("Enter payment's last or upcoming date in MM/DD/YYYY format: "))

                # User Validation
                clearTerminal()
                print("Name:\t" + paymentName)
                print("Value:\t" + str(paymentValue))
                print("Date:\t" + str(paymentDate))
                userValidate = input("\nAre you okay with these values? Y/N: ").lower()
                while userValidate != "y" and userValidate != "n" and userValidate != "yes" and userValidate != "no":
                    printError("Must respond with either Y or N")
                    userValidate = input("Are you okay with these values? Y/N: ").lower()
                if userValidate == "n" or userValidate == "no":
                    readyToSubmit = False
                    continue;
                else:
                    readyToSubmit = True

                # Create Payment and Append to paymentList
                newPayment = Payment(paymentName, paymentValue, paymentDate)
                if not newPayment:
                    printError("Failed to create new payment with given credentials.")
                    break
                paymentList.append(newPayment)

            # Closure
            printHeader("SUCCESSFULLY CREATED PAYMENT")
            printPayment(newPayment)

        elif userInput[0] == "exit":
            printHeader("EXITING PROGRAM")
            print("Thank you for utilizing the service! Goodbye.")
            continueApp = False
            break

        else:
            printError("Invalid parameters provided!")

        printCloser()


def printLine(amt):
    print(amt*"-")

def printHeader(text):
    clearTerminal()
    print(text)
    printLine(50)

def printCloser():
    #print("\n")
    printLine(50)
    input("Press Enter to Continue ")
    clearTerminal()

def printError(text):
    print("\tERROR: "+text)

def printPayments():
    for payment in paymentList:
        printPayment(payment)
        if paymentList.index(payment) != len(paymentList)-1:
            printLine(25)

def printPayment(payment):
    if payment.__class__.__name__ != "Payment":
        return
    print("Name:\t" + payment.name)
    print("Value:\t" + str(payment.value))
    print("Date:\t" + str(payment.date))

def validateDate(givenDate):
    try:
        returnDate = datetime.datetime.strptime(givenDate, '%m/%d/%Y')
    except ValueError:
        return None
    return datetime.datetime.strftime(returnDate, '%m/%d/%Y')

def clearTerminal():
    os.system('cls||clear')


# Main Execution
main()
