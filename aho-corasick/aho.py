from collections import deque

AdjList = []

def init_trie(keywords: list):
    create_empty_trie()
    add_keywords(keywords)
    set_fail_transitions()

def create_empty_trie():
    AdjList.append({
        'value': '',
        'next_states': [],
        'fail_state': 0,
        'output': []
    })

def add_keywords(keywords: list):
    for word in keywords:
        add_keyword(word)

def add_keyword(word: str):
    current_state = 0
    j = 0

    word = word.lower()
    child = find_next_state(current_state, word[j])
    while child:
        current_state = child
        j += 1
        if j < len(word):
            child = find_next_state(current_state, word[j])
        else:
            break
    for i in range(j, len(word)):
        node = {
                'value': word[i],
                'next_states': [],
                'fail_state': 0,
                'output': []
        }
        AdjList.append(node)
        AdjList[current_state]['next_states'].append(len(AdjList)-1)
        current_state = len(AdjList) - 1
    AdjList[current_state]['output'].append(word)


def find_next_state(current_state, value):
    for node in AdjList[current_state]['next_states']:
        if AdjList[node]['value'] == value:
            return node
    return None

def set_fail_transitions():
    Q = deque()
    child = 0
    for node in AdjList[0]['next_states']:
        Q.append(node)
        AdjList[node]['fail_state'] = 0
    while Q:
        R = Q.popleft()
        for child in AdjList[R]['next_states']:
            Q.append(child)
            state = AdjList[R]['fail_state']
            while find_next_state(state, AdjList[child]['value']) == None and state:
                state = AdjList[state]['fail_state']
            AdjList[child]['fail_state'] = find_next_state(state, AdjList[child]['value'])
            if not AdjList[child]['fail_state']:
                AdjList[child]['fail_state'] = 0
            AdjList[child]['output'] = AdjList[child]['output'] + AdjList[AdjList[child]['fail_state']]['output']


def get_keywords_found(line) -> list:
    line = line.lower()
    current_state = 0
    keywords_found = []
    for i in range(len(line)):
        while not find_next_state(current_state, line[i]) and current_state:
            current_state = AdjList[current_state]['fail_state']
        current_state = find_next_state(current_state, line[i])
        if not current_state:
            current_state = 0
        else:
            for j in AdjList[current_state]['output']:
                keywords_found.append({
                    'idx': i-len(j),
                    'word': j
                })
    return keywords_found

if __name__ == '__main__':
    keywords = ['cash', 'shew', 'ew']
    init_trie(keywords)
    T = 'blewcashblewcashew'
    print(T)
    print(get_keywords_found(T))

