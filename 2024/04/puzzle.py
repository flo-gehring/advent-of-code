from typing import List


input = [s.strip() for s in open("2024/04/input.txt").readlines()]
count = 0
def checkWord(x: int, y: int, input: List[str], word: str, xDir: int, yDir:int):
    currX = x
    currY = y
    for char in word:
        if currX >= len(input) or currY >= len(input[currX]):
            return False
        if currX < 0 or currY < 0:
            return False
        if char != input[currX][currY]:
            return False
        currX += xDir
        currY += yDir
    return True

def countWord(x: int, y: int, input: List[str], word: str):
    result = 0
    for deltaX in range(-1,2):
        for deltaY in range(-1,2):
            if deltaX == 0 and deltaY == 0:
                continue
            result += checkWord(x, y, input, word, deltaX, deltaY)
    return result

for x in range(len(input)):
    for y in range(len(input[0])):
        count += countWord(x,y,input, "XMAS")
print(count)

count_xmas = 0
def checkXmas(x: int, y: int, input: List[str]):
    if x < 1 or y < 1 or y >= len(input[0]) - 1 or x >= len(input) -1:
        return False
    diagDown = input[x-1][y-1] + input[x][y] + input[x+1][y+1]
    diagUp = input[x-1][y+1] +  input[x][y] +  input[x+1][y-1]
    return (diagUp == "SAM" or diagUp == "MAS") and (diagDown == "SAM" or diagDown  == "MAS")

for x in range(len(input)):
    for y in range(len(input[0])):
        count_xmas += checkXmas(x,y,input)
print(count_xmas)