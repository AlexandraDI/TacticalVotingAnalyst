"""
This module is for computing the risk of tacitcal voting.

It contains:
    * TacticalVotingRisk: class that compute the risk for each scheme
"""
from itertools import permutations, product, combinations
from typing import Optional, List, Tuple
import math
import numpy as np

from VotingSituation import VotingSituation
from Vot_Scheme import VotingScheme
from Happiness import Happiness


class TacticalVotingRisk:
    """
    Class used to compute the risk of tactical voting given a voting situation.
    All voting scheme are invesitgated.
    """

    keys = {
        "tactical_voting": 0,
        "tv": 0,
        "outcome": 1,
        "o": 1,
        "new_happiness": 2,
        "nh": 2,
        "old_happiness": 3,
        "oh": 3,
        "new_overall_happiness": 4,
        "noh": 4,
        "old_overall_happiness": 5,
        "ooh": 5,
    }

    def __init__(
        self,
        voters: int = 0,
        candidates: int = 0,
        advance_voters_coalition: int = 1,
        situation: Optional[VotingSituation] = None,
        allow_bullet_voting=False,
    ) -> None:
        """
        Compute the risk of tactical voting for 1 voting situation

        If a VotingSituation is not given a new one is created.

        keys: dictionary to interpret the results
        Args:
            voters (int): number of voters.
            candidates (int): number of candidates.
            advance_voters_coalition (int): for the advance tactical voting,
                make coalitions of this size.
            situation (Optional - VotingSituation): given situation
            allow_bullet_voting (bool): whether
        """
        self._bullet = allow_bullet_voting

        # Create new sitiation if not give
        if situation is not None:
            self.situation = situation
        else:
            self.situation = VotingSituation(voters, candidates)

        # Get number of voter and candidates
        self.options, self.voters = self.situation.voting_matrix.shape

        # Compute the number of alternative preferences (exclude honest pref.)
        self.alternative_votings = math.factorial(self.options) - 1
        if self._bullet:
            self.alternative_votings += self.options

        if advance_voters_coalition != 1:
            # Cartesian product
            self.alternative_votings **= advance_voters_coalition

        self._coalition = advance_voters_coalition

    def compute_risk(self) -> Tuple[List, List[int], float, float]:
        """
        Count how many tactival votes each voter has

        Returns:
            Tuple containing the detailed tv, the number of tv for each voters,
            the average risk and boolean risk.

        Note: the return object is a deeply nested structure
        """
        # key: scheme, values: (data, risks, avg_risk, avg_bool_risk)
        results = {}
        for scheme in VotingScheme:
            res, risk = self._compute_risk_coalitions(scheme)
            tmp = np.array(risk)
            avg_risk = np.sum(tmp) / (
                self.alternative_votings * math.comb(self.voters, self._coalition)
            )
            avg_bool_risk = np.sum(tmp > 0) / math.comb(self.voters, self._coalition)
            results[scheme.name] = (res, risk, avg_risk, avg_bool_risk)

        return results

    def _compute_risk_no_coalitions(
        self, scheme_type: VotingScheme, verbose: Optional[bool] = True
    ) -> Tuple[List[List[Tuple]], List[int]]:
        """
        Compute the risk

        Args:
            scheme_type (VotingScheme): scheme used to compute the outcome.
            verbose (bool): print information about the original happiness
        Returns:
            result (list), risks (list): list containing the tactical votings
            and the number of possible tactical votes for each voters.
            For both lists the index represent the voters.
            The result list contain a list of tactical votings for each voters.
            Each tactical vote is a tuple containing the new preference, the
            new outcome, the new individual happines, the old individual happines,
            the new overall happiness, the old overall happines.
        """
        original_outcome = self.situation.calculatevote(scheme_type)
        original_happiness = Happiness(self.situation.voting_matrix, original_outcome)

        if verbose:
            print("--------------")
            print("Scheme = ", scheme_type)
            print("Original outcome = ", original_outcome)
            print("Original happiness = ", original_happiness.happiness)

        result = [
            [None for j in range(self.alternative_votings)] for i in range(self.voters)
        ]
        risks = [0 for i in range(self.voters)]
        for v in range(self.voters):
            # compute permutations
            voting = self.situation.voting_matrix.copy()
            real_preference = voting[:, v]  # real preference of the voter
            all_tv_preference = list(permutations(real_preference))[1:]

            if self._bullet:
                all_tv_preference.extend(self._get_bullet_votings())

            # inspect each possible voting
            for tv in all_tv_preference:
                # change the voting matrix with the tactical vote
                voting[:, v] = tv
                new_outcome = self.situation.calculate_vote_given_matrix(
                    scheme_type, voting
                )
                new_happiness = Happiness(voting, new_outcome)

                # Tactical voting
                if (
                    new_happiness.individual_happiness[v]
                    > original_happiness.individual_happiness[v]
                ):
                    result[v][risks[v]] = (
                        tv,
                        tuple(new_outcome),
                        new_happiness.individual_happiness[v],
                        original_happiness.individual_happiness[v],
                        new_happiness.happiness,
                        original_happiness.happiness,
                    )
                    risks[v] += 1
        result = [[j for j in i if j is not None] for i in result]
        return result, risks

    def _compute_risk_coalitions(
        self, scheme_type: VotingScheme, verbose: Optional[bool] = True
    ) -> Tuple[List[List[Tuple]], List[int]]:
        """
        Compute the risk including voters collusion

        Args:
            scheme_type (VotingScheme): scheme used to compute the outcome.
            verbose (bool): print information about the original happiness
        Returns:
            result (list), risks (list): list containing the tactical votings
            and the number of possible tactical votes for each voters.
            For both lists the index represent the voters.
            The result list contain a list of tactical votings for each voters.
            Each tactical vote is a tuple containing the new preference, the
            new outcome, the new individual happines, the old individual happines,
            the new overall happiness, the old overall happines.
        """

        original_outcome = self.situation.calculatevote(scheme_type)
        original_happiness = Happiness(self.situation.voting_matrix, original_outcome)

        if verbose:
            print("--------------")
            print("Scheme = ", scheme_type)
            print("Original outcome = ", original_outcome)
            print("Original happiness = ", original_happiness.happiness)

        coalitions = list(combinations(range(self.voters), self._coalition))

        result = [[None for j in range(self.alternative_votings)] for i in coalitions]
        risks = [0 for i in coalitions]

        for n, c in enumerate(coalitions):
            # compute permutations
            voting = self.situation.voting_matrix.copy()
            real_preference = voting[:, c]  # real preference of the coalition

            individual_preferences = [None for i in c]
            for i, _ in enumerate(c):
                individual_preferences[i] = list(permutations(real_preference[:, i]))[
                    1:
                ]
                if self._bullet:
                    individual_preferences[i].extend(self._get_bullet_votings())
            all_tv_preference = list(product(*individual_preferences))

            # inspect each possible voting
            for tv in all_tv_preference:
                # preference is should be a column vector
                voting[:, c] = np.array(tv).T
                new_outcome = self.situation.calculate_vote_given_matrix(
                    scheme_type, voting
                )
                new_happiness = Happiness(voting, new_outcome)

                # Tactical voting if happiness improvess for everybody
                if (
                    new_happiness.individual_happiness[list(c)]
                    > original_happiness.individual_happiness[list(c)]
                ).all():
                    # print(risks[n], len(result[n]))
                    result[n][risks[n]] = (
                        tv,
                        tuple(new_outcome),
                        new_happiness.individual_happiness[list(c)],
                        original_happiness.individual_happiness[list(c)],
                        new_happiness.happiness,
                        original_happiness.happiness,
                    )
                    risks[n] += 1
        result = [[j for j in i if j is not None] for i in result]
        return result, risks

    def _get_bullet_votings(self) -> np.array:
        """
        Returns:
            array of possible bullet voting
        """
        # for each option i create (i, -1, -1, ...)
        bullets = [None for i in range(self.options)]
        for i in range(self.options):
            p = [-1 for i in range(self.options)]
            p[0] = i
            bullets[i] = tuple(p)
        return bullets


