import { useEffect } from "react";

function TipCard({ body }) {
    return (
        <div className="flex flex-col border w-full items-center">
            <p>{body}</p>
        </div>
    );
}

export default TipCard;
