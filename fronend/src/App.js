import "./App.css";
import { useEffect, useState, useRef } from "react";
import Heder from "./components/Heder/Heder";
import LiveCamera from "./components/LiveCamera/LiveCamera";
import DataDiv from "./components/DataDiv/DataDiv";
import ImageComponent from "./components/marked_image/marked_image";
function App() {
  const [imageData, setImageData] = useState(null);
  const [websocket, setwebsocket] = useState(null);
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");
    setwebsocket(socket)
    socket.onopen = () => {
      socket.send("Hello from the client!");
    };

    socket.onmessage = (event) => {
      let url = URL.createObjectURL(event.data);
      setImageData(url);
      console.log("new");
    };

    return () => socket.close(); // clean up the WebSocket connection when the component unmounts
  }, []);
  useEffect(() => {
    if (websocket !== null) {
      websocket.send("Live")

    }
  }, [imageData]);
  return (
    <div className="App">
      <Heder />
      <div className="monitor_split">
        <div className="video_section">
          <LiveCamera image={imageData} />
          <div className="buton_and_markd_img">
            <button
              className="button"
              onClick={() => {
                console.log(websocket)
                websocket.send("Calibrate")
              }}
            >
              calibrate
            </button>

            <div className="marked_image">
              {/* <ImageComponent /> */}
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
