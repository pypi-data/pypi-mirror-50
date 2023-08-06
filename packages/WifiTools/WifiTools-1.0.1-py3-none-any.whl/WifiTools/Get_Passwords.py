import random

LITTER_UP = [chr(i) for i in range(65,90)]
LITTER_DOWN = [chr(i) for i in range(97, 123)]
NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

K = []
LITTER = []
for item in LITTER_UP:
    K.append(item)
    LITTER.append(item)
for item in LITTER_DOWN:
    K.append(item)
    LITTER.append(item)
for item in NUMBER:
    K.append(str(item))

Keys = []
s = []

def Report(i, max):
    if i % (max / 10) == 0:
        print("百分之", i / (max / 100))

def Get(Type='NL', max=1000, file='Passwords', count=8, Caps='both', Custom=None, write=True):
    i = 0
    if Type == 'NL' and Caps == 'both':
        while i < max:
            key = ''.join(random.sample(K, count))
            Keys.append(key)
            i +=1

            Report(i , max)
    elif Type == 'N' and Caps == 'both':
        while i < max:
            key = ''.join(random.sample(NUMBER, count))
            Keys.append(key)
            i += 1

            Report(i, max)
    elif Type == 'L':
        while i < max:
            key = ''.join(random.sample(LITTER, count))
            Keys.append(key)
            i += 1

            Report(i , max)
    elif Type == 'custom' and Custom:
        i = 0
        while i < max:
            content = []
            for item in Custom:
                for k, value in item.items():
                    if k == 'N':
                        content.append(''.join(random.sample(NUMBER, value)))
                    elif k == 'Ll':
                        content.append(''.join(random.sample(LITTER, value)))
                    elif k == 'NL':
                        content.append(''.join(random.sample(LITTER_UP, value)))
                    elif k == 'Nl':
                        content.append(''.join(random.sample(LITTER_DOWN, value)))

                i += 1
            Report(i, max)
            key = ''

            for item in content:
                key += item
            Keys.append(key)

    result = set(Keys)

    if write:
        file = open(file, 'w')
        for item in result:
            file.write(item + "\n")
        file.close()

    return result
