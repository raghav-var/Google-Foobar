def solution(s):
    passes = 0
    for i in range(0, len(s)):
        if s[i] == '>':
            for j in range(i + 1, len(s)):
                if s[j] == '<':
                    passes += 1
    return 2 * passes
