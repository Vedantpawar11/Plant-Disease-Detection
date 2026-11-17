//this code css is pasted in temprar.css so if waant to use then use

import { useState } from "react";
import "./App.css";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleImageChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setSelectedImage(file);
    setPreview(URL.createObjectURL(file));

    // Demo result for frontend testing.
    // This will later be replaced by the real ViT API.
    setPrediction(null);
  };

  // const handlePredict = () => {
  //   if (!selectedImage) {
  //     alert("Please upload a plant leaf image first.");
  //     return;
  //   }

  //   // Temporary demo prediction.
  //   // Later this will call FastAPI + ViT.
  //   setPrediction({
  //     disease: "Tomato Early Blight",
  //     confidence: 94.7,
  //     recommendation:
  //       "Remove infected leaves, improve air circulation, and monitor the plant regularly."
  //   });
  // };
  
  const handlePredict = async () => {
    if (!selectedImage) {
      alert("Please upload a plant leaf image first.");
      return;
    }

    try {
      const formData = new FormData();

      formData.append("file", selectedImage);

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Prediction failed."
        );
      }

      setPrediction({
        disease: data.disease,
        confidence: data.confidence,
        recommendation: data.recommendation,
      });

    } catch (error) {

      console.error(error);

      alert(
        "Unable to connect to the prediction server. " +
        "Make sure FastAPI is running."
      );
    }
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">
          🌿 Plant<span>Doctor</span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#detect">Detection</a>
          <a href="#about">About</a>
        </div>
      </nav>

      {/* HERO */}
      <section className="hero" id="home">

        <div className="hero-content">

          <div className="badge">
            AI POWERED • VISION TRANSFORMER
          </div>

          <h1>
            Plant Disease
            <br />
            <span>Detection System</span>
          </h1>

          <p>
            Upload a plant leaf image and use artificial intelligence
            to identify potential diseases and receive treatment
            recommendations.
          </p>

          <a href="#detect" className="hero-button">
            Start Detection →
          </a>

        </div>

        <div className="hero-visual">
          <div className="leaf-circle">
            🌿
          </div>
        </div>

      </section>

      {/* DETECTION */}
      <section className="detection-section" id="detect">

        <div className="section-heading">
          <p>DISEASE DETECTION</p>
          <h2>Analyze Your Plant</h2>
          <span>
            Upload a clear image of the affected plant leaf.
          </span>
        </div>

        <div className="detection-container">

          {/* UPLOAD CARD */}
          <div className="upload-card">

            <div className="upload-icon">
              📷
            </div>

            <h3>Upload Leaf Image</h3>

            <p>
              JPG, JPEG or PNG
            </p>

            <label className="upload-button">
              Choose Image
              <input
                type="file"
                accept="image/png,image/jpeg,image/jpg"
                onChange={handleImageChange}
              />
            </label>

            {preview && (
              <div className="preview-container">
                <img
                  src={preview}
                  alt="Selected plant leaf"
                />
              </div>
            )}

            <button
              className="predict-button"
              onClick={handlePredict}
            >
              🔍 Predict Disease
            </button>

          </div>

          {/* RESULT CARD */}
          <div className="result-card">

            <div className="result-header">
              <div>
                <p className="result-label">
                  AI ANALYSIS
                </p>
                <h3>Prediction Result</h3>
              </div>

              <div className="ai-icon">
                ✨
              </div>
            </div>

            {!prediction ? (
              <div className="empty-result">

                <div className="empty-icon">
                  🌱
                </div>

                <h4>Waiting for image</h4>

                <p>
                  Upload a leaf image and click
                  <strong> Predict Disease </strong>
                  to see the result.
                </p>

              </div>
            ) : (
              <div className="prediction-result">

                <div className="disease-result">

                  <span>Disease Detected</span>

                  <h2>
                    {prediction.disease}
                  </h2>

                </div>

                <div className="confidence">

                  <div className="confidence-header">
                    <span>Confidence</span>
                    <strong>
                      {prediction.confidence}%
                    </strong>
                  </div>

                  <div className="confidence-bar">
                    <div
                      style={{
                        width: `${prediction.confidence}%`
                      }}
                    />
                  </div>

                </div>

                <div className="recommendation">

                  <h4>💡 Recommendation</h4>

                  <p>
                    {prediction.recommendation}
                  </p>

                </div>

              </div>
            )}

          </div>

        </div>

      </section>

      {/* ABOUT */}
      <section className="about-section" id="about">

        <div className="section-heading">
          <p>ABOUT THE PROJECT</p>

          <h2>How It Works</h2>
        </div>

        <div className="steps">

          <div className="step">
            <div>01</div>
            <h3>Upload</h3>
            <p>
              Upload a clear image of the plant leaf.
            </p>
          </div>

          <div className="step">
            <div>02</div>
            <h3>AI Analysis</h3>
            <p>
              The Vision Transformer analyzes the image.
            </p>
          </div>

          <div className="step">
            <div>03</div>
            <h3>Prediction</h3>
            <p>
              The system identifies the disease class.
            </p>
          </div>

          <div className="step">
            <div>04</div>
            <h3>Recommendation</h3>
            <p>
              Get useful disease-management guidance.
            </p>
          </div>

        </div>

      </section>

      {/* FOOTER */}
      <footer>
        <div>
          🌿 <strong>PlantDoctor</strong>
        </div>

        <p>
          Plant Disease Detection using Vision Transformers
        </p>

        <span>
          © 2026 Plant Disease Detection Project
        </span>
      </footer>

    </div>
  );
}

