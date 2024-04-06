# fun fact, I've run over 600,000 hands of poker and still have not gotten a royal flush

from random import *

SUITS = [ "Spades", "Diamonds", "Hearts", "Clubs" ]
RANKS = [ "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", \
          "Queen", "King" ]

def deck():
    """ Creates a 'deck of cards' in order according to SUITS and RANKS. """

    DECK = []
    for suit in SUITS:
        rank = 0
        while rank < len( RANKS ):
            newCard = RANKS[ rank ]  + " of " + suit
            DECK.append( newCard )
            rank += 1
            
    return DECK

def shuffle():
    """ Lists DECK in a random order, resets cards in DECK to 52. """
    
    DECK = deck()
    shuffleDeck = []
    t = 52
    for i in range( 52 ):
        n = randrange( 0, t )
        shuffleDeck.append( DECK[ n ] )
        DECK.remove( DECK[ n ] )
        t -= 1
        
    return shuffleDeck

def deal( deck, cards ):
    """ Returns a list of the top cards in the DECK and removes those cards
    from DECK according to the specified number of cards. If there are not
    enough cards in DECK, returns None. """
    
    newDeck = [ x for x in deck ]
    hand = ""
    if len( newDeck ) < cards:
        return None, []
    
    for _ in range( cards ):
        hand = hand + str( newDeck[ 0 ] ) + "_" 
        newDeck.remove( newDeck[ 0 ] )
    
    return hand, newDeck

def myFind( str1, ch ):
    """ Return the index of the first (leftmost) occurrence of 
     ch in str, if any.  Return -1 if ch does not occur in str. """
    
    index = 0
    for i in str1:
        if i == ch:
            return index
        index += 1
        
    return -1

def myRemove( str1, ch ):
    """ Return a new string with the first occurrence of ch 
     removed.  If there is none, return str. """
    
    newString = ""
    index = 0
    for i in str1:
        if i != ch:
            newString = newString + i
        elif i == ch:
            return newString + str1[ index + 1: ]
        index += 1
        
    return newString

def myReverse( str1 ):
    """ Return a new string like str but with the characters
     in the reverse order. """
    
    newString = ""
    for i in str1:
        newString = i + newString
        
    return newString

def myCount( str1, ch ):
    """ Return the number of times character ch appears
    # in str """
    
    count = 0
    for i in str1:
        if i == ch:
            count += 1
            
    return count


