import './App.css';
import React from 'react';
import Navigator from './components/Navigator'
import { useState } from 'react';

function App() {
  const [body, setBody] = useState(
    [
      {
        'filterParams': {
          'mainGenre': {
            'operator': 'in',
            'value': []
          },
          'language': {
            'operator': 'in',
            'value': []
          },
          'minPopularity': {
            'operator': '>',
            'value': 0
          },
          'maxPopularity': {
            'operator': '<',
            'value': 100
          },
          'minDanceability': {
            'operator': '>',
            'value': 0
          },
          'maxDanceability': {
            'operator': '<',
            'value': 100
          },
          'minEnergy': {
            'operator': '>',
            'value': 0
          },
          'maxEnergy': {
            'operator': '<',
            'value': 100
          },
          'minLoudness': {
            'operator': '>',
            'value': 0
          },
          'maxLoudness': {
            'operator': '<',
            'value': 100
          },
          'minMode': {
            'operator': '>',
            'value': 0
          },
          'maxMode': {
            'operator': '<',
            'value': 100
          },
          'minSpeechiness': {
            'operator': '>',
            'value': 0
          },
          'maxSpeechiness': {
            'operator': '<',
            'value': 100
          },
          'minAcousticness': {
            'operator': '>',
            'value': 0
          },
          'maxAcousticness': {
            'operator': '<',
            'value': 100
          },
          'minInstrumentalness': {
            'operator': '>',
            'value': 0
          },
          'maxInstrumentalness': {
            'operator': '<',
            'value': 100
          },
          'minLiveness': {
            'operator': '>',
            'value': 0
          },
          'maxLiveness': {
            'operator': '<',
            'value': 100
          },
          'minValence': {
            'operator': '>',
            'value': 0
          },
          'maxValence': {
            'operator': '<',
            'value': 100
          },
          'minTempo': {
            'operator': '>',
            'value': 0
          },
          'maxTempo': {
            'operator': '<',
            'value': 100
          }
        },
        'accessCode': '',
        'playlistDetails': {
          'playlistName': '',
          'playlistDescription': '',
          'isPublic': false,
          'prompt': ''
        }
      }
    ]
  )

  return (
    <div className="App">
      <header className="App-header">
        <Navigator
          body={body}
          setBody={setBody}
        ></Navigator>
      </header>
    </div>
  );
}

export default App;
