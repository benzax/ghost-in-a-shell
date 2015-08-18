import random

def ghost():
  print "here we go:"

  dictionary = open('dictionary.txt');
  trie = {}
  for line in dictionary:
    #print line,
    if len(line) < 5 or line[1] < 'a':
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

ghost()
