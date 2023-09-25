'''
I pledge my honor that I have abided by the Stevens Honor System.

Authors: Aidan Ouckama, Cameron Marotti, Michael Buzzetta

    Takes in an input for username and stores music artist
    preferences in a text file database. This database is then
    referenced to find recommendations by pinpointing a user
    with the most similar artist preferences.

12/2/22
CS 115
'''

# current user preference
username = ''
isPrivate = False
isRegistered = False

# user information
user_preferences = []

# options dictionary
options = {
    'e' : 'Enter preferences',
    'r' : 'Get recommendations',
    'p' : 'Show most popular artists',
    'h' : 'How popular is the most popular',
    'm' : 'Which user has the most likes',
    'q' : 'Save and quit',
}

# database information
database = ''
data = {} # stores most up to date user information
#
#   DATA FORMAT:
#
#   {
#       'username1': ['artist1', 'artist2', 'artist3'],
#       'username2': ['artist3', 'artist4', 'artist5'],
#   }
#

def main():
    '''
    First execution of the program. Takes in username input
    and references text database to check if user exists.

    INPUT  --   None
    OUTPUT --   None (Main Program)

    Author: Aidan Ouckama
    '''

    # create / reference database
    global database
    global data

    # read data from database and append to dictionary data
    data = readDatabase()

    # ask for username
    global username
    username = input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ")

    # check if user wants preferences private
    global isPrivate
    isPrivate = username[-1] == '$'

    # check if user is already registered
    global isRegistered
    isRegistered = username in data.keys()

    if not isRegistered:

        # add username to database and add user as registered
        data[username] = []
        isRegistered = True
        enterPreferences()
    else:
        # set user preferences
        global user_preferences
        user_preferences = data[username] 

        # directly give registered user menu
        optionsHandler()

def optionsHandler():
    '''
    Handles the options that are provided by the user
    (seen in global options variable). Takes input from
    the user as shown in options and runs the 
    corresponding function associated to the option.

    INPUT  --   User Input (Keyboard)
    OUTPUT --   None (designated function run)

    Authors: Aidan Ouckama, Cameron Marotti, Michael Buzzetta
    '''

    # print menu
    print('Enter a letter to choose an option:')
    for option in options.keys():
        print(option, '-', options[option])
    response = input()

    # check if response is within options dictionary
    if response in options.keys():

        # enter preferences
        if response == 'e':
            enterPreferences()
        
        # get recommendations
        if response == 'r':
            getRecommendations()

        # show most popular artists
        if response == 'p':
            mostPopular()

        # how popular is most popular
        if response == 'h':
            howPopular()

        # which user has the most likes
        if response == 'm':
            mostLikes()

        # save and quit
        if response == 'q':
            writeToDatabase(username, data[username])

    # invalid input
    else:
        print('\n Invalid input! \n')
        optionsHandler()

def enterPreferences():
    '''
    Asks the user through print statements to enter artists
    they enjoy. The input is then added to a user_preferences
    list. Loop continues until blank Enter is inputted.

    INPUT  --   User Input (Keyboard)
    OUTPUT --   None (appended artists to user_preferences)

    Author: Aidan Ouckama
    '''

    # initialize user preferences
    global user_preferences
    user_preferences = []
    response = ' '

    # ask for artists until a blank response is given
    while response != '':
        response = input('Enter an artist that you like (Enter to finish): ')
        if response == '':
            data[username] = user_preferences # add artists to current data dictionary
            optionsHandler() # once artists are inputted open option menu
        else:
            user_preferences.append(response.strip().title()) # clean data and add to user_preferences

def getRecommendations():
    '''
    Finds a similarity score for all users compared to the
    current user. Uses these scores to make recommendations
    for the current user.

    INPUT  --   None (data in data dictionary)
    OUTPUT --   None (print of recommended artists)
    
    Authors: Aidan Ouckama, Cameron Marotti
    '''

    similarity = {}

    # get every username in current data
    for user in data.keys():
        name = user
        artists = data[user]

        # dont compare user to itself
        if not name == username:
            count = 0

            # loop through each artist and count how many similarities there are
            for artist in artists:
                if artist in user_preferences:
                    count += 1

            # make sure users have something in common and dont have exact same artists and users are not private
            if not count == 0 and not count == len(artists) and not name[-1] == '$':
                similarity[name] = count
    
    # check if dictionary is empty; if so return nothing and print message
    if len(similarity.values()) == 0:
        print('No recommendations available at this time.')
        optionsHandler()
        return

    # print recommended artists based on a recommended user
    if not max(similarity.values()) == 0:
        maxSimilarity = 0
        recUser = "" # recommended user
        # Find the most similar user in the similarity dictionary
        for user in similarity:
            if maxSimilarity < similarity[user]:
                maxSimilarity = similarity[user]
                recUser = user
        
        recArtists = data[recUser]
        for artist in recArtists:
            count = 0

            # only print 3 recommendations and artists not in current users preferences 
            if not artist in user_preferences and count < 3:
                print(artist)
                count += 1
    
    # loop back to options
    optionsHandler()

