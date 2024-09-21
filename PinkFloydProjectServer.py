import socket
import data
import threading

# Getting the data from the file
FILE_CONTENTS = data.open_file()
DATA_STRUCTURE = data.create_data_structure(FILE_CONTENTS)

# Initializing Dictionary With Response To Every Request
RESPONSE_DICT = {
    "REQ_ALBUMS_LIST#": "RES_ALBUMS_LIST#albums=",
    "REQ_ALBUM_SONGS#album=": "RES_ALBUM_SONGS#songs=",
    "REQ_SONG_LENGTH#song=": "RES_SONG_LENGTH#length=",
    "REQ_SONG_LYRICS#song=": "RES_SONG_LYRICS#lyrics=",
    "REQ_FIND_ALBUMS#song=": "RES_FIND_ALBUMS#album=",
    "REQ_NAME_SEARCH#keyWord=": "RES_NAME_SEARCH#song=",
    "REQ_FIND_LYRICS#songLyrics=": "RES_FIND_LYRICS#song=",
    "REQ_SHUT_SERVER#": "RES_SHUT_SERVER#"
}

CLOSE_SOCKET_REQUEST = "REQ_SHUT_SERVER#"

# Initializing Error Message
ERROR = "ER_SERVER_ERROR#errorMessage="

# Initializing Welcome Message And Ending Message
WELCOME_MESSAGE = "Welcome to my Pink Floyd server!"
END_MESSAGE = "See you again!"

# Initializing Server Port
LISTEN_PORT = 7777

# Initializing errors
ERROR_MESSAGES = ["Album Not Found Try Again Soon", "Song Not Found, Try Again Soon", "Invalid Request"]

# Initializing the spots in the internal array in which the data about the song is located
WRITER_SPOT = 0
LENGTH_SPOT = 1
LYRIC_SPOT = 2

# Initializing Max amount of users
MAX_USERS = 5


def create_listening_socket():
    """Function Which creates a listening socket object
    and returns it"""

    # Creating A TCP/IP Socket
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding To Local Port 7777
    server_address = ('', LISTEN_PORT)
    listening_socket.bind(server_address)

    # Returning The Socket Object
    return listening_socket


# noinspection PyUnusedLocal
def get_album_list(void=""):
    return ", ".join(DATA_STRUCTURE.keys())


def get_album_songs(album_name):
    """Function which returns the songs in a given album"""
    # Searching for the album in the data structure (case-sensitive)
    album_data = DATA_STRUCTURE.get(album_name)

    # If the album exists
    if album_data:
        # Extract the song names from the album data
        songs = [list(song_data.keys())[0] for song_data in album_data[1:]]
        return ', '.join(songs)

    return ERROR_MESSAGES[0]


def get_song_length(song_name):
    """Function which gets a song's length"""
    # Initializing string
    length = ""

    # For every album in the data structure
    for album in DATA_STRUCTURE.keys():

        # For every song on the album
        for song in range(1, len(DATA_STRUCTURE[album])):

            # If the given song is on the album
            if song_name in DATA_STRUCTURE[album][song].keys():

                # Getting the song's length
                length = DATA_STRUCTURE[album][song][song_name][LENGTH_SPOT]
                break

    # If the song wasn't found
    if length == "":

        # Add the error into the returned variable
        length = ERROR_MESSAGES[1]

    # Return the string
    return length


def get_song_lyrics(song_name):
    """Function which gets the lyrics of a given song"""
    lyrics = ""
    # For every album in the data structure
    for album in DATA_STRUCTURE.keys():

        # For every song on the album
        for song in range(1, len(DATA_STRUCTURE[album])):

            # If the given song is one of the songs on the album
            if song_name in DATA_STRUCTURE[album][song].keys():

                # Put the lyrics into the variable
                lyrics = DATA_STRUCTURE[album][song][song_name][LYRIC_SPOT]
                break

    # If the lyrics weren't found
    if lyrics == "":

        # Put the error into the returned variable
        lyrics = ERROR_MESSAGES[1]

    # Return the string
    return lyrics


def get_song_album(song_name):
    """Function which find the album in which a song is located"""
    # Initializing variable to hold the album's name
    song_album = ""

    # For every album in the data structure
    for album in DATA_STRUCTURE.keys():

        # For every song on the album
        for song in range(1, len(DATA_STRUCTURE[album])):

            # If the given song name is on the album
            if song_name in DATA_STRUCTURE[album][song].keys():

                # Put the album's name into a variable
                song_album = album
                break

    # If the album wasn't found
    if song_album == "":

        # Put the error into the returned variable
        song_album = ERROR_MESSAGES[0]

    # Return the variable
    return song_album