def handEvaluation( hand, cards ):
    """ Evaluates the ranks and suits of the given hand to determine
    how much the hand is worth. """
    
    suitCounter = []
    rankCounter = []
    
    x = 0
    for i in range( cards ): # breaks the hands down into ranks and suits
        card = hand[ x : myFind( hand, "_" ) ]
        card.strip()
        rank = card[ : myFind( card, " " ) ]
        card = myReverse( card )
        suit = card[ : myFind( card, " " ) ]
        suit = myReverse( suit )
        suitCounter.append( suit )
        rankCounter.append( rank )
        x = myFind( hand, "_" )
        hand = myRemove( hand, "_" )

    # adds ranks and suits to repective lists
    value = []
    for i in range( cards ):
        value.append( RANKS.index( rankCounter[ i ] ) )
        
    kind = []
    for i in range( cards ):
        kind.append( SUITS.index( suitCounter[ i ] ) )

    value.sort()
    kind.sort()
    
    count = 1
    countedCard = 0
    newValue = [ x for x in value ]
    t = cards
    i = 0
    while i < t - 1: # finds matches, stores matching card value
        if newValue.count( newValue[ i ] ) == 2 and count == 3:
            count = 31
            
        elif newValue.count( newValue[ i ] ) == 3 and count == 2:
            count = 31
        
        elif newValue.count( newValue[ i ] ) > count:
            count = newValue.count( newValue[ i ] )
            countedCard = newValue[ i ]
            
            for n in range( count ):
                newValue.remove( countedCard )
                t -= 1
            i = -1
        
        elif newValue.count( newValue[ i ] ) == count and count == 2:
            if newValue[ i ] > countedCard and countedCard != 0:
                for n in range( count ):
                    newValue.append( countedCard )
                    
                countedCard = newValue[ i ]
                
                for n in range( count ):
                    newValue.remove( countedCard )
            count = 21                        
            t = -1
            
        if newValue.count( newValue[ i ] ) == 2 and count == 3:
            count = 31
            
        elif newValue.count( newValue[ i ] ) == 3 and count == 2:
            count = 31

        i += 1
        
    newValue.sort()

    straight = True
    for i in range( cards - 1 ): # finds straights
        
        if value[ i + 1 ] - value[ i ] != 1:
            
            if i == 0:
                if value[ i ] == 0 and value[ i + 1 ] == 9 and value[ i + 2 ] \
                   == 10 and value[ i + 3 ] == 11 and value[ i + 4 ] == 12:
                    continue
                else:
                    straight = False
                
            else:
                straight = False

    flush = True
    for i in range( cards - 1 ): # finds flushes
        if kind[ i + 1 ] != kind[ i ]:
            flush = False

    royal = True    
    for i in range( cards - 1 ): # determines royal flush
        
        if value[ i ] < 9 and \
           value[ i ] != 0:
            royal = False

    # returns hand type, the matching card type, the cards not counted, and
    # the list of ranks in the hand
    if straight and flush:
        if royal:
            return "a Royal Flush.", 1, 0, 0, value
        return "a Straight Flush.", 2, countedCard, newValue, value
    
    if count == 4:
        return "Four of a Kind.", 3, countedCard, newValue, value

    if count == 31:
        return "a Full House.", 4, countedCard, newValue, value

    if flush:
        return "a Flush.", 5, countedCard, newValue, value

    if straight:
        return "a Straight.", 6, countedCard, newValue, value

    if count == 3:
        return "Three of a Kind.", 7, countedCard, newValue, value

    if count == 21:
        return "Two Pair.", 8, countedCard, newValue, value

    if count == 2:
        return "One Pair.", 9, countedCard, newValue, value

    return "nothing.", 10, countedCard, newValue, value

