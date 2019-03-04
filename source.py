import sqlite3


    

class UI:
    def __init__(self):
        self.paperNum = 0
        self.db = Database()
        
    def run(self):
        # main loop
        while True:
            # present main screen
            self.mainScreen()
            # choose an activity option
            choice = input("Make a selection: ")
            if choice == '1':
                # show user all papers
                self.viewPapers(self.db.getAllPapers())
            # exit application
            elif choice == '6':
                break
            else:
                print("Invalid Selection")
            
    
    def mainScreen(self):
        # Present all main options to the user
        
        options = ["1) See All Papers",
                   "2) Get Reviewers Within Range of Papers Reviewed",
                   "3) Sessions Authors Participated In",
                   "4) View Pie Chart of Top 5 Areas",
                   "5) View Bar Chart of Average Scores",
                   "6) Exit"]
        for option in options:
            print(option)
    
    def viewPapers(self,papers):
        # divide all papers into pages
        # papers is a list of dictionaries
        
        pages = self.makePages(papers)
        pageCount = len(pages)
        pageIndex = 0
        # print the first page
        self.printPage(pages[pageIndex])
        loop = True
        while loop:
            # get user input
            key = input("Please choose an action: ")
            print()
            # present the next page of papers
            if key == 'n':
                if pageIndex + 1 < pageCount:
                    pageIndex += 1
                else:
                    # notify the user they already at the last page
                    print("Already at the last page")
                self.printPage(pages[pageIndex])
            # present the user with the previous page of papers
            elif key == 'p':
                if pageIndex - 1 >= 0:
                    pageIndex -= 1
                # notify the user they are already on the first page
                else:
                    print("Already at the first page")
                self.printPage(pages[pageIndex])
                
            # if the user has choosen a paper, show them further options
            elif int(key) >= 1 and int(key) <= self.paperNum:
                loop = False
                self.decideAllPapers(int(key))

                
    
    
    def decideAllPapers(self,key):
        # print options for the selected paper
        # key is the paper id
        
        options = ["1) See all reviewers",
                   "2) Add New Review"]
        for option in options:
            print(option)
        # get decision from user and continue accordingly
        decision = int(input("Make a selection: "))
        if decision == 1:
            self.showReviewEmails(key)
        elif decision == 2:
            self.showPotentialReviewers(key)
        
    
    def showPotentialReviewers(self,key):
        # get all potential reviewers
        # key is the paper id
        
        emails = self.db.getPotentialReviewers(key)
        # notify the user if no potential reviewers exist
        if not emails:
            print("No reviewer options available")
            print()
            return
        # present the user with reviewer options
        options = []
        for i in range(len(emails)):
            options.append(str(i+1)+") "+emails[i][0])
        for option in options:
            print(option)
        # continue to add review page
        choice = int(input("Select a reviewer"))
        self.addReview(key,emails[choice-1][0])
        
    def addReview(self,paper,reviewer):
        # get all neccessary scores from the user
        # paper is the paper id
        # reviewer is the email address of the review
        
        scores = []
        scores.append(int(input("Originality: ")))
        scores.append(int(input("Importance: ")))
        scores.append(int(input("Soundness: ")))
        scores.append(int(input("Overall: ")))
        # input the score into the database
        self.db.inputReview(scores,paper,reviewer)
    
                
    def showReviewEmails(self,key):
        pass
    
    
         
    def printPage(self,page):
        # print requested page
        # page is a dict of papers
        
        print("Current papers:")
        for key,paper in page.items():
            print(str(key+1)+") "+paper[1])
        print("Next Page: n, Last Page: p")    
                    
            
    def makePages(self,papers):
        # split all papers into pages of 5
        # papers is a list of papers
        
        self.paperNum = len(papers)
        if self.paperNum % 5 == 0:
            pageCount = self.paperNum/5
        else:
            pageCount = (self.paperNum//5) + 1
        pageIndex = 0
        pages = []
        for i in range(pageCount):
            page = {}
            for i in range(5):
                if pageIndex == self.paperNum:
                    break
                page[pageIndex] = papers[pageIndex]
                pageIndex += 1
            pages.append(page)
        return pages


class Database:
    def __init__(self):
        self.db_path = "./assign3test.db"
        self.connection = sqlite3.connect(self.db_path)
        # self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.connection.close()
        
    def inputReview(self,scores,paper,reviewer):
        # add review to the database
        # scores is the list of scores for the review
        # paper is the paper id
        # reviewer is the email address of the reviewer
        
        string = '''INSERT INTO reviews
                    VALUES ({},'{}',{},{},{},{})'''.format(paper,reviewer,scores[0],
                                                         scores[1],scores[2],scores[3])
        self.cursor.execute(string)
        self.connection.commit()
        
    def getAllPapers(self):
        # get all papers in the database
        
        self.cursor.execute("SELECT * FROM papers;")
        papers = self.cursor.fetchall()
        return papers
    
    def getPaperReviewers(self,pID):
        # get reviewers for a certain paper
        # pID is the paper id
        
        self.cursor.execute("SELECT reviewer FROM reviews WHERE paper=:id;",{"id":pID})
        emails = self.cursor.fetchall() 
        return emails
    
    def getPotentialReviewers(self,pID):
        # get all potential reviewers for a certain paper
        # pID is the paper id
        
        string = '''SELECT e.reviewer
                    FROM papers p, expertise e
                    WHERE p.area = e.area and p.Id = {}
                    EXCEPT
                    SELECT r.reviewer
                    FROM reviews r
                    WHERE r.paper = {}'''.format(pID,pID) 
        self.cursor.execute(string)
        emails = self.cursor.fetchall()
        return emails
    
    def getAllReviews(self):
        # get all reviews
        # for testing purposes
        
        self.cursor.execute("SELECT * FROM reviews")
        reviews = self.cursor.fetchall()
        return reviews
    
        
        
        
    
if __name__ == "__main__":
    userUI = UI()
    userUI.run()
    #userUI.viewPapers(db.getAllPapers())