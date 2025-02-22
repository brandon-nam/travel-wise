import LandingPage from "./pages/LandingPage.jsx";
import NavBar from "./components/NavBar";
import SuggestionsPage from "./pages/SuggestionsPage.jsx";
import TipsPage from "./pages/TipsPage.jsx";

import { BrowserRouter, Routes, Route } from "react-router";
import ClickMarkerContext, { ClickMarkerProvider } from "./contexts/ClickMarkerContext.jsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
    return (
        <div className="flex flex-col items-center min-h-screen min-w-full bg-gray-100 h-full">
            <QueryClientProvider client={queryClient}>
            <ClickMarkerProvider>
                <BrowserRouter>
                    <div className="fixed top-0 w-full z-50">
                        <NavBar />
                    </div>
                    <div className="min-w-full h-full pt-16">
                        <Routes>
                            <Route path="/" element={<LandingPage />} />

                            <Route path="/suggestions" element={<SuggestionsPage />} />

                            <Route path="/tips" element={<TipsPage />} />
                        </Routes>
                    </div>
                </BrowserRouter>
            </ClickMarkerProvider>
            </QueryClientProvider>
        </div>
    );
}

export default App;
