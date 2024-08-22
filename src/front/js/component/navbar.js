import React, { useContext, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/home.css";


export const Navbar = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(!!store.token);

  useEffect(() => {
    setIsLoggedIn(!!store.token);
    console.log("Token updated in Navbar:", store.token);
  }, [store.token]);

  const handleLogout = () => {
    actions.removeToken();
    navigate("/");
  };

  return (
    <nav className="navbar navbar-secondary bg-secondary">
      <div className="container">
        <Link to="/">
          <span className="navbar-brand mb-0 h1 text-dark text-decoration-none">Back to home</span>
        </Link>
        <div className="ms-auto">
          {isLoggedIn ? (
            <button onClick={handleLogout} className="btn btn-dark">
              Logout
            </button>
          ) : (
            <>
              <Link to="/signup">
                <button className="btn btn-dark me-2">Signup</button>
              </Link>
              <Link to="/login">
                <button className="btn btn-dark">Login</button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};
