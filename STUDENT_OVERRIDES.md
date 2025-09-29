# Student Overrides Implementation

This implementation adds support for student-based grade minimum overrides and custom smart score thresholds as designated by 504 and IEP plans.

## Features Implemented

### 1. StudentOverrides Class (`src/ixl_grader/core/student_overrides.py`)
- Manages student-specific grade minimums and smart score thresholds
- CSV import/export functionality with proper data validation
- Individual override management (add, edit, remove)
- Student ID cleaning (removes "ID" prefix automatically)

### 2. Enhanced Report Class (`src/ixl_grader/core/report.py`)
- Updated `grade()` method to apply student-specific overrides
- New methods for managing student overrides:
  - `import_student_overrides(csv_path)`
  - `set_student_override(student_id, threshold, minimum)`
  - `get_student_override(student_id)`
  - `has_student_overrides()`

### 3. New UI Components

#### Student Overrides Uploader (`src/ixl_grader/ui/components/student_overrides.py`)
- File uploader for CSV with student overrides
- Preview of loaded overrides
- Format documentation and examples
- Input validation and error handling

#### Individual Student Override Editor
- Form to add/edit overrides for specific students
- Support for partial overrides (threshold-only or minimum-only)
- Real-time validation

### 4. Enhanced Sample Calculations
- Shows how overrides affect specific students
- Displays override details in calculations
- Summary of loaded overrides

### 5. Session State Management (`src/ixl_grader/ui/session/student_overrides.py`)
- Tracks override upload status
- Handles override file processing
- Integrates with existing session management

## CSV Format

The student overrides CSV file must contain these exact headers:
```csv
Student ID,Smart Score Threshold,Minimum Grade
12345,70,60
67890,,50
11111,85,
```

- **Student ID**: Required. Student identifier (e.g., "12345" or "ID12345")
- **Smart Score Threshold**: Optional. Custom threshold for this student (0-100)
- **Minimum Grade**: Optional. Minimum grade for this student (0-100)
- Empty cells are allowed for optional fields

## Grading Logic

The enhanced grading algorithm works as follows:

1. **Get Override Data**: For each student, check if overrides exist
2. **Apply Custom Threshold**: Use student's custom threshold if set, otherwise use global threshold
3. **Calculate Grade**: `grade = 100 * min(smart_score, threshold) / threshold`
4. **Apply Minimum Grade**: If calculated grade < minimum_grade, set grade = minimum_grade

### Examples

With global threshold of 80%:

| Student | Smart Score | Override Threshold | Minimum Grade | Final Grade | Explanation |
|---------|-------------|-------------------|---------------|-------------|-------------|
| 12345 | 85% | 70% | 60% | 100% | 85/70 * 100 = 121%, capped at 100% |
| 67890 | 60% | (none) | 50% | 75% | 60/80 * 100 = 75%, above minimum |
| 22222 | 40% | 80% | 70% | 70% | 40/80 * 100 = 50%, raised to minimum 70% |
| 44444 | 30% | 60% | 55% | 55% | 30/60 * 100 = 50%, raised to minimum 55% |

## Benefits

1. **504/IEP Compliance**: Supports accommodations requiring different grading standards
2. **Flexibility**: Partial overrides allow setting only threshold OR minimum grade
3. **Transparency**: Clear display of how overrides affect calculations
4. **Ease of Use**: CSV import for bulk management, UI editor for individual changes
5. **Backward Compatibility**: Students without overrides use existing global settings

## File Structure

```
src/ixl_grader/
├── core/
│   ├── report.py (enhanced)
│   └── student_overrides.py (new)
└── ui/
    ├── components/
    │   ├── student_overrides.py (new)
    │   └── sample_calculations.py (enhanced)
    ├── session/
    │   ├── student_overrides.py (new)
    │   ├── file_upload.py (enhanced)
    │   └── __init__.py (enhanced)
    └── app.py (enhanced)
```

## Testing

The implementation includes:
- Manual verification script (`verify_grading_logic.py`)
- UI component import tests
- Sample CSV files for testing
- Comprehensive error handling and validation

All changes are minimal and surgical, maintaining backward compatibility while adding the requested functionality.