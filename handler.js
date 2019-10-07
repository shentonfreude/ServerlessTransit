const fetch = require('node-fetch');
const axios = require('axios');

const wmataURL = 'https://api.wmata.com/Incidents.svc/json/Incidents';

module.exports.fetch = async (event, context) => {
  const response = await axios({
    method: 'GET',
    url: wmataURL,
    headers: {
      //public demo key
      api_key: 'e13626d03d8e4c03ac07f95541b3091b'
    }
  });

  const incidents = response.data.Incidents;

  const cleanIncidents = incidents.map(incident => {
      return {
        type: incident.IncidentType,
        desc: incident.Description,
        lines: incident.LinesAffected,
        updated: incident.DateUpdated
      }
    });
  return cleanIncidents;
};