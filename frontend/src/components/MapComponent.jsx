import { Map, APIProvider } from "@vis.gl/react-google-maps";

function MapComponent() {
    return (
        <APIProvider apiKey={import.meta.env.VITE_MAP_API} onLoad={() => console.log("Maps API has loaded.")}>
            <Map
                style={{ width: "100vw", height: "100vh" }}
                defaultZoom={13}
                defaultCenter={{ lat: -33.860664, lng: 151.208138 }}
                onCameraChanged={(ev) => console.log("camera changed:", ev.detail.center, "zoom:", ev.detail.zoom)}
                className="h-full w-full"
            ></Map>
        </APIProvider>
    );
}

export default MapComponent;
