import "./App.css";
import { useEffect, useState } from "react";
import Heder from "./components/Heder/Heder";
import LiveCamera from "./components/LiveCamera/LiveCamera";
import DataDiv from "./components/DataDiv/DataDiv";
function App() {
  const [imageData, setImageData] = useState(null);
  const [websocket, setwebsocket] = useState("");
  const [userData, setuserData] = useState({ "z": "null", "x": "null", "y": "null", "angle": "null" });
  useEffect(() => {
    const web = new WebSocket("ws://localhost:8000/ws")
    setwebsocket(web)
  }, [])
  useEffect(() => {
    if (websocket !== "") {
      websocket.onopen = () => {
        websocket.send("Hello from the client!");
      };

      websocket.onmessage = async (event) => {
        const text = await event.data.text();
        const json = JSON.parse(text);
        setImageData(json["live"]);
        console.log(json["live"])
        // setuserData({ "z": "null", "x": "null", "y": "null", "angle": "null" })

      }
    }

  }, [websocket]);
  useEffect(() => {
    if (websocket !== "") {
      if (websocket.readyState === 1) {
        console.log("live")

        websocket.send("Live")
      }
    }

  }, [imageData, websocket]);
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
            <button
              className="button"
              onClick={() => {
                websocket.send("Check My seating")
              }}
            >
              Check My seating
            </button>

          </div>
        </div>
        <DataDiv websocket={websocket} userData={userData} />
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
