# O(m) preprocess
# construct failure_function table
def preprocess(s: str) -> list:
    m = len(s)
    failure_function = [None for _ in range(m)]
    curr = 0
    j = -1
    failure_function[0] = -1
    while curr < m:
        # match
        if s[curr] == s[j]:
            # keep extending
            failure_function[curr] = failure_function[j]
        # mismatch!
        else:
            failure_function[curr] = j
            # dp idea: use previously calculated result
            while j > -1 and s[curr] != s[j]:
                j = failure_function[j]
        curr += 1
        j += 1
    return failure_function

# O(n) search for pattern P in text T
def search(failure_function: list, T: str, P: str) -> list:
    t, p = 0, 0
    ans = []
    # iter over text T
    while t < len(T):
        # match
        if T[t] == P[p]:
            t += 1
            p += 1
            # found pattern P in text T
            if p == len(P):
                ans.append(t-p)
                p = failure_function[p]
        # mismatch
        else:
            # check which idx in P to transition to
            p = failure_function[p]
            if p < 0:
                t += 1
                p += 1
    return ans


if __name__ == '__main__':
    T = 'abcdabcacacabcdac'
    P = 'abc'
    failure_function = preprocess(T)
    beginning_indices = search(failure_function, T, P)
    print(beginning_indices)
    occ = [T[i:i+len(P)] for i in beginning_indices]
    print(occ)
