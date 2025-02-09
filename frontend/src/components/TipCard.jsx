import { useEffect } from "react";

function TipCard({ body }) {
    return (
        <div className="flex flex-col shadow items-center py-10 bg-white m-3 rounded-full">
            <p>{body}</p>
        </div>
    );
}

export default TipCard;
