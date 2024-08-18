import tkinter as tk
from tkinter import simpledialog, messagebox


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = False

    def __str__(self):
        return f"'{self.title}' by {self.author}"


class Patron:
    def __init__(self, name, patron_id):
        self.name = name
        self.patron_id = patron_id
        self.checked_out_books = []

    def __str__(self):
        return self.name


class Library:
    def __init__(self):
        self.books = []
        self.patrons = []

        # Adding static books to the library
        self.add_static_books()

    def add_static_books(self):
        static_books = [
            Book("Alice in Wonderland", "Lewis Carroll", "978-0451532008"),
            Book("Harry Potter", "J.K. Rowling", "978-0545582889"),
            Book("Cinderella", "Charles Perrault", "978-1234567890"),
            Book("Around the World in 30 Days", "Jules Verne", "978-0987654321")
        ]
        self.books.extend(static_books)

    def add_book(self, book):
        self.books.append(book)
        tk.messagebox.showinfo("Success", f"Book '{book.title}' added to the library.")

    def add_patron(self, patron):
        self.patrons.append(patron)

    def display_books(self):
        if self.books:
            # Create a new window
            books_window = tk.Toplevel()
            books_window.title("Library Books")
            books_window.geometry("300x300")
            center_window(books_window, 300, 300)

            # Create a Text widget to display the list of books
            text_widget = tk.Text(books_window, wrap=tk.WORD)
            text_widget.pack(expand=True, fill=tk.BOTH)
            text_widget.tag_configure("color", foreground="red")
            # Insert the list of books into the Text widget
            books_list = "\n".join(str(book) for book in self.books)
            text_widget.insert(tk.END, f"The library has the following books:\n\n{books_list}", "color")

            # Disable editing of the Text widget
            text_widget.config(state=tk.DISABLED)
        else:
            tk.messagebox.showinfo("No Books", "No books are available in the library.")

    def check_out(self, patron, book):
        if book in self.books and not book.checked_out:
            book.checked_out = True
            patron.checked_out_books.append(book)
            tk.messagebox.showinfo("Checked Out", f"{patron.name} has checked out {book}.")
        else:
            tk.messagebox.showinfo("Unavailable", f"Sorry, {book.title} is not available.")

    def check_in(self, patron, book):
        if book in patron.checked_out_books:
            book.checked_out = False
            patron.checked_out_books.remove(book)
            tk.messagebox.showinfo("Returned", f"{patron.name} has returned {book}.")
        else:
            tk.messagebox.showinfo("Not Found", f"{patron.name} does not have {book.title} checked out.")


