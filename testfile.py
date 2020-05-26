
def maxDistToClosest(seats: List[int]) -> int:

    longest = 0
    tracking = 0
    dist = 0
    first = 0

    for i in range(len(seats)):
        if seats[i] == 0:
            tracking += 1
        else:
            if first == 0:
                first = tracking
            if tracking > longest:
                longest = tracking
                if tracking % 2 == 0:
                    seat = i - (tracking // 2)
                else:
                    seat = i - (tracking // 2) + 1

                dist = tracking // 2
                tracking = 0

        if i == len(seats) - 1 and tracking > dist:
            seat = i
            dist = tracking

    if first > dist:
        seat = 0

    return seat

eights = [1,0,0,0,1,0,1]
print(maxDistToClosest(eights))