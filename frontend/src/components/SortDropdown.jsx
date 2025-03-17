import { useState } from "react";
import { sortComments } from "../utils/sorting";

export default function SortDropdown({ comments, setSortedComments }) {
    const [sortBy, setSortBy] = useState("descending");

    const handleSortClick = (e) => {
        if (e.target.value === sortBy) return;
        setSortBy(e.target.value);
        setSortedComments(sortComments(comments, e.target.value));
    };

    return (
        <select value={sortBy} className="ml-5" onChange={handleSortClick}>
            <option value="ascending">Popularity ↑</option>
            <option value="descending">Popularity ↓</option>
        </select>
    );
}