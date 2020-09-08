from pyplatform.datawarehouse import *
from google.cloud import bigquery
import io

from flask import send_file
import datetime
import pytz

def main(request):
    _doc_string = """Return excel file in response to POST request. Return function doc_string for GET request.

    Keyword Arguments for request body:
        query {str} -- standard sql `select statetment` OR
                    `stored procedure call` containing select statements
        filename {str} -- custom filename for the excel file (default: report_timestamp.xlsx)
        sheet_name {str or list} -- custom sheet name for the excel sheet. For multi statement SLECT query or stored procedure, list of sheetname should be provided (default: Sheet1, Sheet2...)
        index {bool or list} -- if ture, writes dataframe index. For multi-sheet list of bool should be provided. By default index is ignored (default: {False})

    Returns:
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    """
    client = bigquery.Client()
    
    requestDateTime = datetime.datetime.now(pytz.timezone(
        'America/Chicago')).strftime('%Y-%m-%d %A %I:%M:%S %p CDT')

    headers = {"client_id": client.get_service_account_email(),
               "project_id": client.project}

    request_json = request.get_json()

    if request_json:
        print(f'PUT request type of request_json {type(request_json)} , {request_json}')
        
        # parse function arguments from request body
        query = request_json.get('query')
        filename = request_json.get('filename')
        sheet_name = request_json.get('sheet_name')
        index = request_json.get('index')

        # setting default values
        job_id = create_bq_job_id("Azure logic App Excel file request")
        if filename == None:
            filename = f'report_{job_id[:19]}.xlsx'
        else:
            filename = filename.split('.')[0] + '.xlsx'

        if not index:
            index = False

        print(f" PUT request provided => query {query}, filename {filename}, sheet_name:{sheet_name}, index: {index}")

        df = bq_to_df(query)
        in_mem_file = io.BytesIO()

        dfs =[df]

        dfs_to_excel(dfs, in_mem_file, sheet_name=sheet_name, index=index)
        in_mem_file.seek(0)

        print("sending requested file")
        response = send_file(in_mem_file, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            as_attachment=True, attachment_filename=filename)

        headers['requestTimestamp'] = requestDateTime
        headers["filename"] = filename
        headers['job_id'] = job_id

        return (response, 200, headers)

    else:
        return (_doc_string,200,headers)

