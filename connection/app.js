import express from "express";
import multer from "multer";
import path from "path";
import dotenv from "dotenv"; // ✅ Correct import
import cors from "cors";
import axios from "axios";
import { text } from "stream/consumers";
// Load environment variables
dotenv.config();

const app = express();


app.use(cors({
  origin: ["http://localhost:3000", "https://your-frontend-domain.com"],
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"], // include OPTIONS
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true
}));



// ✅ Optional: parse JSON if you send metadata
app.use(express.json());


// Configure Multer storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "../uploads/"); // folder to store uploaded files
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + path.extname(file.originalname)); // rename file
  }
});

// Initialize Multer middleware
const upload = multer({ storage });

app.get("/" , (req, res) => {
  res.send("HIII"); 
})
// Route to handle single file upload
app.post("/upload", upload.single("file"), (req, res) => {
  console.log("📥 Received upload request");
  res.json({ message: "File uploaded", file: req.file });
});

app.post("/get-audio-description", async (req, res) => {
    const { path } = req.body;
    if(!path){
       return res.status(404).json({ error : "Audio path not found."});
    }
    try {
      let audio_description = await axios.post(process.env.FLASK_SERVER + '/get-audio', { path : `./uploads/${path}` });

        if(!audio_description.data){
            return res.json({error : "Failed to get audio description"});
        }

        console.log("Successfully recieved audio data");
        return res.status(200).json( {
            msg : "Successfully recieved audio data",
            data : audio_description.data
        })
    } catch (error) {
        console.log("❌Error In audio descriptions: ", error);
        return res.status(500).json({ error : "Internal Server Error"});
    }
});

app.post("/get-test-analysis", async(req, res) => {
     const { text } = req.body;
     
})
app.post("/get-audio-analysis", async (req, res) => {
    const { text } = req.body;
    console.log("Getting audio description");
    try {
        
        
        console.log("Verifying news");
        
        let verify_audio = await axios.post(process.env.FLASK_SERVER + '/verify_news' , { text  });
        return res.json({data : verify_audio.data });
    } catch (error) {
        console.log(error);
        return res.json({error : "Could not get data"});
    }
    
})
// Serve uploaded files publicly
app.use("./uploads", express.static("uploads"));

// Start server
const PORT = process.env.PORT;
app.listen(PORT, () => console.log(`✅ Server running on http://localhost:${PORT}`));
