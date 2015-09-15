import random

# compute the edit distance between two words,
# We need to identify the dictionary word which is closest to the word
# provided by the user.  Ideally we can also classify their word as a
# prefixed / suffixed version, a misspelling, or unheard of.
def edit_distance(w, word):

  # distance[i][j] will contain the edit distance between the first i
  # letters of w and the first j letters of word
  distance = [ [0]*(len(word)+1) for i in xrange(0, len(w)+1)]
  for i in xrange(1, len(w)+1):
    distance[i][0] = i
  for j in xrange(1, len(word)+1):
    distance[0][j] = j

  for i in xrange(0, len(w)):
    for j in xrange(0, len(word)):
      if w[i] == word[j]:
        distance[i+1][j+1] = distance[i][j]
      else:
        distance[i+1][j+1] = min(
          1 + distance[i][j],
          1 + distance[i+1][j],
          1 + distance[i][j+1]
        )
  return distance[-1][-1]

def bk_tree_insert(root, word):
  distance = edit_distance(root[0], word)
  if distance == 0: # word is already inserted
    return
  if distance not in root:
    root[distance] = {0: word}
  else:
    bk_tree_insert(root[distance], word)

def bk_tree_lookup(root, word, slack):
  if isinstance(root, str):
    if edit_distance(root, word) <= slack:
      return [root]
    else:
      return []
  else:
    distance = edit_distance(root[0], word)
    matches = []
    for i in range(distance - slack, distance + slack + 1):
      if i in root:
        matches.extend(bk_tree_lookup(root[i], word, slack))
    return matches

def challenge(letters, bk_root):
  print "Alright, I challenge.  What was your word?"
  word = raw_input("> ")
  if letters not in word:
    print "That doesn't actually contain the letters we had."
  else:
    if letters in bk_tree_lookup(bk_root, word, 0):
      print "oh, I guess that works"
    for slack in range(1, 6):
      matches = bk_tree_lookup(bk_root, word, slack)
      if len(matches) > 0:
        print "the closest word I can come up with is " + matches[0]
        return
    print "yeah, I don't know any word remotely like that"

def ghost():
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
  bk_tree_root = {0: "dictionary"} # arbitrary root node choice
  for line in dictionary:
    #print line,
    word = line[0:-1]
    if len(word) < 4:
      continue
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
    bk_tree_insert(bk_tree_root, word)
    
  print "Alright, let's play Superghost.  Type a letter once and then enter"
  print "to append it, or twice to prepend it.  Enter ? to challenge, or !"
  print "to cheat and get my suggestions."
  
  while (1):
    letters = ""
    while (1):
      letter = raw_input("> "+ letters)
      prepend = False
      if len(letter) == 2:
        prepend = True
        letter = letter[0]
      elif len(letter) > 2:
        print "just one letter please"
        continue
      if letter == "?":
        print "ah, you challenge?"
        while letters not in words:
          if letters in prepends:
            letters = random.choice(tuple(prepends[letters])) + letters
          elif letters in appends:
            letters = letters + random.choice(tuple(appends[letters]))
          else:
            print "actually, I'm stumped"
        print "how about: " + letters
        break
      if letter == "!":
        if letters in prepends:
          print str(prepends[letters])
        if letters in appends:
          print str(appends[letters])
        continue
      if prepend:
        if letters not in prepends or letter not in prepends[letters]:
          print "not legal"
          challenge(letter + letters, bk_tree_root)
          break
        else:
          letters = letter + letters
      else:
        if letters not in appends or letter not in appends[letters]:
          print "not legal"
          challenge(letters + letter, bk_tree_root)
          break
        else:
          letters += letter

      if letters in words:
        print "that's a word"
        break
      else:
        if (letters in prepends and
            (letters not in appends or random.randint(0,1))):
          opponent_letter = random.choice(tuple(prepends[letters]))
          #print "prepending to " + letters
          #print "choices are " + str(prepends[letters])
          print "okay, my turn, I'll add the letter " + opponent_letter,
          print "to the beginning"
          letters = opponent_letter + letters
        elif letters in appends:
          opponent_letter = random.choice(tuple(appends[letters]))
          #print "appending to " + letters
          #print "choices are " + str(appends[letters])
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
 
print "Welcome to Ghost.  Enter h for help, g to play Ghost, or anything",
print "else to play Superghost."

choice = raw_input("> ")

if choice == "h":
  print "Ghost is a word game in which players alternate turns adding one",
  print "letter at a time to build a word.  The player to first complete",
  print "a word, loses.  Superghost differs in that players may choose ",
  print "between adding to the end or the beginning of the word."
elif choice == "g":
  ghost()
else:
  superghost()
