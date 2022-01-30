from random import randint
booksAlreadySent = []
bookScores = []
signedUpLibraries = [] # met libs

class Library:
    def __init__(self, id, signupTime, booksPerDay, bookIDs):
        self.id = id
        self.signupTime = signupTime
        self.booksPerDay = booksPerDay
        self.bookIDs = bookIDs

        self.bookSendOrder = []

    def __str__(self):
        return "Lib" + str(self.id)

    def __repr__(self):
        return "Lib" + str(self.id)

    def printSelf(self):
        print("Library ID", self.id, "signupTime", self.signupTime, "bookperday", self.booksPerDay)

    def getBooksHighestScore(self, amount):
        books = []
        for book in self.bookIDs:
            if (len(books) >= amount): break
            elif (book in booksAlreadySent): continue
            else: books.append(book)
        return books

    def sendBestBooks(self):
        # returnt boekID van gegeven bib die het hoogstscorend is, en nog niet eerder verstuurd
        amountBooksSentToday = 0
        for book in self.bookIDs:
            if book not in booksAlreadySent:
                # print("lib with ID", self.id, "sending book nr", amountBooksSentToday, "today, bookID is", book)
                amountBooksSentToday += 1
                self.bookSendOrder.append(book)
                booksAlreadySent.append(book)
                if (amountBooksSentToday >= self.booksPerDay): break

    def compare_library(self, lib):
        score = 0
        for book in self.bookIDs:
            if (book in lib.bookIDs): score -= bookScores[book]
        return score

    def similarity_cost(self):
        score = 0
        for lib in signedUpLibraries:
            score += self.compare_library(lib)
        return score
        
    def writeToFile(self):
        with open("o.txt", "a") as f:
            f.write(str(self.id) + " " + str(len(self.bookSendOrder)) + "\n")
            for b in self.bookSendOrder: f.write(str(b) + " ")
            f.write("\n")

def writeAll():
    open('o.txt', 'w').close()
    signedUpLibraries = filterUselessLibraries()
    with open("o.txt", "a") as f:
        f.write(str(len(signedUpLibraries)) + "\n")
    for lib in signedUpLibraries:
        lib.writeToFile()


def filterUselessLibraries():
    return [x for x in signedUpLibraries if len(x.bookSendOrder) != 0]

def read():
    print("Input file?")
    allLibraries = []
    with open("input/" + input() + ".txt") as f:
        first = f.readline()
        bookAmount, libraryAmount, dayAmount = first.split(" ")
        bookAmount = int(bookAmount)
        libraryAmount = int(libraryAmount)
        dayAmount = int(dayAmount)
        second = f.readline()
        bookScores = second.split(" ")
        bookScores = [int(x) for x in bookScores]
        for i in range(int(libraryAmount)):
            _, signupTime, booksPerDay = f.readline().split(" ")
            bookIDs = f.readline().split(" ")
            if len(bookIDs) == 0: continue
            bookIDs = [int(x) for x in bookIDs]
            bookIDs.sort(key=lambda x: bookScores[x])
            newLib = Library(i, int(signupTime), int(booksPerDay), reversed(bookIDs))
            allLibraries.append(newLib)
            
    return [int(dayAmount), bookScores, allLibraries]


def calculateAll(days, allLibs):
    libsRemaining = allLibs
    daysUntilNextSignup = 0
    doneSigningUp = False
    currentlySigningUp = None  # welke library is momenteel gesignedup aan het worden
    for curDay in range(days):
        if curDay % 300 == 0: print("day", curDay)
        if (daysUntilNextSignup == 0 and not doneSigningUp):
            if currentlySigningUp is not None: signedUpLibraries.append(currentlySigningUp)
            if len(signedUpLibraries) != len(allLibs):
                allLibsnotSignedup = [x for x in allLibs if x not in signedUpLibraries]
                #allLibsnotSignedup.sort(key=lambda x: - x.signupTime)
                mapped = list(map(lambda x: x.signupTime, allLibsnotSignedup))
                newLib = allLibsnotSignedup[mapped.index(max(mapped))]
                currentlySigningUp = newLib
                daysUntilNextSignup = newLib.signupTime - 1
                #print("new days until signup is ", daysUntilNextSignup)
            else:
                doneSigningUp = True
        else: daysUntilNextSignup -= 1

        #print("currentlsy signed up:", signedUpLibraries)

        #signedUpLibraries.sort(key=lambda x: giveScoreToLib(x, curDay, days))
        for activeLib in signedUpLibraries:
            activeLib.sendBestBooks()


def giveScoreToLib(lib, presentDay, days):
    daysLeft = days-presentDay
    score = magicformula(lib, daysLeft)
    return score

def magicformula(lib, daysLeft):
    highestScoringBooks = lib.getBooksHighestScore((daysLeft - lib.signupTime) * lib.booksPerDay)
    score = (sum(highestScoringBooks) * lib.booksPerDay) + lib.similarity_cost()
    if (len(signedUpLibraries) > 20):  print("sim", lib.similarity_cost())
    return score


if __name__ == "__main__":
    days, bookScores, allLibs = read()
    calculateAll(days, allLibs)
    writeAll()
