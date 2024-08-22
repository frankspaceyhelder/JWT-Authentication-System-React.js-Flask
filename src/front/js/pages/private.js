import React from "react";
import "../../styles/home.css";
import autoagendalogo from "../../img/autoagendalogo.png";

export const Private = () => {
  return (
    <div className="text-center mt-5">
      <h2>Welcome to your private area!</h2>
      <div className="d-flex flex-column justify-content-center align-items-center min-vh-100 text-center">
        <img
          src={autoagendalogo}
          className="img-fluid logo-size"
          alt="AutoAgenda Logo"
        />
        <h1 className="mt-2">
          <i>Exclusive Members Club</i>
        </h1>
      </div>
    </div>
  );
};
