# Setting a pet class
def main():
    class Pet:
        def __init__(self, name, animal_type, age):
            self.__name=name
            self.__animal_type=animal_type
            self.__age=age

        def get_name(self):
            return self.__name

        def set_name(self, name):
            self.__name=name

        def get_animal_type(self):
            return self.__animal_type

        def set_animal_type(self, animal_type):
            self.__animal_type = animal_type

        def get_age(self):
            return self.__age

        def set_age(self, age):
            if age >=0:
                self.__age = age
            else:
                print("Age cannot be negative.")

        def display_info(self):
            print(f"Pet Name: {self.__name}")
            print(f"Animal Type: {self.__animal_type}")
            print(f"Age: {self.__age} years")

    def create_pet():
        name=input("Enter the pet's name: ")
        animal_type = input("Enter the animal type: ")
        age=int(input("Enter the pet's age: "))
        pet=Pet(name, animal_type, age)
        return pet
    my_pet=create_pet()
    print("\nPet Information:")
    my_pet.display_info()

if __name__ == '__main__':
    main()