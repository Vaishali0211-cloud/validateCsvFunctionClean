import logging
import azure.functions as func
import pandas as pd
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔍 Function validatecsv executing...")

    try:
        # Read body of the request
        file_bytes = req.get_body()

        # TEMPORARY DEBUG LOG: Print part of the request body
        logging.info(f"📦 Raw body (first 100 bytes): {file_bytes[:100]}")

        # Try reading CSV from request
        df = pd.read_csv(io.BytesIO(file_bytes))

        # Validation: Check required columns
        if 'EmployeeID' not in df.columns or 'Name' not in df.columns:
            logging.warning("🚫 Invalid CSV: Missing 'EmployeeID' or 'Name'")
            return func.HttpResponse(
                "Invalid CSV: Missing EmployeeID or Name",
                status_code=400
            )

        logging.info("✅ CSV validation passed.")
        return func.HttpResponse("Validation Passed", status_code=200)

    except Exception as e:
        logging.error(f"❌ Internal server error: {str(e)}")
        return func.HttpResponse(
            f"Internal server error: {str(e)}",
            status_code=500
        )
