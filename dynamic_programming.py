
from collections import deque


def dynamic_programming(amount, coins, stock):
    """
    Bounded Dynamic Programming for ATM withdrawal.
    Finds the minimum number of notes using limited stock.
    """

    coins = sorted(coins, reverse=True)

    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    used = [[0] * (amount + 1) for _ in coins]

    for i, note in enumerate(coins):
        available = stock.get(note, 0)
        previous = dp
        current = [float('inf')] * (amount + 1)

        for remainder in range(min(note, amount + 1)):
            candidates = deque()
            j = 0

            for value in range(remainder, amount + 1, note):

                if previous[value] != float('inf'):

                    new_value = previous[value] - j

                    # Remove choices that are not optimal
                    while candidates and candidates[-1][1] >= new_value:
                        candidates.pop()

                    candidates.append((j, new_value))

                # Remove choices that exceed available stock
                while candidates and candidates[0][0] < j - available:
                    candidates.popleft()

                if candidates:
                    best_j, best_value = candidates[0]

                    current[value] = best_value + j
                    used[i][value] = j - best_j

                j += 1

        dp = current

    if dp[amount] == float('inf'):
        return None

    result = {}
    remaining = amount

    for i in range(len(coins) - 1, -1, -1):
        note = coins[i]
        quantity = used[i][remaining]

        if quantity > 0:
            result[note] = quantity

        remaining -= quantity * note

    if remaining != 0:
        return None

    return result
