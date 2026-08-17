/**
 * Fiche d'identification pour un modèle (ViT ou ResNet) : classe prédite,
 * confiance, et top-3 avec barres de confiance façon règle graduée.
 */
export default function PredictionCard({ modelName, prediction, classNames }) {
  if (!prediction) return null;

  const label = (classId) => classNames?.[classId] ?? `Espèce n°${String(classId).padStart(3, "0")}`;

  return (
    <div
      style={{
        flex: 1,
        border: "1px solid var(--line)",
        borderRadius: 4,
        background: "var(--paper-card)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "10px 18px",
          background: "var(--ink)",
          color: "var(--paper)",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
        }}
      >
        <span
          style={{
            fontFamily: "var(--font-display)",
            fontSize: 16,
            fontWeight: 600,
          }}
        >
          {modelName}
        </span>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 10,
            letterSpacing: "0.1em",
            opacity: 0.65,
          }}
        >
          MODÈLE
        </span>
      </div>

      <div style={{ padding: "18px 18px 20px" }}>
        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 10,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            color: "var(--sage-dim)",
            margin: "0 0 6px",
          }}
        >
          Identification retenue
        </p>
        <p
          style={{
            fontFamily: "var(--font-display)",
            fontSize: 19,
            fontWeight: 600,
            margin: "0 0 2px",
          }}
        >
          {label(prediction.predicted_class)}
        </p>
        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 13,
            color: "var(--rust)",
            margin: "0 0 20px",
          }}
        >
          confiance {(prediction.confidence * 100).toFixed(1)}%
        </p>

        <p
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 10,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            color: "var(--sage-dim)",
            margin: "0 0 10px",
          }}
        >
          Autres candidats
        </p>

        {prediction.top3.map((item, i) => (
          <div key={item.class_id} style={{ marginBottom: 10 }}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: 12.5,
                marginBottom: 4,
                color: "var(--ink-soft)",
              }}
            >
              <span>{label(item.class_id)}</span>
              <span style={{ fontFamily: "var(--font-mono)" }}>
                {(item.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div style={{ background: "var(--line)", height: 4, borderRadius: 2 }}>
              <div
                style={{
                  width: `${item.confidence * 100}%`,
                  background: i === 0 ? "var(--sage)" : "var(--sage-dim)",
                  height: "100%",
                  borderRadius: 2,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
