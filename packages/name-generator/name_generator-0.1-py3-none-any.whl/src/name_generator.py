import random

alphabet = "abcdefghijklmnopqrstuvwxyz"
vowels = "aeiouy"
consonants = "bcdfghjklmnpqrstvwxz"

def GenSyllabes(cons, vow):
    syllabes = []
    
    for c_ind, c in enumerate(cons):
        for v_ind, v in enumerate(vow):
            syllabes.append(c+v)
            syllabes.append(v+c)
            
            for c2_ind, c2 in enumerate(cons):
                syllabes.append(c+v+c2)
                
            for v2_ind, v2 in enumerate(vow):
                syllabes.append(v+c+v2)
                
    return syllabes

def rnd(array):
    return random.choice(array)
    
def GenSyllabe(cons, vow):
    # syllabe_types = 
    # [
    #     f"{rnd(cons)}{rnd(vow)}",
    #     f"{rnd(vow)}{rnd(cons)}",
    #     f"{rnd(cons)}{rnd(cons)}{rnd(vow)}",
    #     f"{rnd(vow)}{rnd(cons)}{rnd(cons)}",
    #     f"{rnd(cons)}{rnd(vows)}{rnd(cons)}",
    # ]

    syllabe_formats = [
        "{c1}{v1}",
        "{v1}{c1}",
        "{c1}{c2}{v1}",
        "{v1}{c1}{c2}",
        "{c1}{v1}{c2}",
        "{v1}{c1}{v2}",
    ]

    syllabe_format = random.choice(syllabe_formats)

    c1 = random.choice(cons)
    c2 = random.choice(cons)
    v1 = random.choice(vow)
    v2 = random.choice(vow)

    syllabe = syllabe_format.format(c1=c1, c2=c2, v1=v1, v2=v2)

    return syllabe

    #return random.choice((random.choice(cons)+random.choice(vow), random.choice(vow)+random.choice(cons)))
    
syllabes = (
    "de", "ko", "ro", "ba", "sor", "war", "ham", "kui", "hip", "ku",
    "ru", "bu", "be", "fu", "ng", "do", "mar", "ti", "der", "das", "tar",
    "mi", "ki", "no", "mo", "si", "lu", "ge", "ja", "sa", "wor", "ski", "mid",
    "gar", "tal", "bru", "uh", "oh", "le", "wi", "gla", "er", "eh", "sh", "uf",
    "rar", "mes", "ban", "am", "rei", "ash", "ske", "tor", "com", "hu", "ry",
    "twi", "he", "re", "um", "der", "bul", "mam", "nan", "nam", "nom", "nik", 
    "fi", "fin", "at", "ot", "et", "bet", "fa", "fe", "bro", "ho", "how", 
    "who", "bel", "je", "ju", "we", "wa", "fun", "fen", "fon", "ny", "in",
    "arde", "rap", "dia", "dur", "bur", "mer", "per", "ker", "kur", "wa", 
    "rep", "sol", "er", "ner", "far", "win", "won", "wen", "hank", "bark", 
    "cast", "kek", "em", "die", "dia", "dio", "gay", "oof", "goo", "pip", 
    "pyt", "ral", "gen", "lag", "tre", "ej", "tard", "lib", "ree", "son", 
    "cri", "nic", "fuc", "ola", "ala", "ela", "ole", "ale", "ele", "olo", 
    "elo", "alo", "den", "ben", "ken", "kik", "pik", "fen", "ren", "nen",
    "heh", "geh", "cha", "ce"
)

def GenName(minSyllabesNum=2, maxSyllabesNum=3):
    name = ""
    
    for n in range(random.randint(minSyllabesNum, maxSyllabesNum)):
        if random.randint(1, 4) == 1:
            name += GenSyllabe(consonants, vowels)
        else:
            name += syllabes[random.randint(0, len(syllabes)-1)]
        
    return name

    """
    names = []
        
    for i in range(10000):
        name = ""
        for n in range(random.randint(2, 3)):
            if random.randint(1, 10) == 1:
                name += random.choice(("con", "tent"))
            else:
                name += syllabes[random.randint(0, len(syllabes)-1)]
        if name not in names:
            names.append(name)
            print(name)
        
    file_obj = open("C:\\Users\\Mateusz\\Desktop\\server_names.txt", "w")
    file_obj.write("\n".join(names))
    file_obj.close()
    """
    
#print("\n".join(GenSyllabes(consonants, vowels)))

# print(GenName())

# for i in range(200):
#     print(GenName(maxSyllabesNum=4))