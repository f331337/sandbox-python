import { useState } from "react";
import "./App.css";
import { uploadFile, pollTaskStatus } from "./services/uploader";

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

			const apiUrl = import.meta.env.VITE_API_URL;
			const result = await uploadFile(file, {
				apiUrl,
				fileType: ["text/csv", ".csv"],
				contentType: "multipart/form-data",
				maxSizeMb: 100,
			});

			if (!result.ok) {
				throw new Error(result.message);
			}

			// Show immediate response
			setStatus(result.message || `Uploaded ${file.name} successfully.`);
			setFile(null);

			// If backend returns a task_id, start polling
			const taskId = result?.data?.task_id;
			if (taskId) {
				setStatus(`Upload accepted. Tracking task ${taskId}...`);
				const controller = new AbortController();
				try {
					const final = await pollTaskStatus(apiUrl, taskId, {
						intervalMs: 1000,
						signal: controller.signal,
						onUpdate: (payload) => {
							const st = payload?.status || "pending";
							if (st === "PENDING" || st === "pending") {
								setStatus(`Processing... (task ${taskId})`);
							}
						},
					});

					if (final.status === "success") {
						setStatus(
							typeof final.payload === "object"
								? `Success: ${JSON.stringify(final.payload.result ?? final.payload)}`
							: `Success: ${String(final.payload)}`
						);
					} else if (final.status === "failure") {
						const errMsg =
							typeof final.payload === "object"
								? final.payload.error || JSON.stringify(final.payload)
								: String(final.payload);
						setError(`Task failed: ${errMsg}`);
					} else {
						setError("Task ended with an error while polling.");
					}
				} finally {
					// no-op, controller scope ends
				}
			}
		} catch (err) {
			setError(err.message || "Upload failed");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="upload-container">
			<h1>Upload File </h1>
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
