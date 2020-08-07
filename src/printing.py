import os

def printLine(amt):
    print(amt*"-")

def printHeader(text):
    clearTerminal()
    print(text)
    printLine(50)

def printError(text):
    print("\tERROR: "+text)

def printPayments(paymentList):
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

def printHelp():
    printHeader("RECURRING PAYMENTS TERMINAL")
    print("Welcome to recurring payments application terminal.")
    print("\tType 'view all' to show all existing payments")
    print("\tType 'view name' to show an existing payment")
    print("\tType 'new' to create a new payment")
    print("\tType 'edit name' to edit an existing payment")
    print("\tType 'delete name' to delete an existing payment")
    print("\tType 'help' to return to this menu")
    print("\tType 'exit' to end the program")

def clearTerminal():
    os.system('cls||clear')