import axios from "axios";
import Fuse from "fuse.js";

import ClickMarkerContext from "../contexts/ClickMarkerContext";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";

import { useEffect, useState, useContext } from "react";
import { useSearchParams } from "react-router";
import { useQuery } from "@tanstack/react-query";

import { fetchSuggestions, fetchPosts, fetchSuggestionsByCountry } from "../lib/API";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const { expandedElement, clickedSuggestion, handleClickPlaceDetails } = useContext(ClickDetailsContext);
    const [totalResults, setTotalResults]  = useState([]);
    const [searchResults, setSearchResults] = useState([]);
    const [sortBy, setSortBy] = useState('descending');
    const [totalSuggestions, setTotalSuggestions] = useState([]); 

    const [searchParams] = useSearchParams();
    const country = searchParams.get("country")

    const filterAndFlattenLocations = (data) => {
        const locations = {};
        const result = [];

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
                            // but we'll need to decide if we want to keep every post url or the one with the highest karma
                            comments: [rest],
                        };
                        appendIndex++;
                    } else {
                        // if two comments talk about the same location, append comment
                        const index = locations[locationKey];
                        let { comments, score, ..._ } = result[index];
                        // combine the karma scores
                        score += rest.score;
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
        queryKey: ["travelSuggestions", country],
        queryFn: () => fetchSuggestionsByCountry(country),
        select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
    });

    const suggestionData = suggestionQuery.data;

    useEffect(() => {
        if (suggestionData) {
            const sortedSuggestions = sortSuggestions(suggestionData, 'descending');
            setTotalSuggestions(sortedSuggestions); 
        }
    }, [suggestionData]);

    const fuse = new Fuse(suggestionData, {
        keys: ["characteristic", "location_name"],
        threshold: 0.0, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        handleClickPlaceDetails(null);
        const searchText = event.target.value;

        if (searchText.trim() === "") {
            setSearchResults([]);
        } else {
            const searchsearchResults = fuse.search(searchText).map((result) => result.item);
            setSearchResults(searchsearchResults);
        }
    };

    const sortSuggestions = (suggestions, sortOrder) => {
        let sortedSuggestions = [...suggestions]; // Create a copy to avoid mutating the original array
    
        sortedSuggestions.sort((a, b) => {
            if (sortOrder === 'ascending') {
                return a['score'] - b['score'];
            } else if (sortOrder === 'descending') {
                return b['score'] - a['score'];
            } else {
                // No sorting
                return 0;
            }
        })

        return sortedSuggestions;
    }


    const handleSortClick = (e) => {
        if (e.target.value === sortBy) {
            return; // if the user clicks the same sort by, do nothing. 
        }

        setSortBy(e.target.value);
        if (searchResults.length != 0) {
            const sortedCards = sortSuggestions(searchResults, e.target.value); // if the user has searched the tags, sort the results from the search. 
            setSearchResults(sortedCards);
        } else {
            console.log("suggestionData at handleSortClick: ", suggestionData);
            const sortedCards = sortSuggestions(suggestionData, e.target.value); // else, sort the total result. 
            setTotalSuggestions(sortedCards);
        }
    };

    return (
        <div id="map-place-container" className="flex w-full h-[calc(100vh-4rem)]">
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
                    <select value={sortBy} onChange={handleSortClick} name="sort">
                        <option value="descending">Karma⇂</option>
                        <option value="ascending">Karma↿</option>
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
                            Object.entries(totalSuggestions).map(([_, travelSuggestion], __) => {
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
