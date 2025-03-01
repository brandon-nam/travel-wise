import { useState, useContext, memo } from "react";
import ClickDetailsContext from "../contexts/ClickDetailsContext"

function PlaceCard({ tag, body, highlight, comments }) {
    const { clickedPlace, handleClickDetails } = useContext(ClickDetailsContext);

    return (
        <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded  ${highlight ? "border-2 border-blue-500" : ""}`}>
            <div className="min-h-10px h-10px w-full px-3 py-2 text-gray-400">{tag}</div>
            <div className="w-full text-center py-5">{body}</div>
            <div onClick={() => handleClickDetails(body, tag, comments)} className="w-full text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition">
                See details
            </div>            
            
        </div>
    );
}

export default PlaceCard;
