# Sample CSV Files for IXL Grader

This directory contains sample CSV files to demonstrate the student overrides functionality.

## Files

### sample_report.csv
Example IXL report file with student assignments and smart scores.

### sample_student_overrides.csv
Example student overrides file showing how to specify custom smart score thresholds and minimum grades for students with 504/IEP accommodations.

## Student Overrides Format

The student overrides CSV file must contain these exact column headers:
- **Student ID**: Student identifier (e.g., "12345" or "ID12345")
- **Smart Score Threshold**: Custom smart score threshold for this student (0-100, optional)
- **Minimum Grade**: Minimum grade for this student (0-100, optional)

### Example Scenarios

1. **Student 12345**: Custom threshold of 70% and minimum grade of 60%
   - If smart score is 85%, grade = 100% (85/70 * 100 = 121, capped at 100%)
   - If smart score is 50%, grade = 71% (50/70 * 100), but minimum is 60%, so final grade = 71%

2. **Student 67890**: Only minimum grade of 50% (uses global threshold)
   - Uses the global smart score threshold for calculation
   - Final grade cannot be lower than 50%

3. **Student 22222**: Custom threshold of 80% and minimum grade of 70%
   - Uses 80% as threshold instead of global setting
   - Final grade cannot be lower than 70%

4. **Student 44444**: Custom threshold of 60% and minimum grade of 55%
   - Uses 60% as threshold (more lenient than typical 80%)
   - Final grade cannot be lower than 55%

## Usage

1. Upload your IXL report CSV file first
2. Upload the student overrides CSV file 
3. Set your global grading parameters
4. Click "Grade Assignments" to apply both global settings and student-specific overrides