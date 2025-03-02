import axios from "axios";
import Fuse from "fuse.js";

import ClickMarkerContext from "../contexts/ClickMarkerContext";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";

import { useState, useContext } from "react";
import { useQuery, useQueries } from "@tanstack/react-query";

import { fetchComments, fetchPosts } from "../lib/API";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const { clickedPlace, handleClickDetails } = useContext(ClickDetailsContext);

    const [searchResults, setSearchResults] = useState([]);


    const showPosts = (data) => {
        console.log(data);
        return data;
    }

    const postQuery = useQuery({
        queryKey: ["posts"],
        queryFn: () => fetchPosts(),
        select: (data) => showPosts(data),
        staleTime: Infinity,
        // enabled: !!suggestionQuery.data
    });

    const postData = postQuery.data;

    const postURLSet = () => {
        const urlSet = {}; 
        postData.forEach(post => {
            urlSet[post.id] = post.url;
        }); 

        return urlSet; 
    }


    const filterAndFlattenLocations = (data) => {
        const locations = {};
        const result = [];
        const postURL = postData ? postURLSet() : {};


        let appendIndex = 0;
        data.forEach((suggestion) => {
            // Transforms data into intended data structure: {
            //  location_name, characteristic, lat, lng,
            //  comments : { id, post_id, body, score, start_date, end_date, summary }
            // }
            // from this: {
            //   id, post_id, body, score, start_date, end_date, summary,
            //   location_coordinates: { lat, lng, location_name, characteristic }
            // }

            try {
                if (suggestion.classification === "travel_suggestion") {
                    const { location_coordinates, ...rest } = suggestion;
                    location_coordinates.forEach((location) => {
                        const locationKey = `${location.lat},${location.lng}`;
                        if (!locations[locationKey]) {
                            locations[locationKey] = appendIndex;
                            // console.log(rest);
                            result[appendIndex] = {
                                location_name: location.location_name,
                                characteristic: location.characteristic,
                                lat: location.lat,
                                lng: location.lng,
                                url: postURL[rest.post_id],
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

    const suggestionQuery = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchComments(),
        select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
        enabled: !!postQuery.data
    });

    const suggestionData = suggestionQuery.data;
    

    const fuse = new Fuse(suggestionData, {
        keys: ["characteristic", "location_name"],
        threshold: 0.0, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        handleClickDetails(null, null, null, null);
        const searchText = event.target.value;

        if (searchText.trim() === "") {
            setSearchResults([]);
        } else {
            const searchsearchResults = fuse.search(searchText).map((result) => result.item);
            // console.log("searchsearchResults: ", searchsearchResults);
            setSearchResults(searchsearchResults);
        }
    };

    return (
        <div id="map-place-container" className="flex w-full h-full ">
            <div id="map-container" className="h-[calc(100vh-4rem)] w-3/5">
                {suggestionData &&
                    (searchResults.length != 0 ? (
                        <MapComponent travelSuggestions={searchResults} />
                    ) : (
                        <MapComponent travelSuggestions={suggestionData} />
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
                    {suggestionData && !clickedPlace ? (
                        searchResults.length != 0 ? (
                            // show only the searchResults
                            Object.entries(searchResults).map(([_, travelSuggestion], __) => {
                                // location_name, characteristic, lat, lng, comments : { id, post_id, body, score, start_date, end_date, summary }
                                
                                return (
                                    <PlaceCard
                                        tag={`# ${travelSuggestion.characteristic}`}
                                        body={travelSuggestion.location_name}
                                        key={`${travelSuggestion.lat}-${travelSuggestion.lng}`}
                                        highlight={
                                            clickedMarker
                                                ? `${travelSuggestion.lat}-${travelSuggestion.lng}` === clickedMarker
                                                : false
                                        }
                                        comments={travelSuggestion.comments}
                                        posts={postData}
                                    />
                                );
                            })
                        ) : (
                            // show all data
                            Object.entries(suggestionData).map(([_, travelSuggestion], __) => {
                                return (
                                    <PlaceCard
                                        tag={`# ${travelSuggestion.characteristic}`}
                                        body={travelSuggestion.location_name}
                                        key={`${travelSuggestion.lat}-${travelSuggestion.lng}`}
                                        highlight={
                                            clickedMarker
                                                ? `${travelSuggestion.lat}-${travelSuggestion.lng}` === clickedMarker
                                                : false
                                        }
                                        comments={travelSuggestion.comments}
                                        posts={postData}
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
