import { useEffect, useState, useContext } from "react";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";
import axios from "axios";
import ClickMarkerContext from "../contexts/ClickMarkerContext";

function SuggestionsPage() {
    const [loading, setLoading] = useState(true);
    const [travelSuggestions, setTravelSuggestions] = useState([]);
    const { clickedMarker } = useContext(ClickMarkerContext);

    useEffect(() => {
        // Fetches comments from the backend then classify
        async function fetchAndClassifyData() {
            setLoading(true);
            console.log('Axios Base URL:', axiosInstance.defaults.baseURL);
            const results = await axiosInstance.get("comments");

            const suggestions = results.data.filter((result) => result.classification === "travel_suggestion");

            setTravelSuggestions(suggestions);

            setLoading(false);
        }

        fetchAndClassifyData();
    }, []);

    return (
        <div id="map-tip-container" className="flex w-full h-full ">
            <div className="h-[calc(100vh-4rem)] w-3/5">{!loading && <MapComponent travelSuggestions={travelSuggestions} />}</div>
            <div id="tip-container" className="h-[calc(100vh-4rem)] w-2/5 overflow-y-scroll">
                {!loading &&
                    travelSuggestions.map((travelSuggestion) => {
                        if (travelSuggestion.location_coordinates.length > 1) {
                            const placeCards = [];
                            travelSuggestion.location_coordinates.map((location) => {
                                console.log(`${location.lat}-${location.lng}` === clickedMarker);
                                console.log(`${location.lat}-${location.lng}`);
                                console.log(clickedMarker);
                                placeCards.push(
                                    <PlaceCard
                                        body={location.loc_name}
                                        key={`${location.lat}-${location.lng}`}
                                        highlight={clickedMarker ? `${location.lat}-${location.lng}` === clickedMarker : false}
                                    />
                                );
                            });

                            return <>{placeCards}</>;
                        }
                        return (
                            <PlaceCard
                                body={travelSuggestion.location_coordinates[0].loc_name}
                                key={travelSuggestion.id}
                                highlight={clickedMarker ? travelSuggestion.id == clickedMarker : false}
                            />
                        );
                    })}
            </div>
        </div>
    );
}

export default SuggestionsPage;
