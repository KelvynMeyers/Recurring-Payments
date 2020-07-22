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
            if len(userInput) <= 1 or len(userInput) > 2:
                printError("Invalid parameter extensions for view.")
            elif userInput[1] == "all":
                printHeader("DISPLAYING ALL PAYMENTS")
                printPayments()
            else:
                printHeader("DISPLAYING SPECIFIC PAYMENT")
                foundPayment = findPayment(userInput[1])
                if foundPayment is None:
                    printError(userInput[1] + " does not exist")
                else:
                    printPayment(foundPayment)


        elif userInput[0] == "new":
            readyToSubmit = False
            while not readyToSubmit:
                # Request Payment Name
                printHeader("CREATING A NEW PAYMENT")
                paymentName = input("Enter payment's name: ").lower()
                while len(paymentName) <= 0 or len(paymentName) > 128 or not validateUniqueness(paymentName):
                    printError("Payment's name must be a unique and contain appropriate number of characters (1-128).")
                    paymentName = input("Enter payment's name: ").lower()

                # Request Payment Value
                # TODO: Clean up payment value section
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
                paymentValue = '{:.2f}'.format(paymentValue)

                # Request Payment Date
                paymentDate = validateDate(input("Enter payment's last or upcoming date in MM/DD/YYYY format: "))
                while paymentDate is None:
                    printError("Payment date must be in the MM/DD/YYYY format.")
                    paymentDate = validateDate(input("Enter payment's last or upcoming date in MM/DD/YYYY format: "))

                # User Validation
                printHeader("CONFIRM PAYMENT CREATION")
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
            printLine(50)
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
    printLine(50)
    input("Press Enter to Continue ")
    clearTerminal()

def printError(text):
    print("\tERROR: "+text)

def printPayments():
    if len(paymentList) <= 0:
        printError("No payments exist")
        return
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

def clearTerminal():
    os.system('cls||clear')

def validateDate(givenDate):
    try:
        returnDate = datetime.datetime.strptime(givenDate, '%m/%d/%Y')
    except ValueError:
        return None
    return datetime.datetime.strftime(returnDate, '%m/%d/%Y')

def validateUniqueness(paymentName):
    for payment in paymentList:
        if payment.name.lower() == paymentName:
            return False
    return True

def findPayment(paymentName):
    for payment in paymentList:
        if payment.name.lower() == paymentName.lower():
            return payment

# Main Execution
main()
