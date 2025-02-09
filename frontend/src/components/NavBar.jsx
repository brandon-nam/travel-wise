import { NavLink } from "react-router";

function NavBar() {
    return (
        <div className="flex shadow p-5 px-10 bg-white place-content-between">
            <div>Travelwise</div>
            <div className="flex space-x-10">
                <NavLink to="/" end>
                    Home
                </NavLink>
                <NavLink to="/results" end>
                    Results
                </NavLink>
            </div>
        </div>
    );
}

export default NavBar;
