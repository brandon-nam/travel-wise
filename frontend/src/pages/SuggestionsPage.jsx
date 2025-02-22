import { useEffect, useState, useContext } from "react";
import MapComponent from "../components/MapComponent";
import TipCard from "../components/TipCard";
import axiosInstance from "../utils/AxiosInstance";
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
            <div className="h-[calc(100vh-4rem)] w-3/5">{!loading && <MapComponent suggestions={travelSuggestions} />}</div>
            <div id="tip-container" className="h-[calc(100vh-4rem)] w-2/5 overflow-y-scroll">
                {!loading &&
                    travelSuggestions.map((travelTip) => {
                        return <TipCard body={travelTip.body} key={travelTip.id} highlight={clickedMarker ? travelTip.id == clickedMarker : false}/>;
                    })}
            </div>
        </div>
    );
}

export default SuggestionsPage;
