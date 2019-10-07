'use strict';

const storyUrl = "http://datamine.mta.info/mta_esi.php?key=<key>&feed_id=1";

const iopipe = require('@iopipe/iopipe')({
  token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNzU4ZmMwNC0zOWFjLTQxNjQtYWNhNS1iNjRmN2VlZGNmNDAiLCJqdGkiOiJlYTM5MDYyYy03YzU5LTRhNTMtYTllNS0zZTBlZjI2NjhlZjAiLCJpYXQiOjE1MDIyODczNDgsImlzcyI6Imh0dHBzOi8vaW9waXBlLmNvbSIsImF1ZCI6Imh0dHBzOi8vaW9waXBlLmNvbSxodHRwczovL21ldHJpY3MtYXBpLmlvcGlwZS5jb20vZXZlbnQvLGh0dHBzOi8vZ3JhcGhxbC5pb3BpcGUuY29tIn0.06nUoeOOxchMUYyB8WYIhmLw3IQCcAb1GtB-12p_v9E'
});

module.exports.hello = async event => {
  return {
    iopipe(event, context) {
      // run your code here normally
      context.succeed({
        statusCode: 200,
        body: JSON.stringify(
          {
            message: 'Go Serverless v1.0! Your function executed successfully!',
            input: event,
          },
          null,
          2,
      )});
    }
  };
  // Use this code if you don't use the http event with the LAMBDA-PROXY integration
  // return { message: 'Go Serverless v1.0! Your function executed successfully!', event };
};
