
import streamlit as st
import time

from brute_force import brute_force
from greedy import greedy
from dynamic_programming import dynamic_programming
from backtracking import backtracking


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Smart ATM System",
    page_icon="🏧",
    layout="wide"
)

st.title("🏧 Smart ATM Cash Withdrawal System")
st.subheader("Realistic ATM Simulation - Algorithm Explorer")

st.write(
    "Withdraw cash using four algorithms while checking "
    "the available ATM cash stock."
)


# ==========================================
# ATM CASH SETTINGS
# ==========================================

INITIAL_STOCK = {
    500: 620,
    200: 500,
    100: 500,
    50: 500,
    20: 500,
    10: 500
}

DENOMINATIONS = [500, 200, 100, 50, 20, 10]

MAX_WITHDRAWAL = 100000

ALGORITHMS = [
    "Brute Force",
    "Greedy",
    "Dynamic Programming",
    "Backtracking"
]

if "stock" not in st.session_state:
    st.session_state.stock = INITIAL_STOCK.copy()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def total_cash(stock):
    return sum(
        note * quantity
        for note, quantity in stock.items()
    )


def note_count(result):
    if not result:
        return 0

    return sum(result.values())


def calculate(algorithm, amount, stock):
    """
    Runs the selected algorithm.

    All algorithms are converted into the same format:
    (result, completed)
    """

    if algorithm == "Brute Force":
        output = brute_force(
            amount, DENOMINATIONS, stock
        )

    elif algorithm == "Greedy":
        output = greedy(
            amount, DENOMINATIONS, stock
        )

    elif algorithm == "Dynamic Programming":
        output = dynamic_programming(
            amount, DENOMINATIONS, stock
        )

    elif algorithm == "Backtracking":
        output = backtracking(
            amount, DENOMINATIONS, stock
        )

    else:
        return None, False

    # Handle functions that return tuples
    if isinstance(output, tuple):

        result = output[0] if len(output) > 0 else None

        completed = True

        if len(output) > 1 and isinstance(output[1], bool):
            completed = output[1]

        return result, completed

    # Handle functions that return only a dictionary or None
    return output, True


def valid_stock_result(result, amount, stock):

    if not isinstance(result, dict) or not result:
        return False

    # Check whether the notes add up to the requested amount
    total = sum(
        note * quantity
        for note, quantity in result.items()
    )

    if total != amount:
        return False

    # Check available note stock
    for note, quantity in result.items():

        if note not in stock:
            return False

        if quantity <= 0 or quantity > stock[note]:
            return False

    return True


def display_notes(result):

    if not result:
        return "No exact combination available"

    return ", ".join(
        f"₹{note} × {quantity}"
        for note, quantity in sorted(
            result.items(), reverse=True
        )
        if quantity > 0
    )


def valid_amount(amount):
    return (
        amount >= 10
        and amount <= MAX_WITHDRAWAL
        and amount % 10 == 0
    )


# ==========================================
# ATM DASHBOARD
# ==========================================

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Available ATM Cash",
    f"₹{total_cash(st.session_state.stock):,}"
)

col2.metric(
    "Maximum Withdrawal",
    "₹1,00,000"
)

col3.metric(
    "Available Denominations",
    len(DENOMINATIONS)
)


# ==========================================
# ATM CASH INVENTORY
# ==========================================

st.header("💵 ATM Cash Inventory")

inventory = []

for note, quantity in sorted(
    st.session_state.stock.items(),
    reverse=True
):
    inventory.append({
        "Note Value": f"₹{note}",
        "Available Notes": quantity,
        "Total Value": f"₹{note * quantity:,}"
    })

st.dataframe(
    inventory,
    width="stretch",
    hide_index=True
)


# ==========================================
# RESET ATM STOCK
# ==========================================

if st.button("🔄 Reset ATM Cash Stock"):

    st.session_state.stock = INITIAL_STOCK.copy()
    st.session_state.pop("comparison", None)

    st.success(
        "ATM stock has been restored to its initial quantity."
    )

    st.rerun()


# ==========================================
# WITHDRAWAL INPUT
# ==========================================

st.divider()

st.header("💳 Cash Withdrawal")

amount = st.number_input(
    "Enter withdrawal amount (₹)",
    min_value=10,
    max_value=MAX_WITHDRAWAL,
    value=670,
    step=10
)

st.caption(
    "Enter an amount in multiples of ₹10. "
    "Maximum withdrawal per transaction is ₹1,00,000."
)


# ==========================================
# COMPARE FOUR ALGORITHMS
# ==========================================

if st.button(
    "🔍 Compare All Four Algorithms",
    type="primary"
):

    if not valid_amount(int(amount)):

        st.error(
            "Please enter a valid amount in multiples of ₹10."
        )

    else:

        comparison = {}

        progress = st.progress(0)

        with st.spinner("Comparing all four algorithms..."):

            for index, algorithm in enumerate(ALGORITHMS):

                start = time.perf_counter()

                try:
                    result, completed = calculate(
                        algorithm,
                        int(amount),
                        st.session_state.stock
                    )

                    elapsed = time.perf_counter() - start

                    if not valid_stock_result(
                        result,
                        int(amount),
                        st.session_state.stock
                    ):
                        result = None

                    comparison[algorithm] = {
                        "result": result,
                        "completed": completed,
                        "time": elapsed,
                        "error": None
                    }

                except Exception as error:

                    elapsed = time.perf_counter() - start

                    comparison[algorithm] = {
                        "result": None,
                        "completed": False,
                        "time": elapsed,
                        "error": str(error)
                    }

                progress.progress((index + 1) / len(ALGORITHMS))

        st.session_state.comparison = comparison

        st.success("Algorithm comparison completed!")


