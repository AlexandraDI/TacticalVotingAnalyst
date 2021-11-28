from TacticalVotingRisk import TacticalVotingRisk
from VotingSituation import VotingSituation
from Vot_Scheme import VotingScheme, compute_vot_scheme
import numpy as np
# import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

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


if __name__ == "__main__":

    # Basic TVA
    voters = 15
    candidates = 3
    t = TacticalVotingRisk(voters, candidates)
    result = t.compute_risk()


    for scheme in VotingScheme:
        print(scheme.name)
        for voter in range(voters):
            print(f'How many tactical votes voter {voter} : {result[scheme.name][1][voter]}')

        print("---------------------------------------------------------------------------------------------")

    fig, ax = plt.subplots(1, 4,figsize=(14,4))

    for scheme in VotingScheme:
        print(f'scheme : {scheme.value}')

        ax[scheme.value - 1].hist(result[scheme.name][1], alpha=0.5)
        # ax.hist(result[scheme.name][1], facecolor='blue', alpha=0.5)

        # adding labels
        ax[scheme.value - 1].set_xlabel('voter')
        ax[scheme.value - 1].set_ylabel('total tactical votes available')

        # Set title
        ax[scheme.value - 1].set_title(scheme.name.replace("_", " "))

    plt.show()