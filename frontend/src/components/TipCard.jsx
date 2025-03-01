import { useEffect } from "react";

function TipCard({ tag, body, highlight }) {
    return (
        <div className={`flex flex-col shadow items-center bg-white m-3 rounded ${highlight ? "border-2 border-blue-500" : ""}`}>
            <div className="h-10px w-full px-5 pt-3 text-gray-400">{tag}</div>
            <div className="pt-5 w-full text-center px-10 pb-10">{body}</div>
        </div>
    );
}

export default TipCard;
