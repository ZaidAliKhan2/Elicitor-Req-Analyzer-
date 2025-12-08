import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import { User } from "./userSchema.js";
import dotenv from "dotenv";
import nodemailer from "nodemailer";

dotenv.config();
const JWT_SECRET = process.env.JWT_SECRET;

// --- NODEMAILER TRANSPORTER ---
const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.GMAIL_USER,
    pass: process.env.GMAIL_PASS,
  },
});

// --- HELPER: SEND VERIFICATION EMAIL ---
const sendVerificationEmail = async (newUser, req) => {
  // Generate a verification JWT (3 hours validity)
  const token = jwt.sign(
    { id: newUser._id, email: newUser.email },
    JWT_SECRET,
    { expiresIn: "3h" }
  );

  // NOTE: req.protocol and req.get("host") need to be handled carefully in a separate router setup.
  // Assuming the base URL for verification is known, e.g., http://localhost:3000
  // For local testing, we'll hardcode the base URL as the Node service's URL.
  const verificationLink = `http://${req.headers.host}/verify-email?token=${token}`;

  const mailOptions = {
    from: process.env.GMAIL_USER,
    to: newUser.email,
    subject: "Verify your Elicitor Chatbot Email",
    html: `<p>Click the link below to verify your email:</p>
               <a href="${verificationLink}">Verify Email</a>`,
  };

  await transporter.sendMail(mailOptions);
};

// ------------------ SIGNUP ------------------
export const signup = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    let existingUser = await User.findOne({ email });

    if (existingUser) {
      if (existingUser.isVerified) {
        return res.status(400).json({ message: "Email already in use." });
      } else {
        // If user exists but is not verified, reuse and send new email
        await sendVerificationEmail(existingUser, req);
        return res.status(200).json({
          message:
            "User created previously but not verified. Verification email re-sent.",
        });
      }
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create new user (isVerified defaults to false)
    const newUser = new User({
      name,
      email,
      password: hashedPassword,
    });

    await newUser.save();

    // Send verification email
    await sendVerificationEmail(newUser, req);

    res.status(201).json({
      message:
        "Signup successful. Please check your email for verification link.",
    });
  } catch (err) {
    console.error("Signup error:", err);
    res.status(500).json({ message: "Server error", error: err.message });
  }
};

// ------------------ LOGIN ------------------
export const login = async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });

    const token = jwt.sign({ id: user._id, email: user.email }, JWT_SECRET, {
      expiresIn: "1h",
    });

    res.json({
      token,
      name: user.name,
    });
  } catch (err) {
    res.status(500).json({ message: "Server error", error: err.message });
  }
};

// ------------------ VERIFY EMAIL ROUTE LOGIC ------------------
export const verifyEmail = async (req, res) => {
  try {
    const { token } = req.query;

    if (!token) {
      return res.status(400).send("No token provided.");
    }

    const decoded = jwt.verify(token, JWT_SECRET);

    const updatedUser = await User.findByIdAndUpdate(
      decoded.id,
      { isVerified: true },
      { new: true }
    );

    if (!updatedUser) {
      // User not found, token might point to a deleted user
      return res.status(404).send("User not found or verification failed.");
    }

    // Successful verification - redirect to login page
    // NOTE: We need to know the URL of your UI's login page here.
    // Assuming your UI is served on a different port/route.
    res.redirect(
      "http://127.0.0.1:5500/ui/components/login.html?verified=success"
    );
  } catch (err) {
    console.error("Verification Error:", err);
    // Send a user-friendly message for expired/invalid tokens
    res.status(400).send("Verification failed: Invalid or expired token.");
  }
};

// ------------------ TOKEN VERIFY MIDDLEWARE ------------------
export const verifyTokenMiddleware = (req, res, next) => {
  // ... (Your existing code for this function remains here)
  const authHeader = req.headers.authorization;
  // ... (rest of the verification logic)

  if (!authHeader)
    return res.status(401).json({ message: "No token provided" });

  const token = authHeader.split(" ")[1];

  jwt.verify(token, JWT_SECRET, (err, decodedUser) => {
    if (err) return res.status(403).json({ message: "Invalid token" });

    req.user = decodedUser;
    next();
  });
};
