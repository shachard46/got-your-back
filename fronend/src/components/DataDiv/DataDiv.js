import React, { useEffect, useRef, useState } from "react";
import "./DataDiv.css";
import ImageComponent from "../marked_image/marked_image";

function DataDiv(props) {
  useEffect(() => {
    setLeft_Right(props.userData["x"])
    setAngle(props.userData["angle"])
    setTop_Bootom(props.userData["y"])
    setfront_back(props.userData["z"])
    const currentDate = new Date(Date.now());
    const formattedDate = currentDate.toLocaleString("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "2-digit",
      hour: "2-digit",
      minute: "2-digit"
    });
    setLastUpdate(formattedDate)
    // const currentTimestamp = Date.now();

  }, [props.userData["x"], props.userData["angle"], props.userData["y"], props.userData["z"]]);
  const [Distanse, setDistanse] = useState(0);
  const [HeadTilt, setHeadTilt] = useState(0);
  const [HeadHight, setHeadHight] = useState(0);
  const [LastUpdate, setLastUpdate] = useState(0);

  const [Left_Right, setLeft_Right] = useState(props.userData["x"]);
  const [Angle, setAngle] = useState(props.userData["angle"]);
  const [Top_Bootom, setTop_Bootom] = useState(props.userData["y"]);
  const [front_back, setfront_back] = useState(props.userData["z"]);

  return (
    <div className="Data_div_container">
      <div className="User_heder">User view</div>
      <div className="User_text">{`Last update: ${LastUpdate}`}</div>
      <div className="User_text">{`Left/Right: ${Left_Right}`}</div>
      <div className="User_text">{`Head Angle: ${Angle}`}</div>
      <div className="User_text">{`Top/Bootom: ${Top_Bootom}`}</div>
      <div className="User_text">{`front/back: ${front_back}`}</div>
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
