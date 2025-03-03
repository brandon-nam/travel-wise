import { useEffect, useContext } from "react";
import ClickDetailsContext from "../contexts/ClickDetailsContext"


function TipCard({ tag, summary, body, highlight, postURL }) {
    const { handleClickTipDetails } = useContext(ClickDetailsContext);

    return (
        <div className={`flex flex-col shadow items-center bg-white m-3 rounded ${highlight ? "border-2 border-blue-500" : ""}`}>
            <div className="h-10px w-full px-5 pt-3 text-gray-400">{tag}</div>
            <div className="pt-5 w-full text-center px-10 pb-10">{summary}</div>
            <div onClick={() => handleClickTipDetails(body, tag, postURL)} className="w-full text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition">
                See details
            </div>      
        </div>
    );
}

export default TipCard;
