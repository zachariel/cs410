import csv

class Occupations(object):
    occupations = []
    def __init__(self, path="../docs/occupations.txt", headers=True):
        self.path = path
        self.headers = headers

    def occupations(self):
        self.occupations = list(csv.reader(open(self.path, 'r'), delimiter='\t'))
        if self.headers:
            del self.occupations[0]

        return self.occupations


def occupations():
    return Occupations().occupations()
