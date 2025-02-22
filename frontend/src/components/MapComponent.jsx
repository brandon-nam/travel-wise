import { Map, APIProvider, AdvancedMarker, Pin } from "@vis.gl/react-google-maps";
import { useEffect, useState, useContext } from "react";
import ClickMarkerContext from "../contexts/ClickMarkerContext";

function PoiMarkers({ travelSuggestions }) {
    const { clickedMarker, handleClick } = useContext(ClickMarkerContext);

    return (
        <>
            {travelSuggestions.map((travelSuggestion) =>
                travelSuggestion.location_coordinates.map(({characteristic, lat, lng, loc_name}) => {
                    return (
                        <AdvancedMarker
                            key={`${lat}-${lng}`}
                            position={{ lat, lng }}
                            clickable={true}
                            onClick={() => handleClick(`${lat}-${lng}`)}
                        >
                            <Pin
                                background={clickedMarker == `${lat}-${lng}`? "#FF0000" : "#FBBC04"}
                                glyphColor={"#000"}
                                borderColor={"#000"}
                            />
                        </AdvancedMarker>
                    );
                })
            )}
        </>
    );
}
function MapComponent({ travelSuggestions }) {
    const [defaultCenter, setDefaultCenter] = useState({ lat: 0, lng: 0 });

    useEffect(() => {
        console.log("suggestions:", travelSuggestions);
        setDefaultCenter(travelSuggestions[0]["location_coordinates"][0]);
    }, [defaultCenter]);

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
