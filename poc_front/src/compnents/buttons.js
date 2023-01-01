import React from 'react';
import './buttons.css'
function Buttons(props) {
    const calibrate_system = () => {
        // let URL = 'http://localhost:8000/calibrate_system'
        // fetch(URL)
        //     .then(response => response.json().then(data =>
        //         console.log(data)
        //     ))
        //     .then(data => console.log(data))
        //     .catch(error => console.error(error));
        props.settakecalibrationPhoto(true)
    }
    const check_my_seating = () => {
        let URL = 'http://localhost:8000/check_my_seating'
        fetch(URL)
            .then(response => response.json().then(data =>
                console.log(data)
            ))
            .then(data => console.log(data))
            .catch(error => console.error(error));
    }

    return (
        <div className="buttons">
            <button class="button-34" onClick={() => { calibrate_system() }}>Calibrate system</button>
            <button class="button-34" onClick={() => { check_my_seating() }}>Check my seating</button>
            <button class="button-34" onClick={() => { props.settakeScreenshot(true) }}>Interval check</button>

        </div>
    );
}

export default Buttons;
