def maxArea(height):

    largest = 0
    start = 0

    for h in height:
        start += 1

        for i in range(start + 1, len(height)):
            dist = i - start
            short = min(height[i], h)
            container = dist * short
            if container > largest:
                largest = container

    return largest

eights = [1,8,6,2,5,4,8,3,7]
print(maxArea(eights))