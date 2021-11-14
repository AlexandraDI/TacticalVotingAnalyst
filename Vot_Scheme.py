import enum
import numpy as np


# Enum of the possible voting schemes
class VotingScheme(enum.Enum):
    vote_for_one = 1
    vote_for_two = 2
    veto = 3
    borda = 4


def compute_vot_scheme(scheme, m):
    vot_scheme = np.zeros(m)
    # Only selects the preferred candidate of the voter
    if scheme == VotingScheme.vote_for_one:
        vot_scheme[0] = 1

    # Only selects the preferred 2 candidates of the voter
    elif scheme == VotingScheme.vote_for_two:
        vot_scheme[0:2] = 1

    # Selects all the candidates, except for the least favourite
    elif scheme == VotingScheme.veto:
        vot_scheme[:-1] = 1

    # Use a ranking on the preferred candidates
    elif scheme == VotingScheme.borda:
        for i in range(1, m):
            vot_scheme[i - 1] = m - i
    return vot_scheme


# Number of candidates
m = 10


def display_all_schemes():
    for vot_scheme in VotingScheme:
        print(vot_scheme, ': ', compute_vot_scheme(vot_scheme, m))


display_all_schemes()
