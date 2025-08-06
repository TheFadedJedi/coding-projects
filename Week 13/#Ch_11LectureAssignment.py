#Ch_11LectureAssignment
# Inheritance example:
# Base class (also called parent class)
class Animal:
    def __init__(self, species):
        self.species = species
    def make_sound(self):
        pass
# Derived class (also called child class) inheriting from Animal
class Dog(Animal):
    def __init__(self, name):
        super().__init__('Dog') # Calling the constructor of the base class
        self.name = name
    def make_sound(self):
        return "Woof!"
# Creating an instance of Dog class and accessing properties and methods
dog_instance = Dog('Buddy')
print(dog_instance.species) # Output: Dog
print(dog_instance.name) # Output: Buddy
print(dog_instance.make_sound()) # Output: Woof!
# Polymorphism example:
# Polymorphism with a common method name across different classes
class Cat(Animal):
    def __init__(self, name):
        super().__init__('Cat')
        self.name = name
    def make_sound(self):
        return "Meow!"
# Function to make various animals make sounds
def animal_sounds(animal):
    return animal.make_sound()
# Creating instances of Dog and Cat classes and passing them to the function
dog_instance = Dog('Buddy')
cat_instance = Cat('Whiskers')
print(animal_sounds(dog_instance)) # Output: Woof!
print(animal_sounds(cat_instance)) # Output: Meow!
# Overloading example:
# Overloading a method to handle different parameter types
class MathOperations:
    def add(self, a, b):
        return a + b
    def add(self, a, b, c):
        return a + b + c
math_ops = MathOperations()
#print(math_ops.add(2, 3)) # Output: TypeError (method is overwritten)
print(math_ops.add(2, 3, 4)) # Output: 9
# Overriding example
# Overriding a method in a derived class
class Bird(Animal):
    def __init__(self, species, can_fly):
        super().__init__(species)
        self.can_fly = can_fly
    def make_sound(self):
        return "Chirp"
bird_instance = Bird('Sparrow', True)
print(bird_instance.make_sound()) # Output: Chirp (overrides the make_sound() method from
#the base class)
# Super function:
# Using super() to access methods from the base class
class Parent:
    def display(self):
        print("Parent's display method")
class Child(Parent):
    def display(self):
        super().display() # Call the display() method from the base class
print("Child's display method")
child_instance = Child()
child_instance.display()
# Creating Subclasses, Getters, Setters, Deleters:
# Creating a base class with properties and methods
class Shape:
    def __init__(self, sides):
        self.sides = sides
    def get_area(self):
        pass
# Creating a subclass of Shape and using getters, setters, deleters
class Square(Shape):
    def __init__(self, side_length):
        super().__init__(sides=4)
        self.side_length = side_length
    def get_area(self):
        return self.side_length ** 2
# Getter method
@property
def side_length(self):
    return self._side_length
# Setter method
@side_length.setter
def side_length(self, value):
    if value < 0:
        raise ValueError("Side length cannot be negative.")
    self._side_length = value
# Deleter method
@side_length.deleter
def side_length(self):
    print("Deleting the side length.")
    del self._side_length
square_instance = Square(5)
print(square_instance.get_area()) # Output: 25
# Using the property to access the side_length
print(square_instance.side_length) # Output: 5
# Using the setter to change the side_length
square_instance.side_length = 7
print(square_instance.get_area()) # Output: 49
# Using the deleter to delete the side_length
del square_instance.side_length