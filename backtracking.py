
def backtracking(amount, coins, stock):
    """
    Backtracking algorithm for ATM withdrawal.
    Explores possible note combinations and finds
    the minimum number of notes using limited stock.
    """

    best_result = None
    best_count = float('inf')

    coins = sorted(coins, reverse=True)

    def solve(index, remaining, result, count):
        nonlocal best_result, best_count

        if remaining == 0:
            if count < best_count:
                best_count = count
                best_result = result.copy()
            return

        if index >= len(coins):
            return

        if count >= best_count:
            return

        note = coins[index]
        available = stock.get(note, 0)

        max_count = min(remaining // note, available)

        for number in range(max_count, -1, -1):
            result[note] = number

            solve(
                index + 1,
                remaining - number * note,
                result,
                count + number
            )

        result.pop(note, None)

    solve(0, amount, {}, 0)

    return best_result
