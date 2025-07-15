import logging
import azure.functions as func
import pandas as pd
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("validateCsv function triggered.")

    try:
        # Get raw request body
        file_bytes = req.get_body()

        try:
            # Try reading as bytes (real file)
            df = pd.read_csv(io.BytesIO(file_bytes))
        except Exception:
            # Fallback: decode as string for raw/pasted CSV
            file_text = file_bytes.decode("utf-8")
            df = pd.read_csv(io.StringIO(file_text))

        if 'EmployeeID' not in df.columns or 'Name' not in df.columns:
            return func.HttpResponse("Invalid CSV: Missing EmployeeID or Name", status_code=400)

        return func.HttpResponse("Validation Passed", status_code=200)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Internal server error: {str(e)}", status_code=500)
