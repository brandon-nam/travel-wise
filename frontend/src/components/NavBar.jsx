import { NavLink } from "react-router";
import { useContext } from "react"; 
import ClickDetailsContext from "../contexts/ClickDetailsContext"

function NavBar() {
    const { handleClickPlaceDetails, handleClickTipDetails } = useContext(ClickDetailsContext);

    const onClick = () => {
        handleClickPlaceDetails(null, null, null, null);
        handleClickTipDetails(null, null, null);
    }

    return (
        <div className="flex shadow p-5 px-10 bg-white place-content-between">
            <div className="font-bold">
                <NavLink to="/" onClick={onClick} end>
                    TravelWise
                </NavLink>
            </div>
            <div className="flex space-x-10">
                <NavLink to="/search" onClick={onClick} end>
                    Search
                </NavLink>
                <NavLink to="/suggestions" onClick={onClick} end>
                    Suggestions
                </NavLink>
                <NavLink to="/tips" onClick={onClick} end>
                    Tips
                </NavLink>
            </div>
        </div>
    );
}

export default NavBar;
