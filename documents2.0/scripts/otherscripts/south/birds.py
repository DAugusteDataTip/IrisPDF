"""Here is a list of classes.

Bird is the word!"""


class Bird:
    def __init__(self, has_young, age, name):
        self.has_young = has_young
        self.age = age
        self.name = name

    def wingspan(self, wing):
        totalwingspan = wing * 2
        return totalwingspan


class Hummingbird(Bird):
    def sound(self):
        print(self.name + "goes 'TWEET!'")


class Eagle(Bird):
    def words(self):
        print(self.name + " is a majestic bird.")