def handComparison( values, impCards, remainingCards, listedCards, cards ):
    ''' Takes in every hand and the value of that hand to determine the
    winning hand. '''
    # the comparisons below are incredibly complicated because they consider
    # that aces can be low or high and because games with more than 10 players
    # opens up the possibility of duplicate hands
    
    winner = min( values )
    fromAllHands = [] # indices of the winning hands

    # index of countedCard from earlier will tell the highest, most frequent
    # card; then an index of the other card(s) will decide the remaining 
    
    if values.count( winner ) == 1: # only one of the best hands
        return values.index( winner ) + 1
    
    # for more than one of the best hands, the following code compares them
    removedCards = 0    
    while values.count( winner ) > 0:
        fromAllHands.append( values.index( winner ) + removedCards )
        # lists the indices of the winning hands 
        values.remove( winner )
        removedCards += 1

    
    compare = 0
    store = 0
    store1 = ""
    if winner == 1: # royal flushes
        for n in fromAllHands:
            if store1 == "":
                store1 = str( n + 1 )
                
            else:
                store1 = store1 + " and " + str( n + 1 )
                
        return store1
    
    elif winner == 2: # straight flushes
        for n in fromAllHands:
            if max( listedCards[ n ] ) > compare:
                compare = max( listedCards[ n ] )
                store = n
            elif max( listedCards[ n ] ) == compare:
                # in the odd case of a tie or multiple ties
                if store1 == "":
                    store1 = str( store + 1 ) + " and " + str( n + 1 )
                else:
                    store1 = store1 + " and " + str( n + 1 )
                    
        if store1 == "":
            return store + 1
        return store1

    elif winner == 3: # four of a kinds
        for n in fromAllHands:
            if impCards[ n ] == 0:
                # four of a kind with aces
                if compare != len( RANKS ):
                    # sets aces high
                    compare = len( RANKS )
                    store = n
                else:
                    # tied four of a kind with aces, compare the kicker
                    if remainingCards[ n ] > remainingCards[ store ]:
                        store = n
                    elif remainingCards[ n ] == remainingCards[ store ]:
                        # in the odd case of a tie or multiple ties
                        if store1 == "":
                            store1 = str( store + 1 ) + " and " + str( n + 1 )
                        else:
                            store1 = store1 + " and " + str( n + 1 )   
                    
            if impCards[ n ] > compare:
                compare = impCards[ n ]
                store = n
            elif impCards[ n ] == compare:
                # tied four of a kind, compare the kicker
                if remainingCards[ n ] > remainingCards[ store ]:
                    store = n
                elif remainingCards[ n ] == remainingCards[ store ]:
                    # in the odd case of a tie or multiple ties
                    if store1 == "":
                        store1 = str( store + 1 ) + " and " + str( n + 1 )
                    else:
                        store1 = store1 + " and " + str( n + 1 )
                
        if store1 == "":
            return store + 1
        return store1
            
    elif winner == 4: # full houses
        for n in fromAllHands:
            if impCards[ n ] == 0:
                # aces full of __
                if compare != len( RANKS ):
                    # sets aces high
                    compare = len( RANKS )
                    store = n
                else:
                    # tied aces, compares other cards
                    if max( remainingCards[ n ] ) > max( remainingCards[ store ] ):
                        store = n
                    elif max( remainingCards[ n ] ) == max( remainingCards[ store ] ):
                        # in the odd case of a tie or multiple ties
                        if store1 == "":
                            store1 = str( store + 1 ) + " and " + str( n + 1 )
                        else:
                            store1 = store1 + " and " + str( n + 1 )
                    
            if impCards[ n ] > compare:
                compare = impCards[ n ]
                store = n   
            elif impCards[ n ] == compare:
                # tied, compares the kicker
                if max( remainingCards[ n ] ) > max( remainingCards[ store ] ):
                    store = n
                elif max( remainingCards[ n ] ) == max( remainingCards[ store ] ):
                    # in the odd case of a tie or multiple ties
                    if store1 == "":
                        store1 = str( store + 1 ) + " and " + str( n + 1 )
                    else:
                        store1 = store1 + " and " + str( n + 1 )
                
        if store1 == "":
            return store + 1
        return store1

    elif winner == 5: # flushes
        for n in fromAllHands:
            if listedCards[ n ][ 0 ] == 0:
                # has an ace
                if compare != len( RANKS ):
                    compare == len( RANKS )
                    store = n
                    continue
                else:
                     # tied max of aces, looks at entire hand
                     if store1 == "":
                         store1 = str( store + 1 ) + " and " + str( n + 1 )
                     else:
                         store1 = store1 + " and " + str( n + 1 )
                     z = cards - 1
                     while z > -1:                        
                         if listedCards[ n ][ z ] > listedCards[ store ][ z ]:
                            
                             store = n
                             store1 = ""
                             z = -1
                        
                         elif listedCards[ n ][ z ] < listedCards[ store ][ z ]:
                             store1 = ""
                             z = -1
                        
                         z -= 1
                     continue
                
            if listedCards[ n ][ cards - 1 ] > compare:
                compare = listedCards[ n ][ cards - 1 ]
                store = n
            elif listedCards[ n ][ cards - 1 ] == compare:
                # tied max, looks at entire hand
                if store1 == "":
                    store1 = str( store + 1 ) + " and " + str( n + 1 )
                else:
                    store1 = store1 + " and " + str( n + 1 )
                    z = cards - 1
                    while z > -1:                        
                        if listedCards[ n ][ z ] > listedCards[ store ][ z ]:
                            
                            store = n
                            store1 = ""
                            z = -1
                        
                        elif listedCards[ n ][ z ] < listedCards[ store ][ z ]:
                            store1 = ""
                            z = -1
                        
                        z -= 1

        if store1 == "":
            return store + 1
        return store1
    
    elif winner == 6: # straights
        for n in fromAllHands:
            if min( listedCards[ n ] ) == 0 and max( listedCards[ n ] ) == 12:
                # the only straight where ace is max
                if compare != len( RANKS ):
                    # sets aces high
                    compare = len( RANKS )
                    store = n
                else:
                    if store1 == "":
                        store1 = str( store + 1 ) + " and " + str( n + 1 )
                    
                    else:
                        store1 = store1 + " and " + str( n + 1 )

            
            if max( listedCards[ n ] ) > compare:
                compare = max( listedCards[ n ] )
                store = n
                
            elif max( listedCards[ n ] ) == compare:
                # in the odd case of a tie or multiple ties
                if store1 == "":
                    store1 = str( store + 1 ) + " and " + str( n + 1 )
                    
                else:
                    store1 = store1 + " and " + str( n + 1 )
                    
        if store1 == "":
            return store + 1
        return store1

    elif winner == 7: # three of a kinds
        for n in fromAllHands:
            if impCards[ n ] == 0:
                # aces 
                if compare != len( RANKS ):
                    # sets aces high
                    compare = len( RANKS )
                    store = n
                else:
                    # tied aces, compares other cards
                    if max( remainingCards[ n ] ) > max( remainingCards[ store ] ):
                        store = n
                    elif max( remainingCards[ n ] ) == max( remainingCards[ store ] ):
                        if min( remainingCards[ n ] ) > min( remainingCards[ store ] ):
                            store = n
                        elif min( remainingCards[ n ] ) == min( remainingCards[ store ] ):    
                            # in the odd case of a tie or multiple ties
                            if store1 == "":
                                store1 = str( store + 1 ) + " and " + str( n + 1 )
                            else:
                                store1 = store1 + " and " + str( n + 1 )
                    
            if impCards[ n ] > compare:
                compare = impCards[ n ]
                store = n   
            elif impCards[ n ] == compare:
                # tied, compares the other cards
                if max( remainingCards[ n ] ) > max( remainingCards[ store ] ):
                        store = n
                elif max( remainingCards[ n ] ) == max( remainingCards[ store ] ):
                    if min( remainingCards[ n ] ) > min( remainingCards[ store ] ):
                        store = n
                    elif min( remainingCards[ n ] ) == min( remainingCards[ store ] ):    
                        # in the odd case of a tie or multiple ties
                        if store1 == "":
                            store1 = str( store + 1 ) + " and " + str( n + 1 )
                        else:
                            store1 = store1 + " and " + str( n + 1 )
                
        if store1 == "":
            return store + 1
        return store1
    
    elif winner == 8: # two of a kinds
        secondPairList = []
        for n in fromAllHands:
            z = len( remainingCards[ n ] ) - 1
            while z > -1:                        
                if remainingCards[ n ].count( remainingCards[ n ][ z ] ) == 2:
                    for y in range( n ):
                        secondPairList.append( -1 )
                    secondPairList.append( remainingCards[ n ][ z ] )
                    remainingCards[ n ] = [ i for i in remainingCards[ n ] \
                                            if i != remainingCards[ n ][ z ] ]
                    z = -1
                    
                z -= 1    

            if impCards[ n ] == 0:
                # aces
                if compare != len( RANKS ):
                    # sets aces high
                    compare = len( RANKS )
                    store = n
                else:
                    if secondPairList[ n ] > secondPairList[ store ]:
                        store = n
                    elif secondPairList[ n ] == secondPairList[ store ]:
                        if remainingCards[ n ] > remainingCards[ store ]:
                            store = n
                        elif remainingCards[ n ] == remainingCards[ store ]:
                            if store1 == "":
                                store1 = str( store + 1 ) + " and " + str( n + 1 )
                            else:
                                store1 = store1 + " and " + str( n + 1 )
                continue
        
            if impCards[ n ] > compare:
                compare = impCards[ n ]
                store = n   
            elif impCards[ n ] == compare:
                if secondPairList[ n ] > secondPairList[ store ]:
                        store = n
                elif secondPairList[ n ] == secondPairList[ store ]:
                    if remainingCards[ n ] > remainingCards[ store ]:
                        store = n
                    elif remainingCards[ n ] == remainingCards[ store ]:
                        if store1 == "":
                            store1 = str( store + 1 ) + " and " + str( n + 1 )
                        else:
                            store1 = store1 + " and " + str( n + 1 )
                
        if store1 == "":
            return store + 1
        return store1
    
    elif winner == 9: # one of a kinds
    
        for n in fromAllHands:
            if impCards[ n ] == 0:
                # aces 
                if compare != len( RANKS ):
                    # sets aces high
                    compare = len( RANKS )
                    store = n
                else:
                    # tied aces, compares other cards
                    if store1 == "":
                        store1 = str( store + 1 ) + " and " + str( n + 1 )
                    else:
                        store1 = store1 + " and " + str( n + 1 )
                    z = len( remainingCards[ n ] ) - 1
                    while z > -1:
                        if remainingCards[ n ][ z ] > listedCards[ store ][ z ]:
                            
                            store = n
                            store1 = ""
                            z = -1
                        
                        elif listedCards[ n ][ z ] < listedCards[ store ][ z ]:
                            store1 = ""
                            z = -1
                        
                        z -= 1
                    continue
                    
                    
            if impCards[ n ] > compare:
                compare = impCards[ n ]
                store = n   
            elif impCards[ n ] == compare:
                if store1 == "":                    
                    store1 = str( store + 1 ) + " and " + str( n + 1 )
                else:
                    store1 = store1 + " and " + str( n + 1 )
                z = len( remainingCards[ n ] ) - 1
                while z > -1:
                    if remainingCards[ n ][ z ] > listedCards[ store ][ z ]:
                            
                        store = n
                        store1 = ""
                        z = -1
                        
                    elif listedCards[ n ][ z ] < listedCards[ store ][ z ]:
                        store1 = ""
                        z = -1
                        
                    z -= 1
                
        if store1 == "":
            return store + 1
        return store1
    
    
    elif winner == 10: # none of the above, looks for high card
        
        for n in fromAllHands:
            
            if listedCards[ n ][ 0 ] == 0:
                # has an ace
                if compare != len( RANKS ):
                    compare = len( RANKS )
                    store = n
                    continue
                else:
                    # tied max of aces, looks at entire hand
                    if store1 == "":
                        store1 = str( store + 1 ) + " and " + str( n + 1 )
                    else:
                        store1 = store1 + " and " + str( n + 1 )
                         
                    z = cards - 1
                    while z > -1:                        
                        if listedCards[ n ][ z ] > listedCards[ store ][ z ]:
                            
                            store = n
                            store1 = ""
                            z = -1
                        
                        elif listedCards[ n ][ z ] < listedCards[ store ][ z ]:
                            store1 = ""
                            z = -1
                        
                        z -= 1
                    continue
                
            if listedCards[ n ][ cards - 1 ] > compare:
                compare = listedCards[ n ][ cards - 1 ]
                store = n
                
                
            elif listedCards[ n ][ cards - 1 ] == compare:
                # tied max, looks at entire hand
                
                if store1 == "":
                    store1 = str( store + 1 ) + " and " + str( n + 1 )
                else:
                    store1 = store1 + " and " + str( n + 1 )
                    
                z = cards - 1
                while z > -1:                        
                    if listedCards[ n ][ z ] > listedCards[ store ][ z ]:
                            
                        store = n
                        store1 = ""
                        z = -1
                        
                    elif listedCards[ n ][ z ] < listedCards[ store ][ z ]:
                        store1 = ""
                        z = -1
                        
                    z -= 1

        if store1 == "":
            return store + 1
        return store1
        
