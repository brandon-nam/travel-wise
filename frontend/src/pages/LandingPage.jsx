import { useState } from "react";
import axiosInstance from "../utils/AxiosInstance";
import { useNavigate } from "react-router";

function LandingPage() {
    const [text, setText] = useState("");
    const [result, setResult] = useState("");
    let navigate = useNavigate();

    async function handleClick() {
        // const result = await axiosInstance.get("posts", { input: text });
        // setResult(result.data);
        navigate("/results");
    }

    return (
        <div className="flex flex-col items-center space-y-4 p-6 max-w-5xl mx-auto">
            <div className="text-xl font-semibold text-center text-gray-800 w-full">
                <h1 className="text-4xl font-bold">Welcome to Travelwise</h1>
                <p className="text-lg">Get started by asking me for travel suggestions</p>
            </div>
            <div className="flex w-full flex-col space-y-10 text-left">
                <input
                    type="text"
                    placeholder="Ask me travel suggestions"
                    className="w-full h-14 px-4 border shadow border-gray-300 rounded-full"
                    onChange={(e) => setText(e.target.value)}
                />
                <label>
                    Select a country
                    <select className="w-full h-14 px-4 border shadow border-gray-300 rounded-full">
                        <option value="usa">Japan</option>
                    </select>
                </label>

                <label>
                    off-the-beaten value
                    <input type="range" className="w-full"/>
                </label>

                <button onClick={handleClick} className="h-14 mx-30 bg-blue-500 text-white rounded-full hover:bg-blue-600 shadow">
                    Submit
                </button>
            </div>
        </div>
    );
}

export default LandingPage;
