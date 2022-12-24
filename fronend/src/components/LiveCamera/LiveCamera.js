import React, { useEffect, useRef } from "react";
import "./LiveCamera.css";
function LiveCamera(props) {
  console.log(props);
  return (
    <div className="Live_camera_container">
      <img
        src={`data:image/jpeg;base64,${props.image}`}
        alt="Image"
        style={{ width: "640px" }}
      />
    </div>
  );
}

export default LiveCamera;
