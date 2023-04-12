import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book_hotel(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Checks if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """

        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_security.loc[df_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are you booking SPA data:
        Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """

        return content


print(df)
hotel_ID = input("Enter the id of the Hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="5678")
    if credit_card.validate(expiration="12/28", holder="JANE SMITH", cvc="456"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book_hotel()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            spa = input("Would you like to reserve a spa? ")
            if spa == "yes":
                hotel.book_spa_package()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())
            else:
                print("Goodbye")

        else:
            print("Authentication failed")
    else:
        print("Payment did not go through")

else:
    print("Hotel is not available")
