"""
This module perform the experiments for the Basic TVA.
It also define functions to plot the results.
"""
from typing import Tuple
import matplotlib.pyplot as plt
from TacticalVotingRisk import TacticalVotingRisk
from Vot_Scheme import VotingScheme


# make function to take preferences and voting-scheme, outputs non strategic outcome
# calculate happiness based on non-strategic outcome
def bar_plot_total_tactical_votes_available_per_voter(
    voters: int, result: Tuple
) -> None:
    """
    Generate bar plot with the number of tactical votes for each voters
    for each scheme.

    Args:
        voters: number of voters
        result: result structure from TacticalVotingRisk

    Returns:
        None.

    """
    plot_voters = [str(item) for item in range(1, voters + 1)]

    _, ax = plt.subplots(1, 4, figsize=(13, 4))

    for scheme in VotingScheme:
        # creating the bar plot
        ax[scheme.value - 1].bar(
            plot_voters, result[scheme.name][1], color="maroon", width=0.4
        )
        # adding x label
        ax[scheme.value - 1].set_xlabel("Voter")
        # Set title
        ax[scheme.value - 1].set_title(scheme.name.replace("_", " "))

    # adding y label
    ax[0].set_ylabel("Total tactical votes available")
    plt.show()


def hist_plot_total_tactical_votes_available_per_voter(
    voters: int, result: Tuple
) -> None:
    """
    Generate histogram with the number of tactical votes for each scheme.

    Args:
        voters: number of voters
        result: result structure from TacticalVotingRisk

    Returns:
        None.

    """
    _, ax = plt.subplots(1, 4, figsize=(13, 4))
    # bins = np.linspace(-2, 10, 30)

    for scheme in VotingScheme:
        # creating the bar plot
        ax[scheme.value - 1].hist(result[scheme.name][1], color="maroon", width=0.4)
        # adding x label
        ax[scheme.value - 1].set_xlabel("Tactical votes available")
        # Set title
        ax[scheme.value - 1].set_title(scheme.name.replace("_", " "))

    # adding y label
    ax[0].set_ylabel("Voters that have the same amount of tactical votes")
    plt.show()


def bar_plot_happiness_per_scheme(
    voters: int, result: Tuple, scheme: VotingScheme
) -> None:
    """
    Generate bar plot with the happiness for each voters.
    The plot display both the original happiness and the happiness that a voter
    can achieve with tactical voting.
    The tactical voting are independent and the happiness is computed by
    performing one tactical voting at the time.

    Args:
        voters: number of voters
        result: result structure from TacticalVotingRisk
        scheme: voting scheme to display

    Returns:
        None.

    """
    plot_voters = [str(item) for item in range(1, voters + 1)]
    plot_old_happiness = []
    plot_new_happiness = []
    for i in range(len(result[scheme.name][0])):
        try:
            plot_old_happiness.append(
                result[scheme.name][0][i][0][TacticalVotingRisk.keys["old_happiness"]]
            )
        except (IndexError, KeyError):
            plot_old_happiness.append(0)
            print("Failed to get old happiness for voter ", i + 1)
        try:
            plot_new_happiness.append(
                result[scheme.name][0][i][0][TacticalVotingRisk.keys["new_happiness"]]
            )
        except (IndexError, KeyError):
            plot_new_happiness.append(0)
            print("Failed to get new happiness for voter ", i + 1)

    _, ax = plt.subplots(1, 2, figsize=(13, 4))
    # creating the bar plot
    ax[0].bar(plot_voters, plot_old_happiness, color="maroon", width=0.4)
    # adding x label
    ax[0].set_xlabel("Voter")
    # Set title
    ax[0].set_title(scheme.name.replace("_", " "))
    ax[0].set_ylabel("OLD HAPPINESS")
    ax[0].bar(plot_voters, plot_old_happiness, color="maroon", width=0.4)
    ax[0].axhline(0, color="k")
    # creating the bar plot
    ax[1].bar(plot_voters, plot_new_happiness, color="maroon", width=0.4)
    # adding x label
    ax[1].set_xlabel("Voter")
    # Set title
    ax[1].set_title(scheme.name.replace("_", " "))
    ax[1].set_ylabel("NEW HAPPINESS")
    ax[1].bar(plot_voters, plot_new_happiness, color="maroon", width=0.4)

    ax[1].axhline(0, color="k")
    plt.show()


def bar_plot_happiness_per_scheme_many_voters(
    voters: int, result: Tuple, scheme: VotingScheme
) -> None:
    """
    Generate bar plot with the happiness for each voters.
    The plot display both the original happiness and the happiness that a voter
    can achieve with tactical voting.
    The tactical voting are independent and the happiness is computed by
    performing one tactical voting at the time.

    Args:
        voters: number of voters
        result: result structure from TacticalVotingRisk
        scheme: voting scheme to display

    Returns:
        None.

    """
    plot_voters = [str(item) for item in range(1, voters + 1)]
    plot_old_happiness = []
    plot_new_happiness = []
    for i in range(len(result[scheme.name][0])):
        try:
            plot_old_happiness.append(
                result[scheme.name][0][i][0][TacticalVotingRisk.keys["old_happiness"]]
            )
        except (IndexError, KeyError):
            plot_old_happiness.append(0)
            print("Failed to get old happiness for voter ", i + 1)
        try:
            plot_new_happiness.append(
                result[scheme.name][0][i][0][TacticalVotingRisk.keys["new_happiness"]]
            )
        except (IndexError, KeyError):
            plot_new_happiness.append(0)
            print("Failed to get new happiness for voter ", i + 1)

    _, ax = plt.subplots(1, 1, figsize=(13, 6))

    ax.bar(
        plot_voters,
        plot_new_happiness,
        width=0.6,
        color="r",
        align="center",
        label="New Happiness",
    )
    ax.bar(
        plot_voters,
        plot_old_happiness,
        width=0.6,
        color="g",
        align="center",
        label="Old Happiness",
    )

    my_xticks = ax.get_xticks()
    plt.xticks([my_xticks[0], my_xticks[-1]], visible=True, rotation="horizontal")
    ax.set_title(scheme.name.replace("_", " "))
    ax.set_xlabel("Voter")
    ax.set_ylabel("Happiness")
    ax.legend(loc="upper right")

    plt.show()


if __name__ == "__main__":
    # Basic TVA
    VOTERS = 100
    CANDIDATES = 4
    t = TacticalVotingRisk(VOTERS, CANDIDATES)
    result = t.compute_risk()

    print("--------\nOriginal voting Matrix = \n", t.situation.voting_matrix)
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

    if VOTERS > 20:
        # if the voters are too many better plot the histogram
        hist_plot_total_tactical_votes_available_per_voter(VOTERS, result)
    else:
        # if the voters are less or equal than 20, then plot the bar
        bar_plot_total_tactical_votes_available_per_voter(VOTERS, result)

    for scheme in VotingScheme:
        bar_plot_happiness_per_scheme_many_voters(VOTERS, result, scheme)

    if VOTERS <= 20:
        for scheme in VotingScheme:
            bar_plot_happiness_per_scheme(VOTERS, result, scheme)
