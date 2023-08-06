import random
def palette():
    letters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = "#"
    for x in range(0, 6):
        color += random.choice(letters)
    x = color
    return x