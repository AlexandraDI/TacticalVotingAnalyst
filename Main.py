from VotingSituation import VotingSituation
from Vot_Scheme import VotinngScheme

def getOutcome(voters, candidates):
    preferencesMatrix = VotingSituation(voters, candidates).voting_matrix
    print(preferencesMatrix[0])


# make function to take preferences and voting-scheme, outputs non strategic outcome
# calculate happiness based on non-strategic outcome
