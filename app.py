from flask import Flask, render_template, request
import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load and clean the dataset
df = pd.read_csv("College_data.csv")

# Important columns to clean
important_columns = ['Course', 'Courses', 'City']

for col in important_columns:
    if col in df.columns:
        df[col] = df[col].fillna('').astype(str).str.strip()

# Remove duplicates
df = df.drop_duplicates()

# Column mapping
course_col = 'Course' if 'Course' in df.columns else 'Courses'
location_col = 'City'

priority_columns = {
    'nirf_rank': 'Rank',
    'annual_fees': 'Fees',
    'placement_percent': 'Placement',
    'cost_efficiency_score': 'Cost_Efficiency_Score'
}

# Dropdown lists
course_list = sorted(set(course.strip() for sublist in df[course_col].dropna().str.split(',') for course in sublist))
location_list = sorted(df[location_col].dropna().unique().tolist())

course_list.insert(0, 'All')
location_list.insert(0, 'All')

priority_options = {
    'nirf_rank': 'NIRF Rank',
    'annual_fees': 'Annual Fees',
    'placement_percent': 'Placement %',
    'cost_efficiency_score': 'Cost Efficiency Score'
}

# Function to calculate content-based similarity
def calculate_similarity(user_profile, df, course_col, location_col):
    df['combined'] = df[course_col].fillna('') + ' ' + df[location_col].fillna('')
    
    if df['combined'].str.strip().eq('').all():
        df['similarity'] = 0
        return df

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined'])

    user_profile_vector = vectorizer.transform([user_profile])
    cosine_sim = cosine_similarity(user_profile_vector, tfidf_matrix)

    df['similarity'] = cosine_sim.flatten()
    
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    no_results_message = None

    if request.method == 'POST':
        selected_course = request.form.get('course')
        selected_location = request.form.get('location')
        selected_priority = request.form.get('priority')

        user_profile = ""
        if selected_course and selected_course != 'All':
            user_profile += selected_course.strip() + " "
        if selected_location and selected_location != 'All':
            user_profile += selected_location.strip()

        # Start with full DataFrame
        filtered_df = df.copy()

        # Apply course filter
        if selected_course and selected_course != 'All':
            filtered_df = filtered_df[filtered_df[course_col].str.contains(selected_course, case=False, na=False)]

        # Apply location filter
        if selected_location and selected_location != 'All':
            filtered_df = filtered_df[filtered_df[location_col].str.lower() == selected_location.lower()]

        # Check if any college remains after filtering
        if not filtered_df.empty:
            # Calculate similarity
            filtered_df = calculate_similarity(user_profile, filtered_df, course_col, location_col)

            # Apply priority-based sorting if selected
            if selected_priority and selected_priority in priority_columns:
                priority_col = priority_columns[selected_priority]
                
                if priority_col in filtered_df.columns:
                    ascending_order = True if selected_priority in ['nirf_rank', 'annual_fees'] else False
                    
                    filtered_df = filtered_df.sort_values(
                        by=[priority_col, 'similarity'],
                        ascending=[ascending_order, False]
                    )
                else:
                    # fallback to similarity if priority column not available
                    filtered_df = filtered_df.sort_values(by='similarity', ascending=False)
            else:
                # Default sort by similarity
                filtered_df = filtered_df.sort_values(by='similarity', ascending=False)

            # Select top 10
            results = filtered_df.head(10).to_dict(orient='records')
        else:
            no_results_message = "No colleges found matching your criteria."

    return render_template('index.html',
                           course_list=course_list,
                           location_list=location_list,
                           priority_options=priority_options,
                           results=results,
                           no_results_message=no_results_message)

if __name__ == '__main__':
    app.run(debug=True, port=5001)