from pathlib import Path

def read_text_file(file_path:str)->tuple[Path,str]:
    path = Path(file_path).resolve()

    if not path.exists() or not path.is_file():
        raise ValueError(f"file does not exist:{file_path}")

    if path.suffix.lower() not in {".md",".txt"}:
        raise ValueError("only .md and .txt file are supported")

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"file is not valid UTF-8:{file_path}")from exc
    except OSError as exc:
        raise RuntimeError(f"failed to read file{file_path}")from exc

    return path,content