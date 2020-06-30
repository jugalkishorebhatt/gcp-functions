from flask import escape
from google.cloud import bigquery

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json(silent=True)
    client = bigquery.Client()
    #request_args = request.args
    #data = "something"
    print(request_json)
    if request_json and 'update' in request_json:
        data = request_json['update']
    elif request_json and 'insert' in request_json:    
        data = "insert Section"
    else:
        query_str = """
            SELECT
        CONCAT(
            'https://stackoverflow.com/questions/',
            CAST(id as STRING)) as url,
        view_count
            FROM `bigquery-public-data.stackoverflow.posts_questions`
            WHERE tags like '%google-bigquery%'
            ORDER BY view_count DESC
            LIMIT 10"""

        job = client.query(
            query_str
        )
        #Wait for job to finish
        job.result()
        data = job.to_dataframe()
    return 'Hello {}!'.format(escape(data))