if __name__ == "__main__":
    np.random.seed(42)

    # Basic TVA
    VOTERS = 15
    CANDIDATES = 3
    t = TacticalVotingRisk(VOTERS, CANDIDATES)
    result = t.compute_risk()

    # Values to show (Text, key)
    to_show = [
        ("First Tactical voting for voter", "tactical_voting"),
        ("New happiness", "new_happiness"),
        ("Old happiness", "old_happiness"),
        ("New overall happiness", "new_overall_happiness"),
        ("Old overall happiness", "old_overall_happiness"),
    ]

    for scheme in VotingScheme:
        print("-" * 80)
        print(scheme.name)

        print(f"Tactical voting for all voters {result[scheme.name][0]}")
        print(f"How many tactical votes for all voters {result[scheme.name][1]}")
        print(f"Avg risk is {result[scheme.name][2]}")
        print(f"Avg bool risk is {result[scheme.name][3]}")

        print("-" * 80)

        print("*" * 80)

    for scheme in VotingScheme:
        print("-" * 80)
        print(scheme.name)

        for voter in range(VOTERS):
            if len(result[scheme.name][0][voter]) > 0:
                print(f"voter {voter}")
                for (text, key) in to_show:
                    print(
                        f"{text}: {result[scheme.name][0][voter][0][TacticalVotingRisk.keys[key]]}"
                    )

                print("-" * 80)
