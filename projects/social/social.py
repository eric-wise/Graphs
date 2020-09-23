import random
import math


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}  # {1: User("1"), 2: User("2"), ...}
        self.friendships = {}  # {1: {2,3,4}, 2: {1}, 3: {1}, 4:{1}}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        # Generate all the possible friendships and put them into an array
        # 3 users (0,1,2)
        # [(0,1), (0,2), (1,2)]
        possible_friendships = []
        for user_id in self.users:
            # To prevent duplicate friendships create from user_id +1
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # Shuffel the friendship array
        # [(1,2),(0,1), (0,2)]
        random.shuffle(possible_friendships)

        # Take the first num_users * avg_friendships / 2 and that wil be the friendships for the graph
        for i in range(math.floor(num_users * avg_friendships/2)):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        neighbors_to_visit = Queue()
        neighbors_to_visit.enqueue([user_id])
        while neighbors_to_visit.size() > 0:
            # deque the first path
            current_path = neighbors_to_visit.dequeue()
            # grab most recent vertex
            current_vertex = current_path[-1]
            # if the current vertex has not been visited
            if current_vertex not in visited:
                # if not visited[current_vertex] or current_path not in visited:
                # add current vertex to the visited dict with
                # path that led here
                visited[current_vertex] = current_path
                for n in self.friendships[current_vertex]:
                    path_copy = current_path.copy()
                    path_copy.append(n)
                    neighbors_to_visit.enqueue(path_copy)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
