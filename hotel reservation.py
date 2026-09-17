import random
import time
class Customer:

    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.status = "Available"
class Reservation:

    def __init__(self, booking_id, customer_id, room_number,
                 room_type, days, total_bill):

        self.booking_id = booking_id
        self.customer_id = customer_id
        self.room_number = room_number
        self.room_type = room_type
        self.days = days
        self.total_bill = total_bill
        self.status = "Reserved"
        self.booking_time = time.ctime()
class Hotel:

    def __init__(self):

        self.customers = []
        self.rooms = []
        self.reservations = {}

        self.create_rooms()
        self.load_data()
    def create_rooms(self):

        # Single rooms
        for i in range(101, 106):
            room = Room(i, "Single", 1500)
            self.rooms.append(room)

        # Double rooms
        for i in range(201, 206):
            room = Room(i, "Double", 2500)
            self.rooms.append(room)

        # Deluxe rooms
        for i in range(301, 306):
            room = Room(i, "Deluxe", 3500)
            self.rooms.append(room)

        # Suite rooms
        for i in range(401, 406):
            room = Room(i, "Suite", 5000)
            self.rooms.append(room)
    def add_customer(self):

        print("\n----- ADD CUSTOMER -----")

        name = input("Enter customer name: ")
        phone = input("Enter phone number: ")

        customer_id = "C" + str(len(self.customers) + 1)

        customer = Customer(customer_id, name, phone)

        self.customers.append(customer)

        print("\nCustomer added successfully!")
        print("Customer ID:", customer_id)

        self.save_data()

    def display_customers(self):

        print("\n----- CUSTOMER LIST -----")

        if len(self.customers) == 0:
            print("No customers found.")
            return

        for customer in self.customers:

            print("Customer ID:", customer.customer_id)
            print("Name:", customer.name)
            print("Phone:", customer.phone)
            print("------------------------")


    def generate_booking_id(self):

        while True:

            number = random.randint(1000, 9999)

            booking_id = "BK" + str(number)

            if booking_id not in self.reservations:
                return booking_id

    def find_customer(self, customer_id):

        for customer in self.customers:

            if customer.customer_id == customer_id:
                return customer

        return None


    def find_room(self, room_number):

        for room in self.rooms:

            if room.room_number == room_number:
                return room

        return None


    def show_rooms(self):

        print("\n----- ROOM DETAILS -----")

        for room in self.rooms:

            print("Room:", room.room_number)
            print("Type:", room.room_type)
            print("Price per day:", room.price)
            print("Status:", room.status)
            print("------------------------")


    def find_available_room(self, room_type):

        for room in self.rooms:

            if room.room_type == room_type and room.status == "Available":
                return room

        return None


    def calculate_bill(self, room, days):

        total = room.price * days

        # Weekend charge
        weekend = input("Is the stay on weekend? (yes/no): ")

        if weekend == "yes":
            total = total + (total * 10 / 100)

        # Discount for long stay
        if days > 5:

            discount = total * 10 / 100
            total = total - discount

            print("10% long stay discount applied.")

        return total


    def book_room(self):

        print("\n----- ROOM BOOKING -----")

        customer_id = input("Enter Customer ID: ")

        customer = self.find_customer(customer_id)

        if customer is None:

            print("Customer not found.")
            print("Please add customer first.")
            return


        print("\nRoom Types:")
        print("1. Single")
        print("2. Double")
        print("3. Deluxe")
        print("4. Suite")

        choice = input("Enter your choice: ")


        if choice == "1":
            room_type = "Single"

        elif choice == "2":
            room_type = "Double"

        elif choice == "3":
            room_type = "Deluxe"

        elif choice == "4":
            room_type = "Suite"

        else:
            print("Invalid choice.")
            return


        room = self.find_available_room(room_type)

        if room is None:

            print("Sorry! No", room_type, "room is available.")
            return


        days = int(input("Enter number of days: "))

        if days <= 0:

            print("Invalid number of days.")
            return


        total_bill = self.calculate_bill(room, days)

        booking_id = self.generate_booking_id()


        reservation = Reservation(
            booking_id,
            customer_id,
            room.room_number,
            room.room_type,
            days,
            total_bill
        )


        self.reservations[booking_id] = reservation

        room.status = "Reserved"


        print("\n----- BOOKING SUCCESSFUL -----")
        print("Booking ID:", booking_id)
        print("Customer Name:", customer.name)
        print("Room Number:", room.room_number)
        print("Room Type:", room.room_type)
        print("Number of Days:", days)
        print("Total Bill:", total_bill)
        print("Booking Time:", reservation.booking_time)


        self.save_data()

    def search_reservation(self):

        print("\n----- SEARCH RESERVATION -----")

        booking_id = input("Enter Booking ID: ")

        if booking_id not in self.reservations:

            print("Booking not found.")
            return


        reservation = self.reservations[booking_id]

        print("\nBooking ID:", reservation.booking_id)
        print("Customer ID:", reservation.customer_id)
        print("Room Number:", reservation.room_number)
        print("Room Type:", reservation.room_type)
        print("Days:", reservation.days)
        print("Bill:", reservation.total_bill)
        print("Status:", reservation.status)
        print("Booking Time:", reservation.booking_time)


    def check_in(self):

        print("\n----- CHECK IN -----")

        booking_id = input("Enter Booking ID: ")

        if booking_id not in self.reservations:

            print("Booking not found.")
            return


        reservation = self.reservations[booking_id]


        if reservation.status != "Reserved":

            print("Customer cannot check in.")
            print("Current status:", reservation.status)
            return


        reservation.status = "Checked-In"

        room = self.find_room(reservation.room_number)

        if room is not None:
            room.status = "Checked-In"


        print("Check-in successful!")
        print("Check-in time:", time.ctime())

        self.save_data()


    def check_out(self):

        print("\n----- CHECK OUT -----")

        booking_id = input("Enter Booking ID: ")

        if booking_id not in self.reservations:

            print("Booking not found.")
            return


        reservation = self.reservations[booking_id]


        if reservation.status != "Checked-In":

            print("Customer has not checked in.")
            return


        late = input("Is the checkout late? (yes/no): ")


        final_bill = reservation.total_bill


        if late == "yes":

            late_charge = 500

            final_bill = final_bill + late_charge

            print("Late checkout charge: 500")


        reservation.status = "Checked-Out"


        room = self.find_room(reservation.room_number)

        if room is not None:

            room.status = "Available"


        print("\n----- CHECK OUT SUCCESSFUL -----")
        print("Booking ID:", reservation.booking_id)
        print("Room Number:", reservation.room_number)
        print("Final Bill:", final_bill)
        print("Checkout Time:", time.ctime())


        self.save_data()


    # ---------------- CANCEL BOOKING ----------------

    def cancel_booking(self):

        print("\n----- CANCEL BOOKING -----")

        booking_id = input("Enter Booking ID: ")

        if booking_id not in self.reservations:

            print("Booking not found.")
            return


        reservation = self.reservations[booking_id]


        if reservation.status == "Checked-Out":

            print("Already checked out.")
            return


        if reservation.status == "Cancelled":

            print("Booking already cancelled.")
            return


        print("Original Bill:", reservation.total_bill)

        cancellation_charge = reservation.total_bill * 10 / 100

        print("Cancellation charge:", cancellation_charge)


        reservation.status = "Cancelled"


        room = self.find_room(reservation.room_number)

        if room is not None:

            room.status = "Available"


        print("Booking cancelled successfully.")

        self.save_data()


    def reservation_history(self):

        print("\n----- RESERVATION HISTORY -----")

        if len(self.reservations) == 0:

            print("No reservations found.")
            return


        for booking_id in self.reservations:

            reservation = self.reservations[booking_id]

            print("\nBooking ID:", reservation.booking_id)
            print("Customer ID:", reservation.customer_id)
            print("Room:", reservation.room_number)
            print("Room Type:", reservation.room_type)
            print("Days:", reservation.days)
            print("Bill:", reservation.total_bill)
            print("Status:", reservation.status)
            print("Booking Time:", reservation.booking_time)
            print("-----------------------------")

    def maintenance_room(self):

        print("\n----- ROOM MAINTENANCE -----")

        room_number = int(input("Enter room number: "))

        room = self.find_room(room_number)

        if room is None:

            print("Room not found.")
            return


        if room.status != "Available":

            print("Room is not available for maintenance.")
            print("Current status:", room.status)
            return


        room.status = "Maintenance"

        print("Room marked as Maintenance.")

        self.save_data()

    def make_room_available(self):

        print("\n----- MAKE ROOM AVAILABLE -----")

        room_number = int(input("Enter room number: "))

        room = self.find_room(room_number)

        if room is None:

            print("Room not found.")
            return


        if room.status != "Maintenance":

            print("Room is not under maintenance.")
            return


        room.status = "Available"

        print("Room is now Available.")

        self.save_data()

    def save_data(self):

        file = open("hotel_data.txt", "w")


        # Save customers

        file.write("CUSTOMERS\n")

        for customer in self.customers:

            file.write(
                customer.customer_id + "|" +
                customer.name + "|" +
                customer.phone + "\n"
            )



        file.write("RESERVATIONS\n")

        for booking_id in self.reservations:

            reservation = self.reservations[booking_id]

            file.write(
                reservation.booking_id + "|" +
                reservation.customer_id + "|" +
                str(reservation.room_number) + "|" +
                reservation.room_type + "|" +
                str(reservation.days) + "|" +
                str(reservation.total_bill) + "|" +
                reservation.status + "|" +
                reservation.booking_time + "\n"
            )


        file.close()



    def load_data(self):

        try:

            file = open("hotel_data.txt", "r")

            section = ""


            for line in file:

                line = line.strip()


                if line == "CUSTOMERS":

                    section = "customers"
                    continue


                if line == "RESERVATIONS":

                    section = "reservations"
                    continue


                if line == "":
                    continue


                data = line.split("|")


                if section == "customers":

                    customer_id = data[0]
                    name = data[1]
                    phone = data[2]

                    customer = Customer(
                        customer_id,
                        name,
                        phone
                    )

                    self.customers.append(customer)


                elif section == "reservations":

                    booking_id = data[0]
                    customer_id = data[1]
                    room_number = int(data[2])
                    room_type = data[3]
                    days = int(data[4])
                    total_bill = float(data[5])
                    status = data[6]
                    booking_time = data[7]


                    reservation = Reservation(
                        booking_id,
                        customer_id,
                        room_number,
                        room_type,
                        days,
                        total_bill
                    )


                    reservation.status = status
                    reservation.booking_time = booking_time


                    self.reservations[booking_id] = reservation


                    room = self.find_room(room_number)


                    if room is not None:

                        if status == "Reserved":
                            room.status = "Reserved"

                        elif status == "Checked-In":
                            room.status = "Checked-In"

                        elif status == "Cancelled":
                            room.status = "Available"

                        elif status == "Checked-Out":
                            room.status = "Available"


            file.close()


        except:

            pass

    def menu(self):

        while True:

            print("\n")
            print("======================================")
            print("     SMART HOTEL RESERVATION SYSTEM")
            print("======================================")

            print("1. Add Customer")
            print("2. Display Customers")
            print("3. Show Rooms")
            print("4. Book Room")
            print("5. Search Reservation")
            print("6. Check In")
            print("7. Check Out")
            print("8. Cancel Booking")
            print("9. Reservation History")
            print("10. Put Room in Maintenance")
            print("11. Make Room Available")
            print("12. Exit")

            choice = input("Enter your choice: ")


            if choice == "1":

                self.add_customer()


            elif choice == "2":

                self.display_customers()


            elif choice == "3":

                self.show_rooms()


            elif choice == "4":

                self.book_room()


            elif choice == "5":

                self.search_reservation()


            elif choice == "6":

                self.check_in()


            elif choice == "7":

                self.check_out()


            elif choice == "8":

                self.cancel_booking()


            elif choice == "9":

                self.reservation_history()


            elif choice == "10":

                self.maintenance_room()


            elif choice == "11":

                self.make_room_available()


            elif choice == "12":

                self.save_data()

                print("Thank you!")
                print("Program closed.")

                break


            else:

                print("Invalid choice. Please try again.")



hotel = Hotel()

hotel.menu()