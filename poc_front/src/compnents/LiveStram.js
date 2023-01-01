import React, { useState, useEffect, useRef } from 'react';
import tempImage from '../img/TempPhoto.png';

import './LiveStram.css';

function LiveStram(props) {
    const videoRef = useRef();
    useEffect(() => {
        if (props.takecalibrationPhoto === true) {
            props.setcalibrationPhoto(takeScreenshot())
            props.settakeScreenshot(false)
        }
    }, [props.takecalibrationPhoto])
    useEffect(() => {
        if (props.takeScreenshot === true) {
            let ls = []
            for (var i = 0; i < 2; i++) {
                ls.push(takeScreenshot())
            }
            props.setscreenshotList(ls)
            props.settakeScreenshot(false)
        }
    }, [props.takeScreenshot])
    const takeScreenshot = () => {
        // Create a canvas element
        const canvas = document.createElement('canvas');

        // Set the canvas width and height to the same as the video feed
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;

        // Get the canvas context
        const ctx = canvas.getContext('2d');

        // Draw the video frame to the canvas
        ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

        // Get the image data from the canvas
        const imageData = canvas.toDataURL();

        // Set the screenshot data in the state
        return imageData

    };

    useEffect(() => {
        navigator.getUserMedia(
            {
                video: true,
            },
            (stream) => {
                videoRef.current.srcObject = stream;
                // let video = document.getElementsByClassName('app__videoFeed')[0];
                // if (video) {
                //     video.srcObject = stream;
                // }
            },
            (err) => console.error(err)
        );
    }, [])

    return (
        <div className='All_video'>
            <video
                ref={videoRef}

                height="100%"
                muted
                autoPlay
                className="app__videoFeed"
            ></video>
            <img src={tempImage} alt="My Image" />

        </div>

    );
}

export default LiveStram;
