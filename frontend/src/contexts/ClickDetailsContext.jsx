import React, { useState, createContext } from "react";

const ClickDetailsContext = createContext();

export function ClickDetailsProvider({ children }) {
    const [clickedPlace, setClickedPlace] = useState(null);

    function handleClickDetails(body, tag, comments) {
        if (body) {
            const ConstructedHtml = () => (
                <div className={`flex flex-col shadow items-center bg-white mx-3 mb-3 rounded h-full`}>
                    <div className="min-h-10px h-10px w-full px-3 py-2 text-gray-400">{tag}</div>
                    <div className="w-full text-center py-5">{body}</div>
                    <div className="px-3">
                        {comments.map((comment) => {
                            return <p>✈️ {comment.summary}<br/><br/></p>;
                        })}
                    </div>
                    <div
                        onClick={() => handleClickDetails(null, null, null)}
                        className="w-full text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition"
                    >
                        See less
                    </div>
                </div>
            );

            setClickedPlace(ConstructedHtml);
            console.log("clicked details!: ", clickedPlace);
        } else {
            setClickedPlace(null);
        }
    }

    return <ClickDetailsContext.Provider value={{ clickedPlace, handleClickDetails }}>{children}</ClickDetailsContext.Provider>;
}

export default ClickDetailsContext;
