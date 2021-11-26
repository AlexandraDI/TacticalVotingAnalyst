import enum
import numpy as np


# Enum of the possible voting schemes
class VotingScheme(enum.Enum):
    VOTE_FOR_ONE = 1
    VOTE_FOR_TWO = 2
    VETO = 3
    BORDA = 4


def compute_vot_scheme(scheme, candidate_am):
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
