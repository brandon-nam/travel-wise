import TipCard from "../components/TipCard";

import { useQuery } from "@tanstack/react-query";

function TipsPage() {

    const { isLoading, data, error } = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchComments(),
        select: (data) => data.filter((result) => result.classification === "travel_tip"),
        staleTime: Infinity
    })

    return (
        <div id="map-tip-container" className="flex w-full h-full min-h-screen">
            <div id="tip-container" className="grow-2">
                {!isLoading &&
                    data.map((travelTip) => {
                        return <TipCard body={travelTip.body} key={travelTip.id} />;
                    })}
            </div>
        </div>
    );
}

export default TipsPage;
