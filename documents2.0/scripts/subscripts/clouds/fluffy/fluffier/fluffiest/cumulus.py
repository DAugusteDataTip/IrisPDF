"""This is a document about clouds and such and so on and so on."""


def storm(clouds, color):
    """Let's predict if there will be a storm"""
    if clouds == "cumulonimbus" and color == "black":
        print("There's a storm a-brewin'!")

def nice_day(clouds, color):
    """This will tell you if you should have a picnic."""
    if clouds == "cirrus" and color == "white":
        print("Time for a picnic!")
    elif clouds == "cirrus" and color == "blue":
        print("It's a good day for plein-air painting.")
    else:
        print("Best to stay indoors.")

def cloudy(clouds, color):
    """Let's see if it is an overcast day."""
    if clouds == "nimbus" and color == "grey":
        print("It looks like rain. Better pack an umbrella.")