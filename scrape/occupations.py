import csv

class Occupations(object):
    """
    Class used to read text file containing all O*Net code and occupation titles.
    """
    occupations = []
    def __init__(self, path="../data/occupations.txt", headers=True):
        """
        Params:
        -------
        path : string
            Path to file containing list of occupations.

        headers : boolean
            Flag to indicate if header should be skiped.
        """
        self.path = path
        self.headers = headers

    def occupations(self):
        """
        Return all occupations found.

        Return:
        -------
        occupations : list
            List with occupations, each row contain array with occupation info.
        """
        self.occupations = list(csv.reader(open(self.path, 'r'), delimiter='\t'))
        if self.headers:
            del self.occupations[0]

        return self.occupations


def occupations():
    """
    Helper to fetch all occupations.
    """
    return Occupations().occupations()
