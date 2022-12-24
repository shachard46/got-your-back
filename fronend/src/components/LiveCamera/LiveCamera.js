import React, { useEffect, useRef } from "react";
import "./LiveCamera.css";
function LiveCamera(props) {
  return (
    <div className="Live_camera_container">
      <img src={props.image} alt="My Image" style={{ width: "640px" }} />
    </div>
  );
}

export default LiveCamera;
