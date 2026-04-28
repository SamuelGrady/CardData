SIZE = 52

cards = []
card_indecies = list(range(1,53))
for suit in "sdch":
    for value in ["A"] + list(range(2,11)) + ["J", "Q", "K"]:
        cards.append(f"{suit}-{value}")

input("(E)ncode or (D)ecode?")

