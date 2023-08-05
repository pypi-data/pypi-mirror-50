import phonetics

def phon(txt):
    res = phonetics.nysiis(txt)
    res2 = phonetics.dmetaphone(txt)
    print(f'{txt}  {res2[0]}')

phon('edberg')
phon('edburg')

phon('grey creek')
phon('gray creek')

phon('gro')

phon('low')
phon('lough')

phon('leigh')
phon('lay')

phon('monacco')
phon('monaco')

phon('burg')
phon('berg')









