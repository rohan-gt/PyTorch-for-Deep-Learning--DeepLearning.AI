from typing import Literal
import os


def split_file(file_path: str, part_size_mb: int) -> None:
    """Split a file into fixed size parts in the same directory and remove the original."""
    directory = os.path.dirname(file_path)
    base = os.path.basename(file_path)

    # Idempotency check: skip if any part file already exists
    existing_parts = [
        p for p in os.listdir(directory)
        if p.startswith(base + ".part")
    ]
    if existing_parts:
        return

    # Idempotency check: skip if original missing
    if not os.path.exists(file_path):
        return

    part_size = part_size_mb * 1024 * 1024

    with open(file_path, "rb") as f:
        index = 0
        while True:
            chunk = f.read(part_size)
            if not chunk:
                break
            part_path = os.path.join(directory, f"{base}.part{index}")
            with open(part_path, "wb") as p:
                p.write(chunk)
            index += 1

    os.remove(file_path)


def merge_parts(base_path: str) -> str:
    """Merge all .part files matching the base file name, then delete part files."""
    directory = os.path.dirname(base_path)
    base = os.path.basename(base_path)

    parts = sorted([
        p for p in os.listdir(directory)
        if p.startswith(base + ".part")
    ])

    # Idempotency check: skip if no parts
    if not parts:
        return base_path

    with open(base_path, "wb") as out:
        for part in parts:
            part_path = os.path.join(directory, part)
            with open(part_path, "rb") as p:
                out.write(p.read())

    for part in parts:
        os.remove(os.path.join(directory, part))

    return base_path


def process_files(
    file_paths: list, mode: Literal["split", "merge"], part_size_mb: int = 90
) -> None:
    """Process multiple files in split or merge mode."""
    if mode == "split":
        for path in file_paths:
            split_file(path, part_size_mb)
    elif mode == "merge":
        for path in file_paths:
            merge_parts(path)


if __name__ == "__main__":
    file_paths = [
        "Professional Certificates/Deep Learning Specialization/5. Sequence Models/2. Natural Language Processing & Word Embeddings/Assignments/W2A1/data/glove.6B.50d.txt",
        "Professional Certificates/Deep Learning Specialization/5. Sequence Models/2. Natural Language Processing & Word Embeddings/Assignments/W2A2/data/glove.6B.50d.txt",
        "Professional Certificates/Deep Learning Specialization/5. Sequence Models/4. Transformer Network/Labs/L1/glove/glove.6B.100d.txt",
        "Professional Certificates/Deep Learning Specialization/5. Sequence Models/4. Transformer Network/Labs/L3/model/pytorch/pytorch_model.bin",
        "Professional Certificates/Deep Learning Specialization/5. Sequence Models/4. Transformer Network/Labs/L3/model/tensorflow/tf_model.h5",
    ]
    process_files(file_paths=file_paths, mode="split")