export default App;











// import { useCallback, useEffect, useRef, useState } from "react";
// import "./App.css";

// const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
// const MAX_FILE_MB = 5;
// const REQUEST_TIMEOUT_MS = 30000;
// const LOW_CONFIDENCE = 60; // percent
// const ACCEPTED_TYPES = ["image/jpeg", "image/png"];

// /** "Tomato___Early_blight" -> { plant: "Tomato", condition: "Early blight" } */
// function parseLabel(raw = "") {
//   const clean = (s) => s.replace(/_+/g, " ").replace(/\s+/g, " ").trim();
//   if (raw.includes("___")) {
//     const [plant, ...rest] = raw.split("___");
//     return { plant: clean(plant), condition: clean(rest.join(" ")) };
//   }
//   return { plant: null, condition: clean(raw) };
// }

// function isHealthy(condition = "") {
//   return condition.toLowerCase().includes("healthy");
// }

// function validateFile(file) {
//   if (!ACCEPTED_TYPES.includes(file.type)) {
//     return "Use a JPG or PNG image.";
//   }
//   if (file.size > MAX_FILE_MB * 1024 * 1024) {
//     return `Image is larger than ${MAX_FILE_MB} MB. Choose a smaller file.`;
//   }
//   return null;
// }

// function App() {
//   const [file, setFile] = useState(null);
//   const [preview, setPreview] = useState(null);
//   const [prediction, setPrediction] = useState(null);
//   const [status, setStatus] = useState("idle"); // idle | loading | done | error
//   const [error, setError] = useState("");
//   const [dragging, setDragging] = useState(false);
//   const [server, setServer] = useState({ state: "checking", modelLoaded: null });

//   const inputRef = useRef(null);
//   const abortRef = useRef(null);

//   /* ---- Server health ---- */
//   const checkServer = useCallback(async () => {
//     setServer({ state: "checking", modelLoaded: null });
//     try {
//       const res = await fetch(`${API_URL}/health`);
//       if (!res.ok) throw new Error();
//       const data = await res.json().catch(() => ({}));
//       setServer({
//         state: "online",
//         modelLoaded:
//           typeof data.model_loaded === "boolean" ? data.model_loaded : null,
//       });
//     } catch {
//       setServer({ state: "offline", modelLoaded: null });
//     }
//   }, []);

//   useEffect(() => {
//     checkServer();
//   }, [checkServer]);

//   /* ---- Free the preview URL when it changes or on unmount ---- */
//   useEffect(() => {
//     return () => {
//       if (preview) URL.revokeObjectURL(preview);
//     };
//   }, [preview]);

//   useEffect(() => () => abortRef.current?.abort(), []);

//   /* ---- File handling ---- */
//   const acceptFile = (nextFile) => {
//     if (!nextFile) return;
//     const problem = validateFile(nextFile);
//     if (problem) {
//       setError(problem);
//       setStatus("error");
//       return;
//     }
//     abortRef.current?.abort();
//     setFile(nextFile);
//     setPreview(URL.createObjectURL(nextFile));
//     setPrediction(null);
//     setError("");
//     setStatus("idle");
//   };

//   const handleInputChange = (e) => {
//     acceptFile(e.target.files?.[0]);
//     e.target.value = ""; // allows re-selecting the same file
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     setDragging(false);
//     acceptFile(e.dataTransfer.files?.[0]);
//   };

//   const reset = () => {
//     abortRef.current?.abort();
//     setFile(null);
//     setPreview(null);
//     setPrediction(null);
//     setError("");
//     setStatus("idle");
//   };

