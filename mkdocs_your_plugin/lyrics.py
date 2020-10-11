from random import choice


lyrics = [
    "Hello, Dolly",
    "Well, hello, Dolly",
    "It's so nice to have you back where you belong",
    "You're lookin' swell, Dolly",
    "I can tell, Dolly",
    "You're still glowin', you're still crowin'",
    "You're still goin' strong",
    "We feel the room swayin'",
    "While the band's playin'",
    "One of your old favourite songs from way back when",
    "So, take her wrap, fellas",
    "Find her an empty lap, fellas",
    "Dolly'll never go away again",
]


def random_lyrics():
    """
    Picks a random verse from the lyrics
    """

    return "&laquo; {} &raquo;".format(choice(lyrics))
