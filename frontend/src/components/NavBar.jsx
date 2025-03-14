import { NavLink, useLocation } from "react-router";
import { useContext } from "react";
import ClickDetailsContext from "../contexts/ClickDetailsContext";

function NavBar() {
    const { handleClickPlaceDetails, handleClickTipDetails } = useContext(ClickDetailsContext);
    const location = useLocation();
    const isSuggestionsPage = location.pathname.startsWith("/suggestions");
    const isTipsPage = location.pathname.startsWith("/tips");

    const onClick = () => {
        handleClickPlaceDetails(null, null, null, null);
        handleClickTipDetails(null, null, null);
    };

    return (
        <div className="flex shadow p-5 px-10 bg-white place-content-between">
            <div className="font-bold">
                <NavLink to="/" onClick={onClick} end>
                    TravelWise
                </NavLink>
            </div>
            <div className="flex space-x-10">
                {(isSuggestionsPage || isTipsPage) && (
                    <>
                        <NavLink
                            to="/search"
                            className={
                                (isSuggestionsPage || isTipsPage)
                                    ? "text-gray-400 hover:text-blue-500 transition"
                                    : "font-medium hover:text-blue-500 transition" 
                            }
                            onClick={onClick}
                            end
                        >
                            Back to Search
                        </NavLink>
                        <NavLink
                            to="/suggestions"
                            className={
                                isSuggestionsPage
                                    ? "font-medium hover:text-blue-500 transition"
                                    : "text-gray-400 hover:text-blue-500 transition"
                            }
                            onClick={onClick}
                            end
                        >
                            Suggestions
                        </NavLink>
                        <NavLink
                            to="/tips"
                            className={
                                isTipsPage
                                    ? "font-medium hover:text-blue-500 transition"
                                    : "text-gray-400 hover:text-blue-500 transition"
                            }
                            onClick={onClick}
                            end
                        >
                            Tips
                        </NavLink>
                    </>
                )}
            </div>
        </div>
    );
}

export default NavBar;