//   /* ---- Prediction ---- */
//   const handlePredict = async () => {
//     if (!file || status === "loading") return;

//     abortRef.current?.abort();
//     const controller = new AbortController();
//     abortRef.current = controller;
//     const timeout = setTimeout(() => controller.abort("timeout"), REQUEST_TIMEOUT_MS);

//     setStatus("loading");
//     setError("");
//     setPrediction(null);

//     try {
//       const formData = new FormData();
//       formData.append("file", file);

//       const res = await fetch(`${API_URL}/predict`, {
//         method: "POST",
//         body: formData,
//         signal: controller.signal,
//       });

//       const data = await res.json().catch(() => null);

//       if (!res.ok || !data || data.success === false) {
//         throw new Error(
//           data?.message || data?.detail || `Server returned ${res.status}.`
//         );
//       }

//       const label = parseLabel(data.class_name || data.disease);
//       const top = Array.isArray(data.top_predictions)
//         ? data.top_predictions.slice(0, 3).map((p) => ({
//             ...parseLabel(p.class_name || p.disease),
//             confidence: Number(p.confidence),
//           }))
//         : [];

//       setPrediction({
//         plant: data.plant || label.plant,
//         condition: label.condition,
//         confidence: Number(data.confidence),
//         recommendation: data.recommendation,
//         top,
//         isDemo: data.demo === true,
//       });
//       setStatus("done");
//       setServer((s) => ({ ...s, state: "online" }));
//     } catch (err) {
//       if (controller.signal.aborted && controller.signal.reason !== "timeout") {
//         return; // cancelled by a new upload or reset
//       }
//       const timedOut = controller.signal.reason === "timeout";
//       const offline = err instanceof TypeError;
//       setError(
//         timedOut
//           ? "The server took too long to respond. Try again."
//           : offline
//           ? "Can't reach the prediction server. Start FastAPI with `uvicorn main:app --reload`, then retry."
//           : err.message || "Prediction failed."
//       );
//       if (offline) setServer({ state: "offline", modelLoaded: null });
//       setStatus("error");
//     } finally {
//       clearTimeout(timeout);
//     }
//   };

//   const loading = status === "loading";
//   const healthy = prediction && isHealthy(prediction.condition);
//   const lowConfidence = prediction && prediction.confidence < LOW_CONFIDENCE;
//   const confidenceValue = prediction
//     ? Math.max(0, Math.min(100, prediction.confidence))
//     : 0;

//   return (
//     <div className="app">
//       <header className="topbar">
//         <a className="brand" href="#top">
//           PlantDoctor
//         </a>
//         <div className={`server server--${server.state}`} role="status">
//           <span className="server-dot" aria-hidden="true" />
//           {server.state === "checking" && "Checking server"}
//           {server.state === "online" &&
//             (server.modelLoaded === false ? "Server online, demo mode" : "Server online")}
//           {server.state === "offline" && (
//             <>
//               Server offline
//               <button type="button" className="link-button" onClick={checkServer}>
//                 Retry
//               </button>
//             </>
//           )}
//         </div>
//       </header>

//       <main id="top">
//         <section className="intro">
//           <h1>Check a leaf for disease</h1>
//           <p>
//             Upload a clear photo of a single leaf. A Vision Transformer trained
//             on 38 plant and disease classes suggests what it may be.
//           </p>
//         </section>

//         <div className="workspace">
//           {/* ---------- Upload ---------- */}
//           <section className="panel" aria-labelledby="upload-title">
//             <h2 id="upload-title" className="panel-title">
//               1. Add a photo
//             </h2>

//             <div
//               className={`dropzone ${dragging ? "dropzone--active" : ""} ${
//                 preview ? "dropzone--filled" : ""
//               }`}
//               onDragOver={(e) => {
//                 e.preventDefault();
//                 setDragging(true);
//               }}
//               onDragLeave={() => setDragging(false)}
//               onDrop={handleDrop}
//             >
//               {preview ? (
//                 <img src={preview} alt="Selected leaf" className="dropzone-image" />
//               ) : (
//                 <div className="dropzone-empty">
//                   <p className="dropzone-main">Drag a leaf photo here</p>
//                   <p className="dropzone-sub">JPG or PNG, up to {MAX_FILE_MB} MB</p>
//                 </div>
//               )}
//               <input
//                 ref={inputRef}
//                 type="file"
//                 accept="image/png,image/jpeg"
//                 onChange={handleInputChange}
//                 className="visually-hidden"
//                 id="leaf-input"
//               />
//             </div>

