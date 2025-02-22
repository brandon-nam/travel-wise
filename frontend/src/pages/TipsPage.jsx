import { useEffect, useState } from "react";
import MapComponent from "../components/MapComponent";
import TipCard from "../components/TipCard";
import axiosInstance from "../utils/AxiosInstance";

function TipsPage() {
    const [loading, setLoading] = useState(true);
    const [travelTips, setTravelTips] = useState([]);

    useEffect(() => {
        // Fetches comments from the backend then classify
        async function fetchAndClassifyData() {
            setLoading(true);
            console.log('Axios Base URL:', axiosInstance.defaults.baseURL);
            const results = await axiosInstance.get("comments");

            const tips = results.data.filter((result) => result.classification === "travel_tip");


            setTravelTips(tips);

            setLoading(false);
        }

        fetchAndClassifyData();
    }, []);

    return (
        <div id="map-tip-container" className="flex w-full h-full min-h-screen">
            <div id="tip-container" className="grow-2">
                {!loading &&
                    travelTips.map((travelTip) => {
                        return <TipCard body={travelTip.body} key={travelTip.id} />;
                    })}
            </div>
        </div>
    );
}

export default TipsPage;
