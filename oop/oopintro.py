#!/usr/bin/env python


class Dog(object):

    alive = 0  # Class variable

    def __init__(self, color="white", breed="mutt"):
        self.color = color  # Instance variable
        self.breed = breed
        self.__class__.alive += 1  # Or Dog.alive += 1

    def __del__(self):
        self.__class__.alive -= 1  # Or Dog.alive -= 1

    def __repr__(self):
        return "This dog is a " + self.color + " " + self.breed

    def speak(self):
        print "woof woof"


class Puppy(Dog):
    def __init__(self, color="white", breed="mutt", wormed=True):
        super(Puppy, self).__init__(color, breed)
        self.dewormed = wormed

    def __del__(self):
        if Dog is not None:  # Dog is deleted at the end of the program
            # Dog.__del__(self)
            # Or, self.__class__.__base__.__del__(self)
            super(Puppy, self).__del__()

    def __repr__(self):
        return "This puppy is a " + self.color + " " + self.breed

    def speak(self):
        print "ruff ruff"


def birth():
    fido3 = Dog()
    print "In function", Dog.alive  # ==> 3

fido1 = Dog()
fido2 = Dog("black", "lab")
fido1.speak()  # ==> woof woof
fido2.speak()  # ==> woof woof
print fido1  # ==> This dog is a white mutt
print fido2  # ==> This dog is a black lab

print "\nBefore function", Dog.alive  # ==> 2
birth()
print "After function", Dog.alive  # ==> 2
fido3 = Dog()
print "Now", Dog.alive, "\n"  # ==> 3

print id(Dog.alive), id(fido1.alive), id(fido2.alive), id(fido3.alive)

L = []
for x in xrange(1000):
    L.append(Dog())
print "\nAfter loop", Dog.alive  # ==> 1003

pup1 = Puppy()
pup1.speak()
print "\n", pup1
pup2 = Puppy("brown", "pointer")
print pup2

print "\n", pup2.__class__  # ==> <class '__main__.Puppy'>
print pup2.__class__.__base__  # ==> <class '__main__.Dog'>
print pup2.__class__.__mro__
# ==> (<class '__main__.Puppy'>, <class '__main__.Dog'>, <type 'object'>)
