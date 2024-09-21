FILE_PATH = "Pink_Floyd_DB.txt"
ALBUM_SYMBOL = "#"
SONG_SYMBOL = "*"


def open_file():
    """Function which opens a file and returns its contents"""
    # Opening the file
    with open(FILE_PATH, "r") as file_obj:

        # Getting the contents
        file_contents = file_obj.read()

    # Returning the contents
    return file_contents


def create_data_structure(file_contents):
    """Function which creates a data structure:
    the data structure is a dictionary, every key in it is an album name,
    the value the album name points to contains the album's release year
    and a dictionary for every song on the album
    in that dictionary the song's name is the key and the value is a list
    which contains the songwriter, the song's length and it's lyrics
    input: file's contents
    output: the data structure"""

    # Creating the overall data structure
    data_structure = dict()

    # Splitting the file content's into albums
    albums = file_contents.split('#')

    # removing the empty space at the beginning
    albums.remove(albums[0])

    # For every item in the albums
    for item in albums:

        # Getting the albums
        album = item[:item.find("::")]

        # Their release year
        year = item[item.find("::") + 2: item.find("\n")]

        # And adding them to the dictionary as a list
        data_structure[album] = [year]

        # Splitting the item into separate songs
        songs_info = item.split('*')

        # For every song on the album
        for songs in range(1, len(songs_info)):

            # Getting the song's name
            song_name = songs_info[songs][: songs_info[songs].find("::")]

            # Getting the song's writer/s
            song_writers = songs_info[songs][songs_info[songs].find("::") + 2: songs_info[songs].find("::", songs_info[
                songs].find("::") + 1)]

            # Getting the song's length
            song_length = songs_info[songs][songs_info[songs].find("::", songs_info[songs].find("::") + 1) + 2:
                                            songs_info[songs].rfind("::")]

            # Getting the song's lyrics
            song_lyrics = songs_info[songs][songs_info[songs].rfind("::") + 2:]

            # Creating the song's structure
            song_structure = dict()
            song_structure[song_name] = [song_writers, song_length, song_lyrics]

            # Adding that structure into the data structure
            data_structure[album].append(song_structure)

    # Returning the data structure
    return data_structure
