
def greedy(amount, coins, stock):
    """
    Greedy algorithm for ATM withdrawal.
    Uses the largest available denomination first.
    stock is a dictionary containing available note quantities.
    """

    result = {}
    remaining = amount

    for note in sorted(coins, reverse=True):
        available = stock.get(note, 0)

        if available <= 0:
            continue

        count = min(remaining // note, available)

        if count > 0:
            result[note] = count
            remaining -= note * count

    if remaining == 0:
        return result

    return None
