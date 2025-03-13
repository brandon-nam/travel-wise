import Fuse from "fuse.js";

import TipCard from "../components/TipCard";

import { useState, useContext } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchComments, fetchPosts, fetchTips } from "../lib/API";
import ClickDetailsContext from "../contexts/ClickDetailsContext";

function TipsPage() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
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

    const fuse = new Fuse(tipsData, {
        keys: ["characteristic", "summary"],
        threshold: 0.1, // Fuzzy match sensitivity
    });

    const handleSearch = (event) => {
        handleClickTipDetails(null, null, null, null);
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
        <div id="map-tip-container" className="flex flex-col w-full h-full min-h-screen">
            <div id="search-tips-tag-field" className="fixed w-full bg-gray-100 h-20 py-5 px-3">
                <input
                    type="text"
                    className="bg-white shadow rounded-full h-10 w-full px-5"
                    placeholder="Search for tags and summary"
                    onChange={handleSearch}
                ></input>
            </div>
            <div id="search-tag-field-space" className="w-2/5 h-20"></div>
            {expandedElement && expandedElement}
            <div id="tip-container" className="grow-2">
                {tipsData && !expandedElement ? (
                    results.length != 0 ? (
                        results.map((travelTip) => {
                            return (
                                <TipCard
                                    postURL={travelTip.post_url}
                                    tip={travelTip}
                                    key={travelTip.id}
                                />
                            );
                        })
                    ) : (
                        tipsData.map((travelTip) => {
                            return (
                                <TipCard
                                    postURL={travelTip.post_url}
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
