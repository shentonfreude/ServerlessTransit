def dynamodb_event(event, context):
    print(f'### event={event}')
    for rec in event['Records']:
        ddb = rec['dynamodb']
        # Somewhere there is a function which tranforms this raw DDB data to a
        # Python Dict so I won't need this
        keys = ddb['Keys']
        pk = keys['pk']['S']
        if not pk.startswith('report:'):
            print('### Not a report, ignoring.')
            return
        # TODO: if it starts with "incident:" then call a functino to query the
        # DB to find interested subscribers and send SNS.
        sk = keys['sk']['S']
        ni = ddb['NewImage']
        transit_authority = ni['transit_authority']['S']
        transit_line = ni['transit_line']['S']
        transit_station = ni['transit_station']['S']
        report_source = ni['report_source']['S']
        report_text = ni['report_text']['S']
        status = ni['status']['S']
        print('### Got a report!')
        # TODO: search DB for same line within last 30 minutes
        # if found, create incident.
