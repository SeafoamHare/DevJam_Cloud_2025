# # Import the Vertex AI SDK
# import vertexai
# from vertexai.generative_models import GenerativeModel

# # Replace with your project ID and location
# PROJECT_ID = "devjam-cloud-2025"
# LOCATION = "us-central1"  # Or another supported region like "us-east4"

# # Initialize Vertex AI
# vertexai.init(project=PROJECT_ID, location=LOCATION)

# def generate_book_recommendation(borrowed_book_titles: list[str], available_book_titles: list[str]) -> list[str]:
#     """Generates book recommendations based on borrowed books and available books using Gemini."""
#     try:
#         # Load Gemini model
#         model = GenerativeModel("gemini-2.0-flash-001") # Using gemini-1.0-pro as it's a generally available model

#         borrowed_titles_str = ", ".join(borrowed_book_titles)
#         available_titles_str = ", ".join(available_book_titles)

#         prompt = f"""Based on the user's past borrowed books: [{borrowed_titles_str}], \
# and the list of currently available books in the library: [{available_titles_str}], \
# please recommend up to 3 books from the available list that the user might enjoy.
# Return only the titles of the recommended books, each on a new line.
# If no relevant recommendations can be made from the available list, return an empty response or a polite message indicating so."""

#         response = model.generate_content(prompt)
        
#         # Extracting titles, assuming each recommended title is on a new line
#         recommended_titles = [title.strip() for title in response.text.split('\\n') if title.strip() and title.strip() in available_book_titles]
#         return recommended_titles
#     except Exception as e:
#         print(f"An error occurred during recommendation generation: {e}")
#         return []

# if __name__ == "__main__":
#     from app.dao.books_dao import BookDAO
#     from app.dao.borrow_dao import BorrowDAO
#     from app.dao.user_dao import UserDAO # Assuming you might need user details

#     # Initialize DAOs
#     book_dao = BookDAO()
#     borrow_dao = BorrowDAO()
#     user_dao = UserDAO() # If you need to fetch a specific user's borrows

#     # --- Example: Fetching data for a specific user (e.g., user_id = 1) ---
#     example_user_id = 1 # Replace with a valid user ID from your database

#     # Fetch borrowed book titles for the user
#     user_borrow_records = borrow_dao.get_user_borrow_records(example_user_id)
#     example_borrowed_titles = []
#     if user_borrow_records:
#         for record in user_borrow_records:
#             book = book_dao.get_book(record["book_id"])
#             if book:
#                 example_borrowed_titles.append(book["title"])
#     else:
#         print(f"No borrow history found for user {example_user_id}.")

#     # Fetch all available book titles from the library
#     all_db_books = book_dao.get_books(limit=1000) # Fetch a good number of books
#     example_available_titles = [b["title"] for b in all_db_books if b.get("available_copies", 0) > 0]

#     if not example_available_titles:
#         print("No available books in the library to recommend from.")
    
#     if example_borrowed_titles and example_available_titles:
#         print(f"Generating recommendations for user {example_user_id}...")
#         print(f"Borrowed books: {', '.join(example_borrowed_titles)}")
#         print(f"Available books in library: {len(example_available_titles)}")
        
#         recommendations = generate_book_recommendation(example_borrowed_titles, example_available_titles)
        
#         if recommendations:
#             print("\nRecommended for you:")
#             for title in recommendations:
#                 print(f"- {title}")
#         else:
#             print("\nSorry, we couldn't find specific recommendations based on your history from the available books right now.")
#     elif not example_borrowed_titles:
#         print("Cannot generate recommendations without borrowing history.")

#     # Close DAO connections if necessary (depends on your DAO implementation)
#     # book_dao.close()
#     # borrow_dao.close()
#     # user_dao.close()
