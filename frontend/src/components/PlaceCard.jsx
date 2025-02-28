import { useEffect, memo } from "react";

function PlaceCard({ tag, body, highlight }) {
    return (
        <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded  ${highlight ? "border-2 border-blue-500" : ""}`}>
            <div className="min-h-10px h-10px w-full px-3 py-2 text-gray-400">{tag}</div>
            <div className="pt-5 pb-15 py-10 w-full text-center">{body}</div>
        </div>
    );
}

export default memo(PlaceCard);
