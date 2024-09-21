import socket
import time

# Initializing Request IDs
REQUESTS = ["REQ_ALBUMS_LIST#", "REQ_ALBUM_SONGS#album=", "REQ_SONG_LENGTH#song=", "REQ_SONG_LYRICS#song=",
            "REQ_FIND_ALBUMS#song=", "REQ_NAME_SEARCH#keyWord=", "REQ_FIND_LYRICS#songLyrics=", "REQ_SHUT_SERVER#"]

# Messages that will be printed according to the user's choice
CHOICE_MESSAGES = ["", "Enter the album's name: ", "Enter the song's name: ", "Enter the song's name: ",
                   "Enter the song's name: ", "Enter a keyword: ", "Enter lyrics: ", ""]

# Initializing Server Port And IP Address
SERVER_PORT = 7777
SERVER_IP = "127.0.0.1"

MENU = "Please choose any of the following options:\n1 - Get album list\n2 - Get list of songs from an album\n" \
       "3 - Get song's length\n4 - Get song's lyrics\n5 - Find a song's album\n6 - Search for a song using name\n" \
       "7 - Search for a song using lyrics\n8 - Exit"


def check_choice():
    """Functions which gets the choice from the user"""
    choice = 0

    while not 1 <= choice <= 8:
        # Getting choice from the user
        choice = int(input("Enter your choice: "))

        # If the choice is valid, break the loop
        if 1 <= choice <= 8:
            return choice

        # Otherwise, retry
        else:
            print("Invalid choice, try again")


def get_data(choice):
    """Function which prints the according choice message"""
    if not (choice == 1 or choice == 8):
        data = input(CHOICE_MESSAGES[choice-1])
    else:
        data = ""
    return data


def main():
    # Creating a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating the server address
    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)

    # Getting welcome message from the server
    welcome_msg = sock.recv(1024)
    print(welcome_msg.decode())

    try:
        while True:
            # Printing the menu (time is used in order to allow the user enough time to read the response)
            time.sleep(3)
            print(MENU)

            choice = check_choice()
            # If the choice was 8, sending the termination request to the server
            if choice == 8:
                # Sending the termination request
                sock.sendall(REQUESTS[choice - 1].encode())

                # Getting the response from the server
                response = sock.recv(2048)
                # noinspection PyUnusedLocal
                response = response.decode()

                # Closing the client socket
                sock.close()

                break

            else:
                # Getting the data
                data = get_data(choice)

                # Getting the correct request
                request = REQUESTS[choice - 1]

                # Assembling the request
                complete_request = request + data

                # Sending the request to the server
                sock.sendall(complete_request.encode())

                # Getting the response
                response = sock.recv(2048)
                response = response.decode()

                # Printing the server's response
                print(response[response.find("=") + 1:])

    except Exception as e:
        print("Client Error Encountered:", e)

        sock.close()


if __name__ == '__main__':
    main()
