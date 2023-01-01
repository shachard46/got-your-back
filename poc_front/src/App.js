import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import LiveStram from './compnents/LiveStram';
import Buttons from './compnents/buttons';
import ResultTable from './compnents/resultTable';
import 'react-notifications/lib/notifications.css';
import { NotificationContainer, NotificationManager } from 'react-notifications';

function App() {
  const [takeScreenshot, settakeScreenshot] = useState(false)
  const [screenshotList, setscreenshotList] = useState([])
  const [calibrationPhoto, setcalibrationPhoto] = useState(null)
  const [takecalibrationPhoto, settakecalibrationPhoto] = useState(false)
  const [result, setResult] = useState({ z: undefined, x: undefined, y: undefined, angle: undefined })
  // x={result["x"]} y={result["y"]} z={result["z"]} angle={result["angle"]}
  // useEffect(() => { console.log(result["x"], result["y"], result["z"], result["angle"]) }, [result])
  useEffect(() => {
    if (screenshotList.length > 0) {
      let URL = 'http://localhost:8000/check_my_seating'
      NotificationManager.info('Checking seating');
      fetch(URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          screenshotList: screenshotList,
          calibrationPhoto: calibrationPhoto
        })
      })
        .then(response => response.json())
        .then(data => {
          {
            setResult(data)
            NotificationManager.success('result successful');

          }
        });
    }



  }, [screenshotList])
  return (
    <div className="App">
      <LiveStram takeScreenshot={takeScreenshot} settakeScreenshot={settakeScreenshot} setscreenshotList={setscreenshotList} takecalibrationPhoto={takecalibrationPhoto} settakecalibrationPhoto={settakecalibrationPhoto} setcalibrationPhoto={setcalibrationPhoto} />
      <Buttons settakeScreenshot={settakeScreenshot} settakecalibrationPhoto={settakecalibrationPhoto} calibrationPhoto={calibrationPhoto} />
      <ResultTable result={result} />
      <NotificationContainer />

    </div>
  );
}

export default App;

