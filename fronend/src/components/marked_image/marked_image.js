import React, { useState, useEffect } from "react";
import "./marked_image.css";

function ImageComponent() {
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    async function fetchImage() {
      const response = await fetch("http://localhost:8000/image");
      const data = await response.json();
      setImageData(data.image);
    }
    fetchImage();
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
