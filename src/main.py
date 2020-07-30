from payment import Payment
import datetime
import calendar
import os


paymentList = []


def main():
    continueApp = True
    while continueApp:
        # Greeting & Commands
        printHeader("RECURRING PAYMENTS TERMINAL")
        print("Welcome to recurring payments application terminal.")
        print("\tType 'view all' to show all existing payments")
        print("\tType 'view name' to show an existing payment")
        print("\tType 'new' to create a new payment")
        print("\tType 'edit name' to edit an existing payment")
        print("\tType 'delete name' to delete an existing payment")
        print("\tType 'exit' to end the program")

        # Request User Input
        userInput = input("\nUser Input: ").lower()
        userInput = userInput.split(" ")
        print()

        # Parse User Input
        # TODO: Consider not .lower()'ing payment names, only .lower() for comparison. More visually appealing
        # TODO: Collapse user validation printing in new/edit into a single function to maintain consistency if format changes in the future
        if len(userInput) > 2:
            printError("Parameter count limited to two. Payment names must not contain spaces")
        elif userInput[0] == "view":
            continueApp = programView(userInput)
        elif userInput[0] == "new":
            continueApp = programNew(userInput)
        elif userInput[0] == "edit":
            continueApp = programEdit(userInput) 
        elif userInput[0] == "delete":
            continueApp = programDelete(userInput) 
        elif userInput[0] == "exit":
            continueApp = programExit(userInput)
        else:
            printError("Invalid parameters provided!")

        printCloser()

def programView(userInput):
    if len(userInput) == 1 or userInput[1] == "":
        printError("View must contain a second parameter")
    elif userInput[1] == "all":
        printHeader("DISPLAYING ALL PAYMENTS")
        printPayments()
    else:
        printHeader("DISPLAYING SPECIFIC PAYMENT")
        paymentIndex = findPayment(userInput[1])
        if paymentIndex < 0:
            printError("'" + userInput[1] + "' does not exist.")
            return True
        foundPayment = paymentList[paymentIndex]
        printPayment(foundPayment)
    return True
    
def programNew(userInput):
    readyToSubmit = False
    while not readyToSubmit:
        printHeader("CREATING A NEW PAYMENT")
        # Request Payment Info
        paymentName = requestPaymentName(False)
        paymentValue = requestPaymentValue()
        paymentDate = requestPaymentDate()
        paymentReoccurence = requestPaymentReoccurence(paymentDate)
        
        # User Validation
        printHeader("CONFIRM PAYMENT CREATION")
        printUserInputs(paymentName, paymentValue, paymentDate, paymentReoccurence)
        userValidation = userValidate("Are you okay with these values?")
        if not userValidation:
            readyToSubmit = False
            continue
        readyToSubmit = True

        # Create Payment and Append to paymentList
        newPayment = Payment(paymentName, paymentValue, paymentDate, paymentReoccurence)
        if not newPayment:
            printError("Failed to create new payment with given credentials.")
            return False
        paymentList.append(newPayment)

    # Closure
    printHeader("SUCCESSFULLY CREATED PAYMENT")
    printPayment(newPayment)
    return True

def programEdit(userInput):
    if len(userInput) == 1 or userInput == "":
        printError("Edit must have a second parameter")
        return True
    
    # Find Payment in List
    printHeader("FINDING PAYMENT TO EDIT")
    paymentIndex = findPayment(userInput[1])
    if paymentIndex < 0:
        printError("'" + userInput[1] + "' does not exist.")
        return True
    foundPayment = paymentList[paymentIndex]
    
    # Validate Payment Selection
    printPayment(foundPayment)
    userValidation = userValidate("Do you want to edit this payment?")
    if not userValidation:
        return True
    
    readyToSubmit = False
    while not readyToSubmit:
        printHeader("UPDATING EXISTING PAYMENT")
        # Request Payment Info
        paymentName = requestPaymentName(True)
        paymentValue = requestPaymentValue()
        paymentDate = requestPaymentDate()
        paymentReoccurence = requestPaymentReoccurence(paymentDate)

        # User Validation
        printHeader("CONFIRM PAYMENT UPDATE")
        printUserInputs(paymentName, paymentValue, paymentDate, paymentReoccurence)
        userValidation = userValidate("Are you okay with these values?")
        if not userValidation:
            readyToSubmit = False
            continue
        readyToSubmit = True

        # Update Payment in Payment List
        backupPayment = paymentList[paymentIndex]
        paymentList[paymentIndex] = Payment(paymentName, paymentValue, paymentDate, paymentReoccurence)
        foundPayment = paymentList[paymentIndex]
        if not foundPayment:
            printError("Failed to update existing payment with given credentials. Returning to old values")
            paymentList[paymentIndex] = backupPayment
            return False
    
    # Closure
    printHeader("SUCCESSFULLY EDITED PAYMENT")
    printPayment(foundPayment)
    return True