//             {file && (
//               <p className="file-meta">
//                 {file.name} · {(file.size / 1024).toFixed(0)} KB
//               </p>
//             )}

//             <div className="actions">
//               <button
//                 type="button"
//                 className="btn btn--secondary"
//                 onClick={() => inputRef.current?.click()}
//               >
//                 {file ? "Choose another photo" : "Choose photo"}
//               </button>
//               <button
//                 type="button"
//                 className="btn btn--primary"
//                 onClick={handlePredict}
//                 disabled={!file || loading}
//               >
//                 {loading ? "Analyzing…" : "Analyze leaf"}
//               </button>
//               {file && (
//                 <button type="button" className="btn btn--ghost" onClick={reset}>
//                   Clear
//                 </button>
//               )}
//             </div>
//           </section>

//           {/* ---------- Result ---------- */}
//           <section
//             className="panel panel--result"
//             aria-labelledby="result-title"
//             aria-live="polite"
//           >
//             <h2 id="result-title" className="panel-title">
//               2. Result
//             </h2>

//             {status === "error" && (
//               <div className="notice notice--error" role="alert">
//                 <p>{error}</p>
//                 {file && !error.startsWith("Use a") && !error.startsWith("Image is") && (
//                   <button type="button" className="link-button" onClick={handlePredict}>
//                     Try again
//                   </button>
//                 )}
//               </div>
//             )}

//             {status !== "error" && !prediction && !loading && (
//               <div className="empty">
//                 <p className="empty-main">No result yet</p>
//                 <p className="empty-sub">
//                   Add a photo, then choose <strong>Analyze leaf</strong>.
//                 </p>
//               </div>
//             )}

//             {loading && (
//               <div className="loading" role="status">
//                 <span className="spinner" aria-hidden="true" />
//                 <p>Analyzing your photo…</p>
//               </div>
//             )}

//             {prediction && (
//               <div className="specimen">
//                 {prediction.isDemo && (
//                   <div className="notice notice--demo">
//                     Demo result. The model isn't connected yet, so this is not a
//                     real prediction.
//                   </div>
//                 )}

//                 <div className="specimen-head">
//                   {prediction.plant && (
//                     <p className="specimen-plant">{prediction.plant}</p>
//                   )}
//                   <h3 className={healthy ? "specimen-name specimen-name--ok" : "specimen-name"}>
//                     {prediction.condition}
//                   </h3>
//                 </div>

//                 <div className="meter">
//                   <div className="meter-row">
//                     <span>Model confidence</span>
//                     <strong>{confidenceValue.toFixed(1)}%</strong>
//                   </div>
//                   <div
//                     className="meter-track"
//                     role="progressbar"
//                     aria-valuemin={0}
//                     aria-valuemax={100}
//                     aria-valuenow={Math.round(confidenceValue)}
//                     aria-label="Model confidence"
//                   >
//                     <div
//                       className={`meter-fill ${lowConfidence ? "meter-fill--low" : ""}`}
//                       style={{ width: `${confidenceValue}%` }}
//                     />
//                   </div>
//                   {lowConfidence && (
//                     <p className="meter-warn">
//                       Low confidence. Retake the photo in good light with the
//                       leaf filling the frame, or check with a local expert.
//                     </p>
//                   )}
//                 </div>

//                 {prediction.top.length > 1 && (
//                   <div className="alternatives">
//                     <h4>Other possibilities</h4>
//                     <ul>
//                       {prediction.top.slice(1).map((p, i) => (
//                         <li key={i}>
//                           <span>
//                             {p.plant ? `${p.plant}: ` : ""}
//                             {p.condition}
//                           </span>
//                           <span>{p.confidence.toFixed(1)}%</span>
//                         </li>
//                       ))}
//                     </ul>
//                   </div>
//                 )}

//                 {prediction.recommendation && (
//                   <div className="advice">
//                     <h4>{healthy ? "Keeping it healthy" : "What you can do"}</h4>
//                     <p>{prediction.recommendation}</p>
//                   </div>
//                 )}

//                 <p className="disclaimer">
//                   This is an automated suggestion based on a photo, not a
//                   diagnosis. Confirm with an agronomist before treating crops.
//                 </p>
//               </div>
//             )}
//           </section>
//         </div>
//       </main>

//       <footer className="footer">
//         <p>PlantDoctor · Plant disease detection with a Vision Transformer</p>
//       </footer>
//     </div>
//   );
// }

// export default App;