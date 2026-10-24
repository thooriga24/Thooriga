"""Create a clean, checksummed source folder and ZIP without installed dependencies."""
from pathlib import Path
import argparse
import hashlib
import shutil
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', 'dist', '.mypy_cache', '.ruff_cache'}
EXCLUDED_FILES = {'.env', 'browser-export.zip', '.DS_Store', 'SOURCE_MANIFEST.sha256'}

def package(destination: Path):
    destination = destination.resolve()
    # Avoid recursively packaging an output nested within the source tree.
    if destination == PROJECT or PROJECT in destination.parents:
        raise ValueError('Use a delivery directory outside the source project')
    destination.mkdir(parents=True, exist_ok=True)
    folder = destination / 'Thooriga'
    if folder.exists():
        raise FileExistsError(f'{folder} already exists; choose a new delivery directory')
    folder.mkdir()
    copied = []
    for source in sorted(PROJECT.rglob('*')):
        relative = source.relative_to(PROJECT)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if source.is_symlink() or not source.is_file():
            continue
        if source.name in EXCLUDED_FILES or source.suffix == '.pyc' or (source.name.startswith('.env.') and source.name != '.env.example'):
            continue
        target = folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)
    manifest = folder / 'SOURCE_MANIFEST.sha256'
    manifest.write_text(''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(folder).as_posix()}\n' for path in copied), encoding='utf-8')
    archive = destination / 'Thooriga.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                output.write(path, Path('Thooriga') / path.relative_to(folder))
        if output.testzip() is not None:
            raise RuntimeError('ZIP integrity verification failed')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = destination / 'Thooriga.zip.sha256'
    checksum.write_text(f'{digest}  Thooriga.zip\n', encoding='utf-8')
    print(f'Folder: {folder}\nArchive: {archive}\nFiles: {len(copied)+1}\nSHA256: {digest}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path, help='New delivery location outside this source project')
    package(parser.parse_args().destination)
