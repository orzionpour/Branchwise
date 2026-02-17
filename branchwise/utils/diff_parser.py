import re
from typing import List, Optional, Tuple

from pydantic import BaseModel


class FileChange(BaseModel):
    """Represents a change in a file."""
    old_line_start: int
    new_line_start: int
    lines: List[Tuple[str, Optional[int]]]  # (content, new_line_number)

class DiffParser:
    """Parses git patches into structured file changes."""
    
    @staticmethod
    def parse(patch: str) -> List[FileChange]:
        """
        Parses a git patch string into a list of FileChange objects.
        Each FileChange corresponds to a hunk in the patch.
        """
        changes: List[FileChange] = []
        if not patch:
            return changes
            
        hunk_header_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
        
        lines = patch.splitlines()
        current_hunk: Optional[FileChange] = None
        current_new_line_num = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            match = hunk_header_re.match(line)
            
            if match:
                if current_hunk:
                    changes.append(current_hunk)
                
                old_start = int(match.group(1))
                new_start = int(match.group(3))
                current_new_line_num = new_start
                
                current_hunk = FileChange(
                    old_line_start=old_start,
                    new_line_start=new_start,
                    lines=[]
                )
                i += 1
                continue
            
            if current_hunk:
                if line.startswith("+"):
                    current_hunk.lines.append((line, current_new_line_num))
                    current_new_line_num += 1
                elif line.startswith("-"):
                    current_hunk.lines.append((line, None))
                else:
                    current_hunk.lines.append((line, current_new_line_num))
                    current_new_line_num += 1
            
            i += 1
            
        if current_hunk:
            changes.append(current_hunk)
            
        return changes
