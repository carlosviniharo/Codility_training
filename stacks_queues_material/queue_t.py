

def push(x):
    global tail
    tail = (tail + 1) % N
    queue_t[tail] = x


def pop():
    global head
    head = (head + 1) % N
    return queue_t[head]


def size():
    return (tail - head + N) % N


def empty():
    return head == tail


if __name__ == '__main__':
    N = 5
    queue_t = [0] * N
    head, tail = 0, 0
    push(5)
    push(6)
    print(queue_t)
    