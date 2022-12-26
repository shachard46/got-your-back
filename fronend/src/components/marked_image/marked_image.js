import React, { useState, useEffect } from "react";
import "./marked_image.css";

function ImageComponent(props) {
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    async function fetchImage() {
      props.websocket.send("ImageComponent")
    }
  }, []);
  return (
    <img
      src={`data:image/jpeg;base64,${imageData}`}
      alt="Image"
      style={{ height: "144px" }}
    />
  );
}

export default ImageComponent;
