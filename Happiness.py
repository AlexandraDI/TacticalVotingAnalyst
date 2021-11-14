import numpy as np


class Happiness:

    def __init__(self, voting_matrix, election_vector):
        self.election_vector = election_vector
        self.happiness = 0
        self.get_happiness(voting_matrix)


    def get_voter_happiness(self, voter_p):
        weight = len(voter_p)
        happiness = 0
        total_votes = np.sum(self.election_vector)
        for i, v in enumerate(voter_p):
            happiness += (self.election_vector[v - 1] / total_votes) * (weight - i)
        return happiness

    def get_happiness(self, voting_matrix):
        for voter in voting_matrix:
            self.happiness += self.get_voter_happiness(voter)