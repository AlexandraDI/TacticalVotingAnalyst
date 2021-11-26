import numpy as np

class VotingSituation:
    def __init__(self, voter_am, candidate_am):
        voting_vector = np.arange(1, candidate_am + 1)
        self.voting_matrix = np.repeat(voting_vector, repeats=voter_am).reshape((candidate_am, voter_am))
        self.shufflevote()

    def shufflevote(self):
        np.array([np.random.shuffle(x) for x in self.voting_matrix.T])
