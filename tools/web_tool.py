"""
REDMYTHOS CLAW 🦀 — File Tool
Read, write, edit, delete, list files.
Operations are restricted to the current working directory and the user's home directory.
"""

import os
import shutil
from pathlib import Path


class FileTool:
    """File system operations tool."""

    SAFE_ROOTS = [Path.cwd().resolve(), Path.home().resolve()]

    def execute(self, action: str, path: str,
                content: str = "", encoding: str = "utf-8") -> str:
        """
        Execute a file operation.

        Args:
            action: read/write/edit/delete/list/exists/mkdir
            path: File or directory path
            content: Content for write/edit actions
            encoding: File encoding

        Returns:
            Result string
        """
        try:
            safe_path = self._resolve_allowed_path(path)
        except ValueError as exc:
            return f"❌ Security restriction: {exc}"

        try:
            if action == "read":
                return self._read(safe_path, encoding)
            elif action == "write":
                return self._write(safe_path, content, encoding)
            elif action == "edit":
                return self._edit(safe_path, content, encoding)
            elif action == "delete":
                return self._delete(safe_path)
            elif action == "list":
                return self._list(safe_path)
            elif action == "exists":
                return str(Path(safe_path).exists())
            elif action == "mkdir":
                return self._mkdir(safe_path)
            elif action == "copy":
                return self._copy(safe_path, content)
            elif action == "move":
                return self._move(safe_path, content)
            else:
                return f"❌ Unknown action: {action}. Use: read/write/edit/delete/list/exists/mkdir"
        except PermissionError:
            return f"❌ Permission denied: {safe_path}"
        except Exception as exc:
            return f"❌ File operation error: {exc}"

    def _resolve_allowed_path(self, path: str) -> str:
        """Resolve a path and confirm it stays inside a safe root directory."""
        expanded = os.path.expandvars(os.path.expanduser(path))
        candidate = Path(expanded)

        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        else:
            candidate = candidate.resolve()

        for root in self.SAFE_ROOTS:
            try:
                candidate.relative_to(root)
                return str(candidate)
            except ValueError:
                continue

        raise ValueError(f"'{path}' is outside the allowed sandbox: {', '.join(str(root) for root in self.SAFE_ROOTS)}")

    def _read(self, path: str, encoding: str) -> str:
        """Read file contents."""
        p = Path(path)
        if not p.exists():
            return f"❌ File not found: {path}"
        if p.is_dir():
            return f"❌ '{path}' is a directory. Use action='list'"

        size = p.stat().st_size
        if size > 1_000_000:
            return f"⚠️ File is large ({size/1024:.1f}KB). Reading first 10000 chars only.\n\n" + p.read_text(encoding=encoding, errors='replace')[:10000]

        content = p.read_text(encoding=encoding, errors='replace')
        lines = content.count('\n')
        return f"📄 {path} ({lines} lines, {size} bytes):\n\n{content}"

    def _write(self, path: str, content: str, encoding: str) -> str:
        """Write content to file (creates if not exists)."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        existed = p.exists()
        p.write_text(content, encoding=encoding)
        action = "Updated" if existed else "Created"
        return f"✅ {action}: {path} ({len(content)} chars)"

    def _edit(self, path: str, content: str, encoding: str) -> str:
        """Edit/append to existing file."""
        p = Path(path)
        if not p.exists():
            return self._write(path, content, encoding)

        existing = p.read_text(encoding=encoding, errors='replace')
        p.write_text(existing + "\n" + content, encoding=encoding)
        return f"✅ Edited: {path}"

    def _delete(self, path: str) -> str:
        """Delete file or directory."""
        p = Path(path)
        if not p.exists():
            return f"❌ Not found: {path}"

        if p.is_file():
            p.unlink()
            return f"✅ Deleted file: {path}"
        if p.is_dir():
            shutil.rmtree(path)
            return f"✅ Deleted directory: {path}"
        return f"❌ Unsupported object type: {path}"

    def _list(self, path: str) -> str:
        """List directory contents."""
        p = Path(path) if path else Path.cwd()

        if not p.exists():
            return f"❌ Directory not found: {path}"
        if not p.is_dir():
            return f"❌ '{path}' is a file, not a directory"

        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
        if not items:
            return f"📁 {path} (empty)"

        result = [f"📁 {p.absolute()}:"]
        for item in items[:100]:
            if item.is_dir():
                result.append(f"  📂 {item.name}/")
            else:
                size = item.stat().st_size
                size_str = f"{size}B" if size < 1024 else f"{size//1024}KB"
                result.append(f"  📄 {item.name} ({size_str})")

        if len(items) > 100:
            result.append(f"  ... and {len(items)-100} more items")

        return "\n".join(result)

    def _mkdir(self, path: str) -> str:
        """Create directory."""
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"✅ Created directory: {path}"

    def _copy(self, src: str, dst: str) -> str:
        """Copy file or directory."""
        src_path = Path(src)
        dst_path = Path(dst)
        if dst_path.is_absolute() and not self._resolve_allowed_path(str(dst_path)):
            return "❌ Destination outside sandbox."
        if src_path.is_dir():
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
        return f"✅ Copied: {src} → {dst}"

    def _move(self, src: str, dst: str) -> str:
        """Move file or directory."""
        src_path = Path(src)
        dst_path = Path(dst)
        if dst_path.is_absolute() and not self._resolve_allowed_path(str(dst_path)):
            return "❌ Destination outside sandbox."
        shutil.move(src_path, dst_path)
        return f"✅ Moved: {src} → {dst}"
