import random
from wordfreq import top_n_list

words = top_n_list("en", 10000)
word = random.choice(words)
answer = []
misses = 0
for _ in range(len(word)):
    answer.append("_")
print(*answer)
while True:
    found = False
    user_letter = input("Enter a letter: ")
    for i, letter in enumerate(word):
        if letter == user_letter:
            answer[i] = user_letter
            found = True
    if not found:
        misses += 1
    print(*answer)
    print(misses)
    # print(word)
    if "_" not in answer:
        break
print(f"You won!\nThe guessed word was: {word}")
