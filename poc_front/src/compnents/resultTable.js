import React, { useEffect, useState } from 'react';
import './ResultTable.css';

function ResultTable(props) {
    const [x, setX] = useState("none")
    const [y, setY] = useState("none")
    const [z, setZ] = useState("none")
    const [angle, setAngle] = useState("none")

    useEffect(() => {
        console.log(props.result)
        if (props.result !== null) {
            setX(props.result["x"])
            setY(props.result["y"])
            setZ(props.result["z"])
            setAngle(props.result["angle"])
        }
    }, [props.result])
    return (
        <div className="ResultTable">
            <div className='heder'>
                <div>X</div>
                <div>Y</div>
                <div>Z</div>
                <div>angle</div>
            </div>
            <div className='msg'>
                <div>{x ? x["msg"] : "none"}</div>
                <div>{y ? y["msg"] : "none"}</div>
                <div>{z ? z["msg"] : "none"}</div>
                <div>{angle ? angle["msg"] : "none"}</div>
            </div>
            <div className='pos'>
                <div>{x ? x["pos"] : "none"}</div>
                <div>{y ? y["pos"] : "none"}</div>
                <div>{z ? z["pos"] : "none"}</div>
                <div>{angle ? angle["pos"] : "none"}</div>
            </div>
        </div>
    );
}

export default ResultTable;
