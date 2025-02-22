import axios from "axios";

import ClickMarkerContext from "../contexts/ClickMarkerContext";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";

import { useEffect, useState, useContext } from "react";
import { useQuery } from "@tanstack/react-query"

import { fetchComments } from "../lib/API";


function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);

    const { isLoading, data, error } = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchComments(),
        select: (data) => data.filter((result) => result.classification === "travel_suggestion"),
        staleTime: Infinity
    })

    return (
        <div id="map-tip-container" className="flex w-full h-full ">
            <div className="h-[calc(100vh-4rem)] w-3/5">{!isLoading && <MapComponent travelSuggestions={data} />}</div>
            <div id="tip-container" className="h-[calc(100vh-4rem)] w-2/5 overflow-y-scroll">
                {!isLoading &&
                    data.map((travelSuggestion) => {
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
