"""
This module defines the happiness functions.

It contains:
    * Happiness: class representing the happiness function
"""
import math
from typing import Optional, Callable
import numpy as np


class Happiness:
    """
    Class that contain the happiness functions, the current happiness
    of the voters and the overall happiness
    """

    def __init__(self, voting_matrix: np.array, election_vector: np.array) -> None:
        """
        Args:
            voting_matrix: matrix containing the voting situation
            election_vetctor: outcome of the voting
        """
        self.election_vector = election_vector
        self.happiness = 0
        self.individual_happiness = np.ndarray(voting_matrix.shape[1])
        self.get_happiness(voting_matrix, self.get_voter_happiness)

    def get_voter_happiness(self, voter_p: np.array) -> float:
        """
        Args:
            voter_p: preference of a single voter

        Returns:
            happiness for this voter
        """
        weight = np.arange(len(voter_p), -len(voter_p), -2)
        happiness = 0
        total_votes = np.sum(self.election_vector)
        for i, v in enumerate(voter_p):
            happiness += (self.election_vector[v - 1] / total_votes) * (weight[i])
        return happiness

    def get_voter_happiness_dictatorship(self, voter_p: np.array) -> float:
        """
        Alternative happiness function

        Args:
            voter_p: preference of a single voter

        Returns:
            happiness for this voter
        """
        weight = np.array([1] + [0] * (len(voter_p) - 1))
        happiness = 0
        total_votes = np.sum(self.election_vector)
        for i, v in enumerate(voter_p):
            happiness += (self.election_vector[v - 1] / total_votes) * (weight[i])
        return happiness

    def get_voter_happiness_vector_distance(self, voter_p: np.array) -> float:
        """
        Alternative happiness function

        Args:
            voter_p: preference of a single voter

        Returns:
            happiness for this voter
        """
        ordered_voting_result = np.sort(self.election_vector)[::-1]
        total_distance = 0
        for i, candidate_points in enumerate(self.election_vector):
            position = np.where(ordered_voting_result == candidate_points)
            total_distance += abs(position[0][0] - voter_p[i]) * (len(voter_p) - i)

        worst_distance = math.factorial(len(voter_p))
        return (worst_distance - total_distance) / worst_distance

    def get_happiness(
        self,
        voting_matrix: np.array,
        happiness_func: Optional[Callable[[np.array], float]] = get_voter_happiness,
    ) -> None:
        """
        Compute the overall happiness given an happiness function.

        The value can be retrieved from the :happiness: attribute.

        Args:
            voting_matrix: matrix containing the voting situation
            happiness_func: function that return the happiness of a single voter

        Returns:
            None.

        """
        self.happiness = 0
        for voter in range(voting_matrix.shape[1]):
            self.individual_happiness[voter] = happiness_func(voting_matrix[:, voter])
        self.happiness = np.sum(self.individual_happiness)
