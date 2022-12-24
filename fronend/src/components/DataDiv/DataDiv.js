import React, { useEffect, useRef, useState } from "react";
import "./DataDiv.css";
function DataDiv() {
  const [Distanse, setDistanse] = useState(0);
  const [HeadTilt, setHeadTilt] = useState(0);
  const [HeadHight, setHeadHight] = useState(0);
  const [LastUpdate, setLastUpdate] = useState(0);

  return (
    <div className="Data_div_container">
      <div className="User_heder">User view</div>
      <div className="User_text">{`Last update: ${LastUpdate}`}</div>
      <div className="User_text">{`Distanse: ${Distanse}`}</div>
      <div className="User_text">{`Head tilt: ${HeadTilt}`}</div>
      <div className="User_text">{`Head Hight: ${HeadHight}`}</div>
    </div>
  );
}

export default DataDiv;
