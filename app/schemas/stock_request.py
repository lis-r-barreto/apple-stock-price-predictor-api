from pydantic import BaseModel

class StockDataRequest(BaseModel):
    csv_file_path: str
