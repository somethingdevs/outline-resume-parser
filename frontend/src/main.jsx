import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import "antd/dist/reset.css";
import { ConfigProvider, theme } from "antd";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          borderRadius: 10,
          colorBgLayout: "#09090b",
          colorBgBase: "#09090b",
          colorTextBase: "#f4f4f5",
          colorBorder: "#27272a",
        },
      }}
    >
      <App />
    </ConfigProvider>
  </React.StrictMode>
);
