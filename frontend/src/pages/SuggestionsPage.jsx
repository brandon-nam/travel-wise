import axios from "axios";
import Fuse from "fuse.js";

import ClickMarkerContext from "../contexts/ClickMarkerContext";
import MapComponent from "../components/MapComponent";

import PlaceCard from "../components/PlaceCard";

import { useEffect, useState, useContext } from "react";
import { useQuery } from "@tanstack/react-query";

import { fetchComments } from "../lib/API";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);

    const filterAndFlattenLocations = (data) => {

        return data.flatMap((suggestion) => {
            if (suggestion.classification === "travel_suggestion") {
                return suggestion.location_coordinates.map((location) => ({
                    ...suggestion,
                    location_coordinates: location, // Single location object
                }));
            }
            return [];
        });
    };

    const { isLoading, data, error } = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchComments(),
        select: (data) => data.filter((result) => result.classification === "travel_suggestion"),
        // select: (data) => filterAndFlattenLocations(data),
        staleTime: Infinity,
    });

    const fuse = new Fuse(data, {
        keys: [
            "characteristic",
            "location_coordinates.characteristic", // Search nested fields
        ],
        threshold: 0.3, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        const searchText = event.target.value;
        setQuery(searchText);

        if (searchText.trim() === "") {
            setResults([]);
        } else {
            const searchResults = fuse.search(searchText).map((result) => result.item);
            console.log("searchResults: ", searchResults);
            setResults(searchResults);
        }
    };

    return (
        <div id="map-place-container" className="flex w-full h-full ">
            <div id="map-container" className="h-[calc(100vh-4rem)] w-3/5">
                {!isLoading &&
                    (results.length != 0 ? (
                        <MapComponent travelSuggestions={results} />
                    ) : (
                        <MapComponent travelSuggestions={data} />
                    ))}
            </div>
            <div id="place-container" className="h-[calc(100vh-4rem)] w-2/5 overflow-y-scroll">
                <div id="search-tag-field" className="fixed w-2/5 bg-gray-100 h-20 py-5 px-3">
                    <input
                        type="text"
                        className="bg-white shadow rounded-full h-10 w-full px-5"
                        placeholder="Search for tags"
                        onChange={handleSearch}
                    ></input>
                </div>
                <div id="search-tag-field-space" className="w-full h-20"></div>
                {!isLoading &&
                    (results.length != 0
                        ? results.map((travelSuggestion) => {
                              // If a comment has multiple locations, separate each location into a PlaceCard.
                              if (travelSuggestion.location_coordinates.length > 1) {
                                  const placeCards = [];
                                  travelSuggestion.location_coordinates.map((location) => {
                                      placeCards.push(
                                          <PlaceCard
                                              tag={location.characteristic}
                                              body={location.location_name}
                                              key={`${location.lat}-${location.lng}`}
                                              highlight={
                                                  clickedMarker ? `${location.lat}-${location.lng}` === clickedMarker : false
                                              }
                                          />
                                      );
                                  });

                                  return <>{placeCards}</>;
                              }

                              // Else, the comment has only one location. Show it in a PlaceCard.
                              return (
                                  <PlaceCard
                                      tag={travelSuggestion.location_coordinates[0].characteristic}
                                      body={travelSuggestion.location_coordinates[0].location_name}
                                      key={travelSuggestion.id}
                                      highlight={clickedMarker ? travelSuggestion.id == clickedMarker : false}
                                  />
                              );
                          })
                        //   : console.log(data)
                        // )}
                        
                        : data.map((travelSuggestion) => {
                              // If a comment has multiple locations, separate each location into a PlaceCard.
                              if (travelSuggestion.location_coordinates.length > 1) {
                                  const placeCards = [];
                                  travelSuggestion.location_coordinates.map((location) => {
                                      placeCards.push(
                                          <PlaceCard
                                              tag={location.characteristic}
                                              body={location.location_name}
                                              key={`${location.lat}-${location.lng}`}
                                              highlight={
                                                  clickedMarker ? `${location.lat}-${location.lng}` === clickedMarker : false
                                              }
                                          />
                                      );
                                  });

                                  return <>{placeCards}</>;
                              }

                              // Else, the comment has only one location. Show it in a PlaceCard.
                              return (
                                  <PlaceCard
                                      tag={travelSuggestion.location_coordinates[0].characteristic}
                                      body={travelSuggestion.location_coordinates[0].location_name}
                                      key={travelSuggestion.id}
                                      highlight={clickedMarker ? travelSuggestion.id == clickedMarker : false}
                                  />
                              );
                          }))}
            </div>
        </div>
    );
}

export default SuggestionsPage;
