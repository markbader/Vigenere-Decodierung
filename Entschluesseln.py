class Entschluesseln:
    def __init__(self, file):
        file = open(file, 'r')
        self.text = file.read()
        file.close()
        self.alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.haeufigkeit = ['E','N','I','S','R','A','T','D','H','U','L','C','G','M','O','B','W','F','K','Z','P','V','J','Y','X','Q']

    def kennwort_laenge(self, varianz=7):
        block = {}
        block_abstand = []
        for i in range(len(self.text)-varianz):
            if self.text[i:i+varianz] in block:
                block_abstand.append(i-block[self.text[i:i+varianz]][1])
                block[self.text[i:i+varianz]] = [block[self.text[i:i+varianz]][0]+1, i-block[self.text[i:i+varianz]][1]]
            else:
                block[self.text[i:i+varianz]] = [1, i, 0]
        teiler = []
        for i in block_abstand:
            teiler += self.teiler(i)
        return self.haeufigste(teiler)

    def teiler(self, zahl):
        teiler = []
        for i in range(2, zahl//2):
            if zahl//i==zahl/i:
                teiler.append(i)
        return teiler

    def haeufigste(self, liste):
        maxi = []
        while liste!=[]:
            maxi.append(max(set(liste), key=liste.count))
            while maxi[-1] in liste:
                liste.remove(maxi[-1])
        return maxi

    def kennwort(self, laenge, varianz=1):
        text=[]
        kennwort = ''
        for i in range(laenge):
            text.append([])
        for i in range(len(self.text)):
            text[i%laenge]+=self.text[i]
        for i in text:
            abstaende = []
            h = self.haeufigste(i)[0:varianz]
            for j in range(len(h)):
                abstaende.append((self.alphabet.index(h[j])-self.alphabet.index(self.haeufigkeit[j]))%len(self.alphabet))
            kennwort += self.alphabet[self.haeufigste(abstaende)[0]]
        return kennwort

    def entschluesseln(self, var=0, var_kennwort=8, kennwort=False):
        if not kennwort:
            kennwort = self.kennwort(self.kennwort_laenge(varianz=var_kennwort)[var])
        text = ''
        for i in range(len(self.text)):
            text += str(self.alphabet[(self.alphabet.index(self.text[i])-self.alphabet.index(kennwort[i%len(kennwort)]))%len(self.alphabet)])
        return text

    def schreiben(self, text, name='entschluesselt.txt'):
        file = open(name, 'w')
        file.write(text)
        file.close()

    def ausgabe(self):
        laenge = 0
        kontrolle = 8
        while True:
            kennwort = self.kennwort(self.kennwort_laenge(varianz=kontrolle)[laenge])
            text = self.entschluesseln(var=laenge, var_kennwort=kontrolle, kennwort=kennwort)
            antwort = input('\n'+str(text[0:100])+'\n\n>>>Ist der Textausschnitt lesbar? (j/n): ')
            if antwort == 'j':
                self.schreiben(text)
                print('>>>Der Text wurde in der Datei "entschluesselt.txt" gespeichert.')
                return True
            if antwort == 'n':
                laenge += 1
            else:
                print('>>>Falsche Eingabe!')
                
if __name__=="__main__":
    file = str(input('Datei zum Decodieren: '))
    e = Entschluesseln(file)
    e.ausgabe()
