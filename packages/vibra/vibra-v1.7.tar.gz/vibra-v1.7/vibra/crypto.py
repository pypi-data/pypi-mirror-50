class Crypto(object):
    def initCaesar(self):
        self.al = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "U",
                   "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                   "p",
                   "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self.als = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u",
                    "v", "w", "x", "y", "z"]
        self.i2al = {i: u for i, u in enumerate(self.al)}
        self.i2als = {i: u for i, u in enumerate(self.als)}
        self.al2i = {u: i for i, u in enumerate(self.al)}
        self.als2i = {u: i for i, u in enumerate(self.als)}

    def __init__(self,init='all'):
        if init is 'all':
            self.initCaesar()
        if init is 'caesar':
            self.initCaesar()

    def encode(self,s,encoding): #encoding=(type, shift, small only)

        if encoding[0] is "caesar" and encoding[2]:
            c = ""
            cce=encoding[1]
            for a in s:
                dot=(self.als2i[a]+cce)%26
                c+=self.i2als[dot]
            return c

        elif encoding[0] is "caesar" and encoding[2]==False:
            c = ""
            cce=encoding[1]
            for a in s:
                dot=(self.al2i[a]+cce)%52
                c+=self.i2al[dot]
            return c