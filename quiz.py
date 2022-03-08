import yaml
import re
import json


class Quiz:

    def __init__(self, arg):
        with open(f'{arg}.yaml', 'r') as file:
            self.quiz = yaml.safe_load(file)
        self.cC = 0
        self.cQ = 0
        self.q = None
        self.answers = dict()
        self.standings = dict()
        self.running = False
        self.setupAnswerType = {
            'Exact' : lambda a,o: TypeExact(a),
            'Any' : lambda a,o: TypeAny(a,o),
            'All' : lambda a,o: TypeAll(a,o),
            'Each' : lambda a,o: TypeEach(a,o)
        }

        self.answerInstance = None

    def reset(self):
        self.cC = 0
        self.cQ = 0
        self.standings = dict()
        self.running = False

    def start(self):
        self.running = True
        return self.return_question()

    def next(self):
        if not self.running:
            return None
        if self.cQ < len(self.quiz['Categories'][self.cC]['Questions']) - 1:
            self.cQ += 1
            return self.return_question()
        if self.cC < len(self.quiz['Categories']) - 1:
            self.cC += 1
            self.cQ = 0
            return self.return_question()
        return None


    def return_question(self):
        if not self.running:
            return
        for k,v in self.answers.items():
            try:
                self.standings[k] = self.standings[k] + v
            except KeyError:
                self.standings[k] = v

        self.answers = dict()
        q = self.quiz['Categories'][self.cC]['Questions'][self.cQ]
        self.q = q
        self.answerInstance = self.setupAnswerType[q['Type']](q['Answer'], q['Info'])
        skey = lambda i: i[1]
        sortedStandings = dict(sorted(self.standings.items(), key=skey, reverse=True))
        print(json.dumps(sortedStandings, sort_keys=False, indent=2))
        return q, self.quiz, (self.cC, self.cQ)

    def answer(self, user, userInput):
        if not self.running:
            return None
        pts = self.q['Points'] * int(self.answerInstance.answer(userInput))
        self.answers[user] = pts


class Modify:

    def modify(self, s):
        s = str(s)
        s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
        return s


class TypeExact(Modify):

    def __init__(self, correctAnswer):
        self.correctAnswer = self.modify(correctAnswer)

    def answer(self, userAnswer):
        if self.modify(userAnswer) == self.correctAnswer:
            return True
        else:
            return False


class TypeAny(Modify):

    def __init__(self, correctAnswers, options):
        if isinstance(options, list):
            if all(isinstance(a, int) for a in correctAnswers):
                self.answersText = [ self.modify(options[i-1]) for i in correctAnswers ]
                self.answersIndices = correctAnswers
            else:
                self.answersText = [ self.modify(a) for a in correctAnswers ]
                self.answersIndices = [ options.index(a)+1 for a in correctAnswers ]
        else:
            self.answersText = [ self.modify(a) for a in correctAnswers ]
            self.answersIndices = None

    def answer(self, userAnswer):
        try:
            idx = int(userAnswer)
        except ValueError:
            idx = None

        if self.answersIndices != None and idx != None:
            if idx in self.answersIndices:
                return True
        elif self.modify(userAnswer) in self.answersText:
            return True
        else:
            return False


class TypeAll(TypeAny):

    def answer(self, userAnswer):
        try:
            idxList = { int(self.modify(a)) for a in userAnswer.split(',') }
        except ValueError:
            idxList = None
        if self.answersIndices != None:
            self.answersIndices = set(self.answersIndices)
        answerList = { self.modify(a) for a in userAnswer.split(',') }
        self.answersText = set(self.answersText)

        if len(answerList) != len(self.answersText):
            return False

        if idxList != None and self.answersIndices != None:
            if idxList == self.answersIndices:
                return True
        elif self.answersText == answerList:
            return True
        else:
            return False


class TypeEach(TypeAny):

    def answer(self, userAnswer):
        try:
            idxList = { int(self.modify(a)) for a in userAnswer.split(',') }
        except ValueError:
            idxList = None
        if self.answersIndices != None:
            self.answersIndices = set(self.answersIndices)
        answerList = { self.modify(a) for a in userAnswer.split(',') }
        self.answersText = set(self.answersText)

        correctIdx = 0
        correctText = 0

        if idxList != None and self.answersIndices != None:
            for i in idxList:
                if i in self.answersIndices:
                    correctIdx += 1
                else:
                    correctIdx -= 1
        for a in answerList:
            if a in self.answersText:
                correctText += 1
            else:
                correctText -= 1

        out = max((correctText, correctIdx))
        if out < 0: out = 0
        return out

