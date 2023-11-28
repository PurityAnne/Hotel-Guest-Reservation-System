# Function to load room details from file into multidimensional list
def loadDetails():
    roomData = []
    with open("room_details.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            details = line.strip().split(",")
            category = details[0]
            numRooms = int(details[1])
            capacity = int(details[2])
            pricePerNight = int(details[3])
            pricePerWeek = int(details[4])
            pricePerMonth = int(details[5])
            numOccupied = int(details[6])
            roomData.append([category, numRooms, capacity, pricePerNight, pricePerWeek, pricePerMonth, numOccupied])
    return roomData

# Function to check availability of a room
def checkAvailability(roomData, category, numberOfGuests):
    for i in range(len(roomData)):
        if roomData[i][0] == category and roomData[i][1] > roomData[i][6] and roomData[i][2] >= numberOfGuests:
            return True, i
    return False, None

# Function to calculate the price of a reservation
def calculatePrice(roomData, durationOfStay, roomIndex):
    if durationOfStay < 7:
        price = roomData[roomIndex][3] * durationOfStay
    elif durationOfStay < 30:
        price = roomData[roomIndex][4] * (durationOfStay // 7) + roomData[roomIndex][3] * (durationOfStay % 7)
    else:
        price = roomData[roomIndex][5] * (durationOfStay // 30) + roomData[roomIndex][4] * ((durationOfStay % 30) // 7) + roomData[roomIndex][3] * ((durationOfStay % 30) % 7)
    return price

# Function to create a summary of the availability of rooms
def createSummary(roomData):
    print("Summary of Room Availability")
    print("---------------------------")
    for room in roomData:
        print("Category: {}".format(room[0]))
        print("Number of Rooms Occupied: {}".format(room[6]))
        print("---------------------------")

# Function to update room details file
def updateTextFile(roomData):
    with open("room_details.txt", "w") as file:
        for room in roomData:
            file.write("{},{},{},{},{},{},{}\n".format(room[0], room[1], room[2], room[3], room[4], room[5], room[6]))

# Main function to run the hotel reservation system
def main():
    roomData = loadDetails()

    while True:
        choice = input("Would you like to make a new reservation (N), check out (C), or quit (Q)? ").upper()

        if choice == "N":
            category = input("What type of room would you like (Wonderful/Marvelous/Spectacular/Fantastic/Fabulous/Wow)? ")
            numberOfGuests = int(input("How many guests will be staying in the room? "))
            durationOfStay = int(input("How many nights will you be staying? "))

            isAvailable, roomIndex = checkAvailability(roomData, category, numberOfGuests)
            if isAvailable:
                price = calculatePrice(roomData, durationOfStay, roomIndex)
                print("The total price for your reservation is ${}".format(price))
                roomData[roomIndex][6] = '1'
                updateTextFile(roomData)
                print("Thank you for making a reservation with us.")
            else:
                print("Sorry, we do not have any available rooms that meet your requirements.")

        elif choice == "C":
            category = input("What type of room did you stay in (Wonderful/Marvelous/Spectacular/Fantastic/Fabulous/Wow)? ")
            roomIndex = -1
            for i in range(len(roomData)):
                if roomData[i][0].lower() == category.lower() and int(roomData[i][6]) == 1:
                    roomIndex = i
                    break
            if roomIndex == -1:
                print("Sorry, we could not find a room with that category that you stayed in.")
            else:
                roomData[roomIndex][6] = '0'
                updateTextFile(roomData)
                print("Thank you for staying with us.")

        elif choice == "Q":
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()