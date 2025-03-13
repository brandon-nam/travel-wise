import { useEffect, useContext } from "react";
import ClickDetailsContext from "../contexts/ClickDetailsContext"


function TipCard({ tip }) {
    const { handleClickTipDetails } = useContext(ClickDetailsContext);

    return (
        <div className={`flex flex-col shadow items-center bg-white m-3 rounded`}>
            <div className="flex flex-row justify-between  min-h-10px h-10px w-full px-3 py-2 text-gray-400">
                <div>{"# " + tip.characteristic}</div>
                <div>{"Karma: " + tip.score}</div>
            </div>
            <div className="pt-5 w-full text-center px-10 pb-10">{tip.summary}</div>
            <div onClick={() => handleClickTipDetails(tip)} className="w-full text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition">
                See details
            </div>      
        </div>
    );
}

export default TipCard;
