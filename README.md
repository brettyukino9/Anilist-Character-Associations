# AnilistCharacterAssociations

Uses the AnilistAPI to answer the question: Given someone likes x character, what other characters are they most likely to also like?
Returns a list of the most likely characters along with of number of times more likely than a normal person they are to like said character.

Argument 1: Name of the character to analyze. This should be in quotes.

Argument 2 (optional): Name of another character to compare against. This will find all users with BOTH characters favorited and return all of their usernames.

Lift algorithm taken from https://en.wikipedia.org/wiki/Association_rule_learning
