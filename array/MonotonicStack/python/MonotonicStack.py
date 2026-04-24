def next_greater_elements(values: list[int]) -> list[int]:
    answer = [-1] * len(values)
    stack: list[int] = []

    for index in range(len(values) - 1, -1, -1):
        while stack and stack[-1] <= values[index]:
            stack.pop()
        if stack:
            answer[index] = stack[-1]
        stack.append(values[index])

    return answer
