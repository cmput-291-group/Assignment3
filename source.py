import sqlite3


    

class UI:
    def __init__(self):
        self.paperNum = 0
    
    def viewPapers(self,papers):
        pages = self.makePages(papers)
        pageCount = len(pages)
        pageIndex = 0
        self.printPage(pages[pageIndex])
        while True:
            key = input("Please choose an action: ")
            print()
            if key == 'n':
                if pageIndex + 1 < pageCount:
                    pageIndex += 1
                else:
                    print("Already at the last page")
                self.printPage(pages[pageIndex])
                
            elif key == 'p':
                if pageIndex - 1 >= 0:
                    pageIndex -= 1
                else:
                    print("Already at the first page")
                self.printPage(pages[pageIndex])
            elif key >= 1 and key <= self.paperNum:
                self.showReviewEmails(key)
                
                
    def showReviewEmails(key):
        pass
    
    
         
    def printPage(self,page):
        print("Current papers:")
        for key,paper in page.items():
            print(str(key+1)+") "+paper[1])
        print("Next Page: n, Last Page: p")    
                    
            
    def makePages(self,papers):
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
        
    def getAllPapers(self):
        self.cursor.execute("SELECT * FROM papers;")
        papers = self.cursor.fetchall()
        return papers
    
    def getPaperReviewers(self,pID):
        pID = (pID)
        self.cursor.execute
        ('''SELECT reviewer
            FROM reviews
            WHERE paper=:id
            GROUP BY reviewer,paper;''',{"id":pID})
        emails = self.cursor.fetchall()
        return emails
        
        
    
if __name__ == "__main__":
    userUI = UI()
    db = Database()
    userUI.viewPapers(db.getAllPapers())