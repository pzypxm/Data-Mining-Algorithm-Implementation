from sys import argv
from math import sqrt
from operator import itemgetter


def utility_matrix(fd):

    # Read in rating data set
    rating_dataset = []
    for line in fd:
        rating_dataset.append(line.split("\n")[0].split("\t"))

    u_matrix = {}
    for rate in rating_dataset:
        u_matrix.setdefault(rate[0], {})
        u_matrix[rate[0]].setdefault(rate[2], float(rate[1]))

    # Construct a full list of movie names
    all_movie = []
    for username in u_matrix:
        # Check every user's rate to make sure the list covers all the names
        for movie in u_matrix[username]:
            exist = 0
            for name in all_movie:
                if movie == name:
                    exist = 1
            if exist == 0:
                all_movie.append(movie)

    # Construct final utility matrix
    for username in u_matrix:
        for movie in all_movie:
            u_matrix[username].setdefault(movie, 0.0)
        temp = []
        for i in u_matrix[username]:
            temp.append([i, u_matrix[username][i]])
        u_matrix[username] = sorted(temp)

    return u_matrix


def pearson_correlation(user1, user2):      # Variable user1, user2 are 'rate lists' of two users from utility matrix

    # Convert user's rate list to pure numeric one
    vector1 = []
    vector2 = []
    for rate in user1:
        vector1.append(rate[1])
    for rate in user2:
        vector2.append(rate[1])

    # Calculate mean
    count = 0
    for i in vector1:
        if i != 0.0:
            count += 1
    avg1 = sum(vector1)/count

    count = 0
    for i in vector2:
        if i != 0.0:
            count += 1
    avg2 = sum(vector2)/count

    # Calculate Pearson Correlation Coefficient
    numerator = 0
    denominator_part1 = 0
    denominator_part2 = 0
    for i in range(0, len(vector1)):
        if vector1[i] != 0 and vector2[i] != 0:
            numerator += (vector1[i]-avg1)*(vector2[i]-avg2)
            denominator_part1 += (vector1[i]-avg1)**2
            denominator_part2 += (vector2[i]-avg2)**2
    denominator = (sqrt(denominator_part1) * sqrt(denominator_part2))

    if denominator == 0:
        return 0.0
    else:
        return numerator/denominator


def k_nearest_neighbors(user_name1, k, u_matrix):

    weight = []
    for user_name2 in u_matrix:
        weight.append([user_name2, pearson_correlation(u_matrix[user_name1], u_matrix[user_name2])])

    neighbors = []
    k += 1
    for value in sorted(weight, key=itemgetter(1, 0), reverse=True):
        if k > 0:
            if value[1] != 1.0:
                neighbors.append(value)
            k -= 1
        else:
            break

    return neighbors


def predict(movie_name, k_nearest_neighbors, u_matrix):

    numerator = 0
    denominator = 0
    for name in k_nearest_neighbors:
        for item in u_matrix[name[0]]:
            if item[0] == movie_name:
                if item[1] != 0.0:
                    denominator += name[1]
                    numerator += name[1]*item[1]

    if denominator == 0:
        return 0
    else:
        return numerator/denominator


if __name__ == '__main__':
    # For IDE debugging
    # input_fd = open("/Users/patrickpeng/Workspace_Python/Assignment_3/ratings-dataset.tsv")
    # uid = "Kluver"
    # movie = "The Fugitive"
    # k = 10

    input_fd = open(argv[1])
    uid = str(argv[2])
    movie = str(argv[3])
    k = int(argv[4])

    matrix = utility_matrix(input_fd)

    neighbor = k_nearest_neighbors(uid, k, matrix)

    for i in neighbor:
        if i[1] != 1:
            print i[0], i[1]

    print '\n', '\n', predict(movie, neighbor, matrix)