def programDelete(userInput):
    if len(userInput) == 1 or userInput == "":
        printError("Delete must have a second parameter")
        return True

    # Find Payment in List
    printHeader("FINDING PAYMENT TO DELETE")
    paymentIndex = findPayment(userInput[1])
    if paymentIndex < 0:
        printError("'" + userInput[1] + "' does not exist.")
        return True
    foundPayment = paymentList[paymentIndex]
    
    # Validate Payment Selection
    printPayment(foundPayment)
    userValidation = userValidate("Do you want to delete this payment?")
    if not userValidation:
        return True
    
    # Remove Payment in List
    try:
        paymentList.remove(paymentList[paymentIndex])
    except ValueError:
        printError("Failed to delete payment from payment list")
        return True

    # Closure
    printHeader("SUCCESSFULLY DELETED PAYMENT")
    printPayment(foundPayment)
    return True

def programExit(userInput):
    printHeader("EXITING PROGRAM")
    print("Thank you for utilizing the service! Goodbye.")
    return False

def requestPaymentName(isAnEdit):
    validPayment = False
    while not validPayment:
        paymentName = input("Enter payment's name: ")
        if len(paymentName) <= 0 or len(paymentName) > 255 or not validateUniqueness(paymentName, isAnEdit) or " " in paymentName:
            printError("Payment's name must be unique, contain no spaces, and have the appropriate number of characters (1-255).")
            continue
        validPayment = True
    return paymentName

def requestPaymentValue():
    userMessage = "Enter payment's value: "
    validValue = False
    while not validValue:
        try:
            paymentValue = round(float(input(userMessage)), 2)
        except ValueError:
            printError("Payment's value must be a valid number")
            continue
        if paymentValue <= 0.0:
            printError("Payment's value must be a number greater than zero")
            continue
        validValue = True
    return '{:.2f}'.format(paymentValue)

def requestPaymentDate():
    userMessage = "Enter last payment date in MM/DD/YYYY format: "
    paymentDate = validateDate(input(userMessage))
    while paymentDate is None:
        printError("Payment date must be in the MM/DD/YYYY format.")
        paymentDate = validateDate(input(userMessage))
    return paymentDate

def requestPaymentReoccurence(givenDate):
    userMessage = "Enter number of months between each payment: "
    userValue = 0
    validReoccurence = False
    while not validReoccurence:
        try:
            userValue = int(input(userMessage))
        except ValueError:
            printError("Must provide a valid integer number")
            continue
        if userValue <= 0:
            printError("For a payment to be recurring, time between each payment must be at least 1 month")
            continue
        validReoccurence = True
    # Retrieve Date, Add Months, and Return Reformatted Date
    givenDate = datetime.datetime.strptime(givenDate, '%m/%d/%Y')
    givenDate = addMonths(givenDate,userValue)
    return datetime.datetime.strftime(givenDate, '%m/%d/%Y')

def userValidate(message):
    userMessage = "\n"+message+" [Y/N]: "
    validResponse = False
    while not validResponse:
        userValidate = input(userMessage).lower()
        if userValidate != "y" and userValidate != "n" and userValidate != "yes" and userValidate != "no":
            printError("Must respond with either Y or N")
            continue
        validResponse = True
    if userValidate == "n" or userValidate == "no":
        return False
    return True

def validateDate(givenDate):
    try:
        returnDate = datetime.datetime.strptime(givenDate, '%m/%d/%Y')
    except ValueError:
        return None
    return datetime.datetime.strftime(returnDate, '%m/%d/%Y')

def validateUniqueness(paymentName, isAnEdit):
    if paymentName == "all":
        return False
    for payment in paymentList:
        if payment.name.lower() == paymentName.lower():
            if isAnEdit:
                return True
            return False
    return True

def addMonths(givenDate, numMonths):
    month = givenDate.month - 1 + numMonths
    year = givenDate.year + numMonths // 12
    month = month % 12 + 1
    day = min(givenDate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

def findPayment(paymentName):
    for index, payment in enumerate(paymentList):
        if payment.name.lower() == paymentName.lower():
            return index
    return -1

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
            printLine(50)

def printPayment(payment):
    if payment.__class__.__name__ != "Payment":
        return
    printUserInputs(payment.name,payment.value,payment.lastDate,payment.upcomingDate)

def printUserInputs(paymentName, paymentValue, paymentDate, paymentReoccurence):
    print("Name:\t\t\t" + paymentName)
    print("Value:\t\t\t" + str(paymentValue))
    print("Last Payment:\t\t" + str(paymentDate))
    print("Upcoming Payment:\t" + str(paymentReoccurence))

def clearTerminal():
    os.system('cls||clear')

# Main Execution
#main()
if __name__ == "__main__":
    main()
