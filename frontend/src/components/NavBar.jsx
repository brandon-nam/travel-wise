import { NavLink } from "react-router";

function NavBar() {
    return (
        <div className="flex shadow p-5 px-10 bg-white place-content-between">
            <div className="font-bold">
                <NavLink to="/" end>
                    TravelWise
                </NavLink>
            </div>
            <div className="flex space-x-10">
                <NavLink to="/search" end>
                    Search
                </NavLink>
                <NavLink to="/suggestions" end>
                    Suggestions
                </NavLink>
                <NavLink to="/tips" end>
                    Tips
                </NavLink>
            </div>
        </div>
    );
}

export default NavBar;
