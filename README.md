# 📱 Phones Comparison Platform

## 🌟 Overview

This project is a web-based application that allows users to explore, filter, compare, and manage a shopping cart for phones scraped from multiple online web stores. The application provides features such as currency conversion, PDF export, and real-time cart updates. The backend is powered by Flask and SQLite, while the frontend is built with HTML, CSS, and JavaScript.
#### website link -> https://omarelsehly.pythonanywhere.com/
![image](https://github.com/user-attachments/assets/1120922c-d337-4c59-bf1b-36aa680b19e7)


---

# ✨ Features
 📊 Total Features Overview
 The platform includes 14 main features across different areas, with hosting, categorized as follows:

### Data Preparation: 6 features
### Website Functionalities: 9 features
### Total 15 features.

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
8. **Error Handling**
   - Generate a downloadable PDF comparison report of selected phones for offline viewing using the WeasyPrint library.
   - Also, return ``` No phone selected for comparison ``` when there is no phone to export as pdf.
     ```
     @app.route('/export_comparison', methods=['GET'])
     def export_comparison():
         # Check if compare list exists in the session
         if 'compare_list' not in session or len(session['compare_list']) == 0:
             return "No phones selected for comparison.", 400
         # Retrieve the phone details for the comparison
         phone_ids = session['compare_list']
         phones = Info.query.filter(Info.id.in_(phone_ids)).all()
         phone_details = []
         for phone in phones:
             details = Details.query.filter_by(details_id=phone.id).first()
             price = Price.query.filter_by(price_id=phone.id).first()
             brand = Brand.query.filter_by(brand_id=phone.id).first()
             rating = Rating.query.filter_by(ratings_id=phone.id).first()
             phone_details.append({
                 'phone': phone,
                 'details': details,
                 'price': price,
                 'brand': brand,
                 'rating': rating
             })
         html_content = render_template('compare.html', phone_details=phone_details, for_pdf=True)
         css_path = os.path.join(basedir, 'static', 'pdf_styles.css')
         try:
             pdf_css = CSS(filename=css_path)
         except FileNotFoundError:
             return "CSS file not found. Please ensure the static/pdf_styles.css file exists.", 500
         # Generate the PDF using WeasyPrint with the custom CSS
         pdf = HTML(string=html_content).write_pdf(stylesheets=[pdf_css])
         response = make_response(pdf)
         response.headers['Content-Type'] = 'application/pdf'
         response.headers['Content-Disposition'] = 'attachment; filename=comparison.pdf'
         return response
     ```
9. **Dynamic Cart Management**:
   - Update cart contents in real time using AJAX 
       #### Remove an item from the cart using a POST AJAX request in ``` cart.html ``` to /remove_from_cart.
       ```
       document.querySelectorAll('.remove-button').forEach(button => {
                button.addEventListener('click', () => {
                    const phoneId = button.getAttribute('data-phone-id');
        
                    fetch('/remove_from_cart', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ phone_id: phoneId }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            button.closest('.cart-item').remove();
                            location.reload(); // Reload to update total price
                        } else {
                            alert(data.error);
                        }
                    });
                });
            });
       ```
     #### The AJAX request targets the /remove_from_cart route in ```app.py```.
     ```
     @app.route('/remove_from_cart', methods=['POST'])
     def remove_from_cart():
         data = request.json
         phone_id = data.get('phone_id')
   
       if not phone_id:
           return jsonify({'error': 'Phone ID is required'}), 400
   
       # Ensure cart exists in session
       if 'cart' not in session:
           session['cart'] = []
   
       cart = session['cart']
   
       if phone_id in cart:
           cart.remove(phone_id)
           session['cart'] = cart
           session.modified = True
           return jsonify({'success': True})
       else:
           return jsonify({'error': 'Phone not found in cart'}), 400
     ```
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

