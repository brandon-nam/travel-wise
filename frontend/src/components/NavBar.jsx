import { NavLink, useLocation } from "react-router";
import { useContext } from "react";
import ClickDetailsContext from "../contexts/ClickDetailsContext";
import QueryParametersContext from "../contexts/QueryParametersContext";

function NavBar() {
    const { handleClickPlaceDetails, handleClickTipDetails } = useContext(ClickDetailsContext);
    const { suggestionLink, tipLink, updateLink } = useContext(QueryParametersContext);
    const location = useLocation();
    const isSuggestionsPage = location.pathname.startsWith("/suggestions");
    const isTipsPage = location.pathname.startsWith("/tips");

    const onClick = (link) => {
        handleClickPlaceDetails(null);
        handleClickTipDetails(null);
        if (link == "search" || link == "home") {
            updateLink("");
        }
    };

    return (
        <div className="flex shadow p-5 px-10 bg-white place-content-between">
            <div className="font-bold">
                <NavLink to="/" onClick={() => onClick("home")} end>
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
                            onClick={() => onClick("search")}
                            end
                        >
                            Back to Search
                        </NavLink>
                        <NavLink
                            to={suggestionLink}
                            className={
                                isSuggestionsPage
                                    ? "font-medium hover:text-blue-500 transition"
                                    : "text-gray-400 hover:text-blue-500 transition"
                            }
                            onClick={() => onClick("suggestions")}
                            end
                        >
                            Suggestions
                        </NavLink>
                        <NavLink
                            to={tipLink}
                            className={
                                isTipsPage
                                    ? "font-medium hover:text-blue-500 transition"
                                    : "text-gray-400 hover:text-blue-500 transition"
                            }
                            onClick={() => onClick("tips")}
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
