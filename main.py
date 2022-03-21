# assignment-03

# no other imports needed
from collections import defaultdict
import math


# PARENTHESES MATCHING

# Iterative solution
def parens_match_iterative(mylist):
    """
    Implement the iterative solution to the parens matching problem.
    This function should call `iterate` using the `parens_update` function.

    Params:
      mylist...a list of strings
    Returns
      True if the parenthesis are matched, False otherwise

    e.g.,
    >>>parens_match_iterative(['(', 'a', ')'])
    True
    >>>parens_match_iterative(['('])
    False
    """
    x = iterate(parens_update, 0, mylist)
    if x == 0:
        return True
    else:
        return False


def iterate(f, x, a):
    # done. do not change me.
    """
    Params:
      f.....function to apply
      x.....return when a is empty
      a.....input sequence
    """
    if len(a) == 0:
        return x
    else:
        return iterate(f, f(x, a[0]), a[1:])


def parens_update(current_output, next_input):
    """
    This function will be passed to the `iterate` function to
    solve the balanced parenthesis problem.

    Like all functions used by iterate, it takes in:
    current_output....the cumulative output thus far (e.g., the running sum when doing addition)
    next_input........the next value in the input

    Returns:
      the updated value of `current_output`
    """
    if next_input == "(":
        current_output += 1
    elif next_input == ")" and current_output <= 0:
        current_output = -99999999
    elif next_input == ")":
        current_output -= 1
    return current_output


def test_parens_match_iterative():
    assert parens_match_dc(['(', ')']) == True
    assert parens_match_dc(['(']) == False
    assert parens_match_dc([')']) == False
    assert parens_match_dc([')', '(']) == False
    assert parens_match_dc(['(', ')', '(', ')']) == True
    assert parens_match_dc(['a', '(', ')', '(']) == False
    assert parens_match_dc(['a', 'b', 'c']) == True
    assert parens_match_dc(['a', 'b', 'c', ')']) == False
    assert parens_match_dc(['(', 'a', 'b', 'c']) == False
    assert parens_match_iterative([')', '(']) == False
    assert parens_match_iterative([')', '(', ')']) == False


# Scan solution

def parens_match_scan(mylist):
    """
    Implement a solution to the parens matching problem using `scan`.
    This function should make one call each to `scan`, `map`, and `reduce`

    Params:
      mylist...a list of strings
    Returns
      True if the parenthesis are matched, False otherwise

    e.g.,
    >>>parens_match_scan(['(', 'a', ')'])
    True
    >>>parens_match_scan(['('])
    False

    """

    mapped = list(map(paren_map(), mylist))

    #map = O(n)
    
    for i in mapped:
        if i == -1:
            return False
        if i == 1:
            break

    #Scan = O(n) work, O(log n) span
    
    scanned = scan(add, 0, mapped)[0]

    #Reduce = O(n) work, O(log n) span
    
    reduced = reduce(min_f, 0, scanned)

    #Re

    if reduced != 0:
        return False
    else:
        return True


def reduce(f, id_, a):
    # done. do not change me.
    if len(a) == 0:
        return id_
    elif len(a) == 1:
        return a[0]
    else:
        # can call these in parallel
        res = f(reduce(f, id_, a[:len(a) // 2]),
                reduce(f, id_, a[len(a) // 2:]))
        return res



def scan(f, id_, a):
    """
    This is a horribly inefficient implementation of scan
    only to understand what it does.
    We saw a more efficient version in class. You can assume
    the more efficient version is used for analyzing work/span.
    """
    return (
        [reduce(f, id_, a[:i + 1]) for i in range(len(a))],
        reduce(f, id_, a)
    )


def add(x, y):
    return x + y


def paren_map(x):
    """
    Returns 1 if input is '(', -1 if ')', 0 otherwise.
    This will be used by your `parens_match_scan` function.

    Params:
       x....an element of the input to the parens match problem (e.g., '(' or 'a')

    >>>paren_map('(')
    1
    >>>paren_map(')')
    -1
    >>>paren_map('a')
    0
    """
    if x == '(':
        return 1
    elif x == ')':
        return -1
    else:
        return 0


def min_f(x, y):
    """
    Returns the min of x and y. Useful for `parens_match_scan`.
    """
    if x < y:
        return x
    return y


def test_parens_match_scan():
    assert parens_match_dc(['(', ')']) == True
    assert parens_match_dc(['(']) == False
    assert parens_match_dc([')']) == False
    assert parens_match_dc([')', '(']) == False
    assert parens_match_dc(['(', ')', '(', ')']) == True
    assert parens_match_dc(['a', '(', ')', '(']) == False
    assert parens_match_dc(['a', 'b', 'c']) == True
    assert parens_match_dc(['a', 'b', 'c', ')']) == False
    assert parens_match_dc(['(', 'a', 'b', 'c']) == False
    assert parens_match_iterative([')', '(']) == False
    assert parens_match_iterative([')', '(', ')']) == False

# Divide and conquer solution

def parens_match_dc(mylist):
    """
    Calls parens_match_dc_helper. If the result is (0,0),
    that means there are no unmatched parentheses, so the input is valid.

    Returns:
      True if parens_match_dc_helper returns (0,0); otherwise False
    """
    # done.
    n_unmatched_left, n_unmatched_right = parens_match_dc_helper(mylist)
    return n_unmatched_left == 0 and n_unmatched_right == 0


def parens_match_dc_helper(mylist):
    """
    Recursive, divide and conquer solution to the parens match problem.

    Returns:
      tuple (R, L), where R is the number of unmatched right parentheses, and
      L is the number of unmatched left parentheses. This output is used by
      parens_match_dc to return the final True or False value
    """
    if len(mylist) == 0:
        return 0, 0
    elif len(mylist) == 1:
        if mylist[0] == "(":
            return 0, 1
        elif mylist[0] == ")":
            return 1, 0
        else:
            return 0, 0
    else:

        left = mylist[:len(mylist)//2]
        right = mylist[len(mylist)//2:]
        lr, ll = parens_match_dc_helper(left)
        rr, rl = parens_match_dc_helper(right)

        # [')', '('] -> L:(1, 0), R:(0, 1) -> (1, 1)

        if lr > 0 and rl > 0 and ll == 0 and rr == 0:
            return (lr, rl)
        
        return rr - ll, rl - lr



    pass


def test_parens_match_dc():
    assert parens_match_dc(['(', ')']) == True
    assert parens_match_dc(['(']) == False
    assert parens_match_dc([')']) == False
    assert parens_match_dc([')', '(']) == False
    assert parens_match_dc(['(', ')', '(', ')']) == True
    assert parens_match_dc(['a', '(', ')', '(']) == False
    assert parens_match_dc(['a', 'b', 'c']) == True
    assert parens_match_dc(['a', 'b', 'c', ')']) == False
    assert parens_match_dc(['(', 'a', 'b', 'c']) == False
    assert parens_match_iterative([')', '(']) == False
    assert parens_match_iterative([')', '(', ')']) == False


if __name__ == '__main__':
    print("Testing iterative")
    test_parens_match_iterative()
    print("Iterative passed")
    print("Testing scan")
    test_parens_match_scan()
    print("Scan passed")
    print("Testing d&c")
    test_parens_match_dc()
    print("D&C passed")
