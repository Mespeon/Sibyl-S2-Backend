import random

randomtext = [
"Hello World!",
"Not the random thing you're looking for.",
"Flags are your best friends.",
"cIpHeRs aRe gOoD."
    ]

def generateRandomNumber():
    randomnum = random.randint(0, len(randomtext)-1)
    return randomnum

def getRandomQuote():
    quote = randomtext[generateRandomNumber()]
    return quote
    print(quote)
