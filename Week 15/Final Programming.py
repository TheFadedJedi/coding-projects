# Final Programming, Ocean Level
ocean_level=0
rise=1.6
print("Each year the water raises about 1.6 millimeters per year")
num=int(input("How many years out do you want to see?:"))
for year in range(1, num+1):
    ocean_level+=rise
    print(f"Year {year}: Ocean has risen about {round(ocean_level, 2)} millimeters.")