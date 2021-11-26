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

    def calculatevote(self, voting_scheme):
        scheme_vector = compute_vot_scheme(voting_scheme, self.voting_matrix.shape[1])
        voting_vector = np.zeros(self.candidate_am)
        for i in range(self.candidate_am):
            for vote in self.voting_matrix[i]:
                voting_vector[vote] += scheme_vector[i]

        return voting_vector


situation = VotingSituation(10,5)
scheme = VotingScheme.VOTE_FOR_TWO
voting_results = situation.calculatevote(scheme)

hapiness = Happiness(situation.voting_matrix, voting_results)
print(hapiness.happiness)
