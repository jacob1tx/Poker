# Poker

This is a simple poker simulator I wrote as a passion project during the COVID-19 pandemic my first semester in college. I believe this project is what inspired me to major in Software Engineering. The code is wildly inefficient, and there are several parts of it I would change if I were to redo the project today. However, I have left it in its original form as a reminder of how far I have come as a programmer.

## How to Play
Specifically this is a version of 5 card draw. To run a user must first run the software in the terminal. A welcome message will prompt the user to select from 5 commands: shuffle, show deck, deal, count cards, end. They are flushed out below.

* Shuffle:  The deck begins unshuffled. To receive a realistic hand, the user must first shuffle the cards in their deck before playing. If hands have been played, shuffle will restock the deck with all 52 cards.
* Deal:  This starts the main action flow of the game. Deal will first ask the user for the number of hands to play. If a single hand is selected, the user will receive 5 cards and the program will assess the max value of the hand, defined below. If there are more than one hands selected, all will be displayed and evaluated, and then the winner will be announced. The program draws continuously from a static deck. If there are fewer than 5 cards remaining in the deck, it is reshuffled.
* Show Deck:  (Debugging tool) Displays the remaining cards in the deck, in order
* Count Cards:  (Debugging tool) Displays the number of cards remaining in the deck
* End:  Exits the program

### Hand Values

1)  Royal Flush
2)  Straight Flush
3)  Four of a Kind
4)  Full House
5)  Flush
6)  Straight
7)  Three of a Kind
8)  Two Pair
9)  One Pair
10)  High Card
