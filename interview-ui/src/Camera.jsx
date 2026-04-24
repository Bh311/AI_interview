import React, { useEffect, useRef } from "react";

function Camera() {
  const videoRef = useRef(null);

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div className="mb-4">
      <video
        ref={videoRef}
        autoPlay
        className="w-full rounded"
      />
    </div>
  );
}

export default Camera;