def main():
    DECK = deck()
    cards = 5
    print( "Welcome to my poker simulator!" )
    print()
    while True:
        command = input( "Please enter a command (shuffle, show deck, " \
            "deal, count cards, end): " )
        
        if command.lower().strip() == "shuffle":
            DECK = shuffle()
            print()
            
        elif command.lower().strip() == "show deck":
            # prints the deck in order
            i = 0
            print()
            for n in DECK:
                print( DECK[ i ], "\n", sep = "" )
                i += 1
                
        elif command.lower().strip() == "deal":
            # deals cards according to number of players
            players = int( input( "How many hands should be dealt? " ) )
            print()
            listOfHands = []
            handValues = []
            valueCards = []
            remCards = []
            listedValues = []
            reshuffle = "Dealing a new deck."
            n = 0
            while n < players:
                hand, DECK = deal( DECK, cards )
                if hand == None: # reshuffles the deck, prints reshuffle
                    listOfHands.append( reshuffle )
                    DECK = shuffle()
                    hand, DECK = deal( DECK, cards )
                
                listOfHands.append( hand )
                n += 1

            n = 0
            length = len( listOfHands )
            while n < length:
                
                if str( listOfHands[ n ] ) == reshuffle:
                    print( reshuffle )
                    print()
                    listOfHands.remove( listOfHands[ 0 ] )
                    length -= 1
                        
                print( "Hand", n + 1 )
                newHand = str( listOfHands[ n ] )

                x = 0    
                for t in range( cards ):
                    print( "\t", newHand[ x : myFind( newHand, "_" ) ], \
                                            sep = ""  )
                    x = myFind( newHand, "_" )
                    newHand = myRemove( newHand, "_" )

                statement, newValue, valueCard, remCard, allValues = \
                           handEvaluation( listOfHands[ n ], cards )
                handValues.append( newValue )
                valueCards.append( valueCard )
                remCards.append( remCard )
                listedValues.append( allValues )
                
                print()
                print( "This hand has", statement )
                print()

                n += 1

            if length > 1: # runs hand comparison to determine winner
                print( "The winning hand is Hand", \
                       handComparison( handValues, valueCards, \
                                       remCards, listedValues, cards ) )
                print()
                        
                
        elif command.lower().strip() == "count cards":
            # prints the number of remaining cards in the deck
            print( len( DECK ) )
            print()

            

        elif command.lower().strip() == "error check":
            # identical to "deal" but runs infinetly for random hand sizes
            # run this knowing you have to ctrl c or exit to end program
            reshuffle = "Dealing a new deck."
            
            while True:
                players = randint( 2, 100 )
                listOfHands = []
                handValues = []
                valueCards = []
                remCards = []
                listedValues = []
                n = 0
                while n < players:
                    hand, DECK = deal( DECK, cards )
                    if hand == None:
                        listOfHands.append( reshuffle )
                        DECK = shuffle()
                        hand, DECK = deal( DECK, cards )
                    
                    listOfHands.append( hand )
                    n += 1

                n = 0
                length = len( listOfHands )
                while n < length:
                    
                    if str( listOfHands[ n ] ) == reshuffle:
                        print( reshuffle )
                        print()
                        listOfHands.remove( listOfHands[ 0 ] )
                        length -= 1
                            
                    print( "Hand", n + 1 )
                    newHand = str( listOfHands[ n ] )

                    x = 0    
                    for t in range( cards ):
                        print( "\t", newHand[ x : myFind( newHand, "_" ) ], \
                                                sep = ""  )
                        x = myFind( newHand, "_" )
                        newHand = myRemove( newHand, "_" )

                    statement, newValue, valueCard, remCard, allValues = \
                               handEvaluation( listOfHands[ n ], cards )
                    handValues.append( newValue )
                    valueCards.append( valueCard )
                    remCards.append( remCard )
                    listedValues.append( allValues )
                    
                    print()
                    print( "This hand has", statement )
                    print()

                    n += 1

                if length > 1:
                    print( "The winning hand is Hand", \
                           handComparison( handValues, valueCards, \
                                           remCards, listedValues, cards ) )
                print()
            
            
        elif command.lower().strip() == "end":
            print( "Thanks for playing!" )
            break
        
        else:
            print( "Unrecognized command entered:", command.lower().strip() )
            print()
    
main()
