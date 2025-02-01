from pathlib import Path

from src.core.logger import get_logger

EXCLUDED_DIRS = {"migrations", "venv", "__pycache__", ".git", "tests", "node_modules", "temp", "cache"}

logger = get_logger("gather")


def combine_python_files(directory: str) -> None:
    source_dir = Path(directory)
    output_file = Path("combined.txt")
    logger.info("Комбинируем все .py-файлы из %s в %s", source_dir, output_file)

    with output_file.open("w", encoding="utf-8") as result:
        for py_file in source_dir.rglob("*.py"):
            if any(excluded in py_file.parts for excluded in EXCLUDED_DIRS):
                continue
            content = py_file.read_text(encoding="utf-8")
            processed_content = content.replace(" ", "").replace("\t", "")

            gathered_lines = [line for line in processed_content.splitlines() if line.strip()]
            processed_content = "".join(gathered_lines)
            processed_content = f"#filename:{py_file}\n{processed_content}"
            result.write(processed_content)

    logger.info("✅ Готово! Размер результата: %f.2 K байт", output_file.stat().st_size / 1024)


combine_python_files("src")
