import numpy as np
import pickle
from typing import Optional, Tuple, List, Dict, Any
from matplotlib import pyplot as plt
import math
from itertools import permutations, combinations


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


def exp_bullet_voting(voters: Optional[int] = 10, options: Optional[int] = 4):
    kargs = {
        "voters": voters,
        "candidates": options,
        "allow_bullet_voting": True,
    }

    tva, result = run_exp(**kargs)

    # plot number of tv
    def job(tva, restul, title):
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

            ax.set_title(f"{title} - {scheme}")
            ax.set_xlabel("Voter")
            ax.set_ylabel("Happiness")

            ax.bar(
                range(1, voters + 1),
                new_happiness,
                yerr=new_happiness_std,
                label="New Happiness",
                capsize=20,
            )
            ax.bar(
                range(1, voters + 1),
                original_happiness,
                capsize=20,
                label="Original Happiness",
            )
            ax.legend()
            fig.show()

    kargs = {
        "voters": voters,
        "candidates": options,
        "allow_bullet_voting": True,
    }

    print("-- With bullet voting --")
    tva, result = run_exp(**kargs)
    job(tva, result, "Change of happiness with bullet voting")

    kargs = {
        "situation": tva.situation,
        "allow_bullet_voting": False,
    }

    print("\n\n-- Without bullet voting --")
    tva, result = run_exp(**kargs)
    job(tva, result, "Change of happiness without bullet voting")


def exp_coation(
    voters: Optional[int] = 5, options: Optional[int] = 3, coalition: Optional[int] = 2,
):
    kargs = {
        "voters": voters,
        "candidates": options,
        "advance_voters_coalition": coalition,
    }
    tva, result = run_exp(**kargs)

    hist_plot_total_tactical_votes_available_per_voter(
        math.comb(voters, coalition), result
    )
    bar_plot_total_tactical_votes_available_per_voter(
        math.comb(voters, coalition), result
    )

    coalitions = list(combinations(range(voters), coalition))

    for scheme in VotingScheme:
        # get avg happiness
        happiness = Happiness(
            tva.situation.voting_matrix, tva.situation.calculatevote(scheme)
        )
        original_happiness = happiness.individual_happiness
        happiness_data = [[] for i in range(voters)]

        for coalition, coalition_res in enumerate(result[scheme.name][0]):
            for tv in coalition_res:
                if tv is not None and len(tv) != 0:
                    for v in coalitions[coalition]:  # each voter in the coalition
                        happiness_data[v].append(tv[2])
        new_happiness = [np.average(i) for i in happiness_data]
        new_happiness_std = [np.std(i) for i in happiness_data]

        fig, ax = plt.subplots(figsize=(13, 6))

        ax.set_title(f"Change of happiness with coalitions {coalition} - {scheme}")
        ax.set_xlabel("Voter")
        ax.set_ylabel("Happiness")

        ax.bar(
            range(1, voters + 1),
            new_happiness,
            yerr=new_happiness_std,
            capsize=20,
            label="New Happiness",
        )
        ax.bar(
            range(1, voters + 1),
            original_happiness,
            capsize=20,
            label="Original Happiness",
        )
        ax.legend()
        fig.show()


if __name__ == "__main__":
    np.random.seed(42)
    print("###### BULLET VOTING ########")
    exp_bullet_voting()

    print("###### COALITIONS ########")
    exp_coation()
