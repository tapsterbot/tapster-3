def calculator(bot, val): #val: a string of values to type on the calculator (i.e. "1+1=")
    for i in val:
        match i:
            case "0": bot.tap(-14, -52)
            case "1": bot.tap(-14, -40)
            case "2": bot.tap(-2, -40)
            case "3": bot.tap(12, -40)
            case "4": bot.tap(-14, -30)
            case "5": bot.tap(-2, -30)
            case "6": bot.tap(12, -30)
            case "7": bot.tap(-14, -16)
            case "8": bot.tap(-2, -16)
            case "9": bot.tap(12, -16)
            case ".": bot.tap(-2, -52)
            case "+": bot.tap(24, -48)
            case "-": bot.tap(24, -28)
            case "*": bot.tap(24, -18)
            case "/": bot.tap(24, -6)
            case "=": bot.tap(10, -54)
            case "c": bot.tap(-28, -52)

def strToCalc(bot, str):
    result = ""
    str = str.lower()
    if str[-1] == "o":
        calculator(bot, "0.")
        str = str[:-1]
    for i in str:
        match i:
            case "o": result += "0"
            case "i": result += "1"
            case "e": result += "3"
            case "h": result += "4"
            case "s": result += "5"
            case "g": result += "6"
            case "l": result += "7"
            case "b": result += "8"
            case _:
                return False
    
    resultRev = ""
    for i in result[::-1]: resultRev += i
    calculator(bot, resultRev)