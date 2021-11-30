import numpy as np

from Vot_Scheme import *
from Happiness import Happiness

class VotingSituation:
    def __init__(self, voter_am, candidate_am):
        voting_vector = np.arange(0, candidate_am)

        self.candidate_am = candidate_am
        self.voting_matrix = np.repeat(voting_vector, repeats=voter_am).reshape((candidate_am, voter_am))
        self.shufflevote()

    def shufflevote(self):
        np.array([np.random.shuffle(x) for x in self.voting_matrix.T])

    def calculate_vote_given_matrix(self, voting_scheme, voting_matrix):
        scheme_vector = compute_vot_scheme(voting_scheme, voting_matrix.shape[0])
        voting_vector = np.zeros(self.candidate_am)
        for i in range(self.candidate_am):  # for each candidate / row in matrix
            for vote in voting_matrix[i]:
                if vote != -1:  # No vote
                    voting_vector[vote] += scheme_vector[i]

        return voting_vector

    def calculatevote(self, voting_scheme):
        return self.calculate_vote_given_matrix(voting_scheme, self.voting_matrix)

# situation = VotingSituation(10,5)
# scheme = VotingScheme.VOTE_FOR_TWO
# voting_results = situation.calculatevote(scheme)

# hapiness = Happiness(situation.voting_matrix, voting_results)
# print(hapiness.happiness)
