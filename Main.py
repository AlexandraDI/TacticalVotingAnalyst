from math import factorial

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
    voters = 10
    candidates = 3
    t = TacticalVotingRisk(voters, candidates)
    result = t.compute_risk()


    # for scheme in VotingScheme:
    #     print(scheme.name)
    #     print(f'How many tactical votes for all voters: {result[scheme.name][1]}')
    #     for voter in range(voters):
    #         print(f'How many tactical votes voter {voter} : {result[scheme.name][1][voter]}')
    #     print("---------------------------------------------------------------------------------------------")


    plot_voters = [str(item) for item in range(1, voters+1)]

    fig, ax = plt.subplots(1, 4, figsize=(13, 4))

    for scheme in VotingScheme:
        # creating the bar plot
        ax[scheme.value - 1].bar(plot_voters, result[scheme.name][1], color='maroon',
            width=0.4)
        # adding x label
        ax[scheme.value - 1].set_xlabel("Voter")
        # Set title
        ax[scheme.value - 1].set_title(scheme.name.replace("_", " "))

    # adding y label
    ax[0].set_ylabel("Total tactical votes available")
    plt.show()