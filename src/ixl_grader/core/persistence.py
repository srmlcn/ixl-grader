import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd


class LocalStorage:
    """
    A minimal persistence layer that mimics database functionality using local file storage.
    This replaces session storage with persistent local storage.
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize local storage with a directory for persistence."""
        if storage_dir is None:
            # Use user's home directory for persistence
            home_dir = Path.home()
            storage_dir = home_dir / ".ixl_grader" / "data"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths for different data types
        self.overrides_file = self.storage_dir / "student_overrides.json"
        self.settings_file = self.storage_dir / "settings.json"
    
    def save_student_overrides(self, overrides_df: pd.DataFrame) -> None:
        """Save student overrides to local storage."""
        try:
            # Convert DataFrame to JSON-serializable format
            if overrides_df is not None and len(overrides_df) > 0:
                data = overrides_df.to_dict('records')
                with open(self.overrides_file, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                # Remove file if no overrides
                if self.overrides_file.exists():
                    self.overrides_file.unlink()
        except Exception as e:
            print(f"Error saving student overrides: {e}")
    
    def load_student_overrides(self) -> Optional[pd.DataFrame]:
        """Load student overrides from local storage."""
        try:
            if not self.overrides_file.exists():
                return None
            
            with open(self.overrides_file, 'r') as f:
                data = json.load(f)
            
            if not data:
                return None
            
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error loading student overrides: {e}")
            return None
    
    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Save application settings to local storage."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_settings(self) -> Dict[str, Any]:
        """Load application settings from local storage."""
        try:
            if not self.settings_file.exists():
                return {}
            
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {}
    
    def clear_student_overrides(self) -> None:
        """Clear all student overrides from local storage."""
        try:
            if self.overrides_file.exists():
                self.overrides_file.unlink()
        except Exception as e:
            print(f"Error clearing student overrides: {e}")
    
    def clear_all_data(self) -> None:
        """Clear all persisted data."""
        try:
            if self.overrides_file.exists():
                self.overrides_file.unlink()
            if self.settings_file.exists():
                self.settings_file.unlink()
        except Exception as e:
            print(f"Error clearing all data: {e}")
    
    def has_student_overrides(self) -> bool:
        """Check if student overrides exist in local storage."""
        return self.overrides_file.exists()


# Global instance for the application
_local_storage = LocalStorage()


def get_local_storage() -> LocalStorage:
    """Get the global local storage instance."""
    return _local_storage