'''
Christian Williams
Thesis
17 September 2022
This program takes the parsed q file and creates an oracle for the training and testing data.
'''
from os import getcwd
from json import load, dump
from datetime import datetime
from random import randint, seed


INPUT_PATH = getcwd() + '\\input\\state-records-v2_1.json'
OUTPUT_PATH = getcwd() + '\\output\\translation-oracle-v1.json'



# Returns the input sentence for the oracle
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



        
    


# temporary work around input file format
def get_action_obj(action):
    action_obj = {}
    action_obj['throttle'] = action[0]
    action_obj['steer'] = action[1]
    action_obj['jump'] = action[5]
    action_obj['boost'] = action[6]
    action_obj['handbrake'] = action[7]
    return action_obj




def get_position_sentence(x,y):
    pos = []
    if x >= 0 and y >= 0:
        pos.append('in quadrant 1')
    if x < 0 and y >= 0:
        pos.append('in quadrant 2')
    if x < 0 and y < 0:
        pos.append('in quadrant 3')    
    if x >= 0 and y < 0:
        pos.append('in quadrant 4')
    if x <= 1000 and x >= -1000 and y <= 1000 and y >= -1000:
        pos.append('near the center')
    if x <= 1000 and x >= -1000 and y <= -3120:
        pos.append('near the blue goal')
    if x <= 1000 and x >= -1000 and y >= 3120:
        pos.append('near the orange goal')
    if x <= -3096:
        pos.append('near the east wall')
    if x >= 3096:
        pos.append('near the west wall')
    if y <= -4120:
        pos.append('near the south wall')
    if y >= 4120:
        pos.append('near the north wall')
    sentence = f"I'm {pos[0]} {' and '.join(pos[1:])}".strip() +'.'
    return sentence



def get_interval():
    mid = randint(2, 99)
    low = randint(1, mid-1)
    high = randint((mid+1), 100)
    return low, mid, high



# Input: 4 sentences for a category
# Output: random choice of a sentence    
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

def get_action(key, value):
    if key == 'steer':
        if value == -1:
            return 'left'
        else:
            return 'right'
    if key == 'throttle':
        if value == 1:
            return 'forwards'
        else:
            return 'backwards'


# Accepts the measures and action as an input
# returns the target sentence
def get_target_sentence(obj, action):
    pos = obj['position']
    sentence = ''
    template = get_sentences_template()


    # select sentences from the template and replace the attributes as necessary

    if obj['is_demoed']:
        return get_sentence(template['is_demoed'])
    if obj['boost_amount'] > 0:
        sentence += f" {get_sentence(template['boost_amount']).replace('*r', str(obj['boost_amount']))}"
    if obj['on_ground']:
        sentence += f" {get_sentence(template['on_ground'])}"
    sentence += f" {get_sentence(template['speed']).replace('*r', str(obj['speed']))}"
    sentence += f" {get_sentence(template['direction']).replace('*r', get_direction(obj['direction']))}"
    sentence += f" {get_position_sentence(pos[0], pos[1])}"
    
    if action['handbrake']:
        sentence += f" {get_sentence(template['action']['handbrake'])}"
    
    else:
        temp1 = f" {get_sentence(template['action']['steer']).replace('*r', get_action('steer', action['steer']))}"
        temp2 = f" {get_sentence(template['action']['throttle']).replace('*r', get_action('throttle', action['throttle']))}"
        sentence += f" {' and '.join([temp1.replace('.', ''), temp2])}"
    # if action['boost']:
    #     sentence += f" {get_sentence(template['action']['boost'])}"


    return sentence.strip()






# returns the sentences template
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
        'direction': ["I'm currently travelling *r.", "I'm heading in the *r direction.",
            'My current direction is *r.', "I'm heading *r."],
        'position': [],
        'action': {
            'handbrake': ["I'm currently braking.", "I pressed the brakes.", 
                "I'm stopping", "I stopped."],
            'steer': ["I'm steering *r.", "I'm turning *r.", 'I turned *r.',
                 "I'm about to turn *r."],
            'throttle': ["I'm driving *r", "I'm going *r.", "I'm moving *r.", "I'm travelling *r."],
            'boost': ["I've used boost.", "I'm using boost.", "I've used the speed up.", "I have boosted."]
        }
    }
    return template




# returns the oracle from the data set
def get_oracle(dataset):
    oracle = {}
    oracle['data'] = []
    for data in dataset:
        obj = {}
        action = get_action_obj(data['action'])
        data = data['state']['measurements']
        obj['input'] = f"{get_input_sentence(data)} {' '.join(f'{key} {action[key]}' for key in action.keys())}"
        obj['target'] = get_target_sentence(data, action)
        oracle['data'].append(obj)
        # print(obj)
    return oracle



def get_dataset(file_path):
    with open(file_path) as f:
        dataset = load(f)
    return dataset['data']

def output_oracle():
    seed(datetime.now())
    dataset = get_dataset(INPUT_PATH)
    oracle = get_oracle(dataset)
    with open(OUTPUT_PATH, 'w') as f:
        dump(oracle, f, indent=4)



def main():
    output_oracle()





if __name__ == '__main__':
    main()