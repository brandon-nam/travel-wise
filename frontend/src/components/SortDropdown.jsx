import { useState } from "react";
import { sortSuggestions } from "../utils/sorting";

export default function SortDropdown({ suggestions, setSortedSuggestions }) {
    const [sortBy, setSortBy] = useState("descending");

    const handleSortClick = (e) => {
        if (e.target.value === sortBy) return;
        setSortBy(e.target.value);
        setSortedSuggestions(sortSuggestions(suggestions, e.target.value));
    };

    return (
        <select value={sortBy} onChange={handleSortClick}>
            <option value="ascending">Ascending</option>
            <option value="descending">Descending</option>
        </select>
    );
}