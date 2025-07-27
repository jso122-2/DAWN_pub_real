"""
Task Validator Module
====================
Handles validation of tasks, memory fragments, and responses.
Separates validation concerns from routing logic.
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    is_valid: bool
    reason: Optional[str] = None
    details: Optional[Dict] = None

class TaskValidator:
    """Validates tasks, memory fragments, and responses"""
    
    @staticmethod
    def validate_response(response: str) -> ValidationResult:
        """Validate that the response follows the required format."""
        required_sections = [
            "📝 Summary:",
            "🎯 Tactical Suggestion:",
            "📛 Sigils:"
        ]
        
        # Check if all required sections are present
        for section in required_sections:
            if section not in response:
                return ValidationResult(
                    is_valid=False,
                    reason=f"Missing required section: {section}"
                )
        
        # Check if sigils are properly formatted
        sigils_section = response.split("📛 Sigils:")[1].split("\n")[0].strip()
        if not sigils_section.startswith("[") or not sigils_section.endswith("]"):
            return ValidationResult(
                is_valid=False,
                reason="Sigils section not properly formatted"
            )
        
        return ValidationResult(is_valid=True)

    @staticmethod
    def validate_memory_fragments(memory_excerpts: list) -> ValidationResult:
        """Validate memory fragments for length and content."""
        try:
            if not memory_excerpts:
                return ValidationResult(
                    is_valid=False,
                    reason="No memory fragments found"
                )

            for i, excerpt in enumerate(memory_excerpts):
                # Check if excerpt is empty
                if not excerpt or not excerpt.strip():
                    return ValidationResult(
                        is_valid=False,
                        reason=f"Empty memory fragment at index {i}"
                    )

                # Estimate token count (rough approximation: 4 chars ≈ 1 token)
                token_count = len(excerpt) // 4
                if token_count > 512:
                    return ValidationResult(
                        is_valid=False,
                        reason=f"Memory fragment at index {i} exceeds 512 tokens ({token_count})"
                    )

            return ValidationResult(is_valid=True)

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                reason=f"Error validating memory fragments: {str(e)}"
            )

    @staticmethod
    def validate_cairn_checkpoint(cairn_note: str) -> ValidationResult:
        """Validate cairn checkpoint presence and content."""
        try:
            if not cairn_note or cairn_note == "No cairn checkpoint available":
                return ValidationResult(
                    is_valid=False,
                    reason="Invalid cairn checkpoint"
                )

            return ValidationResult(is_valid=True)

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                reason=f"Error validating cairn checkpoint: {str(e)}"
            )

    @staticmethod
    def validate_matrix_entry(matrix_entry: Dict) -> ValidationResult:
        """Validate the structure and content of a matrix entry."""
        required_fields = ['topic', 'origin_seed', 'memory_excerpts', 'cairn_note']
        
        for field in required_fields:
            if field not in matrix_entry:
                return ValidationResult(
                    is_valid=False,
                    reason=f"Missing required field: {field}"
                )
        
        # Validate memory excerpts
        memory_result = TaskValidator.validate_memory_fragments(
            matrix_entry.get('memory_excerpts', [])
        )
        if not memory_result.is_valid:
            return memory_result
        
        # Validate cairn note
        cairn_result = TaskValidator.validate_cairn_checkpoint(
            matrix_entry.get('cairn_note')
        )
        if not cairn_result.is_valid:
            return cairn_result
        
        return ValidationResult(is_valid=True) 