import React, { useEffect, useState } from 'react';
import './buttons.css'
import 'react-notifications/lib/notifications.css';
import { NotificationContainer, NotificationManager } from 'react-notifications';

function Buttons(props) {
    const [style, setStyle] = useState({});

    const calibrate_system = () => {
        props.settakecalibrationPhoto(true)

    }

    useEffect(() => {
        if (props.calibrationPhoto === null)
            setStyle({
                backgroundColor: '#333333',
            })
        else {
            setStyle({
                backgroundColor: '#5E5DF0',
            })
        }
    }, [props.calibrationPhoto])
    return (
        <div className="buttons">
            <button class="button-34" onClick={() => { calibrate_system() }}>Calibrate system</button>
            {/* <button class="button-34" onClick={() => { check_my_seating() }}>Check my seating</button> */}
            <button class="button-34" style={style} onClick={() => { props.settakeScreenshot(true) }}>Check my seating</button>

        </div>
    );
}

export default Buttons;
