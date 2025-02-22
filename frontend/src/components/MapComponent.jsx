import { Map, APIProvider, AdvancedMarker, Pin } from "@vis.gl/react-google-maps";
import { useEffect, useState, useContext } from "react";
import ClickMarkerContext from "../contexts/ClickMarkerContext";


function PoiMarkers({ pois }) {
    const { clickedMarker, handleClick } = useContext(ClickMarkerContext);

    return (
        <>
            {pois.map((poi) => (
                poi.location_coordinates.map((coord, index) => (
                    <AdvancedMarker
                        key={`${poi.id}-${index}`}
                        position={coord}
                        clickable={true}
                        onClick={() => handleClick(poi.id)}
                    >
                        <Pin
                            background={clickedMarker == poi.id ? "#FF0000" : "#FBBC04"}
                            glyphColor={"#000"}
                            borderColor={"#000"}
                        />
                    </AdvancedMarker>
                ))
            ))}
        </>
    );
}
function MapComponent({ suggestions }) {
    const [defaultCenter, setDefaultCenter] = useState({ lat: 0, lng: 0 });

    useEffect(() => {
        console.log('suggestions:', suggestions[0]);
        if (suggestions !== null && suggestions !== undefined && suggestions.length !== 0) {
            setDefaultCenter(suggestions[0]['location_coordinates'][0]);
        }
    }, []);

    return (
        <APIProvider apiKey={import.meta.env.VITE_MAP_API} onLoad={() => console.log("Maps API has loaded.")}>
            <Map
                style={{ width: "100vw", height: "100vh" }}
                defaultZoom={5}
                defaultCenter={defaultCenter}
                onCameraChanged={(ev) => console.log("camera changed:", ev.detail.center, "zoom:", ev.detail.zoom)}
                className="h-full w-full"
                mapId={import.meta.env.VITE_MAP_ID}
            >
                <PoiMarkers pois={suggestions} />
            </Map>
        </APIProvider>
    );
}

export default MapComponent;
