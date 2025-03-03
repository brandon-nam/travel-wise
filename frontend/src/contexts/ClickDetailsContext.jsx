import React, { useState, createContext } from "react";

const ClickDetailsContext = createContext();

export function ClickDetailsProvider({ children }) {
    const [expandedElement, setExpandedElement] = useState(null);

    function handleClickPlaceDetails(body, tag, comments, postURL) {
        if (body) {
            const ConstructedHtml = () => (
                <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded h-full`}>
                    <div className="w-full flex-none px-3 py-2 text-gray-400">{tag}</div>
                    <div className="w-full flex-none text-center py-5" >{body}</div>
                    <div className="w-full px-3 grow">
                        {comments.map((comment) => {
                            return <p>✈️ {comment.summary}<br/><br/></p>;
                        })}
                        <a className="break-all text-blue-300  hover:text-blue-500 transition" target="_blank" href={postURL}>Go to reddit post</a>
                    </div>
                    <div
                        onClick={() => handleClickPlaceDetails(null, null, null)}
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

    function handleClickTipDetails(body, tag, postURL) {
        if (body) {
            console.log("posturl, ", postURL)
            const ConstructedHtml = () => (
                <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded`}>
                    <div className="w-full flex-none px-3 py-2 text-gray-400">{tag}</div>
                    <div className="w-full grow text-center py-5 px-3" >{body}</div>
                    <a className="break-all text-blue-300  hover:text-blue-500 transition" target="_blank" href={postURL}>Go to reddit post</a>
                    <div
                        onClick={() => handleClickTipDetails(null, null, null)}
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

    return <ClickDetailsContext.Provider value={{ expandedElement, handleClickPlaceDetails, handleClickTipDetails }}>{children}</ClickDetailsContext.Provider>;
}

export default ClickDetailsContext;
