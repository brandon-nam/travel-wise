import Fuse from "fuse.js";
import ClickMarkerContext from "../contexts/ClickMarkerContext";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import MapComponent from "../components/MapComponent";
import PlaceCard from "../components/PlaceCard";

import { useEffect, useState, useContext, useRef } from "react";
import { useSearchParams } from "react-router";
import { useSuggestions } from "../hooks/useSuggestionsData";
import { useLocationCharacteristics } from "../hooks/useLocationCharacteristics";
import { sortComments } from "../utils/sorting";
import SortDropdown from "../components/SortDropdown";
import CharacteristicsFilterContainer from "../components/CharacteristicsFilterContainer";

function SuggestionsPage() {
    const { clickedMarker } = useContext(ClickMarkerContext);
    const { expandedElement, clickedSuggestion } = useContext(ClickDetailsContext);
    const [searchCharacteristicsResults, setSearchCharacteristicsResults] = useState([]);
    const [totalSuggestions, setTotalSuggestions] = useState([]);
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [showAllPopup, setShowAllPopup] = useState(false);
    const [searchParams] = useSearchParams();

    const [searchResults, setSearchResults] = useState([]);

    const country = searchParams.get("country");

    const suggestionData = useSuggestions(country).data;

    const [isOpen, setIsOpen] = useState(false);
    const [rotation, setRotation] = useState(0);
    const dropdownRef = useRef(null);
    const showAllRef = useRef(null);

    const [characteristics, setCharacteristics] = useState([]);

    const characteristicData = useLocationCharacteristics().data;

    useEffect(() => {
        if (suggestionData) {
            const sortedSuggestions = sortComments(suggestionData, "descending");
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

                    <CharacteristicsFilterContainer
                        handleSearch={handleSearch}
                        toggleDropdown={toggleDropdown}
                        isOpen={isOpen}
                        dropdownRef={dropdownRef}
                        characteristics={searchCharacteristicsResults.length > 0 ? searchCharacteristicsResults : characteristics}
                        handleOptionSelect={handleOptionSelect}
                        selectedOptions={selectedOptions}
                        handleShowAll={handleShowAll}
                        rotation={rotation}
                    />

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
                    <SortDropdown
                        comments={searchResults.length > 0 ? searchResults : totalSuggestions}
                        setSortedComments={setSearchResults}
                    />
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
