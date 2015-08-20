import random

def ghost():
  print "here we go:"

  dictionary = open('dictionary.txt');
  trie = {}
  for line in dictionary:
    #print line,
    if len(line) < 5:
      continue
    curr = trie
    # reduce upper limit by one to remove "\n"s
    for i in range(0, len(line)):
      char = line[i]
      #print char
      if char not in curr:
        #curr[char][next_char] = {}
        curr[char] = {}
      curr = curr[char]

  print len(str(trie))
  #for key in trie:
  #  print key + "  " + str(trie[key])
  #
  #indent = 0
  #for char in str(trie):
  #  print char,
  #  if char == " ":
  #    continue
  #  if char == ",":
  #    print "\n" + (indent-4)*" ",
  #  if char == "{":
  #    print "\n" + indent*" ",
  #    indent += 2
  #  if char == "}":
  #    indent -= 2
  #    print "\n" + (indent-2)*" ",
  #print ""
  #
  letters = ""
  current = trie

  while (1):
    letter = raw_input("> "+ letters)
    if len(letter) != 1:
      print "just one letter please"
      continue
    letters += letter
    if letter in current:
      current = current[letter]
    else:
      print "not possible"
      break
    if "\n" in current:
      print "that is a word"
      break
    if not current.keys():
      print "you win!"
      break
    else:
      opponent_letter = random.choice(current.keys())
      print "okay, my turn, I'll add the letter " + opponent_letter
      letters += opponent_letter
      current = current[opponent_letter]
      if "\n" in current:
        print "oops, you win"
        break

def superghost():
  dictionary = open('dictionary.txt');
  appends = {}
  prepends = {}
  words = {}
  histogram = [0]*40
  for line in dictionary:
    #print line,
    word = line[0:-1]
    if len(word) > 3:
      words[word] = 1
    for i in range(0, len(word)):
      for j in range(i, len(word)):
        if word[i+1:j+1] in prepends:
          if word[i] not in prepends[word[i+1:j+1]]:
            prepends[word[i+1:j+1]].add(word[i])
        else:
          prepends[word[i+1:j+1]] = { word[i] } 
        if word[i:j] in appends:
          if word[j] not in appends[word[i:j]]:
            appends[word[i:j]].add(word[j])
        else:
          appends[word[i:j]] = { word[j] }        
 
  while (1):
    letters = ""
    while (1):
      if letters in appends:
        print str(appends[letters])
      letter = raw_input("> "+ letters)
      prepend = False
      if len(letter) == 2:
        prepend = True
        letter = letter[0]
      elif len(letter) > 2:
        print "just one letter please"
        continue
      if prepend:
        if letters not in prepends or letter not in prepends[letters]:
          print "not legal"
          break
        else:
          letters = letter + letters
      else:
        if letters not in appends or letter not in appends[letters]:
          print "not legal"
          break
        else:
          letters += letter

      if letters in words:
        print "that's a word"
        break
      else:
        if random.randint(0,1) and letters in prepends:
          opponent_letter = random.choice(tuple(prepends[letters]))
          print "prepending to " + letters
          print "choices are " + str(prepends[letters])
          print "okay, my turn, I'll add the letter " + opponent_letter,
          print " to the beginning"
          letters = opponent_letter + letters
        elif letters in appends:
          opponent_letter = random.choice(tuple(appends[letters]))
          print "appending to " + letters
          print "choices are " + str(appends[letters])
          print "okay, my turn, I'll add the letter " + opponent_letter
          letters += opponent_letter
        else:
          print "huh, I guess I challenge?"
          break

        if letters in words:
          print "oops, you win"
          break
    
    print "alright, new game"

  #print str(histogram)
  #print str(len(appends)) + ", " + str(len(prepends))
 
superghost()
