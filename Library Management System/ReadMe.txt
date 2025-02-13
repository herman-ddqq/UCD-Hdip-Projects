# Library Management System

## Overview
The **Library Management System** is a Python-based application developed using Object-Oriented Programming (OOP) principles. It allows users to manage a collection of books, perform searches, update book details, and analyze book data.

## Features
### Book Management
- Create and manage **Book** objects with:
  - Title
  - Author
  - Year of Publication
  - Genres
- Load books from a file and save books to a file
- Update book details (author, year, genres)
- Remove books by title

### Library Operations
- Store and manage a collection of books in a **Library** class
- Search for books by:
  - Title
  - Author
  - Year
  - Genre
- Retrieve book statistics:
  - Number of books per author
  - Most published author
- Suggest similar books based on:
  - Same author
  - Shared genres

### Data Analysis & Visualization
- Generate a **bar chart** using Matplotlib to visualize book count per author
- Display search results and analytics in a structured format

## Usage
### Running the Program
```bash
python library_management.py
```
Or, if using Jupyter Notebook:
```python
%run library_management.py
```

### File Handling
- Books are stored in a text file in the format:
  ```
  Title, Author, Year, [Genre1, Genre2, ...]
  ```
- The system can read from and write to the file while preserving the correct format.

### Example Operations
1. **Add a new book**
2. **Search for books** by author, title, year, or genre
3. **Update book details**
4. **Remove a book** from the library
5. **Generate and display analytics**

## Software Design Principles
- **Encapsulation**: Data attributes are managed within their respective classes
- **Composition**: The `Library` class manages multiple `Book` objects
- **Modular Code**: Separate functions handle different responsibilities
- **Error Handling**: Ensures file handling and input operations are robust

## Future Enhancements
- Implement a **GUI interface** for user-friendly interaction
- Support **exporting reports** to CSV or JSON format
- Enhance **recommendation algorithms** for better book suggestions

---
Developed by Herman Dolhyi as part of **UCD HDip in Computer Science** coursework.

