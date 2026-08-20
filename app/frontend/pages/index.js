import { useEffect, useState } from "react";
import UploadZone from "../components/UploadZone";
import PredictionCard from "../components/PredictionCard";
import AttentionOverlay from "../components/AttentionOverlay";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Formate une taille de fichier en octets vers une unité lisible (Ko / Mo)
function formatFileSize(bytes) {
  if (!bytes) return "";
  const units = ["o", "Ko", "Mo", "Go"];
  let value = bytes;
  let unitIndex = 0;
  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024;
    unitIndex += 1;
  }
  return `${value.toFixed(unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
}

export default function Home() {
  const [imageFile, setImageFile] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [attentionOverlay, setAttentionOverlay] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [classNames, setClassNames] = useState({});

  // Indépendant des modèles entraînés - vient des métadonnées du dataset (rôle A)
  useEffect(() => {
    fetch(`${API_BASE_URL}/classes`)
      .then((res) => res.json())
      .then(setClassNames)
      .catch(() => setClassNames({}));
  }, []);

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

      // Les deux appels partent en parallèle : la prédiction et la carte
      // d'attention sont indépendantes côté API.
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

  const hasSelection = Boolean(imageFile);
  const modelsAgree =
    predictions && predictions.vit.predicted_class === predictions.resnet.predicted_class;

  return (
    <div style={{ minHeight: "100vh" }}>
      {/* -------------------- EN-TÊTE -------------------- */}
      <header className="site-header">
        <div className="page-shell header-row">
          <div>
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
                fontSize: "clamp(28px, 4vw, 38px)",
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

          {/* Plaque de métadonnées façon étiquette de musée */}
          <dl className="spec-plate">
            <div>
              <dt>Jeu de données</dt>
              <dd>CUB-200-2011</dd>
            </div>
            <div>
              <dt>Espèces</dt>
              <dd>200</dd>
            </div>
            <div>
              <dt>Modèles</dt>
              <dd>ViT · ResNet-50</dd>
            </div>
          </dl>
        </div>
      </header>

      {/* -------------------- CORPS : grille pleine largeur -------------------- */}
      <main className="page-shell workspace-grid">
        {/* ---- Colonne latérale : dépôt + fiche du spécimen ---- */}
        <div className="sidebar-col">
          <UploadZone onImageSelected={handleImageSelected} hasSelection={hasSelection} />

          {hasSelection && (
            <div className="specimen-card">
              <img className="specimen-card__photo" src={imagePreviewUrl} alt="Aperçu du spécimen" />
              <div className="specimen-card__body">
                <p className="specimen-card__filename">
                  {imageFile.name}
                  {imageFile.size ? ` · ${formatFileSize(imageFile.size)}` : ""}
                </p>
                <p className="specimen-card__status">
                  <span
                    className={`status-dot ${loading ? "is-loading" : ""} ${
                      !loading && predictions ? "is-done" : ""
                    }`}
                  />
                  {loading && <span style={{ color: "var(--ink-soft)" }}>Examen en cours…</span>}
                  {!loading && predictions && (
                    <span style={{ color: "var(--sage)" }}>Identification complète</span>
                  )}
                  {!loading && !predictions && !error && (
                    <span style={{ color: "var(--ink-soft)" }}>En attente</span>
                  )}
                </p>
                {error && <p className="error-box" style={{ marginTop: 10 }}>{error}</p>}
              </div>
            </div>
          )}
        </div>

        {/* ---- Colonne de résultats ---- */}
        <div className="results-col">
          {!hasSelection && (
            <div className="empty-results">
              <p>
                Déposez une photographie dans la colonne de gauche pour lancer
                l&apos;identification et comparer les deux modèles.
              </p>
            </div>
          )}

          {predictions && (
            <>
              <div>
                <p className="section-label">Résultats</p>
                <div className="verdict-row">
                  <span className={`agreement-badge ${modelsAgree ? "agree" : "disagree"}`}>
                    {modelsAgree ? "Les deux modèles s'accordent" : "Désaccord entre les modèles"}
                  </span>
                  <p className="verdict-caption">{imageFile?.name}</p>
                </div>
              </div>

              <div className="predictions-row">
                <PredictionCard modelName="Vision Transformer" prediction={predictions.vit} classNames={classNames} />
                <PredictionCard modelName="ResNet-50" prediction={predictions.resnet} classNames={classNames} />
              </div>
            </>
          )}

          <AttentionOverlay overlayBase64={attentionOverlay} />
        </div>
      </main>

      {/* -------------------- PIED DE PAGE -------------------- */}
      <footer className="site-footer">
        <div className="page-shell">Vision Transformer vs CNN</div>
      </footer>
    </div>
  );
}