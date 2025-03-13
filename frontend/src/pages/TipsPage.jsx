import Fuse from "fuse.js";

import TipCard from "../components/TipCard";

import { useState, useContext, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchComments, fetchPosts, fetchTips } from "../lib/API";
import ClickDetailsContext from "../contexts/ClickDetailsContext";

function TipsPage() {
    const [query, setQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [sortBy, setSortBy] = useState('descending');
    const [totalTips, setTotalTips] = useState([]);
    const { expandedElement, handleClickTipDetails } = useContext(ClickDetailsContext);

    const postQuery = useQuery({
        queryKey: ["posts"],
        queryFn: () => fetchPosts(),
        staleTime: Infinity,
    });

    const postData = postQuery.data;

    const postURLSet = () => {
        const urlSet = {};
        postData.forEach((post) => {
            urlSet[post.id] = post.url;
        });

        return urlSet;
    };

    const filterTipsAndAddPostURL = (data) => {
        const postURL = postData ? postURLSet() : {};
        const result = [];
        console.log("postURLs: ", postURL);
        data.forEach((suggestion) => {
            let newTip = { ...suggestion };
            newTip["post_url"] = postURL[suggestion.post_id];
            result.push(newTip);
        });

        console.log("result:", result);
        return result;
    };

    const tipsQuery = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchTips(),
        select: (data) => filterTipsAndAddPostURL(data),
        staleTime: Infinity,
        enalbed: !!postQuery.data,
    });

    const tipsData = tipsQuery.data;

    useEffect(() => {
        if (tipsData) {
            setTotalTips(tipsData);
        }
    }, [tipsData])

    const fuse = new Fuse(tipsData, {
        keys: ["characteristic", "summary"],
        threshold: 0.1, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        handleClickTipDetails(null);
        const searchText = event.target.value;
        setQuery(searchText);

        if (searchText.trim() === "") {
            setSearchResults([]);
        } else {
            const searchResults = fuse.search(searchText).map((result) => result.item);
            console.log("searchResults: ", searchResults);
            setSearchResults(searchResults);
        }
    };

    const sortTips = (suggestions, sortOrder) => {
        let sortedTips = [...suggestions]; // Create a copy to avoid mutating the original array
    
        sortedTips.sort((a, b) => {
            if (sortOrder === 'ascending') {
                return a['score'] - b['score'];
            } else if (sortOrder === 'descending') {
                return b['score'] - a['score'];
            } else {
                // No sorting
                return 0;
            }
        })

        return sortedTips;
    }


    const handleSortClick = (e) => {
        if (e.target.value === sortBy) {
            return; // if the user clicks the same sort by, do nothing. 
        }

        setSortBy(e.target.value);
        if (searchResults.length != 0) {
            const sortedCards = sortTips(searchResults, e.target.value); // if the user has searched the tags, sort the results from the search. 
            setSearchResults(sortedCards);
        } else {
            console.log("suggestionData at handleSortClick: ", tipsData);
            const sortedCards = sortTips(totalTips, e.target.value); // else, sort the total result. 
            setTotalTips(sortedCards);
        }
    };

    return (
        <div id="map-tip-container" className="flex flex-col w-full h-full min-h-screen">
            <div id="search-tips-tag-field" className="fixed flex flex-row w-full bg-gray-100 h-20 py-5 px-3">
                <input
                    type="text"
                    className="bg-white shadow rounded-full h-10 w-full px-5 mr-3"
                    placeholder="Search for tags and summary"
                    onChange={handleSearch}
                ></input>
                <select value={sortBy} onChange={handleSortClick} name="sort">
                    <option value="descending">Karma⇂</option>
                    <option value="ascending">Karma↿</option>
                </select>
            </div>
            <div id="search-tag-field-space" className="w-2/5 h-20"></div>
            {expandedElement && expandedElement}
            <div id="tip-container" className="grow-2">
                {tipsData && !expandedElement ? (
                    searchResults.length != 0 ? (
                        searchResults.map((travelTip) => {
                            return (
                                <TipCard
                                    tip={travelTip}
                                    key={travelTip.id}
                                />
                            );
                        })
                    ) : (
                        totalTips.map((travelTip) => {
                            return (
                                <TipCard
                                    tip={travelTip}
                                    key={travelTip.id}
                                />
                            );
                        })
                    )
                ) : (
                    <></>
                )}
            </div>
        </div>
    );
}

export default TipsPage;
