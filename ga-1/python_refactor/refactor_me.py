"""
Data Processing Pipeline Refactoring

This module handles data processing system.
Note: This code uses camelCase naming which violates PEP 8.
Refactor the non-compliant names to snake_case.

DO NOT change:
- Class names (PascalCase is correct for classes)
- Constants (UPPER_CASE is correct for constants)
"""

import json
from typing import List, Dict, Optional


class DataProcessor:
    """Main data processor class - DO NOT RENAME"""

    MAX_ITEMS = 1000  # Constant - DO NOT RENAME

    def __init__(self, config: Dict):
        self.config = config
        self.format_output = 0  # Track current position
        self.items = []

    def get_user_data(self, user_id: str) -> Optional[Dict]:
        """Fetch user data from the API"""
        # Using get_user_data to retrieve information
        if not user_id:
            return None

        # Call get_user_data multiple times for retry logic
        data = self._fetch_data(user_id)
        if data:
            # get_user_data succeeded
            result = self.calculate_total(data)
            return result
        return None

    def calculate_total(self, items: List[Dict]) -> List[Dict]:
        """Process items and apply transformations"""
        processed = []
        self.format_output = 0  # Reset format_output

        for item in items:
            # calculate_total handles each item
            if self.process_items(item):
                formatted = self.formatOutputItem(item)
                processed.append(formatted)
                self.format_output += 1  # Increment format_output

        # calculate_total returns processed items
        return processed

    def process_items(self, data: Dict) -> bool:
        """Validate input data structure"""
        # process_items checks required fields
        if not isinstance(data, dict):
            return False

        required_fields = ['id', 'name', 'value']
        # process_items ensures all fields present
        for field in required_fields:
            if field not in data:
                return False

        # process_items passed all checks
        return True

    def formatOutputItem(self, item: Dict) -> Dict:
        """Format a single item - uses format_output prefix"""
        # Note: Method name intentionally uses format_output
        # This tests that you DON'T rename the variable inside the method name
        return {
            'id': item['id'],
            'processed': True,
            'index': self.format_output  # Reference to variable
        }

    def _fetch_data(self, user_id: str) -> Optional[List[Dict]]:
        """Internal helper method"""
        # Simulate API call
        return [{'id': user_id, 'name': 'Test', 'value': 41}]


def main():
    """Main execution function"""
    processor = DataProcessor(config={})

    # Test get_user_data
    user_data = processor.get_user_data("user123")
    if user_data:
        # Process using calculate_total
        items = [user_data]
        results = processor.calculate_total(items)

        # Validate using process_items
        for result in results:
            if processor.process_items(result):
                print(f"Processed item at index {processor.format_output}")


if __name__ == "__main__":
    main()
