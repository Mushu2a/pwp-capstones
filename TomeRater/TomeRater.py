import re


class EmailDoesNotExistException(Exception):
    """
    Exception for email doesn't exist for this user
    """


class InvalidRatingException(Exception):
    """
    Exception rating is a 'int' can't be more than 4 and less than 0
    """


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.book = {}

    def verify_email(email):
        regex = re.compile(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[(com|edu|org)]+")
        if (regex.match(email) is not None):
            return True
        else:
            return False

    def get_email(self):
        if self.name:
            return self.email
        else:
            raise EmailDoesNotExistException("Not email for this user")

    def change_email(self, address):
        if (self.verify_email(address)):
            print("Address invalid !")
        else:
            self.email = self.verify_email(address)
            print("Email address has been changed !")

    def read_book(self, book, rating=None):
        self.book[book] = rating

    def get_books(self):
        for book in self.book:
            print(book)

    def get_sum_cost_books(self):
        cost = 0
        for book in self.book:
            cost += book.price

        return cost

    def get_average_rating(self):
        count = 0
        average = 0
        for book, rating in self.book.items():
            if (rating != None):
                average += rating
                count += 1

        if (count != 0):
            return round(average / count, 1)
        else:
            return 0

    def __repr__(self):
        return "User {user}, email: {email}, books read: {count}".format(user=self.name, email=self.email, count=len(self.book))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email


class Book(object):
    def __init__(self, title, price, isbn):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("This book’s ({}) ISBN has been updated !".format(self.title))

    def set_price(self, price):
        self.price = price
        print("This book’s ({}) price has been updated !".format(self.title))

    def get_price(self):
        return self.price

    def add_rating(self, rating):
        if type(rating) == int:
            if (rating < 5 and rating > 0):
                self.ratings.append(rating)
                message = "Rating added successfull !"
            else:
                message = "Valid rating (at least 0 and at most 4)"

            print(message)
        else:
            raise InvalidRatingException("Rating is a invalid integer")

    def get_average_rating(self):
        count = 0
        average = 0
        for rating in self.ratings:
            average += rating
            count += 1

        if (count != 0):
            return round(average / count, 1)
        else:
            return 0

    def __repr__(self):
        return "Book {title} have ISBN: {isbn}".format(title=self.title, isbn=self.isbn)

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    # Make book hashable
    # Doc: https://docs.python.org/3/library/functions.html#hash
    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, price, isbn):
        super().__init__(title, price, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, price, isbn):
        super().__init__(title, price, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, price, isbn):
        new_book = Book(title, price, isbn)
        return new_book

    def create_novel(self, title, author, price, isbn):
        new_fiction = Fiction(title, author, price, isbn)
        return new_fiction

    def create_non_fiction(self, title, subject, level, price, isbn):
        new_non_fiction = Non_Fiction(title, subject, level, price, isbn)
        return new_non_fiction

    def add_book_to_user(self, book, email, rating=None):
        for user in self.users:
            if (not self.users.get(email)):
                print("No user with email {email}!".format(email=email))
            else:
                user = self.users[email]
                user.read_book(book, rating)

                book = Book(book.title, book.price, book.isbn)
                if (rating != None):
                    book.add_rating(rating)

                if (book not in self.books):
                    self.books[book] = 1
                else:
                    self.books[book] += 1

    def add_user(self, name, email, user_books=None):
        if (not self.users.get(email)):
            if (User.verify_email(email)):
                user = User(name, email)
                self.users[email] = user
                if (user_books != None):
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("This email {email}, not a good formatted email !".format(
                    email=email))
        else:
            print("Can't save email {email}, already taken !".format(
                email=email))

    # The most read books
    # Show n book(s)
    # @return books array
    def get_n_most_read_books(self, n):
        read_book = {}
        isSorted = []
        if (n <= len(self.books.values())):
            for book, read in self.books.items():
                read_book[book.title] = read

            books = sorted(read_book.items(),
                           reverse=True, key=lambda x: x[1])
            for book in books:
                isSorted.append(book[0])

        return isSorted[:n]

    # The most prolific readers
    # Show n reader(s)
    # @return users array
    def get_n_most_prolific_readers(self, n):
        user_read_book = {}
        isSorted = []
        if (n <= len(self.users.values())):
            for user in self.users.values():
                user_read_book[user.name] = len(user.book)

            users = sorted(user_read_book.items(),
                           reverse=True, key=lambda x: x[1])
            for user in users:
                isSorted.append(user[0])

        return isSorted[:n]

    def get_n_most_expensive_books(self, n):
        price_book = {}
        isSorted = []
        if (n <= len(self.books.values())):
            for book in self.books:
                price_book[book.title] = book.get_price()

            books = sorted(price_book.items(),
                           reverse=True, key=lambda x: x[1])
            for book in books:
                isSorted.append(book[0])

        return isSorted[:n]

    def get_worth_of_user(self, user_email):
        if (self.users.get(user_email)):
            user = self.users[user_email]

            return "All book from {user} cost in total {total}€".format(user=user.name, total=user.get_sum_cost_books())

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users:
            print(user)

    def show_user_books(self, email):
        if (self.users.get(email)):
            print("- User books:")
            user = self.users[email]
            user.get_books()
        else:
            print("No user with email {email}!".format(email=email))

    def most_read_book(self):
        max_read = 0
        book_item = ""
        for book, read in self.books.items():
            if (read > max_read):
                book_item = book
                max_read = read

        return book_item

    def highest_rated_book(self):
        max_rated_average = 0
        book_item = ""
        for book, value in self.books.items():
            if (book.get_average_rating() > max_rated_average):
                book_item = book
                max_read = book.get_average_rating()

        return book_item

    def most_positive_user(self):
        max_positive_user = 0
        user_item = ""
        for email in self.users.keys():
            user = self.users[email]
            if (user.get_average_rating() > max_positive_user):
                user_item = user
                max_positive_user = user.get_average_rating()

        return user_item

    # The most prolific readers
    # @return user
    def most_reader_user(self):
        max_reader_user = 0
        user_item = ""
        for email in self.users.keys():
            user = self.users[email]
            if (len(user.book) > max_reader_user):
                user_item = user
                max_reader_user = len(user.book)

        return user_item

    def __repr__(self):
        return "Welcome here, to try some functionalities"

    def __eq__(self, other_tome):
        return self.users == other_tome.users and self.books == other_tome.books
