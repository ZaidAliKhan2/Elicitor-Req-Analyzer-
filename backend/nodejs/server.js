import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import dotenv from "dotenv";
import { signup, login, verifyTokenMiddleware, verifyEmail } from "./auth.js"; // <-- ADDED: verifyEmail

dotenv.config();

const app = express();

app.use(cors());

app.use(
  cors({
    origin: "*",
    methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
    preflightContinue: false,
    optionsSuccessStatus: 204,
  })
);

app.use(express.json());

// MongoDB Connect
mongoose
  .connect(process.env.MONGO_URL)
  .then(() => console.log("MongoDB Connected"))
  .catch((err) => console.log("DB Error:", err));

// Routes
app.post("/signup", signup);
app.post("/login", login);

// <-- NEW VERIFICATION ROUTE
app.get("/verify-email", verifyEmail);

app.get("/profile", verifyTokenMiddleware, (req, res) => {
  res.json({ message: "Token is valid!", user: req.user });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Node server running on ", PORT));
