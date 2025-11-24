import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Login from "./components/Login";
import App from "./App";

function Root() {
  const [user, setUser] = React.useState(null);

  function handleLogin(userData) {
    setUser(userData);
  }

  function handleLogout() {
    setUser(null);
  }

  return user ? (
    <App user={user} onLogout={handleLogout} />
  ) : (
    <Login onLogin={handleLogin} />
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Root />);
