🎓 College Recommendation System
This project is a College Recommendation System built using Flask and Machine Learning techniques.
It helps users find the best-fit colleges based on their selected course, location, and priority preferences like NIRF rank, placement rates, fees, and cost-efficiency.

📚 Features
Search for colleges based on course and city.

Sort recommendations based on:

NIRF Ranking

Annual Fees

Placement Percentage

Cost Efficiency

Content-based filtering using TF-IDF and Cosine Similarity.

Dynamic dropdowns for easy course and location selection.

Top 10 most relevant colleges displayed.

Built with:

Flask (Python Web Framework)

Pandas, NumPy for data handling

scikit-learn for similarity calculation

Deployable on Render / Heroku / any cloud platform.

🛠️ Technologies Used
Python

Flask

Pandas

NumPy

Scikit-learn

Gunicorn (for production server)

🚀 How It Works
User selects a course and/or location.

The system filters the college dataset accordingly.

It then calculates similarity between user preferences and college data.

Results are sorted based on the selected priority (Rank, Fees, Placement, etc.).

Top recommendations are shown to the user.

📂 Project Structure
plaintext
Copy
Edit
V5/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/ (if needed for CSS/JS/images)
└── College_data.csv
📈 Future Improvements
Add user authentication (login/signup).

Save user search history.

Add more filters (e.g., stream, college type, government/private).

Improve UI with Bootstrap or TailwindCSS.

Support for multiple recommendation algorithms.

🙌 Contribution
Feel free to fork this project, raise issues, or submit pull requests!
