from source import Database


class Tests:
    def __init__(self):
        self.db = Database()
    
    def run(self):
        self.testGetAllPapers()
        self.testGetPaperReviewers()
        self.testPotentialReviewers()
        # self.testInsert()
        self.testGetRange()
    
    def testGetPaperReviewers(self):
        testPassed = True
        expected1 = [('Minnie@Email',), ('Donald@Email',), ('Mickey@Email',)]
        expected2 = [("Anakin@Email",),("Darth@Email",),("Pluto@Email",)]
        expected3 = [("C3P0@Email",),("R2D2@Email",),("Tom@Email",)]
        # case 1
        testPassed = self.db.getPaperReviewers(1) == expected1
        # case 2
        testPassed = self.db.getPaperReviewers(2) == expected1
        # case 3
        testPassed = self.db.getPaperReviewers(3) == expected2
        # case 4
        testPassed = self.db.getPaperReviewers(4) == expected2
        # case 5
        testPassed = self.db.getPaperReviewers(5) == expected3
    
        if testPassed == True:
            print("Getting paper reviewers has passed")
        else:
            print("Getting paper reviewers has failed")
    
    def testGetAllPapers(self):
        expected = [(1, 'Bass players are undervalued big time', 'A', 'DB', 'Harry@Email', 'DB'), (2, 'System of a Down rocks!', 'A', 'SE', 'Harry@Email', 'SE'), (3, 'Three moons are better than one', 'A', 'SE', 'Ron@Email', 'SE'), (4, 'Donald was not always been a duck', 'R', 'SE', 'Hermoine@Email', 'SE'), (5, 'Mickey and Anakin are bothers', 'R', 'SE', 'Snape@Email', 'SE'), (6, 'Previous text here caused an error', 'A', 'DB', 'Harry@Email', 'DB')]
        
        if self.db.getAllPapers() == expected:
            print("Get all papers has passed")
        else:
            print("Get all papers has failed")
            
    def testPotentialReviewers(self):
        testPassed = True
        expected6 = [("Mickey@Email",),("Donald@Email",)]
        expected2 = [("Tom@Email",),("Jerry@Email",),("Anakin@Email",),
                    ("Darth@Email",),("Pluto@Email",),("R2D2@Email",),
                    ("C3P0@Email",)]
        expected3 = [("Tom@Email",),("Jerry@Email",),("Minnie@Email",),("R2D2@Email",),
                    ("C3P0@Email",)]
        expected4 = [("Tom@Email",),("Jerry@Email",),("Minnie@Email",),("R2D2@Email",),
                    ("C3P0@Email",)]
        expected5 = [("Jerry@Email",),("Anakin@Email",),
                    ("Darth@Email",),("Pluto@Email",),("Minnie@Email",)]        
        
        
        # case 1
        testPassed = self.db.getPotentialReviewers(1) == []
        # case 2
        testPassed = set(self.db.getPotentialReviewers(2)) == set(expected2)
        # case 3
        testPassed = set(self.db.getPotentialReviewers(3)) == set(expected3)
        # case 4
        testPassed = set(self.db.getPotentialReviewers(4)) == set(expected4)
        # case 5
        testPassed = set(self.db.getPotentialReviewers(5)) == set(expected5)
        # case 6
        testPassed = set(self.db.getPotentialReviewers(6)) == set(expected6)
        
        if testPassed == True:
            print("Get Potential Reviewers has passed")
        else:
            print("Get Potential Reviewers has failed")
            
        
    def testInsert(self):
        before = self.db.getAllReviews()
        self.db.inputReview([3,3,3,3],2,"Minnie@Email")
        after = self.db.getAllReviews()
        if after != before:
            print("Insert passed")
        else:
            print("Insert failed")
            
    def testGetRange(self):
        testPassed = True
        expected1 = [("C3P0@Email",1,),("R2D2@Email",1,),("Tom@Email",1,)]
        expected0 = [("Jerry@Email",0,)]
        # case 1
        testPassed = self.db.getReviewersInRange(1,1) == expected1
        testPassed = self.db.getReviewersInRange(0,0) == expected0
        
        if testPassed == True:
            print("Get range test passed")
        else:
            print("Get range test failed")


if __name__ == "__main__":
    tests = Tests()
    tests.run()