class LibraryGUI:
    def __init__(self, root):
        self.library = Library()

        # Create a window to enter patron's name and ID
        self.patron_info_window(root)

        # Set up the main window after patron information is validated
        self.main_window(root)

    def patron_info_window(self, root):
        # Create a new window for entering patron information
        patron_window = tk.Toplevel(root)
        patron_window.title("Enter Patron Information")
        patron_window.geometry("300x200")
        center_window(patron_window, 300, 200)
        patron_window.configure(bg="lightblue")

        # Patron Name Label and Entry
        patron_name_label = tk.Label(patron_window, text="Patron Name:", anchor="w", bg="lightblue")
        patron_name_label.pack(fill="x", padx=10, pady=5)
        self.patron_name_entry = tk.Entry(patron_window)
        self.patron_name_entry.pack(fill="x", padx=10, pady=5)

        # Patron ID Label and Entry
        patron_id_label = tk.Label(patron_window, text="Patron ID:", anchor="w", bg="lightblue")
        patron_id_label.pack(fill="x", padx=10, pady=5)
        self.patron_id_entry = tk.Entry(patron_window)
        self.patron_id_entry.pack(fill="x", padx=10, pady=5)

        # Function to handle the "Submit" action
        def submit():
            patron_name = self.patron_name_entry.get()
            patron_id = self.patron_id_entry.get()
            if patron_name and patron_id:
                self.patron = Patron(patron_name, patron_id)
                self.library.add_patron(self.patron)
                patron_window.destroy()  # Close the patron info window
                root.deiconify()  # Show the main window
            else:
                tk.messagebox.showerror("Error", "Please provide both the name and ID.")

        # Submit Button
        submit_button = tk.Button(patron_window, text="Submit", command=submit, fg="black")
        submit_button.pack(pady=10, padx=10, side=tk.BOTTOM)  # Position at the bottom with padding

        # Hide the main window while entering patron information
        root.withdraw()

    def main_window(self, root):
        # Set up the main window
        root.title("Library Management System")
        root.geometry("400x400")
        center_window(root, 400, 400)

        # Buttons
        self.display_button = tk.Button(root, text="Display Books", command=self.display_books, bg="lightblue",
                                        fg="black")
        self.display_button.pack(pady=10)

        self.lend_button = tk.Button(root, text="Lend a Book", command=self.lend_book, bg="lightgreen", fg="black")
        self.lend_button.pack(pady=10)

        self.add_button = tk.Button(root, text="Add a Book", command=self.add_book, bg="lightyellow", fg="black")
        self.add_button.pack(pady=10)

        self.return_button = tk.Button(root, text="Return a Book", command=self.return_book, bg="lightcoral",
                                       fg="black")
        self.return_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit, bg="gray", fg="white")
        self.quit_button.pack(pady=10)

    def display_books(self):
        self.library.display_books()

    def lend_book(self):
        book_title = self.simple_input("Lend a Book", "Enter the name of the book you want to lend:")
        book_to_lend = next((book for book in self.library.books if book.title == book_title), None)
        if book_to_lend:
            self.library.check_out(self.patron, book_to_lend)
        else:
            tk.messagebox.showerror("Not Found", "This book is not available in the library.")

    def add_book(self):
        # Create a new window for adding a book
        add_book_window = tk.Toplevel()
        add_book_window.title("Add a Book")
        add_book_window.geometry("300x350")
        center_window(add_book_window, 300, 350)
        add_book_window.configure(bg="lightblue")

        # Title Label and Entry
        title_label = tk.Label(add_book_window, text="Title:", anchor="w", bg="lightblue")
        title_label.pack(fill="x", padx=10, pady=5)
        title_entry = tk.Entry(add_book_window)
        title_entry.pack(fill="x", padx=10, pady=5)

        # Author Label and Entry
        author_label = tk.Label(add_book_window, text="Author:", anchor="w", bg="lightblue")
        author_label.pack(fill="x", padx=10, pady=5)
        author_entry = tk.Entry(add_book_window)
        author_entry.pack(fill="x", padx=10, pady=5)

        # ISBN Label and Entry
        isbn_label = tk.Label(add_book_window, text="ISBN:", anchor="w", bg="lightblue")
        isbn_label.pack(fill="x", padx=10, pady=5)
        isbn_entry = tk.Entry(add_book_window)
        isbn_entry.pack(fill="x", padx=10, pady=5)

        # Function to handle the "Enter" action
        def submit():
            book_title = title_entry.get()
            book_author = author_entry.get()
            book_isbn = isbn_entry.get()
            if book_title and book_author and book_isbn:
                new_book = Book(book_title, book_author, book_isbn)
                self.library.add_book(new_book)
                add_book_window.destroy()
            else:
                tk.messagebox.showerror("Error", "Please provide all the details.")

        # Enter Button
        submit_button = tk.Button(add_book_window, text="Enter", command=submit, fg="black")
        submit_button.pack(pady=10, padx=10, side=tk.BOTTOM)  # Position at the bottom with padding

    def return_book(self):
        book_title = self.simple_input("Return a Book", "Enter the name of the book you want to return:")
        book_to_return = next((book for book in self.patron.checked_out_books if book.title == book_title), None)
        if book_to_return:
            self.library.check_in(self.patron, book_to_return)
        else:
            tk.messagebox.showerror("Not Found", "This book was not checked out by you.")

    def simple_input(self, title, prompt):
        return simpledialog.askstring(title, prompt)


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
