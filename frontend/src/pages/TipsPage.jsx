import Fuse from "fuse.js";

import TipCard from "../components/TipCard";

import { useState } from "react"
import { useQuery } from "@tanstack/react-query";

function TipsPage() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);

    const { isLoading, data, error } = useQuery({
        queryKey: ["travelSuggestions"],
        queryFn: () => fetchComments(),
        select: (data) => data.filter((result) => result.classification === "travel_tip"),
        staleTime: Infinity
    })

    const fuse = new Fuse(data, {
        keys: [
            "characteristic",
            "summary"
        ],
        threshold: 0.1, // Fuzzy match sensitivity
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
            <div id="tip-container" className="grow-2">
                {!isLoading &&
                    results.length != 0 ? (
                        results.map((travelTip) => {
                            return <TipCard tag={`# ${travelTip.characteristic}`} body={travelTip.summary} key={travelTip.id} />;
                        })
                    ) : (
                        data.map((travelTip) => {
                            return <TipCard tag={`# ${travelTip.characteristic}`} body={travelTip.summary} key={travelTip.id} />;
                        })
                    )
                }
            </div>
        </div>
    );
}

export default TipsPage;
