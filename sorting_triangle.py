
# Codility exercises for developers

def _do_max_product_of_three(A):
    n = len(A)
    A.sort()
    if n < 3:
        return 0
    for index in range(0, n-2):
        if A[index] + A[index + 1] > A[index + 2]:
            return 1
    return 0


if __name__ == '__main__':
    A = []
    print(_do_max_product_of_three(A))
