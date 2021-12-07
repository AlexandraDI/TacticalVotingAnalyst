import numpy as np
import pickle
from typing import Optional, Tuple, List, Dict, Any
from matplotlib import pyplot as plt

from Main import (
    bar_plot_happiness_per_scheme,
    bar_plot_happiness_per_scheme_many_voters,
    hist_plot_total_tactical_votes_available_per_voter,
    bar_plot_total_tactical_votes_available_per_voter,
)

from TacticalVotingRisk import TacticalVotingRisk
from Vot_Scheme import VotingScheme
from Happiness import Happiness


def run_exp(**kargs: Dict[str, Any]) -> Tuple[TacticalVotingRisk, List]:
    """
    Run the tva, print some stats and return the results and the tva

    Args:
        **kargs (dict): arguments for the tva.

    Returns:
        tva: TacticalVotingRisk.
        result: risk results from the tva.

    """
    tva = TacticalVotingRisk(**kargs)
    result = tva.compute_risk()
    print("--------\nOriginal voting Matrix = \n", tva.situation.voting_matrix)
    for scheme in VotingScheme:
        print("-------------")
        print("RISK FOR SCHEME: ", scheme.name)
        risks = result[scheme.name][1]
        total_risk = 0
        for r in risks:
            total_risk += r
        print("Individual risk list: ", risks)
        print("Total risk: ", total_risk)
        print("Average risk: ", result[scheme.name][2])
        print("Average bool risk: ", result[scheme.name][3])
    return tva, result


def exp_bullet_voting(
    voters: Optional[int] = 10,
    options: Optional[int] = 4,
    save: Optional[bool] = False,
    load: Optional[str] = None,
):
    kargs = {
        "voters": voters,
        "candidates": options,
        "allow_bullet_voting": True,
    }
    if load is not None:
        with open(f"{load}_tva.pkl", "rb") as f:
            tva = pickle.load(f)
        with open(f"{load}_result.pkl", "rb") as f:
            result = pickle.load(f)
    else:
        tva, result = run_exp(**kargs)

    if save:
        with open(f"bullet_{voters}_{options}_tva.pkl", "wb") as f:
            pickle.dump(tva, f)
        with open(f"bullet_{voters}_{options}_result.pkl", "wb") as f:
            pickle.dump(result, f)

    # plot number of tv
    hist_plot_total_tactical_votes_available_per_voter(voters, result)
    bar_plot_total_tactical_votes_available_per_voter(voters, result)

    for scheme in VotingScheme:
        # get avg happiness
        happiness = Happiness(
            tva.situation.voting_matrix, tva.situation.calculatevote(scheme)
        )
        original_happiness = happiness.individual_happiness
        new_happiness = [0 for i in range(voters)]
        new_happiness_std = [0 for i in range(voters)]

        for voter, voter_res in enumerate(result[scheme.name][0]):
            tmp = []
            for tv in voter_res:
                if tv is not None and len(tv) != 0:
                    tmp.append(tv[2])
            new_happiness[voter] = np.average(tmp)
            new_happiness_std[voter] = np.std(tmp)

        # plot happiness
        fig, ax = plt.subplots(figsize=(13, 6))

        ax.set_title(f"Change of happiness - {scheme}")
        ax.set_xlabel("Voter")
        ax.set_ylabel("Happiness")

        ax.bar(
            range(1, voters + 1),
            new_happiness,
            yerr=new_happiness_std,
            label="New Happiness",
        )
        ax.bar(range(1, voters + 1), original_happiness, label="Original Happiness")
        ax.legend()
        fig.show()


def exp_coation(
    voters: Optional[int] = 10,
    options: Optional[int] = 4,
    coalition: Optional[int] = 2,
    save: Optional[bool] = False,
):
    pass


if __name__ == "__main__":
    np.random.seed(42)
    exp_bullet_voting()
