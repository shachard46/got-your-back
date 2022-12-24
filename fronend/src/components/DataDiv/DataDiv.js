import React, { useEffect, useRef, useState } from "react";
import "./DataDiv.css";
import ImageComponent from "../marked_image/marked_image";

function DataDiv(props) {
  const [Distanse, setDistanse] = useState(0);
  const [HeadTilt, setHeadTilt] = useState(0);
  const [HeadHight, setHeadHight] = useState(0);
  const [LastUpdate, setLastUpdate] = useState(0);

  const [Left_Right, setLeft_Right] = useState(0);
  const [Angle, setAngle] = useState(0);
  const [Top_Bootom, setTop_Bootom] = useState(0);

  return (
    <div className="Data_div_container">
      <div className="User_heder">User view</div>
      <div className="User_text">{`Last update: ${LastUpdate}`}</div>
      <div className="User_text">{`Left/Right: ${Left_Right}`}</div>
      <div className="User_text">{`Head Angle: ${Angle}`}</div>
      <div className="User_text">{`Top/Bootom: ${Top_Bootom}`}</div>
      <p></p>
      <div className="User_heder">User position</div>
      <div className="User_text">{`Last update: ${LastUpdate}`}</div>
      <div className="User_text">{`position: ${Distanse}`}</div>
      <div className="User_text">{`Head tilt: ${HeadTilt}`}</div>
      <div className="User_text">{`Head Hight: ${HeadHight}`}</div>
      <div className="marked_image">
        <ImageComponent websocket={props.websocket} />
      </div>
    </div>
  );
}

export default DataDiv;