# ==========================================
# DISPLAY ALGORITHM RESULTS
# ==========================================

if "comparison" in st.session_state:

    st.divider()
    st.header("📊 Algorithm Comparison")

    tabs = st.tabs(ALGORITHMS)

    for tab, algorithm in zip(tabs, ALGORITHMS):

        data = st.session_state.comparison[algorithm]
        result = data["result"]

        with tab:

            st.subheader(algorithm)

            if data["error"]:

                st.error(
                    f"Algorithm error: {data['error']}"
                )

            elif result:

                st.success("Valid withdrawal combination found!")

                st.write("**Notes to dispense:**")
                st.write(display_notes(result))

                st.metric(
                    "Total Number of Notes",
                    note_count(result)
                )

            elif not data["completed"]:

                st.warning(
                    "Search stopped before completion. "
                    "A solution or optimal result could not be confirmed."
                )

            else:

                st.error(
                    "No exact withdrawal combination found "
                    "with the available stock."
                )

            st.write(
                f"**Execution Time:** {data['time']:.6f} seconds"
            )

            if algorithm == "Brute Force":

                st.write(
                    "**Approach:** Tries different combinations of notes."
                )

                st.write(
                    "**Time Complexity:** Exponential in the worst case."
                )

                st.write(
                    "**Space Complexity:** O(K) recursion depth."
                )

            elif algorithm == "Greedy":

                st.write(
                    "**Approach:** Selects the largest available note first."
                )

                st.write(
                    "**Time Complexity:** O(K log K) including sorting."
                )

                st.write(
                    "**Space Complexity:** O(K) for the result."
                )

                st.info(
                    "Greedy is fast, but it does not guarantee "
                    "the minimum number of notes in every situation."
                )

            elif algorithm == "Dynamic Programming":

                st.write(
                    "**Approach:** Uses previous results to find "
                    "the minimum number of notes."
                )

                st.write(
                    "**Time Complexity:** O(A × K) for the "
                    "bounded monotone-queue implementation."
                )

                st.write(
                    "**Space Complexity:** O(A × K) for the "
                    "current implementation."
                )

            elif algorithm == "Backtracking":

                st.write(
                    "**Approach:** Explores possible combinations "
                    "and prunes unnecessary searches."
                )

                st.write(
                    "**Time Complexity:** Exponential in the worst case."
                )

                st.write(
                    "**Space Complexity:** O(K) recursion depth."
                )

            if not data["completed"] and not data["error"]:

                st.warning(
                    "The search limit was reached. "
                    "Optimality is not guaranteed."
                )


    # ======================================
    # COMPARISON TABLE
    # ======================================

    st.subheader("Algorithm Performance Table")

    table = []

    for algorithm in ALGORITHMS:

        data = st.session_state.comparison[algorithm]
        result = data["result"]

        if data["error"]:
            note_result = "Error"
        elif result:
            note_result = note_count(result)
        elif not data["completed"]:
            note_result = "Incomplete"
        else:
            note_result = "Not possible"

        table.append({
            "Algorithm": algorithm,
            "Notes Required": note_result,
            "Execution Time": f"{data['time']:.6f} sec",
            "Search Complete": (
                "Yes" if data["completed"] else "No"
            )
        })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# DISPENSE CASH
# ==========================================

st.divider()

st.header("🏧 Dispense Cash")

selected_algorithm = st.selectbox(
    "Choose an algorithm for withdrawal",
    [
        "Dynamic Programming",
        "Greedy",
        "Brute Force",
        "Backtracking"
    ]
)

if st.button("💰 Withdraw Cash"):

    if not valid_amount(int(amount)):

        st.error(
            "Please enter an amount in multiples of ₹10."
        )

    else:

        try:

            result, completed = calculate(
                selected_algorithm,
                int(amount),
                st.session_state.stock
            )

            if not valid_stock_result(
                result,
                int(amount),
                st.session_state.stock
            ):

                st.error(
                    "Withdrawal failed! The ATM does not have "
                    "the required combination of notes."
                )

            else:

                # Deduct notes from ATM stock
                for note, quantity in result.items():

                    st.session_state.stock[note] -= quantity

                st.success("Cash withdrawal successful!")

                st.write(
                    f"**Amount Withdrawn:** ₹{int(amount):,}"
                )

                st.write(
                    f"**Algorithm Used:** {selected_algorithm}"
                )

                st.write("**Notes Dispensed:**")
                st.write(display_notes(result))

                st.write(
                    f"**Number of Notes:** {note_count(result)}"
                )

                if not completed:

                    st.warning(
                        "The search limit was reached. "
                        "The dispensed combination is valid, "
                        "but minimum-note optimality is not guaranteed."
                    )

                st.write(
                    f"**Remaining ATM Cash:** "
                    f"₹{total_cash(st.session_state.stock):,}"
                )

                st.session_state.pop("comparison", None)

        except Exception as error:

            st.error(
                f"Withdrawal could not be completed: {error}"
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.info(
    "This is an educational ATM simulation. "
    "It models cash inventory, note availability and "
    "withdrawal limits; it does not connect to a real bank."
)

st.caption(
    "Smart ATM Cash Withdrawal System | Python + Streamlit"
)
