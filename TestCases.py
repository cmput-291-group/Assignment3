from source import Database


class Tests:
    def __init__(self):
        self.db = Database()
    
    def run(self):
        self.testGetAllPapers()
    
    def testGetPaperReviewers(self):
        pass
    
    def testGetAllPapers(self):
        expected = [(1, 'Bass players are undervalued big time', 'A', 'DB', 'Harry@Email', 'DB'), (2, 'System of a Down rocks!', 'A', 'SE', 'Harry@Email', 'SE'), (3, 'Three moons are better than one', 'A', 'SE', 'Ron@Email', 'SE'), (4, 'Donald was not always been a duck', 'R', 'SE', 'Hermoine@Email', 'SE'), (5, 'Mickey and Anakin are bothers', 'R', 'SE', 'Snape@Email', 'SE'), (6, 'Previous text here caused an error', 'A', 'DB', 'Harry@Email', 'DB')]
        
        if self.db.getAllPapers == expected:
            print("Get all papers has passed")
        else:
            print("Get all papers has failed")


if __name__ == "__main__":
    tests = Tests()
    tests.run()