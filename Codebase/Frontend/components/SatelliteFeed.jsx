"use client";

import { useEffect, useState } from "react";
import socket from "../utils/socket";

export default function SatelliteFeed() {
    const [positions, setPositions] = useState([]);

    useEffect(() => {
        socket.on("positions", (data) => {
            console.log("Received positions:", data);
            setPositions(data);
        });

        return () => socket.off("positions");
    }, []);

    return (
        <div style={{ padding: "1rem" }}>
            <h2>🛰 Live Satellite Positions</h2>
            <pre>{JSON.stringify(positions, null, 2)}</pre>
        </div>
    );
}