import LandingPage from "./pages/LandingPage.jsx";
import NavBar from "./components/NavBar";
import ResultsPage from "./pages/ResultsPage.jsx";

import { BrowserRouter, Routes, Route } from "react-router";

function App() {
    return (
        <div className="flex flex-col items-center min-h-screen min-w-full bg-gray-100 h-full">
            <BrowserRouter>
                <div className="fixed top-0 w-full z-50">
                    <NavBar />
                </div>
                <div className="min-w-full h-full pt-16">
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/results" element={<ResultsPage />} />
                    </Routes>
                </div>
            </BrowserRouter>
        </div>
    );
}

export default App;
