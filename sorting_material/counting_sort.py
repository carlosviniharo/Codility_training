
def counting_sort(A, k):
    n = len(A)
    count = [0] * (k + 1)
    for i in range(n):
        count[A[i]] += 1
    p = 0
    for i in range(k + 1):
        for j in range(count[i]):
            A[p] = i
            p += 1
    return A


if __name__ == '__main__':
    A = [1, 2, 4, 5, 8, 2, 4, 5, 6]
    k = 8
    print(counting_sort(A, k))
