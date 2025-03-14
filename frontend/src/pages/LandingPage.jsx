import { useState } from "react";
import { useNavigate } from "react-router";

function LandingPage() {
    const [text, setText] = useState("");
    const [result, setResult] = useState("");
    let navigate = useNavigate();

    function handleClick() {

        navigate("/search");
    }

    return (
        <div className="flex flex-col items-center space-y-4 max-w-5xl mx-auto">
            <div className="text-xl font-semibold text-center text-gray-800 w-full px-10 py-10 text-wrap ">
                <h1 className="text-6xl font-bold leading-[1.2] ">Plan your One and Only Customized Trip with <p className="text-red-300">TravelWise</p></h1>
            </div>
            <div className="flex w-full flex-col space-y-10 text-left">
                <button onClick={handleClick} className="h-14 mx-30 bg-[#5cb7b7] text-white rounded-full hover:bg-[#50a0a0] shadow">
                    Start
                </button>
            </div>
        </div>
    );
}

export default LandingPage;
