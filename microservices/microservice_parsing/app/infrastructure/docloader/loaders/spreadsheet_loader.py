from app.infrastructure.docloader.interfaces.base_loader import BaseLoader
from app.infrastructure.docloader.models.io import SpreadsheetDocument
from typing import Literal, overload
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import io

class SpreadsheetLoader(BaseLoader):
    def __init__(self, header_fill_threshold: float = 0.6) -> None:
        self.header_fill_threshold = header_fill_threshold
        if self.header_fill_threshold < 0 or self.header_fill_threshold > 1:
            raise ValueError("header_fill_threshold must be between 0 and 1.")
        
    @overload
    def _detect_header_row(self, xlsx_bytes: bytes, max_rows: int = 20): ...

    @overload
    def _detect_header_row(self, xlsx_path: Path, max_rows: int = 20): ...

    @overload
    def _detect_header_row(self, dataframe: pd.DataFrame, max_rows: int = 20): ...

    def _detect_header_row(self, xlsx_path: Path = None, xlsx_bytes: bytes = None, dataframe: pd.DataFrame = None, max_rows=20):
        if dataframe is None:
            if xlsx_bytes is not None:
                dataframe = pd.read_excel(io.BytesIO(xlsx_bytes), header=None, nrows=max_rows)
            elif xlsx_path is not None:
                dataframe = pd.read_excel(xlsx_path, header=None, nrows=max_rows)
            else:
                raise ValueError("No input provided to detect header row.")

        for i, row in dataframe.iterrows():
            non_null = row.notna().sum()
            total = len(row)
            string_like = sum(isinstance(x, str) for x in row if pd.notna(x))
            unique_ratio = row.nunique() / (non_null or 1)

            if (
                non_null / total > self.header_fill_threshold and
                string_like / (non_null or 1) > 0.5 and
                unique_ratio > 0.8
            ):
                return i

        return 0

    def _clean_dict(self, data: dict):
        def clean_str(s):
            return s.replace('\n', ' ').strip() if isinstance(s, str) else s

        return [
            {clean_str(k): v for k, v in row.items()}
            for row in data
        ]
    
    @overload
    def load(self,
             file_bytes: bytes,
             file_name: str = None,
             created_at: str = None,
             modified_at: str = None,
             output_format: Literal["json", "csv"] = 'json') -> SpreadsheetDocument: ...
    
    @overload
    def load(self,
             file_path: os.PathLike,
             output_format: Literal["json", "csv"] = 'json') -> SpreadsheetDocument: ...
    
    def load(self, 
             file_path: Path = None, 
             file_bytes: bytes = None, 
             file_name: str = None,
             created_at: str = None,
             modified_at: str = None,
             output_format: Literal["json", "csv"] = 'json') -> SpreadsheetDocument:
        
        sheet_data = {}

        if file_path:
            if not isinstance(file_path, Path):
                file_path = Path(file_path)
            if file_path.suffix.lower() not in ['.xlsx', '.xls']:
                raise ValueError(f"File {file_path} is not a valid Excel file.")
            if not file_path.exists():
                raise FileNotFoundError(f"File {file_path} does not exist.")

            file_name = file_path.name
            file_size = file_path.stat().st_size
            created_at = datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            modified_at = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            excel_dict = pd.read_excel(file_path, sheet_name=None, header=None, engine='openpyxl')

        elif file_bytes:
            if not isinstance(file_bytes, bytes):
                raise ValueError("file_bytes must be of type bytes.")

            file_name = "spreadsheet.xlsx"
            file_size = len(file_bytes)
            created_at = modified_at = datetime.now().isoformat()
            stream = io.BytesIO(file_bytes)
            excel_dict = pd.read_excel(stream, sheet_name=None, header=None, engine='openpyxl')

        else:
            raise ValueError("Either file_path or file_bytes must be provided.")

        # Process each sheet
        for sheet_name, df in excel_dict.items():
            # Detect header row
            header_row = self._detect_header_row(dataframe=df)
            df.columns = df.iloc[header_row]
            df = df.drop(index=list(range(header_row + 1))).reset_index(drop=True)

            # Clean and format
            if output_format == 'csv':
                df = df.fillna('').astype(str).map(lambda x: x.strip() if isinstance(x, str) else x)
                sheet_data[sheet_name] = df.to_csv(index=False)
            elif output_format == 'json':
                df = df.map(lambda x: None if pd.isna(x) else x).astype(str).map(lambda x: x.strip() if isinstance(x, str) else x)
                sheet_data[sheet_name] = self._clean_dict(df.to_dict(orient='records'))
            else:
                raise ValueError(f"Unsupported output format: {output_format}")

        return SpreadsheetDocument(
            file_name=file_name,
            total_sheets=len(sheet_data),
            file_size_bytes=file_size,
            created_at=created_at,
            modified_at=modified_at,
            sheets=sheet_data,
            type=output_format,
            file_path=str(file_path) if file_path else None
        )