import logging
import azure.functions as func
import pandas as pd
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("validateCsv function triggered.")

    try:
        file_bytes = req.get_body()
        df = pd.read_csv(io.BytesIO(file_bytes))

        if 'EmployeeID' not in df.columns or 'Name' not in df.columns:
            return func.HttpResponse("Invalid CSV: Missing EmployeeID or Name", status_code=400)

        return func.HttpResponse("Validation Passed", status_code=200)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Internal server error: {str(e)}", status_code=500)
