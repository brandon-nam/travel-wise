import { Map, APIProvider, AdvancedMarker, Pin } from "@vis.gl/react-google-maps";
import { useEffect, useState, useContext, memo } from "react";
import ClickMarkerContext from "../contexts/ClickMarkerContext";

function PoiMarkers({ travelSuggestions }) {
    const { clickedMarker, handleClick } = useContext(ClickMarkerContext);

    return (
        <>
            {Object.entries(travelSuggestions).map(([_, travelSuggestion], __) => {
                // console.log("travel suggestion: ", travelSuggestion)
                let lat = travelSuggestion.lat
                // console.log("lat: ", lat)
                let lng = travelSuggestion.lng
                return (
                    <AdvancedMarker
                        key={`${lat}-${lng}`}
                        position={{ lat, lng }}
                        clickable={true}
                        onClick={() => handleClick(`${lat}-${lng}`)}
                    >
                        <Pin
                            background={clickedMarker == `${lat}-${lng}` ? "#FF0000" : "#FBBC04"}
                            glyphColor={"#000"}
                            borderColor={"#000"}
                        />
                    </AdvancedMarker>
                );
            })}
        </>
    );
}
function MapComponent({ travelSuggestions }) {
    const [defaultCenter, setDefaultCenter] = useState({ lat: 36.2048, lng: 138.2529 });

    useEffect(() => {
        console.log(Object.entries(travelSuggestions));
        let [ _, suggestion ]= Object.entries(travelSuggestions)[0];
        console.log("default sugestion: ", suggestion)
        setDefaultCenter({ lat: suggestion.lat, lng: suggestion.lng });
    }, []);

    return (
        <APIProvider apiKey={import.meta.env.VITE_MAP_API} onLoad={() => console.log("Maps API has loaded.")}>
            <Map
                style={{ width: "100vw", height: "100vh" }}
                defaultZoom={5}
                defaultCenter={defaultCenter}
                className="h-full w-full"
                mapId={import.meta.env.VITE_MAP_ID}
            >
                <PoiMarkers travelSuggestions={travelSuggestions} />
            </Map>
        </APIProvider>
    );
}

export default MapComponent;
