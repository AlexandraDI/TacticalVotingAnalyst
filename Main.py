from VotingSituation import VotingSituation
from Vot_Scheme import VotingScheme, compute_vot_scheme
import numpy as np

def getOutcome(voters, candidates, scheme_type):

    scheme = compute_vot_scheme(scheme_type, candidates)

    preferencesMatrix = VotingSituation(voters, candidates).voting_matrix

    votes_per_candidate = [0 for i in range(candidates)]

    for voter in range(voters):
        for pref in range(candidates):
            i = preferencesMatrix[pref, voter]
            print(i)
            votes_per_candidate[i - 1] += scheme[pref]

    print(preferencesMatrix[0])
    return votes_per_candidate

# make function to take preferences and voting-scheme, outputs non strategic outcome
# calculate happiness based on non-strategic outcome
