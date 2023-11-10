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


def rankedChoiceVoting(
    ballots: List[int], candidates: Optional[List[int]] = [1, 2, 3, 4, 5, 6]
) -> Optional[int]:
    """implement ranked choice, taking into account empty ballots
    and multiple votes on one ballot, return ID of winner or None"""
    sanitized_ballots = sanitizeBallots(ballots)
    # print(f"sanitized_ballots for this run: {sanitized_ballots}")
    if sanitized_ballots is None:
        return None
    # sanitized_ballots is the effective voting record for all future rounds
    # B: the average number of votes per ballot
    # N: the number ballots
    # M: The number of candidates
    winner_found_or_no_ballots = False
    cur_first_choice_votes = {}
    for c in candidates:
        cur_first_choice_votes[
            c
        ] = (
            []
        )  # all candidates passed in, once a key is no longer in the dict they are eliminated
    for i, b in enumerate(sanitized_ballots):
        cur_ballot_top_vote = b[-1]
        # print(f"{type(cur_ballot_top_vote)}, {cur_ballot_top_vote}")
        if cur_ballot_top_vote in cur_first_choice_votes:
            cur_first_choice_votes[cur_ballot_top_vote].append(i)
        else:
            cur_first_choice_votes[cur_ballot_top_vote] = [i]
    cur_num_votes = len(sanitized_ballots)
    while not winner_found_or_no_ballots:  # O(M) O(B*N + M*(N+M+N*B))
        # print(f"current top votes dict: {cur_first_choice_votes}")
        # now we have a dict with index of first choice voters
        # if that dict only has one entry, only one candidate remaining
        if len(cur_first_choice_votes.items()) == 1:
            return list(cur_first_choice_votes.keys())[0]

        # else, need to find highest and lowest vote getter
        max_vote_ids = []
        max_vote_number = -1
        min_vote_ids = []
        min_vote_number = cur_num_votes + 1
        # track unique vote counts received by all candidates
        # seen_number_of_votes = set()
        for candidate_id, voter_ids in cur_first_choice_votes.items():  # O(M)
            num_votes = len(voter_ids)
            # if num_votes not in seen_number_of_votes:
            # seen_number_of_votes.add(num_votes)
            if num_votes > max_vote_number:
                max_vote_ids = [candidate_id]
                max_vote_number = num_votes
            elif num_votes == max_vote_number:
                max_vote_ids.append(candidate_id)
            if num_votes < min_vote_number:
                min_vote_ids = [candidate_id]
                min_vote_number = num_votes
            elif num_votes == min_vote_number:
                min_vote_ids.append(candidate_id)
        # now we have the candidate id and number of votes for highest vote-getter
        if max_vote_number > (cur_num_votes / 2):
            # we have a winner
            return max_vote_ids[0]
        elif (
            max_vote_number == min_vote_number
        ):  # all candidates have same number of votes, cannot eliminate anyone
            return None
        else:
            # need to remove lowest vote getter from each ballot
            voter_ids_to_reassign = []
            for min_id in min_vote_ids:
                voter_ids_to_reassign.extend(cur_first_choice_votes[min_id])
                del cur_first_choice_votes[min_id]
            # if their next votes are for eliminated candidates, keep looping until gone
            for vid in voter_ids_to_reassign:
                del sanitized_ballots[vid][-1]
                while (
                    len(sanitized_ballots[vid]) > 0
                    and sanitized_ballots[vid][-1] not in cur_first_choice_votes
                ):
                    del sanitized_ballots[vid][-1]
                if len(sanitized_ballots[vid]) > 0:
                    vid_next_best_choice = sanitized_ballots[vid][-1]
                    cur_first_choice_votes[vid_next_best_choice].append(vid)
            remaining_votes = 0
            # need to retally the number of remaining votes
            for voter_ids in cur_first_choice_votes.values():
                remaining_votes += len(voter_ids)
            cur_num_votes = remaining_votes

    return 0


test_ballots_1 = [[1], [1], [2], [2], [], [3, 4, 5], [5, 5, 4, 4, 3, 4]]
test_ballots_2 = [[1], [1], [2], [], [3, 4, 5]]
test_ballots_3 = [[]]
test_run_1 = rankedChoiceVoting(test_ballots_1)
test_run_2 = rankedChoiceVoting(test_ballots_2)
test_run_3 = rankedChoiceVoting(test_ballots_3)
print(f"test 1, expected: None, actual: {test_run_1}\n")
print(f"test 2, expected: 1,    actual: {test_run_2}\n")
print(f"test 3, expected: None, actual: {test_run_3}\n")
