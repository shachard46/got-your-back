import "./App.css";
import { useEffect, useState } from "react";
import Heder from "./components/Heder/Heder";
import LiveCamera from "./components/LiveCamera/LiveCamera";
import DataDiv from "./components/DataDiv/DataDiv";
import ImageComponent from "./components/marked_image/marked_image";
function App() {
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
      // send a message to the server when the WebSocket connection is established
      socket.send("Hello from the client!");
    };

    socket.onmessage = (event) => {
      setImageData(event.data);
      console.log("new");
    };

    return () => socket.close(); // clean up the WebSocket connection when the component unmounts
  }, []);
  return (
    <div className="App">
      <Heder />
      <div className="monitor_split">
        <div className="video_section">
          <LiveCamera image={imageData} />
          <div className="buton_and_markd_img">
            <button
              className="button"
              onClick={() => fetch("http://localhost:8000/calibrate ")}
            >
              calibrate
            </button>

            <div className="marked_image">
              <ImageComponent />
            </div>
          </div>
        </div>
        <DataDiv />
      </div>
      {/* <div className="Camera">
        <div>
          {screenshot && <img src={screenshot} alt="Webcam screenshot" />}
        </div>
      </div>
      <button className="button" onClick={() => updateScreenshot()}>
        calibrate
      </button> */}
    </div>
  );
}

export default App;
