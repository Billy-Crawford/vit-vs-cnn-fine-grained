import { useState } from "react";
import UploadZone from "../components/UploadZone";
import PredictionCard from "../components/PredictionCard";
import AttentionOverlay from "../components/AttentionOverlay";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [imageFile, setImageFile] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [attentionOverlay, setAttentionOverlay] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelected = async (file) => {
    setImageFile(file);
    setImagePreviewUrl(URL.createObjectURL(file));
    setPredictions(null);
    setAttentionOverlay(null);
    setError(null);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const [predictRes, attentionRes] = await Promise.all([
        fetch(`${API_BASE_URL}/predict`, { method: "POST", body: formData }),
        fetch(`${API_BASE_URL}/attention`, { method: "POST", body: formData }),
      ]);

      if (!predictRes.ok) throw new Error("Erreur lors de la prédiction.");
      if (!attentionRes.ok) throw new Error("Erreur lors de la génération de la heatmap.");

      const predictData = await predictRes.json();
      const attentionData = await attentionRes.json();

      setPredictions(predictData);
      setAttentionOverlay(attentionData.attention_overlay_base64);
    } catch (err) {
      setError(err.message || "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh" }}>
      <header
        style={{
          borderBottom: "1px solid var(--line)",
          padding: "28px 0",
        }}
      >
        <div style={{ maxWidth: 760, margin: "0 auto", padding: "0 24px" }}>
          <p
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: 11,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              color: "var(--sage)",
              margin: "0 0 6px",
            }}
          >
            Atelier d&apos;identification — CUB-200-2011
          </p>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 30,
              fontWeight: 700,
              margin: 0,
              color: "var(--ink)",
            }}
          >
            ViT <span style={{ color: "var(--rust)" }}>vs</span> CNN
          </h1>
          <p style={{ margin: "8px 0 0", color: "var(--ink-soft)", fontSize: 14.5, maxWidth: 520 }}>
            Deux naturalistes artificiels examinent le même cliché. Comparez
            leurs verdicts et la manière dont chacun regarde l&apos;image.
          </p>
        </div>
      </header>

      <main style={{ maxWidth: 760, margin: "0 auto", padding: "36px 24px 80px" }}>
        <UploadZone onImageSelected={handleImageSelected} />

        {imagePreviewUrl && (
          <div style={{ marginTop: 24, display: "flex", gap: 16, alignItems: "flex-start" }}>
            <img
              src={imagePreviewUrl}
              alt="Aperçu du spécimen"
              style={{
                width: 140,
                height: 140,
                objectFit: "cover",
                borderRadius: 4,
                border: "1px solid var(--line)",
              }}
            />
            <div style={{ paddingTop: 4 }}>
              <p
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: 11,
                  letterSpacing: "0.1em",
                  textTransform: "uppercase",
                  color: "var(--sage-dim)",
                  margin: "0 0 6px",
                }}
              >
                Statut
              </p>
              {loading && <p style={{ margin: 0, color: "var(--ink-soft)" }}>Examen en cours…</p>}
              {error && <p style={{ margin: 0, color: "var(--rust)" }}>{error}</p>}
              {!loading && !error && predictions && (
                <p style={{ margin: 0, color: "var(--sage)" }}>Identification complète.</p>
              )}
            </div>
          </div>
        )}

        {predictions && (
          <div style={{ display: "flex", gap: 16, marginTop: 28 }}>
            <PredictionCard modelName="Vision Transformer" prediction={predictions.vit} />
            <PredictionCard modelName="ResNet-50" prediction={predictions.resnet} />
          </div>
        )}

        <AttentionOverlay overlayBase64={attentionOverlay} />
      </main>
    </div>
  );
}
