import React, { useState, createContext } from 'react';

const ClickMarkerContext = createContext();

export function ClickMarkerProvider({ children }) {
    const [clickedMarker, setClickedMarker] = useState("");

    function handleClick(marker) {
        setClickedMarker(marker);
    }

    return (
        <ClickMarkerContext.Provider value={{ clickedMarker, handleClick }}>
            {children}
        </ClickMarkerContext.Provider>
    );
}

export default ClickMarkerContext;