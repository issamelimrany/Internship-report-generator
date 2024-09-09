# Internship Report Generator

This project is a web application that generates detailed internship reports using Google's Gemini AI model. It allows users to input their internship details and receive a LaTeX-formatted report.

## Features

- User-friendly web interface for inputting internship details
- Integration with Google's Gemini AI model for report generation
- Real-time progress updates during report generation
- Downloadable LaTeX file output
- Supports multiple languages (English and French)

## Technologies Used

- Backend:
  - Python
  - Flask
  - Google Generative AI (Gemini 1.5 Pro)
- Frontend:
  - HTML
  - JavaScript
  - Tailwind CSS

## Setup and Installation

1. Clone the repository
2. Install the required Python packages:
   ```pip install flask flask-wtf google-generativeai```
4. Run the Flask application:
   ```python app.py```

## Usage

1. Open the application in a web browser
2. Fill in the internship details form
3. Enter your Google AI API key
4. Click "Generate Report"
5. Wait for the report to be generated
6. Download the LaTeX file

## File Structure

- `app.py`: Main Flask application
- `templates/index.html`: HTML template for the web interface


