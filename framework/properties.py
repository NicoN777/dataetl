import glob
import os
ROOT = os.path.abspath(os.path.dirname(__file__))
RESOURCES = os.path.join(ROOT, 'conf')
_files = glob.glob(f'{RESOURCES}/*.ini')
_reports = os.path.join(ROOT, 'data/reports')
csv_dir = os.path.join(_reports, 'csv')
_chunk_size = 20








