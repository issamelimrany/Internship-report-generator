from flask import Flask, request, render_template, send_file, jsonify, Response, stream_with_context
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length
import os
from werkzeug.utils import secure_filename
import google.generativeai as genai
import json


# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'temp_files'

class InternshipForm(FlaskForm):
    api_key = StringField('API Key', validators=[DataRequired()])
    language = SelectField('Language', choices=[('en', 'English'), ('fr', 'French')], validators=[DataRequired()])
    intern_name = StringField('Intern Name', validators=[DataRequired(), Length(max=100)])
    start_date = DateField('Internship Start Date', validators=[DataRequired()])
    end_date = DateField('Internship End Date', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    intern_role = StringField('Intern Role', validators=[DataRequired(), Length(max=100)])
    project_overview = TextAreaField('Project Overview', validators=[DataRequired(), Length(max=500)])
    tools_technologies = StringField('Tools/Technologies Used', validators=[DataRequired(), Length(max=200)])
    key_achievements = TextAreaField('Key Achievements', validators=[DataRequired(), Length(max=500)])

def generate_report(intern_name, start_date, end_date, company_name, intern_role, project_overview, tools_technologies, key_achievements, language):
    try:
        prompt = f"""
        Generate a detailed internship report based on the following information:
        Intern Name: {intern_name}
        Internship Period: {start_date} to {end_date}
        Company: {company_name}
        Intern Role: {intern_role}
        Project Overview: {project_overview}
        Tools/Technologies Used: {tools_technologies}
        Key Achievements: {key_achievements}
        
        The report should include:
        1. Introduction
        2. Company Overview
        3. Internship Role and Responsibilities
        4. Project Description
        5. Technical Details
        6. Development Process
        7. Challenges Faced and Solutions
        8. Key Achievements and Outcomes
        9. Skills Acquired
        10. Conclusion and Future Prospects
        
        Please format the output with appropriate section headers.
        
        Provide this report directly in LaTeX format:

        Please ensure proper LaTeX formatting, including:
        - Document class and necessary packages
        - Title page
        - Table of contents
        - Sections and subsections
        - Proper handling of special characters
        
        Make the report as detailed as possible, preferably around 20 to 30 pages, the more the better.
        All this in {language} language.
        """
        
        response = model.generate_content(prompt)
        latex_code = response.text.strip()

        return latex_code
    except Exception as e:
        app.logger.error(f"Error generating report: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InternshipForm()
    return render_template('index.html', form=form)

@app.route('/generate-report', methods=['POST'])
def generate_report_route():
    data = request.json
    api_key = data.get('api_key')
    genai.configure(api_key=api_key)
    intern_name = data.get('intern_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    company_name = data.get('company_name')
    intern_role = data.get('intern_role')
    project_overview = data.get('project_overview')
    tools_technologies = data.get('tools_technologies')
    key_achievements = data.get('key_achievements')
    language = data.get('language')

    def generate():
        yield "data: Initializing report generation...\n\n"
        yield "data: Analyzing input data...\n\n"
        yield "data: Crafting report structure...\n\n"
        yield "data: If you're lucky, it won't take more than 2 minutes...\n\n"

        latex = generate_report(intern_name, start_date, end_date, company_name, intern_role, project_overview, tools_technologies, key_achievements, language)
        
        if latex:
            yield "data: Finalizing report...\n\n"
            yield f"data: {json.dumps({'success': True, 'latex': latex})}\n\n"
        else:
            yield f"data: {json.dumps({'success': False, 'error': 'Failed to generate report'})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/download-latex', methods=['POST'])
def download_latex():
    latex_content = request.json.get('latex')
    if not latex_content:
        return jsonify({'success': False, 'error': 'No LaTeX content provided'}), 400
    
    filename = f"internship_report_{secure_filename(request.json.get('company_name', 'company'))}.tex"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)