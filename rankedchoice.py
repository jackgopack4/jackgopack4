from typing import Optional, List
import heapq

"""
ballot : [1, 2, 3], [2, 3]

[ [1], [1], [2], [2], [], [3, 4, 5], [1,1,2,1,2]] -> [1,2]
"""


def sanitizeBallots(ballots: List[int]) -> Optional[List[int]]:
    """Sanitize ballots for empty or duplicate votes,
    return in opposite order for easy indexing of top vote"""
    res = []
    for b in ballots:
        if len(b) > 0:
            seen = set()
            sanitized_ballot = []
            for i in b:
                if i in seen:
                    continue
                sanitized_ballot.append(i)
                seen.add(i)
            res.append(sanitized_ballot[::-1])
    if len(res) > 0:
        return res
    else:
        return None


def rankedChoiceVoting(ballots: List[int]) -> Optional[int]:
    """implement ranked choice, taking into account empty ballots
    and multiple votes on one ballot, return ID of winner or None"""
    sanitized_ballots = sanitizeBallots(ballots)
    # print(sanitized_ballots)
    if sanitized_ballots is None:
        return None
    # sanitized_ballots is the effective voting record for all future rounds
    # B: the average number of votes per ballot
    # N: the number ballots
    # M: The number of candidates
    winner_found_or_no_ballots = False
    while not winner_found_or_no_ballots:  # O(M) O(B*N + M*(N+M+N*B))
        cur_first_choice_votes = {}
        for b in sanitized_ballots:
            cur_ballot_top_vote = b[-1]
            # print(f"{type(cur_ballot_top_vote)}, {cur_ballot_top_vote}")
            if cur_ballot_top_vote in cur_first_choice_votes:
                cur_first_choice_votes[cur_ballot_top_vote] += 1
            else:
                cur_first_choice_votes[cur_ballot_top_vote] = 1
        # now we have a dict with number of first choice votes
        # if that dict only has one entry, only one candidate remaining
        if len(cur_first_choice_votes.items()) == 1:
            return list(cur_first_choice_votes.keys())[0]

        # else, need to find highest and lowest vote getter
        cur_num_votes = len(sanitized_ballots)
        max_vote_id = -1
        max_vote_number = 0
        min_vote_id = -1
        min_vote_number = cur_num_votes + 1
        seen_number_of_votes = set()
        for candidate_id, num_votes in cur_first_choice_votes.items():  # O(M)
            if num_votes not in seen_number_of_votes:
                seen_number_of_votes.add(num_votes)
            if num_votes > max_vote_number:
                max_vote_id = candidate_id
                max_vote_number = num_votes
            if num_votes < min_vote_number:
                min_vote_id = candidate_id
                min_vote_number = num_votes
        # now we have the candidate id and number of votes for highest vote-getter
        if max_vote_number > (cur_num_votes / 2):
            # we have a winner
            return max_vote_id
        elif (
            len(seen_number_of_votes) == 1
        ):  # all candidates have same number of votes,
            # cannot eliminate anyone
            return None
        else:
            # need to remove lowest vote getter from each ballot
            for i in range(len(sanitized_ballots) - 1, -1, -1):  # O(N)
                if sanitized_ballots[i][-1] == min_vote_id:
                    del sanitized_ballots[i][-1]
                    if len(sanitized_ballots[i]) == 0:
                        del sanitized_ballots[i]
            # now new ballots has lowest vote getter removed

    return 0


test_ballots_1 = [[1], [1], [2], [2], [], [3, 4, 5], [5, 5, 4, 4, 3, 4]]
test_ballots_2 = [[1], [1], [2], [], [3, 4, 5]]
test_ballots_3 = [[]]
print(rankedChoiceVoting(test_ballots_1))
print(rankedChoiceVoting(test_ballots_2))
print(rankedChoiceVoting(test_ballots_3))
