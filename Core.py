from random import randint, choice


class Game:
    def __init__(self, difficulty):
        self.numbersList = []
        self.operations = []
        self.goal = 0

        if difficulty == 0:
            self.numbersList = [randint(2, 9) for _ in range(6)]

        elif difficulty == 1:
            smalls = randint(3, 4)
            self.numbersList = [randint(2, 9) for _ in range(smalls)]
            self.numbersList += [randint(10, 20) for _ in range(6-smalls)]

        elif difficulty == 2:
            smalls = randint(2, 3)
            self.numbersList = [randint(6, 14) for _ in range(smalls)]
            self.numbersList += [randint(12, 25) for _ in range(6-smalls)]

        else:  # if difficulty = 3
            self.numbersList = [randint(10, 25) for _ in range(6)]

        self.makeGoal(difficulty)

    def makeGoal(self, difficulty):
        while True:
            operation = [['+', '+', '+', '+', '+', '+', '-', '-'],
                         ['+', '+', '+', '+', '-', '-', '*', '*'],
                         ['+', '+', '+', '-', '-', '*', '*', '*'],
                         ['+', '+', '-', '-', '*', '*', '*', '*']]
            operation = operation[difficulty]

            numbersList = self.numbersList.copy()
            self.operations = []

            num = choice(numbersList)
            numbersList.remove(num)
            self.goal = str(num)

            for i in range(2 + difficulty):
                while True:
                    ope = choice(operation)
                    num = choice(numbersList)

                    goal = str(self.goal)
                    goal = str(eval(goal + ope + str(num)))
                    try:
                        if int(goal) > 0:
                            self.goal = int(goal)
                            self.operations.append(ope)
                            operation.remove(ope)
                            numbersList.remove(num)
                            break
                    except ValueError:
                        pass

            ranges = [(10, 50), (50, 100), (100, 250), (200, 800)]
            low, high = ranges[difficulty]
            if low < self.goal < high:
                break
