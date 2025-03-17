import Fuse from "fuse.js";
import ClickMarkerContext from "../contexts/ClickMarkerContext";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import MapComponent from "../components/MapComponent";
import PlaceCard from "../components/PlaceCard";
import { useEffect, useState, useContext, useRef } from "react";
import { useSearchParams } from "react-router";
import { useQuery } from "@tanstack/react-query";
import { fetchSuggestionsByCountry, fetchCharacteristics } from "../lib/API";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const { expandedElement, clickedSuggestion } = useContext(ClickDetailsContext);
    const [searchCharacteristicsResults, setSearchCharacteristicsResults] = useState([]);
    const [sortBy, setSortBy] = useState("descending");
    const [totalSuggestions, setTotalSuggestions] = useState([]);
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [showAllPopup, setShowAllPopup] = useState(false);
    const [searchParams] = useSearchParams();

    const [searchResults, setSearchResults] = useState([]);

    const country = searchParams.get("country");

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

    const sortSuggestions = (suggestions, sortOrder) => {
        let sortedSuggestions = [...suggestions]; // Create a copy to avoid mutating the original array
        sortedSuggestions.sort((a, b) => {
            if (sortOrder === "ascending") {
                return a["score"] - b["score"];
            } else if (sortOrder === "descending") {
                return b["score"] - a["score"];
            } else {
                // No sorting

                return 0;
            }
        });

        return sortedSuggestions;
    };

    const handleSortClick = (e) => {
        if (e.target.value === sortBy) {
            return; // if the user clicks the same sort by, do nothing.
        }
        setSortBy(e.target.value);
        if (searchResults.length != 0) {
            const sortedCards = sortSuggestions(searchResults, e.target.value); // if the user has searched the tags, sort the results from the search.
            setSearchCharacteristicsResults(sortedCards);
        } else {
            console.log("suggestionData at handleSortClick: ", suggestionData);
            const sortedCards = sortSuggestions(suggestionData, e.target.value); // else, sort the total result.
            setTotalSuggestions(sortedCards);
        }
    };

    const [isOpen, setIsOpen] = useState(false);
    const [rotation, setRotation] = useState(0);
    const dropdownRef = useRef(null);
    const showAllRef = useRef(null);

    const [characteristics, setCharacteristics] = useState([]);

    const characteristicQuery = useQuery({
        queryKey: ["suggestionsCharacteristics"],
        queryFn: () => fetchCharacteristics("travel-suggestion"),
        staleTime: Infinity,
    });

    const characteristicData = characteristicQuery.data;

    useEffect(() => {
        if (suggestionData) {
            const sortedSuggestions = sortSuggestions(suggestionData, "descending");
            setTotalSuggestions(sortedSuggestions);
        }
    }, [suggestionData]);

    useEffect(() => {
        if (characteristicData) {
            setCharacteristics(characteristicData);
        }
    }, [characteristicData]);

    const fuse = new Fuse(characteristicData, {
        keys: ["characteristic"],
        threshold: 0.0, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        const searchText = event.target.value;
        if (searchText.trim() === "") {
            setSearchCharacteristicsResults([]);
        } else {
            const characteristicsData = fuse.search(searchText).map((result) => result.item);

            setSearchCharacteristicsResults(characteristicsData);
        }
    };

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
        setRotation(rotation + 360);
    };

    const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setIsOpen(false);
        }
    };

    const handleClickOutsideShowAll = (event) => {
        if (showAllRef.current && !showAllRef.current.contains(event.target)) {
            setShowAllPopup(false);
        }
    };

    const handleOptionSelect = (optionValue) => {
        if (selectedOptions.includes(optionValue)) {
            setSelectedOptions(selectedOptions.filter((opt) => opt !== optionValue));
        } else {
            setSelectedOptions([...selectedOptions, optionValue]);
        }
    };

    const handleOptionsChange = () => {
        const filtered = totalSuggestions.filter((suggestion) => selectedOptions.includes(suggestion.characteristic));
        console.log("filtered: ", filtered);
        setSearchResults(filtered);
    };

    useEffect(() => {
        console.log(selectedOptions);
        handleOptionsChange();
    }, [selectedOptions]);

    const handleShowAll = () => {
        setIsOpen(false);
        setShowAllPopup(true);
    };

    const popupStyles = {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.5)", // Greyed out background
    };

    const closePopup = () => {
        setShowAllPopup(false);
        setIsOpen(false);
    };

    useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);
        document.addEventListener("mousedown", handleClickOutsideShowAll);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
            document.removeEventListener("mousedown", handleClickOutsideShowAll);
        };
    }, []);

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
                    <div className="h-full bg-white rounded-full shadow flex items-center"></div>
                    <div className="h-full bg-white rounded-full shadow flex items-center relative">
                        <input
                            className="h-full px-3 flex-grow border-none outline-none"
                            type="text"
                            onChange={handleSearch}
                            onClick={toggleDropdown}
                        />

                        {isOpen && (
                            <div
                                ref={dropdownRef}
                                className="absolute top-full left-0 w-full bg-white rounded-[10%] shadow-md mt-1 overflow-hidden"
                            >
                                <ul className="overflow-y-auto max-h-[200px]">
                                    {searchCharacteristicsResults.length > 0
                                        ? searchCharacteristicsResults.map((option) => (
                                            <div onClick={() => handleOptionSelect(option)}>
                                                <li
                                                    key={option}
                                                    className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
                                                >
                                                    <input
                                                        type="checkbox"
                                                        id={option}
                                                        checked={selectedOptions.includes(option)}
                                                        onChange={() => {}}
                                                        className="mr-2"
                                                    />
                                                    <div className="cursor-pointer">{option}</div>
                                                </li>
                                            </div>
                                        ))
                                        : characteristics.map((option) => (
                                            <div onClick={() => handleOptionSelect(option)}>
                                                <li
                                                    key={option}
                                                    className="px-3 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
                                                >
                                                    <input
                                                        type="checkbox"
                                                        id={option}
                                                        checked={selectedOptions.includes(option)}
                                                        onChange={() => {}}
                                                        className="mr-2"
                                                    />
                                                    <div className="cursor-pointer">{option}</div>
                                                </li>
                                            </div>
                                        ))}
                                </ul>

                                <div
                                    className="w-full px-3 py-2 hover:bg-gray-100 cursor-pointer text-center"
                                    onClick={handleShowAll}
                                >
                                    Show All Categories
                                </div>
                            </div>
                        )}

                        <button
                            className="px-3 transition-transform duration-300"
                            style={{ transform: `rotate(${rotation}deg)` }}
                            onClick={toggleDropdown}
                        >
                            ✈️
                        </button>
                    </div>

                    {showAllPopup && (
                        <div style={popupStyles} className="flex items-center justify-center">
                            <div className="bg-white p-6 rounded shadow-lg" ref={showAllRef}>
                                <p>All Categories</p>
                                <ul className="mt-2 grid grid-cols-5 gap-2">
                                    {characteristics.map((option) => (
                                        <div onClick={() => handleOptionSelect(option)}>
                                            <li
                                                key={option}
                                                className="px-2 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
                                            >
                                                <input
                                                    type="checkbox"
                                                    id={option}
                                                    checked={selectedOptions.includes(option)}
                                                    onChange={() => handleOptionSelect(option)}
                                                    className="mr-2"
                                                />
                                                <div className="cursor-pointer">{option}</div>
                                            </li>
                                        </div>
                                    ))}
                                </ul>

                                <button
                                    className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:cursor-pointer"
                                    onClick={closePopup}
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    )}

                    <select value={sortBy} onChange={handleSortClick} name="sort" className="ml-5">
                        <option value="descending">Popularity⇂</option>
                        <option value="ascending">Popularity↿</option>
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
