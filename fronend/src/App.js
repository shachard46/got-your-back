import './App.css';
import { useEffect, useState } from 'react';
function App() {
  const [screenshot, setScreenshot] = useState(null)
  // const getImage = async () => {
  //   const response = await fetch('http://127.0.0.1:8000/screenshot');
  //   console.log(response)
  //   const image = await response.blob();
  //   setImage(URL.createObjectURL(image));
  // }
  async function updateScreenshot() {
    const response = await fetch('http://192.168.1.102:8000/calibrate');
    const json = await response.json();

    setScreenshot(`data:image/png;base64,${json}`);
  }


  return (
    <div className="App">
      <div className='Camera'>
        <div>
          {screenshot && <img src={screenshot} alt="Webcam screenshot" />}
        </div>

      </div>
      <button className='button' onClick={() => updateScreenshot()}>calibrate</button>

    </div>
  );
}

export default App;
