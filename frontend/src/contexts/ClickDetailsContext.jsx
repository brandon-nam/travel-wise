import React, { useState, createContext } from "react";

const ClickDetailsContext = createContext();

export function ClickDetailsProvider({ children }) {
    const [clickedPlace, setClickedPlace] = useState(null);

    function handleClickDetails(body, tag, comments, postURL) {
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
                        onClick={() => handleClickDetails(null, null, null)}
                        className="w-full flex-none text-right px-3 py-2 text-blue-300 cursor-pointer hover:text-blue-500 transition"
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
