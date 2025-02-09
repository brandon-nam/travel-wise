import { useEffect } from "react";

function PlaceCard({ coordinate }) {
    return (
        <div className="flex flex-col border w-full items-center">
            <div className="p-10">image</div>
            <h1>{coordinate[0]["lng"]}</h1>
        </div>
    );
}

export default PlaceCard;
