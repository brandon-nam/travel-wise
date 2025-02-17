import { useEffect } from "react";

function TipCard({ body, highlight }) {
    return (
        <div className={`flex flex-col shadow items-center py-10 bg-white m-3 rounded px-10 ${highlight ? "border-2 border-blue-500" : ""}`}>
            <p>{body}</p>
        </div>
    );
}

export default TipCard;
