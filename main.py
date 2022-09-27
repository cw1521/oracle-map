'''
Christian Williams
Thesis
17 September 2022
This program takes the parsed q file and creates an oracle for the training and testing data.
'''
from os import getcwd
from json import load
from datetime import datetime
from random import randint, seed


INPUT_PATH = getcwd() + '\\input\\state-records-v2_1.json'


def get_input_sentence(obj):
    output = ''
    for key in obj.keys():
        if output != '':
            output += ' '
        if key == 'position':
            output += f"{key} {' '.join(str(elem) for elem in obj[key])}"
        else:
            output += f'{key} {str(obj[key])}'
    return output


# def get_interval(num_divisions):
#     interval = [0 for elem in range(num_divisions)]
#     interval.insert(1, randint(1, 100))
#     for i in range(0, num_divisions, 2):
#         interval.insert(i+2, randint(1, 100))
#         interval.insert(i, randint(1, interval[i+1]))
#     print(interval)
#     return interval


def get_direction(heading):
    if heading >= 337 or heading < 22:
        return "east"
    elif heading >= 22 and heading < 67:
        return 'northeast'
    elif heading >= 67 and heading < 112:
        return 'north'
    elif heading >= 112 and heading < 157:
        return 'northwest'
    elif heading >= 157 and heading < 202:
        return 'west'
    elif heading >= 202 and heading < 247:
        return 'southwest'
    elif heading >= 247 and heading < 292:
        return 'south'
    elif heading >= 292 and heading < 337:
        return 'southeast'


def get_position():
    return ''



def get_interval():
    mid = randint(2, 99)
    low = randint(1, mid-1)
    high = randint((mid+1), 100)
    return low, mid, high

    
def get_sentence(sentences):
    low, mid, high = get_interval()
    rand_num = randint(1, 100)
    if rand_num <= low:
        return sentences[0]
    elif rand_num > low and rand_num <= mid:
        return sentences[1]
    elif rand_num > mid and rand_num <= high:
        return sentences[2]
    elif rand_num > high:
        return sentences[3]

# to do
def get_target_sentence(obj):
    # print(obj)
    sentence = ''
    template = get_sentences_template()
    if obj['is_demoed']:
        # print(get_sentence(template['is_demoed']))
        return get_sentence(template['is_demoed'])
    if obj['boost_amount'] > 0:
        # print(get_sentence(template['boost_amount']).replace('*r', str(obj['boost_amount'])))
        sentence += f" {get_sentence(template['boost_amount']).replace('*r', str(obj['boost_amount']))}"
    if obj['on_ground']:
        # print(get_sentence(template['on_ground']))
        sentence += f" {get_sentence(template['on_ground'])}"
    sentence += f" {get_sentence(template['speed']).replace('*r', str(obj['speed']))}"
    sentence += f" {get_sentence(template['direction']).replace('*r', get_direction(obj['direction']))}"

    return sentence.strip()



def get_sentences_template():
    template = {
        'is_demoed': ['My car has been demolished.', 'My car has exploded!',
            'I crashed my car!', 'I wrecked my car.'],
        'boost_amount': ['My current boost is *r.', 'I currenly have *r percent boost.', 
            'I have *r boost.', 'My boost is *r percent.'],
        'on_ground': ['My car is on the ground.', "I'm on the ground.", "I'm not in the air.",
            "I'm currently driving on the ground."],
        'ball_touched': ['I have the ball!', "I've got the ball!", "I currently have the ball.",
            "The ball is in my possession."],
        'speed': ['My current speed is *r.', "I'm travelling *r miles per hour.", 
            'My current speed is *r mph.', 'My current speed is *r miles per hour.'],
        'direction': ["I'm currently traveling *r.", "I'm heading in the *r direction.",
            'My current direction is *r', "I'm heading *r."],
        'position': []
    }
    return template





def get_oracle(dataset):
    oracle = {}
    oracle['data'] = []
    for data in dataset:
        obj = {}
        action = data['action']
        data = data['state']['measurements']
        obj['input'] = get_input_sentence(data) +' action ' + ' '.join(str(elem) for elem in action)
        obj['target'] = get_target_sentence(data)
        oracle['data'].append(obj)
        print(obj)
    return oracle



def get_dataset(file_path):
    with open(file_path) as f:
        dataset = load(f)
    return dataset['data']





def main():
    seed(datetime.now())
    dataset = get_dataset(INPUT_PATH)
    oracle = get_oracle(dataset)

    # print(dataset)
    # print(len(dataset))
    # print(oracle)
    # print(len(oracle))





if __name__ == '__main__':
    main()