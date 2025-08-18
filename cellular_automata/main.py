import time

import conways_GOL


class Wolfram:
    # fmt: off
    rules = [
        [0, 1, 1, 1, 1, 0, 1, 1],
        [0, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0]
    ]
    # fmt: on

    @classmethod
    def automata(cls, array, newArr, i, rule):
        arr = []
        if i == len(array) - 1:
            arr.append(array[i - 1])
            arr.append(array[i])
            arr.append(array[0])
        else:
            arr.append(array[i - 1])
            arr.append(array[i])
            arr.append(array[i + 1])
        if arr == [0, 0, 0]:
            newArr[i] = Wolfram.rules[rule][0]
            return
        if arr == [0, 0, 1]:
            newArr[i] = Wolfram.rules[rule][1]
            return
        if arr == [0, 1, 0]:
            newArr[i] = Wolfram.rules[rule][2]
            return
        if arr == [0, 1, 1]:
            newArr[i] = Wolfram.rules[rule][3]
            return
        if arr == [1, 0, 0]:
            newArr[i] = Wolfram.rules[rule][4]
            return
        if arr == [1, 0, 1]:
            newArr[i] = Wolfram.rules[rule][5]
            return
        if arr == [1, 1, 0]:
            newArr[i] = Wolfram.rules[rule][6]
            return
        if arr == [1, 1, 1]:
            newArr[i] = Wolfram.rules[rule][7]
            return

    @classmethod
    def printArrBlocks(cls, array):
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] == 1:
                    print("▓▓", end="")
                else:
                    print("░░", end="")
            print("")
        print(
            "______________________________________________________________________________________"
        )

    @classmethod
    def printArr(cls, array):
        print("|", end="")
        for i in range(len(array)):
            if array[i] == 1:
                print("#", end="")
            else:
                print(" ", end="")
            print("|", end="")
        print("")

    @classmethod
    def printArrSquares(cls, array):
        for i in range(len(array)):
            if array[i] == 1:
                print("⬜", end="")
            else:
                print("⬛", end="")
        print("")

    @classmethod
    def wolframGame(cls):
        array = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        Wolfram.printArrSquares(array)
        newArray = []
        for i in range(len(array)):
            newArray.append(0)
        while 1:
            # for a in range(50):
            for i in range(len(array)):
                Wolfram.automata(array, newArray, i, 4)
            time.sleep(0.1)
            Wolfram.printArrSquares(newArray)
            array = list(newArray)


if __name__ == "__main__":
    # Wolfram.wolframGame()
    conways_GOL.main()
    pass
