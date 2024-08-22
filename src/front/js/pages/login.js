import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/appContext";

export const Login = () => {
  const { actions } = useContext(Context);
  const [loginDetails, setLoginDetails] = useState({
    email: "",
    password: "",
  });

  const navigate = useNavigate();
  const apiUrl = "https://super-duper-space-trout-69vr79r5wv95f5469-3001.app.github.dev/api";

  const handleChange = (e) => {
    setLoginDetails({
      ...loginDetails,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const loginResponse = await fetch(`${apiUrl}/login`, {
        body: JSON.stringify(loginDetails),
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
      });

      if (loginResponse.ok) {
        const loginData = await loginResponse.json();

        if (loginData && loginData.token) {
          actions.addToken(loginData.token); 
          navigate("/private");
        } else {
          console.error("Token not found in the response.");
        }
      } else {
        console.error("Login failed with status:", loginResponse.status);
      }
    } catch (error) {
      console.error("An error occurred during login:", error);
    }
  };

  return (
    <div className="container mt-5 border border-secondary rounded">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            value={loginDetails.email}
            onChange={handleChange}
            placeholder="Enter email"
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            name="password"
            value={loginDetails.password}
            onChange={handleChange}
            placeholder="Enter password"
            required
          />
        </div>
        <button type="submit" className="btn btn-dark">Login</button>
      </form>
    </div>
  );
};
