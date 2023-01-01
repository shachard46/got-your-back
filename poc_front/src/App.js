import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import LiveStram from './compnents/LiveStram';
import Buttons from './compnents/buttons';
import ResultTable from './compnents/resultTable';
import axios from 'axios';

function App() {
  const [takeScreenshot, settakeScreenshot] = useState(false)
  const [screenshotList, setscreenshotList] = useState([])
  const [calibrationPhoto, setcalibrationPhoto] = useState(null)
  const [takecalibrationPhoto, settakecalibrationPhoto] = useState(false)
  const [result, setResult] = useState({ z: undefined, x: undefined, y: undefined, angle: undefined })
  // x={result["x"]} y={result["y"]} z={result["z"]} angle={result["angle"]}
  // useEffect(() => { console.log(result["x"], result["y"], result["z"], result["angle"]) }, [result])
  useEffect(() => {
    let URL = 'http://localhost:8000/check_my_seating'
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
        }
      });


  }, [screenshotList])
  return (
    // x={result["x"]} y={result["y"]} z={result["z"]} angle={result["angle"]}
    <div className="App">
      {/* <Webcam /> */}
      <LiveStram takeScreenshot={takeScreenshot} settakeScreenshot={settakeScreenshot} setscreenshotList={setscreenshotList} takecalibrationPhoto={takecalibrationPhoto} settakecalibrationPhoto={settakecalibrationPhoto} setcalibrationPhoto={setcalibrationPhoto} />
      <Buttons settakeScreenshot={settakeScreenshot} settakecalibrationPhoto={settakecalibrationPhoto} />
      <ResultTable result={result} />
    </div>
  );
}

export default App;

