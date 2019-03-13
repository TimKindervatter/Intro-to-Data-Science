#%%
import random
import numpy as np


#%%
def simulate_prizedoor(nsim):
    """
    Generate a random array of 0s, 1s, and 2s, representing
    hiding a prize between door 0, door 1, and door 2

    Args:
        nsim (int): The number of simulations to run

    Returns:
        sims (np array): Random array of 0s, 1s, and 2s

    Example:
        >>> print simulate_prizedoor(3)
        array([0, 0, 2])
    """

    return np.random.randint(0,3, (nsim))


#%%
def simulate_guess(nsim):
    """
    Return any strategy for guessing which door a prize is behind. This
    could be a random strategy, one that always guesses 2, whatever.

    Args:
        nsim (int): The number of simulations to generate guesses for

    Returns:
        guesses (np array): An array of guesses. Each guess is a 0, 1, or 2

    Example:
        >>> print simulate_guess(5)
        array([0, 0, 0, 0, 0])
    """

    guesses = np.array([], dtype = np.int)
    for sim in range(nsim):
        guesses = np.append(guesses, random.randint(0,2))
    return guesses


#%%
def reveal_door(prizedoors, guesses):
    """
    Simulate the opening of a "goat door" that doesn't contain the prize,
    and is different from the contestants guess

    Args:
        prizedoors (np array): The door that the prize is behind in each simulation
        guesses (np array): The door that the contestant guessed in each simulation

    Returns:
    goats (np array): The goat door that is opened for each simulation. Each item is 0, 1, or 2, and is different from both prizedoors and guesses

    Examples:
        >>> print goat_door(np.array([0, 1, 2]), np.array([1, 1, 1]))
        >>> array([2, 2, 0])
    """

    assert(len(prizedoors) == len(guesses)), "Both input arrays must have the same length! The given arrays had lengths {0} and {1}".format(len(prizedoors), len(guesses))
    doors = [0,1,2]
    revealed_doors = np.array([], dtype = np.int)

    #For each simulation
    for i in range(len(prizedoors)):
        #Start with the list of all doors
        door_to_reveal = np.array(doors[:])
        #We don't want to reveal the prize door, so remove it from the list
        door_to_reveal = door_to_reveal[door_to_reveal != prizedoors[i]]

        #We also don't want to reveal the contestant's door.
        #If the contestant's door is in the list door_to_reveal, remove it.
        if guesses[i] in door_to_reveal:
            door_to_reveal = door_to_reveal[door_to_reveal != guesses[i]]

        #All of the remaining doors are valid choices to reveal, pick one at random.
        revealed_doors = np.append(revealed_doors, random.choice(door_to_reveal))

        assert(revealed_doors[i] != guesses[i]), "Something went wrong, the contestant's guess should not have been revealed."

    return revealed_doors


#%%
def switch_guess(guesses, revealed_doors):
    """
    The strategy that always switches a guess after the goat door is opened

    Args:
        guesses (np array): Array of original guesses, for each simulation
        revealed_doors (np array): Array of revealed goat doors for each simulation

    Returns:
        The new door after switching. Should be different from both guesses and goatdoors

    Examples:
        >>> print switch_guess(np.array([0, 1, 2]), np.array([1, 2, 1]))
        >>> array([2, 0, 0])
    """

    assert(len(prizedoors) == len(guesses)), "Both input arrays must have the same length! The given arrays had lengths {0} and {1}".format(len(guesses), len(revealed_doors))
    doors = [0,1,2]
    new_guesses = np.array([], dtype = np.int)

    #For each simulation
    for i in range(len(guesses)):
        #Start with list of all doors
        new_guess = np.array(doors[:])
        #The new guess can't be the old guess, so remove it
        new_guess = new_guess[new_guess != guesses[i]]
        #The new guess can't be the revealed door, so remove it
        new_guess = new_guess[new_guess != revealed_doors[i]]

        #Any of the remaining doors are valid choices for a new guess, pick randomly among them
        new_guesses = np.append(new_guesses, random.choice(new_guess))
        assert(guesses[i] != new_guesses[i]), "The new guess needs to be different than the old guess."

    return new_guesses


#%%
def win_percentage(prizedoors, guesses):
    """
    Calculate the percent of times that a simulation of guesses is correct

    Args:
        guesses (np array): Guesses for each simulation
        prizedoors (np array): Location of prize for each simulation

    Returns:
        percentage (float between 0 and 100): The win percentage

    Examples:
        >>> print win_percentage(np.array([0, 1, 2]), np.array([0, 0, 0]))
        33.333
    """

    assert(len(prizedoors) == len(guesses)), "Both input arrays must have the same length! The given arrays had lengths {0} and {1}".format(len(prizedoors), len(guesses))
    wins = np.array([], dtype = int)

    #For each simulation
    for i in range(len(prizedoors)):
        #If the prize door was guessed
        if prizedoors[i] == guesses[i]:
            #Mark the simulation as a win
            wins = np.append(wins, 1)
        #If the prize door was not guessed
        else:
            #Mark the simulation as a loss
            wins = np.append(wins, 0)

    #All entries are 0 (loss) or 1 (win), so the mean is the percentage of wins
    return wins.mean()

#%%
#Run 10000 simulations
prizedoors = simulate_prizedoor(10000)
guesses = simulate_guess(10000)
revealed_doors = reveal_door(prizedoors, guesses)
new_guesses = switch_guess(guesses, revealed_doors)

#Determine the percentage of wins if the contestant does not switch their choice
win_percentage_without_switch = win_percentage(prizedoors, guesses)
#Determine the percentage of wins if the contestant switches their choice
win_percentage_with_switch = win_percentage(prizedoors, new_guesses)

print("{0: .2f} percent of games were won when the contestant did not switch doors.".format(100*win_percentage_without_switch))
print("{0: .2f} percent of games were won when the contestant switched doors.".format(100*win_percentage_with_switch))
#%%
