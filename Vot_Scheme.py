"""
This module defines the voting schemes.

It contains:
    * VotingScheme: the enumerator used to identify the different schemes
    * compute_vot_scheme: a function that generate the voting vector
"""

import enum
import numpy as np


class VotingScheme(enum.Enum):
    """
    Enumerator that identify the voting schemes
    """

    VOTE_FOR_ONE = 1
    VOTE_FOR_TWO = 2
    VETO = 3
    BORDA = 4


def compute_vot_scheme(scheme: VotingScheme, candidate_am: int) -> np.array:
    """
    Function to generate the voting vectors

    Args:
        scheme (VotingScheme): the scheme needed.
        candidate_am (int): number of candidates.

    Returns:
        Numpy array containing the amount of votes for each candidate.
        The array is sorted by preference:
            [votes 1st pref., votes 2nd pref., ..., vote last pref.]
        The length of the array is candidate_am
    """
    vot_scheme = np.zeros(candidate_am)
    # Only selects the preferred candidate of the voter
    if scheme == VotingScheme.VOTE_FOR_ONE:
        vot_scheme[0] = 1

    # Only selects the preferred 2 candidates of the voter
    elif scheme == VotingScheme.VOTE_FOR_TWO:
        vot_scheme[0:2] = 1

    # Selects all the candidates, except for the least favourite
    elif scheme == VotingScheme.VETO:
        vot_scheme[:-1] = 1

    # Use a ranking on the preferred candidates
    elif scheme == VotingScheme.BORDA:
        for i in range(1, candidate_am):
            vot_scheme[i - 1] = candidate_am - i
    return vot_scheme
