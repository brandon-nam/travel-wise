import axios from "axios";
import Fuse from "fuse.js";

import ClickMarkerContext from "../contexts/ClickMarkerContext";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";

import { useState, useContext } from "react";
import { useQuery } from "@tanstack/react-query";

import { fetchComments } from "../lib/API";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const { clickedPlace, handleClickDetails } = useContext(ClickDetailsContext);

    const [query, setQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);

    const filterAndFlattenLocations = (data) => {
        const locations = {};
        const result = [];
        let appendIndex = 0;
        data.forEach((suggestion) => {
            // Intended data structure: {
            //  location_name, characteristic, lat, lng,
            //  comments : { id, post_id, body, score, start_date, end_date, summary
            // }}
            // right now: {
            //   id, post_id, body, score, start_date, end_date, summary,
            //   location_coordinates: { lat, lng, location_name, characteristic }
            //}
            // rest: { id, post_id, body, score, start_date, end_date, summary }
            try {
                if (suggestion.classification === "travel_suggestion") {
                    const { location_coordinates, ...rest } = suggestion;
                    location_coordinates.forEach((location) => {
                        const locationKey = `${location.lat},${location.lng}`;
                        if (!locations[locationKey]) {
                            locations[locationKey] = appendIndex;

                            result[appendIndex] = {
                                location_name: location.location_name,
                                characteristic: location.characteristic,
                                lat: location.lat,
                                lng: location.lng,
                                comments: [rest],
                            };
                            appendIndex++;
                        } else {
                            const index = locations[locationKey];
                            let { comments, ..._ } = result[index];
                            comments = [...comments, rest];
                            result[index]["comments"] = comments;
                        }
                    });
                }
            } catch (e) {
                console.log("error: ", e);
            }
        });

        console.log(result);
        return result;
    };

    const { isLoading, data, error } = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchComments(),
        select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
    });

    const fuse = new Fuse(data, {
        keys: ["characteristic", "location_name"],
        threshold: 0.0, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        handleClickDetails(null, null, null);
        const searchText = event.target.value;
        setQuery(searchText);

        if (searchText.trim() === "") {
            setSearchResults([]);
        } else {
            const searchsearchResults = fuse.search(searchText).map((result) => result.item);
            console.log("searchsearchResults: ", searchsearchResults);
            setSearchResults(searchsearchResults);
        }
    };

    return (
        <div id="map-place-container" className="flex w-full h-full ">
            <div id="map-container" className="h-[calc(100vh-4rem)] w-3/5">
                {!isLoading &&
                    (searchResults.length != 0 ? (
                        <MapComponent travelSuggestions={searchResults} />
                    ) : (
                        <MapComponent travelSuggestions={data} />
                    ))}
            </div>
            <div id="place-container" className="h-[calc(100vh-4rem)] w-2/5 flex flex-col">
                <div id="search-place-tag-field" className="fixed w-2/5 bg-gray-100 h-20 py-5 px-3">
                    <input
                        type="text"
                        className="bg-white shadow rounded-full h-10 w-full px-5"
                        placeholder="Search for tags"
                        onChange={handleSearch}
                    ></input>
                </div>
                <div id="search-place-tag-field-space" className="py-10"></div>
                {clickedPlace && clickedPlace}
                <div className="overflow-y-scroll">
                    {!isLoading && !clickedPlace ? (
                        searchResults.length != 0 ? (
                            Object.entries(searchResults).map(([_, travelSuggestion], __) => {
                                // location_name, characteristic, lat, lng, comments : { id, post_id, body, score, start_date, end_date, summary }
                                return (
                                    <PlaceCard
                                        tag={travelSuggestion.characteristic}
                                        body={travelSuggestion.location_name}
                                        key={`${travelSuggestion.lat}-${travelSuggestion.lng}`}
                                        highlight={
                                            clickedMarker
                                                ? `${travelSuggestion.lat}-${travelSuggestion.lng}` === clickedMarker
                                                : false
                                        }
                                        expanded={false}
                                        comments={travelSuggestion.comments}
                                    />
                                );
                            })
                        ) : (
                            Object.entries(data).map(([_, travelSuggestion], __) => {
                                return (
                                    <PlaceCard
                                        tag={travelSuggestion.characteristic}
                                        body={travelSuggestion.location_name}
                                        key={`${travelSuggestion.lat}-${travelSuggestion.lng}`}
                                        highlight={
                                            clickedMarker
                                                ? `${travelSuggestion.lat}-${travelSuggestion.lng}` === clickedMarker
                                                : false
                                        }
                                        expanded={false}
                                        comments={travelSuggestion.comments}
                                    />
                                );
                            })
                        )
                    ) : (
                        <></>
                    )}
                </div>
            </div>
        </div>
    );
}

export default SuggestionsPage;
