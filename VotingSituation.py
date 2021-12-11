"""
This module defines the voting situation

It contains:
    * VotingSituation: class representing the voting situation
"""

import numpy as np

from Vot_Scheme import VotingScheme, compute_vot_scheme
from Happiness import Happiness


class VotingSituation:
    """
    This class simulate a voting as matrix containg the preference of the voters.

    Each column of the matrix is a voter. The order of the columns doe not matter.

    The rows represent the preference of each voter. The first row is the highest
    preference.

    The values in the matrix identify the different candidates.
    """

    def __init__(self, voter_am: int, candidate_am: int) -> None:
        """
        Args:
            voter_am: number of voters
            candidate_am: number of candidates
        """
        voting_vector = np.arange(0, candidate_am)

        self.candidate_am = candidate_am
        self.voting_matrix = np.repeat(voting_vector, repeats=voter_am).reshape(
            (candidate_am, voter_am)
        )
        self.shufflevote()

    def shufflevote(self) -> None:
        """
        Shuffle the preference matrix to generate a new situation
        Returns:
            None: DESCRIPTION.

        """
        np.array([np.random.shuffle(x) for x in self.voting_matrix.T])

    def calculate_vote_given_matrix(
        self, voting_scheme: VotingScheme, voting_matrix: np.array
    ) -> np.array:
        """
        Compute the outcome of the votation

        Args:
            voting_scheme: scheme used to assign votes
            voting_matrix: voting situation

        Returns:
            voting_vector: number of votes for the each candidate.
            The vector is sorted by candidate and not by number of votes.
            [votes candidate 1, votes candidate 2, ..., votes candidate n]

        """
        scheme_vector = compute_vot_scheme(voting_scheme, voting_matrix.shape[0])
        voting_vector = np.zeros(self.candidate_am)
        for i in range(self.candidate_am):  # for each candidate / row in matrix
            for vote in voting_matrix[i]:
                if vote != -1:  # No vote
                    voting_vector[vote] += scheme_vector[i]

        return voting_vector

    def calculatevote(self, voting_scheme):
        """
        Compute the outcome of this voting situation

        Args:
            voting_scheme: scheme used to assign votes

        Returns:
            voting_vector: number of votes for the each candidate.
            The vector is sorted by candidate and not by number of votes.
            [votes candidate 1, votes candidate 2, ..., votes candidate n]

        """
        return self.calculate_vote_given_matrix(voting_scheme, self.voting_matrix)


if __name__ == "__main__":
    print("Tesing the voting situation and the happiness function.")
    print("Edit this file for other experiments.")
    VOTERS = 10
    CANDIDATES = 5
    SCHEME = VotingScheme.VOTE_FOR_TWO

    situation = VotingSituation(VOTERS, CANDIDATES)
    voting_results = situation.calculatevote(SCHEME)

    hapiness = Happiness(situation.voting_matrix, voting_results)
    print("Overall happiness:", hapiness.happiness)
    hapiness.get_happiness(
        situation.voting_matrix, hapiness.get_voter_happiness_dictatorship
    )
    print("Overall happiness (dictatorship):", hapiness.happiness)
    hapiness.get_happiness(
        situation.voting_matrix, hapiness.get_voter_happiness_vector_distance
    )
    print("Overall happiness (vector distance):", hapiness.happiness)