def find_song_by_name(keyword):
    """Function which finds a song using a keyword"""
    # Initializing list to hold the songs
    found_songs = []

    # For every album's data in the structure
    for album_data in DATA_STRUCTURE.values():

        # For every song's data on the album's data
        for song_data in album_data[1:]:

            # If the keyword is in the song's name, add it to the list
            song_name = list(song_data.keys())[0]
            if keyword.lower() in song_name.lower():
                found_songs.append(song_name)

    # If the list isn't empty
    if not found_songs == []:
        # Return the list as a joined string
        return ', '.join(found_songs)

    # Otherwise
    else:
        # Return the error message
        return ERROR_MESSAGES[1]


def find_song_by_lyrics(lyrics_to_search):
    """Function which searches for a song by its lyrics"""
    # Initializing list to store potential songs
    found_songs = list()

    # For every album's data in the data structure
    for album_data in DATA_STRUCTURE.values():

        # For every song's data on the album's dat
        for song_data in album_data[1:]:

            # Get the lyrics from the song's data
            song_data_list = list(song_data.values())
            lyrics = song_data_list[0][LYRIC_SPOT]

            # If the given lyrics are in the songs lyrics, add them to the list
            if lyrics_to_search.lower() in lyrics.lower():
                song_name = list(song_data.keys())
                song_name = ''.join(song_name)
                found_songs.append(song_name)

    # If the list isn't empty
    if not found_songs == []:
        # Return the list as a joined string
        return ', '.join(found_songs)

    # Otherwise
    else:
        # Return the error message
        return ERROR_MESSAGES[1]


# Creating the dictionary for mapping after all the functions have been initialized
REQUEST_FUNCTIONS = {
    "REQ_ALBUMS_LIST#": get_album_list,
    "REQ_ALBUM_SONGS#album=": get_album_songs,
    "REQ_SONG_LENGTH#song=": get_song_length,
    "REQ_SONG_LYRICS#song=": get_song_lyrics,
    "REQ_FIND_ALBUMS#song=": get_song_album,
    "REQ_NAME_SEARCH#keyWord=": find_song_by_name,
    "REQ_FIND_LYRICS#songLyrics=": find_song_by_lyrics,
    "REQ_SHUT_SERVER#": str
}


def direct_request(request):
    """Function which directs the request to the appropriate function and returns the complete response"""

    # Getting the Request ID
    if "=" in request:
        request_id = request[:request.find("=") + 1]
        user_data = request[request.find("=") + 1:]
    else:
        request_id = request
        user_data = ''

    # Assemble the appropriate response
    response_function = REQUEST_FUNCTIONS.get(request_id)
    if response_function:
        response_data = response_function(user_data)
        if response_data in ERROR_MESSAGES:
            # Assembling the error
            assembled_response = ERROR + response_data
        else:
            # Assembling the appropriate request
            assembled_response = RESPONSE_DICT.get(request_id, '') + response_data
    else:
        assembled_response = ERROR + ERROR_MESSAGES[2]

    # Returning the assembled response
    return assembled_response


def handle_client(client_socket, client_address):
    """Function which handles the requests of every client"""
    # Sending a welcome message
    client_socket.sendall(WELCOME_MESSAGE.encode())

    print(f"| Welcome message has been sent to {client_address}!")

    # Flag to track if the socket should be closed
    close_socket = False

    while not close_socket:
        try:
            # Getting the message from the user
            request = client_socket.recv(1024).decode()
            print(f"| User's message from {client_address} has been accepted!\n| The request is: ", request)

            # Providing the information to a function that returns the appropriate response
            print("| Directing the request...")
            response = direct_request(request)
            print("| The response is: ", response)

            # Sending the response to the user
            client_socket.sendall(response.encode())

            print(f"| Response has been sent to {client_address}!")

            # Checking if the request was to close the conversation socket
            if request == CLOSE_SOCKET_REQUEST:
                print(f"| User from {client_address} has requested to close the conversation socket!")

                # Sending the response to the client
                client_socket.sendall(END_MESSAGE.encode())

                close_socket = True  # Set the flag to indicate socket closure

        except ConnectionError:
            # Handle the connection error gracefully
            print(f"| Connection with {client_address} was closed unexpectedly!")
            close_socket = True

    # Closing the client socket
    client_socket.close()
    print(f"| Conversation socket with {client_address} has been closed!")


def main():
    # Printing random messages to make this server look cooler than it actually is
    print("| Setting up server...")

    # Creating a TCP/IP socket
    listening_socket = create_listening_socket()

    print("| Listening socket has been created!")

    # Catching exceptions if there are any
    try:
        # Listening for incoming traffic
        listening_socket.listen(MAX_USERS)

        while True:
            # Create a new conversation socket
            client_socket, client_address = listening_socket.accept()

            print("| A user has created a conversation socket!")

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except Exception as e:
        # Sending the exception
        print("| Sending closing message...")
        client_socket.sendall("Server Has Encountered an error, closing...".encode())
        client_socket.close()
        print("Error encountered", e)

    finally:
        listening_socket.close()


if __name__ == '__main__':
    main()
