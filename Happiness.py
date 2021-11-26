import numpy as np


class Happiness:
    def __init__(self, voting_matrix, election_vector):
        self.election_vector = election_vector
        self.happiness = 0
        self.individual_happiness = np.ndarray(voting_matrix.shape[1])
        self.get_happiness(voting_matrix)


    # change to range -2 to 2
    def get_voter_happiness(self, voter_p):
        weight = np.arange(len(voter_p), -len(voter_p), -2)
        happiness = 0
        total_votes = np.sum(self.election_vector)
        for i, v in enumerate(voter_p):
            happiness += (self.election_vector[v - 1] / total_votes) * (weight[i])
        return happiness

    def get_happiness(self, voting_matrix):
        self.happiness = 0
        for voter in range(voting_matrix.shape[1]):
            self.individual_happiness[voter] = self.get_voter_happiness(voting_matrix[:,voter])
        self.happiness = np.sum(self.individual_happiness)
