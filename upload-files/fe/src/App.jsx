import { useState } from "react";
import "./App.css";
import { uploadFile } from "./services/uploader";

function App() {
	const [file, setFile] = useState(null);
	const [error, setError] = useState("");
	const [status, setStatus] = useState("");
	const [loading, setLoading] = useState(false);

	const handleFileChange = (e) => {
		const selected = e.target.files[0];
		if (!selected) return;

		// validate type
		if (selected.type !== "text/csv" && !selected.name.endsWith(".csv")) {
			setError("Please upload a valid CSV file.");
			setFile(null);
			return;
		}

		// validate size (100 MB = 100 * 1024 * 1024 bytes)
		if (selected.size > 100 * 1024 * 1024) {
			setError("File must be smaller than 100 MB.");
			setFile(null);
			return;
		}

		setError("");
		setStatus("");
		setFile(selected);
	};

	const handleUpload = async () => {
		if (!file) return;

		try {
			setLoading(true);
			setError("");
			setStatus("Uploading...");

			const result = await uploadFile(file, {
				apiUrl: import.meta.env.VITE_API_URL,
				fileType: ["text/csv", ".csv"],
				contentType: "multipart/form-data",
				maxSizeMb: 100,
			});

			if (!result.ok) {
				throw new Error(result.message);
			}

			setStatus(result.message || `Uploaded ${file.name} successfully.`);
			setFile(null);
		} catch (err) {
			setError(err.message || "Upload failed");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="upload-container">
			<h1>Upload CSV</h1>
			<input type="file" accept=".csv,text/csv" onChange={handleFileChange} />
			{error && <p style={{ color: "red" }}>{error}</p>}
			{status && <p style={{ color: "green" }}>{status}</p>}
			{file && (
				<p>
					Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
				</p>
			)}
			<button onClick={handleUpload} disabled={!file || loading}>
				{loading ? "Uploading..." : "Upload"}
			</button>
		</div>
	);
}

export default App;
