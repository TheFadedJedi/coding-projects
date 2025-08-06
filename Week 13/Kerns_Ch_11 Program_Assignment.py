#Ch_11 Program_Assignment
class Animal:
    def __init__(self, species):
        self.species = species
    def make_sound(self):
        pass
class Dog(Animal):
    def __init__(self, name):
        super().__init__('Dog')
        self.name = name
    def make_sound(self):
        return "Woof!"
dog_instance = Dog('Buddy')
print("The "+dog_instance.species+" "+dog_instance.name+" says "+dog_instance.make_sound())
class Cat(Animal):
    def __init__(self, name):
        super().__init__('Cat')
        self.name = name
    def make_sound(self):
        return "Meow!"
cat_instance = Cat('Mittens')
print("The "+cat_instance.species+" "+cat_instance.name+" says "+cat_instance.make_sound())
def animal_sounds(animal):
    return animal.make_sound()
class Bird(Animal):
    def __init__(self, name):
        super().__init__('Bird')
        self.name = name
    def make_sound(self):
        return "Chirp"
bird_instance = Bird('Sparrow')
print("The "+bird_instance.species+" "+bird_instance.name+" goes "+bird_instance.make_sound())
class Cow(Animal):
    def __init__(self, name):
        super().__init__('Cow')
        self.name = name
    def make_sound(self):
        return "Moooo"
cow_instance = Cow('Bessie')
print("The "+cow_instance.species+" "+cow_instance.name+" goes "+cow_instance.make_sound())
