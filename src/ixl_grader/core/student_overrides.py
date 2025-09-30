import pandas as pd
from typing import Optional, Dict, Tuple

from .persistence import get_local_storage


class StudentOverrides:
    """Manages student-specific grade minimum and smart score threshold overrides."""
    
    def __init__(self):
        self._overrides: pd.DataFrame | None = None
        self._local_storage = get_local_storage()
        # Load existing overrides from local storage on initialization
        self._load_from_local_storage()
    
    def _load_from_local_storage(self) -> None:
        """Load student overrides from local storage."""
        self._overrides = self._local_storage.load_student_overrides()
    
    def _save_to_local_storage(self) -> None:
        """Save current overrides to local storage."""
        self._local_storage.save_student_overrides(self._overrides)
    
    def import_overrides(self, csv_path: str) -> None:
        """Import student overrides from CSV file.
        
        Expected columns: Student ID, Smart Score Threshold, Minimum Grade
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Validate required columns
            required_columns = ["Student ID", "Smart Score Threshold", "Minimum Grade"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Clean and validate data
            df = self._clean_overrides_data(df)
            self._overrides = df
            
            # Save to local storage for persistence
            self._save_to_local_storage()
            
        except Exception as e:
            raise ValueError(f"Error importing student overrides: {str(e)}")
    
    def _clean_overrides_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate override data."""
        # Clean student IDs (similar to report cleaning)
        df["Student ID"] = (
            df["Student ID"].astype(str).str.lstrip("ID").astype(str).str.strip()
        )
        
        # Convert numeric columns and handle missing values
        df["Smart Score Threshold"] = pd.to_numeric(df["Smart Score Threshold"], errors="coerce")
        df["Minimum Grade"] = pd.to_numeric(df["Minimum Grade"], errors="coerce")
        
        # Remove rows with invalid data
        df = df.dropna(subset=["Student ID"])
        
        # Ensure thresholds and minimums are within valid ranges
        df.loc[df["Smart Score Threshold"] < 0, "Smart Score Threshold"] = None
        df.loc[df["Smart Score Threshold"] > 100, "Smart Score Threshold"] = None
        df.loc[df["Minimum Grade"] < 0, "Minimum Grade"] = None
        df.loc[df["Minimum Grade"] > 100, "Minimum Grade"] = None
        
        return df
    
    def set_override(self, student_id: str, smart_score_threshold: Optional[float] = None, 
                    minimum_grade: Optional[float] = None) -> None:
        """Set override for a specific student."""
        if self._overrides is None:
            self._overrides = pd.DataFrame(columns=["Student ID", "Smart Score Threshold", "Minimum Grade"])
        
        # Clean student ID
        student_id = str(student_id).lstrip("ID").strip()
        
        # Check if student already has overrides
        existing_idx = self._overrides[self._overrides["Student ID"] == student_id].index
        
        if len(existing_idx) > 0:
            # Update existing override
            if smart_score_threshold is not None:
                self._overrides.loc[existing_idx, "Smart Score Threshold"] = smart_score_threshold
            if minimum_grade is not None:
                self._overrides.loc[existing_idx, "Minimum Grade"] = minimum_grade
        else:
            # Add new override
            new_override = pd.DataFrame({
                "Student ID": [student_id],
                "Smart Score Threshold": [smart_score_threshold],
                "Minimum Grade": [minimum_grade]
            })
            self._overrides = pd.concat([self._overrides, new_override], ignore_index=True)
        
        # Save to local storage for persistence
        self._save_to_local_storage()
    
    def get_override(self, student_id: str) -> Tuple[Optional[float], Optional[float]]:
        """Get smart score threshold and minimum grade for a student.
        
        Returns:
            Tuple of (smart_score_threshold, minimum_grade), with None if not set
        """
        if self._overrides is None:
            return None, None
        
        # Clean student ID for lookup
        student_id = str(student_id).lstrip("ID").strip()
        
        student_row = self._overrides[self._overrides["Student ID"] == student_id]
        if len(student_row) == 0:
            return None, None
        
        row = student_row.iloc[0]
        smart_score_threshold = row["Smart Score Threshold"] if pd.notna(row["Smart Score Threshold"]) else None
        minimum_grade = row["Minimum Grade"] if pd.notna(row["Minimum Grade"]) else None
        
        return smart_score_threshold, minimum_grade
    
    def remove_override(self, student_id: str) -> None:
        """Remove override for a specific student."""
        if self._overrides is None:
            return
        
        student_id = str(student_id).lstrip("ID").strip()
        self._overrides = self._overrides[self._overrides["Student ID"] != student_id]
        
        # Save to local storage for persistence
        self._save_to_local_storage()
    
    def get_all_overrides(self) -> pd.DataFrame:
        """Get all student overrides as a DataFrame."""
        if self._overrides is None:
            return pd.DataFrame(columns=["Student ID", "Smart Score Threshold", "Minimum Grade"])
        return self._overrides.copy()
    
    def has_overrides(self) -> bool:
        """Check if any overrides are loaded."""
        return self._overrides is not None and len(self._overrides) > 0
    
    def export_overrides(self, output_path: str) -> None:
        """Export current overrides to CSV file."""
        if self._overrides is None or len(self._overrides) == 0:
            raise ValueError("No overrides to export")
        
        self._overrides.to_csv(output_path, index=False)
    
    def clear_all_overrides(self) -> None:
        """Clear all student overrides from both memory and local storage."""
        self._overrides = None
        self._local_storage.clear_student_overrides()