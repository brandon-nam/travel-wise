import React, { useState, createContext } from "react";

const ClickDetailsContext = createContext();

export function ClickDetailsProvider({ children }) {
    const [expandedElement, setExpandedElement] = useState(null);
    const [clickedSuggestion, setClickedSuggestion] = useState([]);

    function handleClickPlaceDetails(suggestion) {
        if (suggestion) {
            const ConstructedHtml = () => (
                <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded h-full`}>
                    <div className="w-full flex-none px-3 py-2 text-gray-400">{"# " + suggestion.characteristic}</div>
                    <div>{suggestion.location_name}</div>
                    <div className="w-full flex-none text-center py-5">{suggestion.body}</div>
                    <div className="w-full px-3 grow">
                        {suggestion.comments.map((comment) => {
                            return (
                                <>
                                    <p>✈️ {comment.summary}</p>
                                    <a
                                        className="break-all text-blue-300  hover:text-blue-500 transition"
                                        target="_blank"
                                        href={comment.post_url + "/" + comment.id}
                                    >
                                        {" "}
                                        -{">"} Go to reddit post
                                    </a>
                                    <br />
                                    <br />
                                </>
                            );
                        })}
                    </div>
                    <div
                        onClick={() => handleClickPlaceDetails(null)}
                        className="w-full flex-none text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition"
                    >
                        See less
                    </div>
                </div>
            );

            setExpandedElement(ConstructedHtml);
            setClickedSuggestion([suggestion]);
            console.log("clicked details!: ", expandedElement);
        } else {
            setExpandedElement(null);
            setClickedSuggestion([]);
        }
    }

    function handleClickTipDetails(tip) {
        if (tip) {
            const ConstructedHtml = () => (
                <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded`}>
                    <div className="w-full flex-none px-3 py-2 text-gray-400">{tip.characteristic}</div>
                    <div className="w-full grow text-center py-5 px-3">{tip.body}</div>
                    <a className="break-all text-blue-300  hover:text-blue-500 transition" target="_blank" href={tip.post_url}>
                        Go to reddit post
                    </a>
                    <div
                        onClick={() => handleClickTipDetails(null)}
                        className="w-full flex-none text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition"
                    >
                        See less
                    </div>
                </div>
            );

            setExpandedElement(ConstructedHtml);
            console.log("clicked details!: ", expandedElement);
        } else {
            setExpandedElement(null);
        }
    }

    return (
        <ClickDetailsContext.Provider
            value={{ expandedElement, clickedSuggestion, handleClickPlaceDetails, handleClickTipDetails }}
        >
            {children}
        </ClickDetailsContext.Provider>
    );
}

export default ClickDetailsContext;
