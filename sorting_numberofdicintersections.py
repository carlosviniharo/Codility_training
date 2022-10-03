
def solution(A):
    n = len(A)
    lower = [0] * n
    upper = [0] * n

    # all the lower and upper points
    for i in range(n):
        lower[i] = i - A[i]
        upper[i] = i + A[i]
    lower.sort()
    upper.sort()
    lower_index = 0
    intersections = 0

    for upper_index in range(n):
        while lower_index < n and upper[upper_index] >= lower[lower_index]:
            lower_index += 1
        intersections += lower_index - upper_index - 1

    if intersections > 10000000:
        return -1
    return intersections


if __name__ == '__main__':
    A = [1, 5, 2, 1, 4, 0]
    print(solution(A))
