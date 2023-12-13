import express from 'express';
import multer, { diskStorage } from 'multer';
import cors from 'cors';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import fs from "fs";
import { exec } from 'child_process';

const filename = fileURLToPath(import.meta.url);
const directory = dirname(filename);
const app = express();
const port = 5000;
app.use(cors());

// Configure multer to handle file uploads
const storage = diskStorage({
  destination: (req, file, cb) => {
    // Specify the directory where you want to save the files
    cb(null, join(directory, 'uploaded_image'));
  },
  filename: (req, file, cb) => {
    // Use the original name of the file for saving
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });

const clean_uploaded_image_folder = () => {
  fs.readdir("uploaded_image", (err, files) => {
    if (err) {
      console.error('Error reading folder:', err);
      return res.status(500).json({ error: 'Internal Server Error' });
    }
    files.forEach((file) => {
      const filePath = join("uploaded_image", file);
      fs.unlink(filePath, (unlinkErr) => {
        if (unlinkErr) {
          console.error('Error removing file:', unlinkErr);
        }
      });
    });
  });
}

// Define a route for file upload
app.post('/search-similar', upload.single("image"), (req, res) => {
  console.log(`../uploaded_image/${req.file.filename}`);

  // Run the Python script
  exec(`python ./ai/model.py uploaded_image/${req.file.filename}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      clean_uploaded_image_folder();
      res.status(500).send('Internal Server Error');
    } else {
      // Send the output of the Python script as the response
      // console.log(`Python script output: ${stdout}`);
      clean_uploaded_image_folder();
      res.status(200).send(stdout);
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});