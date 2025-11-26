import os
import glob
import json
import pandas as pd
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SYLLABI_DIR = "syllabi"
OUTPUT_FILE = "syllabus_analysis.csv"
MODEL = "gpt-5.1-mini"

# Initialize OpenAI client
# Expects OPENAI_API_KEY in environment variables
client = OpenAI()

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def analyze_syllabus(text):
    prompt = """
    You are an assistant that analyzes course syllabi.
    Extract the following information from the syllabus text provided below:
    1. List of assignments/assessments that contribute to the final grade.
    2. For each assignment, determine:
       - Name: Name of the assignment.
       - Weight: Percentage of the final grade (0-100). If not explicitly stated, estimate or distribute remaining percentage equally.
       - Type: 'Take Home' or 'In Class'. 'Take Home' includes papers, projects, homework. 'In Class' includes exams, quizzes, participation (unless specified otherwise).
       - AI_Solvable: A boolean (true/false) indicating if a generative AI could plausibly complete this assignment with high quality.
       - AI_Solvable_Percentage: Estimate the percentage (0-100) of this assignment that AI could complete.
    3. AI_Policy_Note: Extract any specific text regarding the use of AI (ChatGPT, etc.) in the course. If none, return "None".

    Return the output strictly as a JSON object with the following structure:
    {
      "assignments": [
        {
          "name": "Midterm Exam",
          "weight": 30,
          "type": "In Class",
          "ai_solvable": false,
          "ai_solvable_percentage": 10
        },
        ...
      ],
      "ai_policy_note": "Students are not allowed to use AI..."
    }
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text[:20000]} # Truncate to avoid token limits if necessary, though 5.1-mini should handle large context.
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None

def main():
    results = []
    
    # Find all PDF files recursively
    pdf_files = glob.glob(os.path.join(SYLLABI_DIR, "**/*.pdf"), recursive=True)
    print(f"Found {len(pdf_files)} syllabi to analyze.")
    
    for i, pdf_path in enumerate(pdf_files):
        print(f"Processing {i+1}/{len(pdf_files)}: {pdf_path}")
        
        # Parse filename for metadata
        # Format: syllabi/2024/Spring/2024_Spring_GOV_679HB_37605.pdf
        parts = pdf_path.split('/')
        if len(parts) >= 4:
            year = parts[1]
            semester = parts[2]
            filename = parts[-1]
        else:
            year = "Unknown"
            semester = "Unknown"
            filename = os.path.basename(pdf_path)

        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
            
        analysis = analyze_syllabus(text)
        if analysis:
            assignments = analysis.get("assignments", [])
            ai_policy = analysis.get("ai_policy_note", "None")
            
            # Calculate total AI solvable grade
            total_ai_score = 0
            for asm in assignments:
                weight = asm.get("weight", 0)
                solvable_pct = asm.get("ai_solvable_percentage", 0)
                total_ai_score += weight * (solvable_pct / 100.0)
            
            results.append({
                "Filename": filename,
                "Year": year,
                "Semester": semester,
                "AI_Solvable_Grade_Percent": round(total_ai_score, 2),
                "AI_Policy": ai_policy,
                "Assignments_JSON": json.dumps(assignments)
            })
            
    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Analysis complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
