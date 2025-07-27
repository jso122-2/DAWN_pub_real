"""
PromptCodex.001: Symbolic Invocation Layer
Constructs and validates standardized symbolic prompt structures for Claude-compatible external cognition.
"""

from typing import List, Dict, Optional, Tuple, Any
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from matrix_controller import CAIRNMatrix

# === Codex Constants ===
REQUIRED_TAGS = {
    "summary": "📝 Summary",
    "heat": "🌡️ Heat",
    "entropy": "🧭 Entropy",
    "sigil": "✅ sigil"
}

# === Logging Setup ===
LOG_DIR = Path("logs/prompt/")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "prompt_compiler.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@dataclass
class PromptMetadata:
    """Metadata for a compiled prompt."""
    task_id: str
    timestamp: str
    token_count: int
    sigil: Optional[str]
    memory_fragments: int
    parent_sigil: Optional[str] = None
    rebloom_lineage: Optional[List[str]] = None
    heat: Optional[float] = None
    entropy: Optional[float] = None

class PromptValidationError(Exception):
    """Raised when prompt validation fails."""
    pass

class PromptCompiler:
    """Central structuring layer for symbolic invocation."""
    
    def __init__(self, cairn_matrix: CAIRNMatrix):
        self.cairn_matrix = cairn_matrix
        self._validator = PromptValidator()
        self._auditor = PromptAuditor()
        self._archive = PromptArchive()
    
    def build_context_from_task(self, task: Any, strict_mode: bool = True) -> Tuple[str, PromptMetadata]:
        """
        Compiles semantic metadata + symbolic memory into structured symbolic input.
        
        Args:
            task: The task object containing metadata and matrix entry
            strict_mode: If True, raises exceptions on validation failures
            
        Returns:
            Tuple[str, PromptMetadata]: The formatted prompt and its metadata
            
        Raises:
            PromptValidationError: If strict_mode=True and validation fails
        """
        context_parts: List[str] = []
        
        try:
            # === Task Overview ===
            context_parts.append("## 🧾 Task Overview")
            context_parts.append(f"Task ID: {task.task_id}")
            context_parts.append(f"Priority: {task.priority}")
            context_parts.append(f"Score: {task.score}")

            # === Memory Excerpts ===
            memory_fragments: List[str] = task.matrix_entry.get("memory_excerpts", [])
            if memory_fragments:
                context_parts.append("\n## 🧠 Memory Fragments")
                for i, fragment in enumerate(memory_fragments, 1):
                    context_parts.append(f"Fragment {i}:\n{fragment}")

            # === Sigil Context ===
            sigil: Optional[str] = task.matrix_entry.get("sigil")
            parent_sigil: Optional[str] = task.matrix_entry.get("parent_sigil")
            rebloom_lineage: Optional[List[str]] = task.matrix_entry.get("rebloom_lineage")
            
            if sigil:
                sigil_context: Optional[str] = self.cairn_matrix.get_sigil_context(sigil)
                if sigil_context:
                    context_parts.append("\n## 🧿 Sigil Context")
                    context_parts.append(sigil_context)

            # === Instructions ===
            context_parts.append("\n## 🎯 Instructions")
            context_parts.append("Respond using the following strict symbolic format:")
            context_parts.append("""
📝 Summary: <one paragraph summary of symbolic insight>

🌡️ Heat: <float between 0.0 and 1.0>

🧭 Entropy: <float between 0.0 and 1.0>

✅ sigil: <one-line symbolic identifier>
            """)

            # Build final prompt
            prompt = "\n".join(context_parts)
            
            # Validate structure
            if not self._validator.validate_prompt_structure(prompt, strict_mode):
                if strict_mode:
                    raise PromptValidationError("Prompt validation failed")
                logging.warning("Prompt validation failed")
            
            # Create metadata
            metadata = PromptMetadata(
                task_id=task.task_id,
                timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
                token_count=self._auditor.count_prompt_tokens(prompt),
                sigil=sigil,
                memory_fragments=len(memory_fragments),
                parent_sigil=parent_sigil,
                rebloom_lineage=rebloom_lineage,
                heat=task.matrix_entry.get("heat"),
                entropy=task.matrix_entry.get("entropy")
            )
            
            # Archive prompt
            self._archive.save_prompt(prompt, metadata)
            
            return prompt, metadata
            
        except Exception as e:
            logging.error(f"Error building prompt for task {task.task_id}: {str(e)}")
            if strict_mode:
                raise
            return "", PromptMetadata(
                task_id=task.task_id,
                timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
                token_count=0,
                sigil=None,
                memory_fragments=0
            )

class PromptValidator:
    """Ensures conformity to symbolic tag schema."""
    
    def validate_prompt_structure(self, prompt: str, strict_mode: bool = True) -> bool:
        """
        Validate that the prompt contains all required tags and follows the structure.
        
        Args:
            prompt: The prompt text to validate
            strict_mode: If True, raises exceptions on validation failures
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            PromptValidationError: If strict_mode=True and validation fails
        """
        try:
            for tag in REQUIRED_TAGS.values():
                if tag not in prompt:
                    if strict_mode:
                        raise PromptValidationError(f"Missing required tag: {tag}")
                    return False
            return True
        except Exception as e:
            if strict_mode:
                raise
            return False

class PromptAuditor:
    """Tracks token weight + symbolic construction fidelity."""
    
    def count_prompt_tokens(self, prompt: str) -> int:
        """
        Provides rough token estimation (≈ 4 characters per token).
        Future: replace with tokenizer like tiktoken for Claude/OpenAI API parity.
        """
        return len(prompt) // 4

class PromptArchive:
    """Persistent audit trail for semantic prompt lineage."""
    
    def save_prompt(self, prompt: str, metadata: PromptMetadata) -> None:
        """
        Saves prompt and metadata to the audit trail.
        
        Args:
            prompt: The prompt text to save
            metadata: Associated metadata
        """
        try:
            # Save prompt text
            prompt_path = LOG_DIR / f"prompt_{metadata.task_id}_{metadata.timestamp}.txt"
            with open(prompt_path, "w") as f:
                f.write(prompt)
            
            # Save metadata
            meta_path = LOG_DIR / f"prompt_{metadata.task_id}_{metadata.timestamp}_meta.json"
            with open(meta_path, "w") as f:
                import json
                json.dump(metadata.__dict__, f, indent=2)
                
            logging.info(
                f"Archived prompt for task {metadata.task_id} - "
                f"Tokens: {metadata.token_count}, "
                f"Sigil: {metadata.sigil or 'None'}"
            )
            
        except Exception as e:
            logging.error(f"Error archiving prompt: {str(e)}")
            raise 