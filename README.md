# 📱 Phones Comparison Platform

## 🌟 Overview

This project is a web-based application that allows users to explore, filter, compare, and manage a shopping cart for phones scraped from multiple online web stores. The application provides features such as currency conversion, PDF export, and real-time cart updates. The backend is powered by Flask and SQLite, while the frontend is built with HTML, CSS, and JavaScript.
website like -> https://omarelsehly.pythonanywhere.com/

---

# ✨ Features
 📊 Total Features Overview
 The platform includes 14 main features across different areas, with hosting, categorized as follows:

### Data Preparation: 6 features
### Website Functionalities: 8 features
### Total 14 features.

## Data Preparation
1. **Web Scraping**: Extracting phone data from multiple web stores to collect raw data efficiently.
2. **CSV Export**: Storing cleaned and organized data into CSV files for backup and easy transfer.

   #### In this stage, The data were scrapped from the websites class by class in the div blocks. As shown in the image
    ![image](https://github.com/user-attachments/assets/9866b369-a5ef-4571-8ba3-76bc8c4cbebd)
   #### Developing Python code to extract the data
   ![image](https://github.com/user-attachments/assets/935a218f-ef0e-455c-aef6-fc20f0f244f3)
   #### Saving all the scrapping data into CSV files
   ![image](https://github.com/user-attachments/assets/d540214b-4e10-4384-b41c-e40cfe11c93d)
   
3. **Data Cleaning**: Handling missing values, fixing inconsistencies, and standardizing formats to ensure data accuracy and reliability.
    ![image](https://github.com/user-attachments/assets/0e4a30ed-f730-46b5-9a96-d61a5bedcf37)
    ![image](https://github.com/user-attachments/assets/eff6e036-825b-4916-8716-8760e0263746)
4. **Data Organization**: Categorizing data into structured tables for easier database integration and queries.
    ![image](https://github.com/user-attachments/assets/63b76854-36c2-4527-ae02-a4caa4fbf2ee)
5. **Adding Unique IDs**: Assigning unique IDs to phones for maintaining relationships across different data tables.
    ![image](https://github.com/user-attachments/assets/d1ed7f94-d022-4572-84e0-e5bb9e8c39d9)
6. **Database Creation**: Importing the CSV data into an SQLite database with proper relationships for structured storage and retrieval.
   ![image](https://github.com/user-attachments/assets/00063c94-4178-4871-a990-a87f00e7506b)

### Website Functionalities
1. **Homepage**: Displays a list of all available phones with pagination and highlights for new or featured items.
2. **Search Functionality**: Enables users to search phones by name or keyword for quick access to desired models.
3. **Filter Functionality**: Allows users to filter phones by criteria such as:
   - Brand: Focus on phones from specific manufacturers.
   - Webstore: View availability on a preferred online store.
   - Price range: Find phones within a budget-friendly range.
4. **Phone Details Page**: Shows detailed specifications, prices, and brand information for a selected phone, including promotions and savings.
5. **Comparison Page**:
   - Compare up to 4 phones side by side.
   - Highlight specifications, prices, and promotions for informed decision-making.
6. **Shopping Cart Page**:
   - Add or remove phones seamlessly.
   - View the total price with a breakdown of items.
   - Perform currency conversion specifically for eBay listings (e.g., USD → EGP).
7. **PDF Export for Comparison**:
   - Generate a downloadable PDF comparison report of selected phones for offline viewing.
8. **Dynamic Cart Management**:
   - Update cart contents in real time using AJAX for a smoother user experience.

---

## Technical Details

### Backend
- **Framework**: Flask
- **Database**: SQLite
- **Data Handling**: Python for cleaning and organizing data

### Frontend
- **HTML**: Structure of the web pages
- **CSS**: Styling for a user-friendly interface
- **JavaScript**: Dynamic cart updates and user interactions

### Key Libraries
- **Flask**: For routing and backend logic
- **SQLAlchemy**: ORM for database interactions
- **WeasyPrint**: PDF generation for comparison reports
- **jQuery**: AJAX requests for cart updates

---

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/project.git
   ```
2. Navigate to the project directory:
   ```bash
   cd project
   ```
3. Install required Python packages:
4. Run the application:
   ```bash
   python app.py
   ```
5. Open the application in your browser at `http://127.0.0.1:5000/`.

---



## Future Improvements
1. Add user authentication for personalized experiences.
2. Enable real-time currency conversion with API integration.
3. Improve the UI with modern frameworks like React or Vue.js.
4. Enhance filtering options with more criteria.

---


## Acknowledgments
- **Flask**: For its simplicity and flexibility.
- **WeasyPrint**: For enabling seamless PDF generation.
- **SQLite**: For lightweight database management.
- **jQuery**: For facilitating AJAX operations.

