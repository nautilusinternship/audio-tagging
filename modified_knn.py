# -----------------------------------------------------------
# modified_knn.py: db layer program for Audio Tagging application
# (likely not being used but saved for reference!)
# -----------------------------------------------------------
import operator
# Row: audio file --> {word:freq, ...}
class Row:
    def __init__(self, audio, word_dict):
        self.audio = audio
        self.word_dict = word_dict

class Pair:
    def __init__(self, audio, dist):
        self.audio = audio
        self.dist = dist

def find_audio_knn(query, k):
    # build list of (audio, dist) pairs
    dist_list = []
    for row in dataset:
        current_wd = row.word_dict
        for key in current_wd:
            for word in query:
                if key == word:
                    dist = 1/float(current_wd[key])
                    dist_list.append(Pair(row.audio, dist))
    # sort pairs by value
    sorted_dist_list = sorted(dist_list, key=operator.attrgetter("dist"), reverse=False)
    for entry in sorted_dist_list:
        print(entry.audio + ", " + str(entry.dist))
    # grab first k entries of sorted list
    sorted_dist_list = sorted_dist_list[:k]
    # find mode of labels
    mode_dict = {}
    for entry in sorted_dist_list:
        if entry.audio in mode_dict:
            mode_dict[entry.audio] += 1
        else:
            mode_dict[entry.audio] = 1
    for key, value in mode_dict.items():
        print(key + ", " + str(value))
    sorted_mode_dict = sorted(mode_dict.items(), key=lambda x: x[1], reverse=True)
    return list(sorted_mode_dict[0])[0]
    
def find_audio_sum(query):
    # build list of (audio, dist) pairs
    dist_dict = {}
    for row in dataset:
        current_wd = row.word_dict
        for key in current_wd:
            for word in query:
                if key == word:
                    dist = 1/float(current_wd[key])
                    if row.audio in dist_dict:
                        dist_dict[row.audio]+=dist
                    else:
                        dist_dict[row.audio]=dist
    # sort pairs by value
    sorted_dist_dict = sorted(dist_dict.items(), key=lambda x: x[1], reverse=False)
    for key, value in sorted_dist_dict:
        print(key + ", " + str(value))
    return list(sorted_dist_dict[0])[0]

# tests
# create word dicts (for pseudo dataset)
wd1 = {'red': 2, 'blue': 4, 'yellow': 6}
wd2 = {'red': 2, 'purple': 4, 'green': 6}
wd3 = {'red': 1, 'blue': 4, 'orange': 6}
# create peudo dataset rows
row1 = Row('audio1', wd1)
row2 = Row('audio2', wd2)
row3 = Row('audio3', wd3)
dataset = [row1, row2, row3]
# create query word dict
query = ['red', 'blue', 'green']
print("knn: " + find_audio_knn(query, 3))
print("sum: " + find_audio_sum(query))
