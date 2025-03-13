import axios from "axios";
import Fuse from "fuse.js";

import ClickMarkerContext from "../contexts/ClickMarkerContext";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";

import { useState, useContext } from "react";
import { useQuery } from "@tanstack/react-query";

import { fetchSuggestions, fetchPosts } from "../lib/API";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const { expandedElement, clickedSuggestion, handleClickPlaceDetails } = useContext(ClickDetailsContext);

    const [searchResults, setSearchResults] = useState([]);

    const postQuery = useQuery({
        queryKey: ["posts"],
        queryFn: () => fetchPosts(),
        staleTime: Infinity,
        // enabled: !!suggestionQuery.data
    });

    const postData = postQuery.data;

    const postURLSet = () => {
        const urlSet = {};
        postData.forEach((post) => {
            urlSet[post.id] = post.url;
        });

        return urlSet;
    };

    const filterAndFlattenLocations = (data) => {
        const locations = {};
        const result = [];
        const postURL = postData ? postURLSet() : {};

        let appendIndex = 0;
        data.forEach((suggestion) => {
            try {
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
                            score: rest.score, // score of the first comment
                            postURL: postURL[rest.post_id], // url of the first comment,
                            // but we'll need to decide if we want to keep every post url or the one with the highest karma
                            comments: [rest],
                        };
                        appendIndex++;
                    } else {
                        // if two comments talk about the same location, append comment
                        const index = locations[locationKey];
                        let { comments, score, ..._ } = result[index];
                        // only keep the higher karma score
                        if (score < rest.score) {
                            score = rest.score;
                        }
                        comments = [...comments, rest]; // appending rest
                        result[index]["comments"] = comments;
                        result[index]["score"] = score; 
                    }
                });
            } catch (e) {
                console.log("error: ", e);
            }
        });

        console.log(result);
        return result;
    };

    const suggestionQuery = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchSuggestions(),
        select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
        enabled: !!postQuery.data,
    });

    const suggestionData = suggestionQuery.data;

    const fuse = new Fuse(suggestionData, {
        keys: ["characteristic", "location_name"],
        threshold: 0.0, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        handleClickPlaceDetails(null, null, null, null);
        const searchText = event.target.value;

        if (searchText.trim() === "") {
            setSearchResults([]);
        } else {
            const searchsearchResults = fuse.search(searchText).map((result) => result.item);
            setSearchResults(searchsearchResults);
        }
    };

    return (
        <div id="map-place-container" className="flex w-full h-full ">
            <div id="map-container" className="h-[calc(100vh-4rem)] w-3/5">
                {suggestionData &&
                    (clickedSuggestion.length > 0 ? (
                        <MapComponent travelSuggestions={clickedSuggestion} />
                    ) : searchResults.length != 0 ? (
                        <MapComponent travelSuggestions={searchResults} />
                    ) : (
                        <MapComponent travelSuggestions={suggestionData} />
                    ))}
            </div>
            <div id="place-container" className="h-[calc(100vh-4rem)] w-2/5 flex flex-col">
                <div id="search-place-tag-field" className="fixed flex flex-row w-2/5 bg-gray-100 h-20 py-5 px-3">
                    <input
                        type="text"
                        className="bg-white shadow rounded-full h-10 w-full px-5 mr-3"
                        placeholder="Search for tags"
                        onChange={handleSearch}
                    ></input>
                    <select name="sort">
                        <option>Karma⇂</option>
                        <option>Karma↿</option>
                    </select>
                </div>
                <div id="search-place-tag-field-space" className="py-10"></div>
                {expandedElement && expandedElement}
                <div className="overflow-y-scroll">
                    {suggestionData && !expandedElement ? (
                        searchResults.length != 0 ? (
                            // show only the searchResults
                            Object.entries(searchResults).map(([_, travelSuggestion], __) => {
                                // location_name, characteristic, lat, lng, comments : { id, post_id, body, score, start_date, end_date, summary }
                                const coordinate = `${travelSuggestion.lat}-${travelSuggestion.lng}`;

                                return (
                                    <PlaceCard
                                        key={coordinate}
                                        highlight={clickedMarker ? coordinate === clickedMarker : false}
                                        suggestion={travelSuggestion}
                                    />
                                );
                            })
                        ) : (
                            // show all data
                            Object.entries(suggestionData).map(([_, travelSuggestion], __) => {
                                const coordinate = `${travelSuggestion.lat}-${travelSuggestion.lng}`;

                                return (
                                    <PlaceCard
                                        key={coordinate}
                                        highlight={clickedMarker ? coordinate === clickedMarker : false}
                                        suggestion={travelSuggestion}
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
