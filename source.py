import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


class UI:
    def __init__(self):
        self.paperNum = 0
        path = input("Enter database name: ")
        print()
        self.db = Database(path)
        
    def run(self):
        
        # main loop
        while True:
            # present main screen
            self.mainScreen()
            print()
            # choose an activity option
            choice = input("Make a selection: ")
            print()
            if choice == '1':
                # show user all papers
                self.viewPapers(self.db.getAllPapers())
            elif choice == '2':
                # show reviewers with review counts in a given range
                self.showReviewerInRange()
            elif choice == '3':
                # show number of sessions authors participated in
                self.showBarPlot()
            elif choice == '4':
                # get user to choose an author to see paper count
                self.showAuthors()
            elif choice == '5':
                # show pie chart for top 5 areas
                self.showPieChart()
            elif choice == '6':
                # show reviewer bar chart
                self.showReviewerBarChart()
            # exit application
            elif choice == '7':
                break
            else:
                print("Invalid Selection")

    def mainScreen(self):
        # Present all main options to the user
        
        options = ["1) See All Papers",
                   "2) Get Reviewers Within Range of Papers Reviewed",
                   "3) Sessions Authors Participated In Bar Plot",
                   "4) Sessions Authors Participated In Individual",
                   "5) View Pie Chart of Top 5 Areas",
                   "6) View Bar Chart of Average Scores",
                   "7) Exit"]
        for option in options:
            print(option)

    def showAuthors(self):
        # show all authors to the user
        
        # get authors a show them to the user in a list
        authors = self.db.getAuthors()
        for i in range(len(authors)):
            print(str(i+1)+") "+authors[i][0])
        
        # loop until the user has made a valid choice
        while True:
            try:
                print()
                choice = int(input("Choose an author: "))
                if choice < 1 or choice > len(authors):
                    raise ValueError
            except ValueError:
                print("Input must an integer with the given range")
                continue
            break
        
        self.showAuthorPaperCount(authors[choice-1][0])
            
    def showAuthorPaperCount(self,author):
        # show the number of accepted papers the author has
        # author is the email of the author
    
        count = self.db.getAuthorPaperCount(author)
        print()
        print("Author {} has participated in {} sessions".format(author,count[0]))
        print()

    def showBarPlot(self):
        # present the user with a bar plot of all the sessions each author
        # has participated in
        
        data = self.db.getBarPlotStats()
        plot = data.plot.bar(x="author")
        plt.plot()
        plt.show()

    def showReviewerInRange(self):
        # show all reviewers with review counts in a given range
        
        while True:
            try:
                low = int(input("Lower Bound: "))
                high = int(input("Upper Bound "))
                
                if low < 0 or high < 0:
                    raise ValueError
            except ValueError:
                print("Input must be a positive integer")
                continue
                
            break
            
        reviewers = self.db.getReviewersInRange(low,high)
        print()
        print("All reviewers within that range (inclusive)")
        for email in reviewers:
            print(email[0])
        print()

    def viewPapers(self,papers):
        # divide all papers into pages
        # papers is a list of dictionaries
        
        pages = self.makePages(papers)
        pageCount = len(pages)
        pageIndex = 0
        # print the first page
        self.printPage(pages[pageIndex])
        
        while True:
            print()
            # get user input
            key = input("Please make a selection: ")
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
            try:
                key = int(key)
                if key < 1 or key > self.paperNum:
                    raise ValueError
            except ValueError:
                print("Invalid input")
                continue
            break
            # if the user has choosen a paper, show them further options
        self.decideAllPapers(int(key))

    def decideAllPapers(self,key):
        # print options for the selected paper
        # key is the paper id
        
        options = ["1) See all reviewers",
                   "2) Add New Review"]
        for option in options:
            print(option)
        # get decision from user and continue accordingly
        loop = True
        while loop:
            try:
                print()
                decision = int(input("Make a selection: "))
                
                if decision == 1:
                    self.showReviewEmails(key)
                    loop = False
                elif decision == 2:
                    self.showPotentialReviewers(key)
                    loop = False
                else:
                    print("Input must be 1 or 2")
            except ValueError:
                print("Input must be an integer")                      

                
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
        
        while True:
            # continue to add review page
            try:
                choice = int(input("Select a reviewer"))
                if choice < 1 or choice > len(emails):
                    raise ValueError
            except ValueError:
                print("Invalid input given")
                continue
            break
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
        # print the reviewers for the paper that matches the key
        # key is the paper id
        
        reviews = self.db.getReviewEmails()
        # slim down list to reviews for the given paper
        reviews = reviews[reviews.paper == key]
        print()
        if reviews.empty:
            # no reviews for this paper exist
            print("No reviewers have reviewed this paper")
        else:
            print(reviews.reviewer.to_string(index=False))
        print()
    
    def showPieChart(self):
        # show a pie chart of the most popular areas
        
        areas = self.db.getPieAreas()
        plot=areas.plot.pie(labels=areas.Area, y="Count")
        plt.plot()
        plt.show()

    def showReviewerBarChart(self):
        # show a bar chart of each reviewers average scores
        
        reviews = self.db.getReviewerBarChart()
        reviews.plot.bar(x='reviewer')
        plt.plot()
        plt.show()

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
        
        # calculate how many pages will be needed
        self.paperNum = len(papers)
        if self.paperNum % 5 == 0:
            pageCount = self.paperNum/5
        else:
            pageCount = (self.paperNum//5) + 1
        pageIndex = 0
        pages = []
        
        # create pages
        for i in range(pageCount):
            page = {}
            # Add 5 papers to the page, or break upon running out of papers
            for i in range(5):
                if pageIndex == self.paperNum:
                    break
                page[pageIndex] = papers[pageIndex]
                pageIndex += 1
            pages.append(page)
        return pages


class Database:
    def __init__(self, path):
        self.db_path = path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.connection.close()
    
    def getReviewerBarChart(self):
        # get average marks for all reviewers
        
        reviews = pd.read_sql_query(
            '''SELECT reviewer, AVG(originality) as Originality, AVG(importance) as Importance, AVG(soundness) as Soundness, AVG(overall) as Overall 
            FROM reviews 
            GROUP BY reviewer''', self.connection)
        return reviews

    def getPieAreas(self):
        # get number of papers in each area
        # get the 5th largest and keep ties
        areas = pd.read_sql_query('''
        SELECT area as Area, COUNT(*) as Count 
        FROM papers
        GROUP BY Area
        HAVING Count >= 
        (
        SELECT COUNT(*)
        FROM papers
        GROUP BY Area
        ORDER BY COUNT(*) DESC
        LIMIT 1 OFFSET 4
        ) 
        OR (
        SELECT COUNT(DISTINCT area)
        FROM papers
)       <= 5''', self.connection)

        return areas
    
    def getReviewEmails(self):
        # get reviewer emails
        
        reviews = pd.read_sql_query("SELECT paper, reviewer FROM reviews", self.connection)
        return reviews

    def getAuthorPaperCount(self,author):
        # gets the accepted paper count of an author
        # author is the email address of the author
        
        string = '''SELECT COUNT(CASE WHEN p.decision = 'A' THEN 1 ELSE NULL END) as paperCount
                    FROM papers p
                    WHERE p.author = '{}'
                    GROUP BY p.author'''.format(author)
        self.cursor.execute(string)
        count = self.cursor.fetchone()
        return count

    def getAuthors(self):
        # get all distinct authors
        
        string = '''SELECT DISTINCT p.author
                    FROM papers p'''
        self.cursor.execute(string)
        authors = self.cursor.fetchall()
        return authors

    def getBarPlotStats(self):
        # get the number of papers that have been accepted for each author
        
        string = '''SELECT p.author, COUNT(CASE WHEN p.decision = 'A' THEN 1 ELSE NULL END) as paperCount
                    FROM papers p
                    GROUP BY p.author;'''
        data = pd.read_sql_query(string,self.connection)
        return data

    def inputReview(self,scores,paper,reviewer):
        # add review to the database
        # scores is the list of scores for the review
        # paper is the paper id
        # reviewer is the email address of the reviewer
        
        string = '''INSERT INTO reviews
                    VALUES ({},'{}',{},{},{},{});'''.format(paper,reviewer,scores[0],
                                                         scores[1],scores[2],scores[3])
        self.cursor.execute(string)
        self.connection.commit()
        
    def getAllPapers(self):
        # get all papers in the database
        
        self.cursor.execute("SELECT * FROM papers;")
        papers = self.cursor.fetchall()
        return papers

    def getPotentialReviewers(self,pID):
        # get all potential reviewers for a certain paper
        # pID is the paper id
        
        string = '''SELECT e.reviewer
                    FROM papers p, expertise e
                    WHERE p.area = e.area and p.Id = {}
                    EXCEPT
                    SELECT r.reviewer
                    FROM reviews r
                    WHERE r.paper = {};'''.format(pID,pID) 
        self.cursor.execute(string)
        emails = self.cursor.fetchall()
        return emails
    
    def getAllReviews(self):
        # get all reviews
        # for testing purposes
        
        self.cursor.execute("SELECT * FROM reviews;")
        reviews = self.cursor.fetchall()
        return reviews
    
    def getReviewersInRange(self,low,high):
        # get all reviewers with review count in the given range (inclusive)
        # low in the lower bound of the range
        # high is the upper bound of the range
        
        string = '''SELECT e.reviewer, COUNT(CASE WHEN e.reviewer = r.reviewer
                    THEN 1 ELSE NULL END) as caseCount
                    FROM (SELECT DISTINCT reviewer FROM expertise) as e, reviews r 
                    GROUP BY e.reviewer
                    HAVING caseCount >= {} AND caseCount <= {};'''.format(low,high)
        self.cursor.execute(string)
        emails = self.cursor.fetchall()
        return emails

if __name__ == "__main__":
    userUI = UI()
    userUI.run()