def mostPopular():
    '''
    Evaluates the data dictionary and determines the top three popular artists
    and prints them individually. If less than three artists are found all of 
    them are printed individually.

    INPUT  --   None (data dictionary)
    OUTPUT --   None (three or less most popular artists printed)
    
    Authors: Michael Buzzetta, Aidan Ouckama, Cameron Marotti
    '''

    # create a dictionary of each artists popularity
    popular = {}

    ARTIST_LIMIT = 3 # limit of artists to be printed

    # loop through each user in data and extract artists and increment popularity in popular dictionary
    for user in data:
        if not user[-1] == '$': # if user is not private
            for artist in data[user]:
                if artist in popular: # if artist is in dictionary increment, if not add to dictionary
                    popular[artist] += 1
                else:  
                    popular[artist] = 1

    # sort the dictionary by value
    mostPopularList = sorted(popular, key=popular.get, reverse=True)

    # Make sure there are artists in the list
    if mostPopularList:
        # Make sure we aren't printing more than the maximum number of artists
        for i in range(min(ARTIST_LIMIT, len(mostPopularList))):
            print (mostPopularList[i])
    else:
        print("Sorry, no artists found.")
        
    # loop back to options
    optionsHandler()

def howPopular():
    '''
    Evaluates the data dictionary and prints the amount of likes the most
    popular artist has. 

    INPUT  --   None (data dictionary)
    OUTPUT --   None (the amount of likes of the most popular artist)
    
    Authors: Michael Buzzetta, Aidan Ouckama
    '''

    # create a dictionary of each artists popularity
    popular = {}

    # loop through each user in data and extract artists and increment popularity in popular dictionary
    for user in data:
        if not user[-1] == '$': # if user is not private
            for artist in data[user]:
                if artist in popular:
                    popular[artist] += 1
                else:
                    popular[artist] = 1
                    
    # Make sure there are entries in the list
    if popular:
        # print the largest value in popular dictionary values a.k.a the most popular artist likes count
        print(max(popular.values()))
    else:
        print("Sorry, no artists found.")
    # loop back to options
    optionsHandler()

def mostLikes():
    '''
    Prints the username of the user with the most favorited artists
    Postconditions: the username of the first user (alphabetically) with the
                    most liked artists will be printed to the console. The menu
                    will be activated again after this

    Author: Cameron Marotti
    '''
    userWithMostLikes = ""
    # Loop through the data a first time
    for user in data:
        # Find the first user who isn't private and use them as the initial
        # user value
        if user[-1] != '$':
            userWithMostLikes = user
            break
    # If there are no non-private users, we can't do anything
    if not userWithMostLikes:
        print("Sorry, no user found.")
    else:
        # Loop through the users again to find the user with the most likes
        for user in data:
            if user[-1] != '$' and len(data[user]) > len(data[userWithMostLikes]):
                userWithMostLikes = user
        # Print the username
        print(userWithMostLikes)

    # Loop back through the menu
    optionsHandler()

def writeToDatabase(currentUsername, currentUserPreferences):
    '''
    Writes new data to the database
    Input:  currentUsername - the username for the user currently using the app
            currentUserPreferences - the list of bands the current user likes

    Author: Cameron Marotti
    '''
    # Read the data that's currently in the file
    oldData = readDatabase()
    # Sort the new preferences before adding them to the file
    currentUserPreferences.sort()
    # Add the new preference and username to the data
    oldData[currentUsername] = currentUserPreferences
    # Store all of the usernames as a list
    usernames = list(oldData.keys())
    # Sort the list of usernames
    usernames.sort()
    # Open the file for writing
    file = open("musicrecplus.txt", 'w')
    # Loop through all of the saved user data using the ordered usernames
    for username in usernames:
        # Configure the username and user preferences into a line
        writeStr = username + ":" + ','.join(oldData[username]) + '\n'
        # Write the given line to the file
        file.write(writeStr)
    file.close()

def readDatabase():
    '''
    Reads the data in musicrecplus.txt if it exists (or creates that file if
        it does not) and returns a dictionary of the usernames on file paired to
        the user's favorite bands
    Output: a dictionary with usernames as keys and lists of favorite bands as
            values

    Authors: Cameron Marotti, Aidan Ouckama
    '''
    # Create the file if needed
    try:
        open("musicrecplus.txt")
    except FileNotFoundError:
        save = open("musicrecplus.txt", 'w')
    # Initialize the dictionary
    data = {}
    # Open the file for reading
    save = open("musicrecplus.txt", 'r')    
    # Iterate through the lines in the file
    for line in save:
        # Store the text behind the colon as the username and the text after the
        # colon as the artists (we strip it to ignore \n characters)
        [username, favArtists] = line.strip().split(':')
        # Split the string of artists separated by commas into a list
        artistList = favArtists.split(',')
        # Assign the username as a key in the dictionary paired to the list of
        # band names
        data[username] = artistList

    save.close()
    return data

if __name__ == "__main__":
    main()
