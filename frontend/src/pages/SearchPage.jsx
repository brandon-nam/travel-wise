import { useContext, useState } from "react";
import { useNavigate } from "react-router";
import QueryParametersContext from "../contexts/QueryParametersContext";

function SearchPage() {
    const { suggestionLink, updateLinks } = useContext(QueryParametersContext);

    let navigate = useNavigate();

    function handleClick() {
        navigate(suggestionLink);
    }

    const handleCountryChange = (e) => {
        console.log("country: ", e.target.value)
        updateLinks(e.target.value);
    };

    return (
        <div className="flex flex-col items-center p-6 max-w-5xl mx-auto h-full">
            <div className="text-xl font-semibold text-center text-gray-800 w-full py-10">
                <h1 className="text-4xl font-bold">Search your travel destinations</h1>
            </div>
            <div className="flex w-full flex-col space-y-10 text-left py-5">
                <label className="">
                    Select a country
                    <select
                        onChange={handleCountryChange}
                        className="w-full h-14 px-4 border shadow border-gray-300 rounded-full"
                    >
                        <option value="">All</option>
                        <option value="japan">Japan</option>
                        <option value="korea">Korea</option>
                    </select>
                </label>
                <div className="w-full flex flex-row justify-center py-5">
                    <button
                        onClick={handleClick}
                        className="h-14 w-2/3 bg-blue-500 text-white rounded-full hover:bg-blue-600 shadow"
                    >
                        Submit
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SearchPage;
