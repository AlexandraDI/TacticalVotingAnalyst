from itertools import permutations
from typing import Optional, List, Tuple
import math
import numpy as np

from VotingSituation import VotingSituation
from Vot_Scheme import VotingScheme
from Happiness import Happiness


class TacticalVotingRisk:
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
        voters: int,
        candidates: int,
        advance_voters_coalition: int = 1,
        situation: Optional[VotingSituation] = None,
        allow_bullet_voting=False,
    ) -> None:
        """
        Compute the risk of tactical voting for 1 voting situation

        keys: dictionary to interpret the results

        Args:
            voters (int): number of voters.
            candidates (int): number of candidates.
            advance_voters_coalition (int): for the advance tactical voting, make coalitions of this size.
            situation (Optional - Situation): given situation
            allow_bullet_voting (bool): whether
        """
        self._bullet = allow_bullet_voting

        if situation is not None:
            self.situation = situation
        else:
            self.situation = VotingSituation(voters, candidates)

        self.options, self.voters = self.situation.voting_matrix.shape
        self._coalition = advance_voters_coalition

        if advance_voters_coalition == 1:
            self.alternative_votings = math.factorial(self.options) - 1
        else:
            pass  # TODO advance tv

    def compute_risk(self):
        """
        Count how many tactival votes each voter has

        Returns:
            None.

        """
        results = {}  # key: scheme, values: (data, risks, avg_risk, avg_bool_risk)
        if self._coalition == 1:  # simple tv, 1 voter
            for scheme in VotingScheme:
                res, risk = self._compute_risk_no_coalitions(scheme)
                tmp = np.array(risk)
                avg_risk = np.sum(tmp) / (self.alternative_votings * self.voters)
                avg_bool_risk = np.sum(tmp > 0) / self.voters
                results[scheme.name] = (res, risk, avg_risk, avg_bool_risk)
        else:  # advance tv, coalition of voters
            pass

        return results

    def _compute_risk_no_coalitions(
        self, scheme_type: VotingScheme
    ) -> Tuple[List[List[Tuple]], List[int]]:
        """
        Compute the risk

        Args:
            scheme_type (VotingScheme): scheme used to compute the outcome.

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

        result = [
            [None for j in range(self.alternative_votings + 1)]
            for i in range(self.voters)
        ]
        risks = [0 for i in range(self.voters)]
        for v in range(self.voters):
            # compute permutations
            voting = self.situation.voting_matrix.copy()
            real_preference = voting[:, v]  # real preference of the voter
            all_tv_preference = list(permutations(real_preference))[1:]

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
                    risks[v] += 1
                    result[v][risks[v]] = (
                        tv,
                        tuple(new_outcome),
                        new_happiness.individual_happiness[v],
                        original_happiness.individual_happiness[v],
                        new_happiness.happiness,
                        original_happiness.happiness,
                    )
        result = [[j for j in i if j is not None] for i in result]
        return result, risks


if __name__ == "__main__":
    t = TacticalVotingRisk(15, 3)
    res = t.compute_risk()
