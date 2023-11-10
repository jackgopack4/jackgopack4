from typing import Optional, List

"""
ballot : [1, 2, 3], [2, 3]

[ [1], [1], [2], [2], [], [3, 4, 5], [1,1,2,1,2]] -> [1,2]
"""


def sanitizeBallots(ballots: List[int]) -> Optional[List[int]]:
    """Sanitize ballots for empty or duplicate votes, return in opposite order
    for easy indexing of top vote. O(N * B) where N is number of ballots, B is
    number of votes per ballot"""
    res = []
    # Need to check each ballot for empty or duplicate entries, utilize set
    # for duplicate checking and list for maintaing order of remaining items
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


def initialVoteCount(sanitized_ballots: List[int], candidates: List[int]) -> dict:
    vote_count = {c: [] for c in candidates}  # O(M)
    for i, b in enumerate(sanitized_ballots):  # O(N)
        if b[-1] in vote_count:
            vote_count[b[-1]].append(i)
        else:
            vote_count[b[-1]] = [i]
    return vote_count


def findMinAndMaxVoterLists(
    vote_counts: dict, cur_num_votes: int
) -> (List[int], List[int], int, int):
    max_vote_ids = []
    max_vote_number = -1
    min_vote_ids = []
    min_vote_number = cur_num_votes + 1
    for candidate_id, voter_ids in vote_counts.items():  # O(M)
        num_votes = len(voter_ids)
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
    return min_vote_ids, max_vote_ids, min_vote_number, max_vote_number


def rankedChoiceVoting(
    ballots: List[int], candidates: Optional[List[int]] = [1, 2, 3, 4, 5, 6]
) -> Optional[int]:
    """implement ranked choice, taking into account empty ballots
    and multiple votes on one ballot, return ID of winner or None.
    Overall complexity O(M*(N+B) + N*B + M^2)"""
    sanitized_ballots = sanitizeBallots(ballots)  # O(N*B)
    # print(f"sanitized_ballots for this run: {sanitized_ballots}")
    if sanitized_ballots is None:
        return None
    # sanitized_ballots is the effective voting record for all future rounds
    # B: the number of votes per ballot
    # N: the number ballots/voters
    # M: The number of candidates
    cur_first_choice_votes = initialVoteCount(sanitized_ballots, candidates)  # O(M + N)
    cur_num_votes = len(sanitized_ballots)
    # Begin voting round loop, up to M times for M candidates
    for round_number in range(len(candidates)):  # O(M*(B+M+N))
        # print(f"starting voting round {round_number+1}:\n")
        # print(f"current top votes dict: {cur_first_choice_votes}")

        # now we have a dict with index of first choice voters
        # if that dict only has one entry, only one candidate remaining
        if len(cur_first_choice_votes.items()) == 1:
            return list(cur_first_choice_votes.keys())[0]

        # else, need to find highest and lowest vote getter
        (
            min_vote_ids,
            max_vote_ids,
            min_vote_number,
            max_vote_number,
        ) = findMinAndMaxVoterLists(cur_first_choice_votes, cur_num_votes)

        # now we have the candidate ids and number of votes for highest and
        # lowest vote-getters (we can eliminate all lowest vote-getters at once)
        if max_vote_number > (cur_num_votes / 2):
            # we have a vote getter with actual majority
            return max_vote_ids[0]
        elif max_vote_number == min_vote_number:
            # all candidates have same number of votes, cannot eliminate anyone
            return None
        else:  # All the operations in this else block total O(B+M+N)
            # need to find all voters who voted for the lowest vote-getter(s)
            # and then eliminate those candidates from the list
            voter_ids_to_reassign = []
            for min_id in min_vote_ids:  # O(M)
                voter_ids_to_reassign.extend(cur_first_choice_votes[min_id])
                del cur_first_choice_votes[min_id]

            for vid in voter_ids_to_reassign:  # O(N)
                del sanitized_ballots[vid][-1]
                # If the current voter's next votes were for eliminated candidates,
                # continue to delete their next votes until getting their choice or they
                # have no more votes left
                while (
                    len(sanitized_ballots[vid]) > 0
                    and sanitized_ballots[vid][-1] not in cur_first_choice_votes
                ):  # O(B)
                    del sanitized_ballots[vid][-1]
                if len(sanitized_ballots[vid]) > 0:
                    vid_next_best_choice = sanitized_ballots[vid][-1]
                    cur_first_choice_votes[vid_next_best_choice].append(vid)
            remaining_votes = 0

            # need to retally the number of remaining votes
            for voter_ids in cur_first_choice_votes.values():  # O(M)
                remaining_votes += len(voter_ids)
            cur_num_votes = remaining_votes
    # If we get here, that means no one won after num_candidates rounds, so no one wins
    return None


test_ballots_1 = [[1], [1], [2], [2], [], [3, 4, 5], [5, 5, 4, 4, 3, 4]]
test_ballots_2 = [[1], [1], [2], [], [3, 4, 5]]
test_ballots_3 = [[]]
test_run_1 = rankedChoiceVoting(test_ballots_1)
test_run_2 = rankedChoiceVoting(test_ballots_2)
test_run_3 = rankedChoiceVoting(test_ballots_3)
print(f"test 1, expected: None, actual: {test_run_1}\n")
print(f"test 2, expected: 1,    actual: {test_run_2}\n")
print(f"test 3, expected: None, actual: {test_run_3}\n")
