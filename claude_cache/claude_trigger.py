import time
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from task_router import TaskRouter
from matrix_controller import CAIRNMatrix
from anthropic import Anthropic
from codex.prompt_compiler import PromptCompiler
import os

# === Symbolic Processing Constants ===
REQUIRED_TAGS = {
    "summary": "📝 Summary",
    "heat": "🌡️ Heat",
    "entropy": "🧭 Entropy",
    "sigil": "✅ sigil"
}

# === Response Validation ===
@dataclass
class ClaudeResponse:
    summary: str
    heat: float
    entropy: float
    sigil: str
    raw_response: str

    @classmethod
    def from_text(cls, text: str) -> Optional['ClaudeResponse']:
        try:
            # Extract required tags
            summary = cls._extract_tag(text, REQUIRED_TAGS["summary"])
            heat = float(cls._extract_tag(text, REQUIRED_TAGS["heat"]))
            entropy = float(cls._extract_tag(text, REQUIRED_TAGS["entropy"]))
            sigil = cls._extract_tag(text, REQUIRED_TAGS["sigil"])

            return cls(
                summary=summary,
                heat=heat,
                entropy=entropy,
                sigil=sigil,
                raw_response=text
            )
        except (ValueError, KeyError) as e:
            logging.error(f"Failed to parse Claude response: {e}")
            return None

    @staticmethod
    def _extract_tag(text: str, tag: str) -> str:
        """Extract content after a tag until the next tag or end."""
        try:
            start = text.index(tag) + len(tag)
            end = text.find("\n\n", start)
            if end == -1:
                end = len(text)
            return text[start:end].strip()
        except ValueError:
            raise KeyError(f"Missing required tag: {tag}")

# === Claude Integration ===
class ClaudeProcessor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable or api_key parameter is required")
        self.client = Anthropic(api_key=self.api_key)
        
    def process_context(self, context: str) -> Tuple[Optional[ClaudeResponse], Optional[str]]:
        """Process context through Claude API and validate response."""
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                system="You are DAWN's external symbol processor. Follow the response format exactly as specified.",
                messages=[
                    {"role": "user", "content": context}
                ]
            )
            
            if not response.content:
                return None, "Empty response from Claude"
                
            response_text = response.content[0].text
            claude_response = ClaudeResponse.from_text(response_text)
            
            if not claude_response:
                return None, "Invalid response format"
                
            return claude_response, None
            
        except Exception as e:
            return None, f"Claude processing error: {str(e)}"

# === Response Handling ===
def save_and_register_response(task, response: ClaudeResponse, cairn_matrix: CAIRNMatrix):
    """Save Claude's response and register it in the CAIRNMatrix."""
    try:
        # Create cache directory if it doesn't exist
        cache_dir = Path("claude_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Save response in multiple formats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = cache_dir / f"{task.task_id}_{timestamp}"
        
        # Save as markdown
        with open(f"{base_path}.md", "w") as f:
            f.write(response.raw_response)
            
        # Save as JSON with metadata
        metadata = {
            "task_id": task.task_id,
            "timestamp": timestamp,
            "heat": response.heat,
            "entropy": response.entropy,
            "sigil": response.sigil,
            "summary": response.summary
        }
        with open(f"{base_path}.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        # Register in CAIRNMatrix
        cairn_matrix.register_response(
            task_id=task.task_id,
            response=response.raw_response,
            metadata=metadata
        )
        
        logging.info(f"Saved and registered response for task {task.task_id}")
        
    except Exception as e:
        logging.error(f"Error saving response: {e}")
        raise

# === Main Execution ===
def main():
    # Setup logging
    LOG_DIR = Path("logs/trigger/")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_DIR / "claude_trigger.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    # Initialize components
    task_router = TaskRouter()
    cairn_matrix = CAIRNMatrix()
    claude_processor = ClaudeProcessor()
    prompt_compiler = PromptCompiler(cairn_matrix)

    logging.info("Claude trigger started. Listening for .claude_ready tasks...")

    try:
        while True:
            task = task_router.fetch_next_ready()

            if not task:
                time.sleep(10)
                continue

            logging.info(f"Processing task: {task.file_path}")

            try:
                # Build context using PromptCompiler
                context = prompt_compiler.compile(task)
                
                # Process through Claude
                response, error = claude_processor.process_context(context)
                
                if error:
                    logging.error(f"Error processing task {task.file_path}: {error}")
                    task_router.mark_task_rejected(task, error)
                    continue
                
                # Save and register response
                save_and_register_response(task, response, cairn_matrix)
                
                # Handle task completion
                task_router.mark_task_done(task)
                logging.info(f"Task completed: {task.file_path}")
                
                # Check if task needs refinement
                if response.heat > 0.8 or response.entropy > 0.7:
                    logging.info(f"Task {task.task_id} marked for refinement due to high heat/entropy")
                    task_router.reloop_task(task)
            
            except Exception as e:
                logging.error(f"Error processing task {task.file_path}: {e}")
                task_router.mark_task_rejected(task, str(e))
                continue

    except KeyboardInterrupt:
        logging.info("Claude trigger manually stopped.")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main() 